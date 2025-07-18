"""
GHG (Greenhouse Gas) savings calculation endpoint
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import random

from app.models.schemas import (
    GHGCalculationRequest, 
    GHGCalculationResponse,
    EnvironmentalBenefit,
    CarbonCreditRequest,
    CarbonCreditResponse,
    MarketInfo
)

router = APIRouter()

# IPCC emission factors (kg CO2e per kg of waste)
EMISSION_FACTORS = {
    # Burning emission factors
    "burning_factors": {
        "rice straw": 0.0012,  # kg CO2e per kg
        "wheat straw": 0.0011,
        "corn husks": 0.0010,
        "sugarcane bagasse": 0.0009,
        "cotton stalks": 0.0013,
        "banana leaves": 0.0008,
        "cow dung": 0.0015,
        "buffalo dung": 0.0014,
        "chicken manure": 0.0016,
        "vegetable scraps": 0.0007,
        "food waste": 0.0006,
        "default": 0.0012
    },
    # Processing emission factors  
    "biogas_factors": {
        "rice straw": 0.0002,
        "wheat straw": 0.0003,
        "corn husks": 0.0002,
        "sugarcane bagasse": 0.0001,
        "cotton stalks": 0.0003,
        "banana leaves": 0.0001,
        "cow dung": 0.0001,
        "buffalo dung": 0.0001,
        "chicken manure": 0.0002,
        "vegetable scraps": 0.0001,
        "food waste": 0.0001,
        "default": 0.0002
    },
    "compost_factors": {
        "rice straw": 0.0003,
        "wheat straw": 0.0004,
        "corn husks": 0.0003,
        "sugarcane bagasse": 0.0002,
        "cotton stalks": 0.0004,
        "banana leaves": 0.0002,
        "cow dung": 0.0003,
        "buffalo dung": 0.0003,
        "chicken manure": 0.0004,
        "vegetable scraps": 0.0002,
        "food waste": 0.0002,
        "default": 0.0003
    }
}

# Methane emission factors for decomposition
METHANE_FACTORS = {
    "anaerobic_decomposition": {
        "rice straw": 0.0025,  # kg CH4 per kg waste
        "wheat straw": 0.0023,
        "corn husks": 0.0020,
        "sugarcane bagasse": 0.0018,
        "cotton stalks": 0.0025,
        "banana leaves": 0.0015,
        "cow dung": 0.0030,
        "buffalo dung": 0.0028,
        "chicken manure": 0.0035,
        "vegetable scraps": 0.0020,
        "food waste": 0.0025,
        "default": 0.0025
    }
}

def get_emission_factor(waste_type: str, process_type: str) -> float:
    """Get emission factor for specific waste type and process"""
    waste_type_lower = waste_type.lower()
    
    # Find matching waste type (partial match)
    for known_waste in EMISSION_FACTORS[f"{process_type}_factors"]:
        if known_waste in waste_type_lower or waste_type_lower in known_waste:
            return EMISSION_FACTORS[f"{process_type}_factors"][known_waste]
    
    # Return default if no match found
    return EMISSION_FACTORS[f"{process_type}_factors"]["default"]

def calculate_avoided_emissions(waste_type: str, quantity: float, processing_method: str) -> dict:
    """Calculate CO2 emissions avoided by processing instead of burning/decomposing"""
    
    # Get emission factors
    burning_ef = get_emission_factor(waste_type, "burning")
    
    if processing_method.lower() == "biogas":
        processing_ef = get_emission_factor(waste_type, "biogas")
    else:
        processing_ef = get_emission_factor(waste_type, "compost")
    
    # Calculate emissions
    burning_emissions = quantity * burning_ef  # tons CO2e
    processing_emissions = quantity * processing_ef  # tons CO2e
    
    # Net savings
    co2_saved = burning_emissions - processing_emissions
    
    # Additional methane emission reduction (if waste would decompose anaerobically)
    methane_ef = METHANE_FACTORS["anaerobic_decomposition"].get(
        waste_type.lower(), 
        METHANE_FACTORS["anaerobic_decomposition"]["default"]
    )
    
    # Convert CH4 to CO2e (1 kg CH4 = 25 kg CO2e)
    methane_emissions_avoided = quantity * methane_ef * 25
    
    total_co2_saved = co2_saved + methane_emissions_avoided
    
    return {
        "burning_emissions": burning_emissions,
        "processing_emissions": processing_emissions,
        "direct_co2_saved": co2_saved,
        "methane_emissions_avoided": methane_emissions_avoided,
        "total_co2_saved": total_co2_saved
    }

def generate_environmental_benefits(processing_method: str, co2_saved: float) -> list:
    """Generate list of environmental benefits"""
    
    base_benefits = [
        EnvironmentalBenefit(
            title="GHG Emission Reduction",
            category="Greenhouse Gas Reduction",
            description=f"Prevents {co2_saved:.2f} tons of CO₂ equivalent emissions",
            impact_level="High"
        ),
        EnvironmentalBenefit(
            title="Air Quality Improvement",
            category="Air Quality Improvement", 
            description="Eliminates smoke and particulate matter from burning",
            impact_level="High"
        ),
        EnvironmentalBenefit(
            title="Resource Recovery",
            category="Resource Recovery",
            description="Converts waste into valuable resources instead of disposal",
            impact_level="Medium"
        )
    ]
    
    if processing_method.lower() == "biogas":
        base_benefits.extend([
            EnvironmentalBenefit(
                title="Renewable Energy Production",
                category="Renewable Energy Production",
                description="Generates clean biogas energy replacing fossil fuels",
                impact_level="High"
            ),
            EnvironmentalBenefit(
                title="Liquid Fertilizer Production",
                category="Liquid Fertilizer Production",
                description="Creates nutrient-rich liquid fertilizer reducing chemical fertilizer need",
                impact_level="Medium"
            )
        ])
    else:  # compost
        base_benefits.extend([
            EnvironmentalBenefit(
                title="Soil Health Improvement",
                category="Soil Health Improvement",
                description="Produces organic compost enhancing soil structure and fertility",
                impact_level="High"
            ),
            EnvironmentalBenefit(
                title="Carbon Sequestration",
                category="Carbon Sequestration",
                description="Sequesters carbon in soil through organic matter addition",
                impact_level="Medium"
            )
        ])
    
    return base_benefits

@router.post("/ghg-savings", response_model=GHGCalculationResponse)
async def calculate_ghg_savings(request: GHGCalculationRequest):
    """
    Calculate greenhouse gas emissions savings from waste processing
    
    **Calculation Method:**
    - Uses IPCC emission factors for different waste types
    - Compares burning vs. processing emissions
    - Includes methane emission reduction
    - Accounts for energy displacement benefits
    """
    
    try:
        # Calculate emissions
        emissions_data = calculate_avoided_emissions(
            request.waste_type,
            request.quantity,
            request.processing_method
        )
        
        # Generate environmental benefits
        environmental_benefits = generate_environmental_benefits(
            request.processing_method,
            emissions_data["total_co2_saved"]
        )
        
        # Calculate energy output (for biogas)
        energy_output = 0
        if request.processing_method.lower() == "biogas":
            # ~6 kWh per m³ biogas, ~0.03 m³ per kg waste
            energy_output = request.quantity * 0.03 * 6
        
        # Additional metrics
        trees_equivalent = emissions_data["total_co2_saved"] * 40  # 1 tree = 25kg CO2/year
        car_miles_equivalent = emissions_data["total_co2_saved"] * 2500  # 1 ton CO2 = 2500 miles
        
        return GHGCalculationResponse(
            co2_saved=round(emissions_data["total_co2_saved"], 3),
            co2_saved_unit="tons CO₂e",
            methane_reduction=round(emissions_data["methane_emissions_avoided"], 3),
            energy_generated=round(energy_output, 1) if energy_output > 0 else None,
            baseline_emissions=round(emissions_data["burning_emissions"], 3),
            processing_emissions=round(emissions_data["processing_emissions"], 3),
            net_reduction=round(emissions_data["total_co2_saved"], 3),
            environmental_benefits=environmental_benefits,
            message=f"GHG savings calculated for {request.quantity}kg of {request.waste_type}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"GHG calculation failed: {str(e)}"
        )

@router.get("/emission-factors")
async def get_emission_factors():
    """Get emission factors for different waste types and processes"""
    return {
        "emission_factors": EMISSION_FACTORS,
        "methane_factors": METHANE_FACTORS,
        "conversion_factors": {
            "ch4_to_co2e": 25,  # Global Warming Potential
            "energy_per_m3_biogas": 6,  # kWh per m³
            "biogas_yield_per_kg": 0.03  # m³ per kg waste
        },
        "data_sources": [
            "IPCC Guidelines for National Greenhouse Gas Inventories",
            "FAO Guidelines for measuring GHG emissions from agriculture",
            "National emission factor databases"
        ]
    }

@router.get("/environmental-impact-categories")
async def get_impact_categories():
    """Get information about environmental impact categories"""
    return {
        "categories": {
            "Greenhouse Gas Reduction": {
                "description": "Direct CO₂ equivalent emission reductions",
                "measurement_unit": "tons CO₂e",
                "impact_scope": "Global climate change mitigation"
            },
            "Air Quality Improvement": {
                "description": "Reduction in air pollutants from burning",
                "measurement_unit": "percentage reduction",
                "impact_scope": "Local and regional air quality"
            },
            "Resource Recovery": {
                "description": "Conversion of waste to useful products",
                "measurement_unit": "percentage utilization",
                "impact_scope": "Circular economy contribution"
            },
            "Renewable Energy Production": {
                "description": "Clean energy generation from waste",
                "measurement_unit": "kWh generated",
                "impact_scope": "Energy system sustainability"
            },
            "Soil Health Improvement": {
                "description": "Organic matter addition to agricultural soil", 
                "measurement_unit": "kg organic matter",
                "impact_scope": "Soil ecosystem health"
            },
            "Carbon Sequestration": {
                "description": "Long-term carbon storage in soil",
                "measurement_unit": "tons carbon sequestered",
                "impact_scope": "Climate change mitigation"
            }
        }
    }

@router.post("/carbon-credits", response_model=CarbonCreditResponse)
async def calculate_carbon_credits(request: CarbonCreditRequest):
    """
    Calculate potential carbon credits from GHG emissions reductions
    
    **Carbon Credit Calculation:**
    - Based on verified CO₂ equivalent emissions reductions
    - 1 carbon credit = 1 ton CO₂e reduced
    """
    
    try:
        # Validate input
        if request.co2_saved < 0:
            raise HTTPException(
                status_code=400,
                detail="CO₂ savings must be non-negative"
            )
        
        # Calculate carbon credits
        carbon_credits = request.co2_saved  # 1-to-1 conversion for credits
        
        return CarbonCreditResponse(
            carbon_credits=round(carbon_credits, 3),
            message=f"Carbon credits calculated: {carbon_credits} tons CO₂e",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Carbon credit calculation failed: {str(e)}"
        )

@router.get("/market-info")
async def get_market_info():
    """Get information about carbon credit markets and pricing"""
    return {
        "markets": [
            {
                "name": "Voluntary Carbon Market",
                "description": "Market where companies and individuals can purchase carbon credits voluntarily",
                "pricing_mechanism": "Varies by project and credit type",
                "example_projects": [
                    "Reforestation projects",
                    "Renewable energy projects",
                    "Methane capture projects"
                ]
            },
            {
                "name": "Compliance Carbon Market",
                "description": "Market where companies buy carbon credits to comply with regulatory requirements",
                "pricing_mechanism": "Fixed by regulatory authorities",
                "example_projects": [
                    "Cap-and-trade programs",
                    "Carbon offset projects"
                ]
            }
        ],
        "current_pricing": {
            "average_price_per_ton": 3.5,  # Example average price
            "currency": "USD",
            "source": "Latest market reports"
        },
        "further_reading": [
            "Guide to Carbon Credit Markets",
            "How Carbon Pricing Works",
            "Benefits of Carbon Offsetting"
        ]
    }

@router.post("/carbon-credit", response_model=CarbonCreditResponse)
async def calculate_carbon_credits(request: CarbonCreditRequest):
    """
    Calculate carbon credits based on CO2 savings and waste processing
    
    **Features:**
    - Carbon credit calculation based on CO2 savings
    - Market value estimation
    - Verification methodology assessment
    - Multiple market options comparison
    - Risk assessment and recommendations
    """
    
    try:
        # Base carbon credit calculation (1 credit = 1 ton CO2e saved)
        credits_earned = round(request.co2_saved, 2)
        
        # Market rates (INR per credit)
        market_rates = {
            "voluntary": {"min": 800, "max": 2500, "current": 1500},
            "compliance": {"min": 2000, "max": 8000, "current": 4500},
            "premium": {"min": 3500, "max": 12000, "current": 7500}
        }
        
        # Processing method multipliers
        method_multipliers = {
            "Anaerobic Digestion": 1.2,  # Higher value due to biogas production
            "Composting": 1.0,
            "Pyrolysis": 1.3,
            "Gasification": 1.4,
            "Direct Burning": 0.8  # Lower value due to emissions
        }
        
        # Waste type bonuses
        waste_bonuses = {
            "CATTLE MANURE": 1.1,
            "Rice Straw": 1.0,
            "Wheat Straw": 1.0,
            "Corn Stalks": 0.95,
            "Cotton Waste": 0.9
        }
        
        # Apply multipliers
        method_multiplier = method_multipliers.get(request.processing_method, 1.0)
        waste_bonus = waste_bonuses.get(request.waste_type, 1.0)
        
        final_credits = credits_earned * method_multiplier * waste_bonus
        
        # Select market based on verification level
        if request.verification_level == "premium":
            market_type = "premium"
        elif request.verification_level == "standard":
            market_type = "compliance"
        else:
            market_type = "voluntary"
            
        current_rate = market_rates[market_type]["current"]
        market_value = round(final_credits * current_rate, 2)
        
        # Market info
        market_info = MarketInfo(
            market_type=market_type.title(),
            current_rate=current_rate,
            value_range={
                "min": market_rates[market_type]["min"],
                "max": market_rates[market_type]["max"]
            },
            transaction_costs=round(market_value * 0.05, 2)  # 5% transaction costs
        )
        
        # Risk assessment
        risk_factors = []
        if request.co2_saved < 5:
            risk_factors.append("Low volume may increase per-credit costs")
        if request.verification_level == "basic":
            risk_factors.append("Basic verification may limit market access")
            
        risk_assessment = {
            "risk_level": "Medium" if risk_factors else "Low",
            "factors": risk_factors,
            "mitigation": "Consider pooling with other farmers for better rates"
        }
        
        # Market recommendations
        recommendations = [
            {
                "market": "Voluntary Carbon Market",
                "suitability": "High" if request.co2_saved >= 1 else "Medium",
                "pros": ["Lower barriers to entry", "Faster verification"],
                "cons": ["Lower prices", "Market volatility"]
            },
            {
                "market": "Compliance Market",
                "suitability": "High" if request.co2_saved >= 5 else "Low",
                "pros": ["Higher prices", "Stable demand"],
                "cons": ["Stricter verification", "Higher costs"]
            }
        ]
        
        # Next steps
        next_steps = [
            "Document all processing activities and measurements",
            "Choose appropriate verification standard",
            "Register project with carbon registry",
            "Monitor and verify emission reductions",
            "Issue and sell carbon credits"
        ]
        
        return CarbonCreditResponse(
            co2_saved=request.co2_saved,
            waste_type=request.waste_type,
            processing_method=request.processing_method,
            credits_earned=final_credits,
            credits_unit="tCO₂e",
            market_value=market_value,
            currency="INR",
            market_info=market_info,
            all_market_options=market_rates,
            eligibility_status="Eligible" if request.co2_saved >= 1 else "Below minimum threshold",
            verification_methodology=f"VM0042 - Methodology for improved agricultural management",
            risk_assessment=risk_assessment,
            market_recommendations=recommendations,
            next_steps=next_steps,
            estimated_timeline="6-12 months for full verification and credit issuance",
            message=f"Carbon credits calculated successfully for {request.waste_type} processing"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Carbon credit calculation failed: {str(e)}"
        )
