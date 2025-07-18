"""
Carbon credit calculation and estimation endpoint
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import random

from app.models.schemas import (
    CarbonCreditRequest, 
    CarbonCreditResponse,
    MarketInfo
)

router = APIRouter()

# Carbon credit market rates (INR per credit)
CARBON_CREDIT_RATES = {
    "voluntary_market": {
        "current_rate": 1500,  # INR per credit
        "rate_range": (1200, 1800),
        "market_type": "Voluntary Carbon Market (VCM)",
        "verification": "Third-party verification required",
        "trading_platforms": ["Verra", "Gold Standard", "Climate Action Reserve"]
    },
    "compliance_market": {
        "current_rate": 2200,  # INR per credit
        "rate_range": (1800, 2500),
        "market_type": "Compliance Carbon Market",
        "verification": "Government approved verification",
        "trading_platforms": ["EU ETS", "California Cap-and-Trade", "Regional markets"]
    },
    "indian_market": {
        "current_rate": 1300,  # INR per credit
        "rate_range": (1000, 1600),
        "market_type": "Indian Carbon Market",
        "verification": "Bureau of Energy Efficiency (BEE) approved",
        "trading_platforms": ["Indian Carbon Exchange", "Multi Commodity Exchange (MCX)"]
    }
}

# Credit eligibility criteria
ELIGIBILITY_CRITERIA = {
    "minimum_co2_saved": 0.1,  # tons CO2e minimum
    "minimum_project_duration": 365,  # days
    "verification_requirements": [
        "Baseline emissions documentation",
        "Monitoring and verification plan", 
        "Third-party validation",
        "Additionality demonstration",
        "Permanence assurance"
    ],
    "eligible_methodologies": [
        "CDM Methodology for biogas projects",
        "Composting methodology for organic waste",
        "Agricultural waste management protocols",
        "Small-scale renewable energy projects"
    ]
}

def calculate_credit_eligibility(co2_saved: float, waste_type: str, processing_method: str) -> dict:
    """Calculate carbon credit eligibility and potential credits"""
    
    # Basic eligibility check
    eligible = co2_saved >= ELIGIBILITY_CRITERIA["minimum_co2_saved"]
    
    # Credit calculation (1 ton CO2e = 1 carbon credit)
    potential_credits = round(co2_saved, 2)
    
    # Apply methodology-specific factors
    methodology_factor = 1.0
    
    if processing_method.lower() == "biogas":
        # Biogas projects typically have higher crediting rates
        methodology_factor = 0.95  # 95% crediting rate
        methodology = "AMS-I.C: Thermal energy production with or without electricity"
    else:  # compost
        # Composting projects have good crediting rates for methane avoidance
        methodology_factor = 0.85  # 85% crediting rate  
        methodology = "AMS-III.F: Avoidance of methane emissions through composting"
    
    # Calculate final credits
    verified_credits = potential_credits * methodology_factor
    
    # Risk assessment
    risk_factors = []
    confidence_level = 90
    
    if co2_saved < 1.0:
        risk_factors.append("Small project size may have higher verification costs")
        confidence_level -= 10
    
    if waste_type.lower() in ["mixed waste", "unknown"]:
        risk_factors.append("Waste type uncertainty may affect verification")
        confidence_level -= 5
    
    return {
        "eligible": eligible,
        "potential_credits": potential_credits,
        "verified_credits": verified_credits,
        "methodology": methodology,
        "methodology_factor": methodology_factor,
        "risk_factors": risk_factors,
        "confidence_level": max(confidence_level, 70)
    }

def estimate_market_value(credits: float, market_type: str = "voluntary_market") -> dict:
    """Estimate market value of carbon credits"""
    
    market_info = CARBON_CREDIT_RATES.get(market_type, CARBON_CREDIT_RATES["voluntary_market"])
    
    # Base calculation
    base_value = credits * market_info["current_rate"]
    
    # Market volatility consideration (±15%)
    min_value = credits * market_info["rate_range"][0] 
    max_value = credits * market_info["rate_range"][1]
    
    # Transaction costs (typically 10-20%)
    transaction_cost_rate = 0.15
    net_value = base_value * (1 - transaction_cost_rate)
    
    return {
        "gross_value": round(base_value, 2),
        "net_value": round(net_value, 2),
        "value_range": {
            "minimum": round(min_value * (1 - transaction_cost_rate), 2),
            "maximum": round(max_value * (1 - transaction_cost_rate), 2)
        },
        "transaction_costs": round(base_value * transaction_cost_rate, 2),
        "market_type": market_info["market_type"],
        "current_rate": market_info["current_rate"]
    }

def generate_market_recommendations(credits: float, project_scale: str) -> list:
    """Generate market-specific recommendations"""
    
    recommendations = []
    
    if credits < 1.0:
        recommendations.append({
            "market": "Voluntary Carbon Market",
            "rationale": "Best suited for small-scale projects with lower verification costs",
            "action": "Consider aggregating with other small projects to reduce costs",
            "timeline": "6-12 months for registration and verification"
        })
    elif credits < 10.0:
        recommendations.append({
            "market": "Indian Carbon Market", 
            "rationale": "Domestic market with streamlined processes for medium projects",
            "action": "Apply through Bureau of Energy Efficiency (BEE) certification",
            "timeline": "8-15 months for full certification"
        })
    else:
        recommendations.append({
            "market": "Compliance Carbon Market",
            "rationale": "Higher prices available for large-scale verified projects",
            "action": "Pursue international certification (CDM/Gold Standard)",
            "timeline": "12-24 months for full international verification"
        })
    
    # Additional recommendations
    recommendations.append({
        "market": "Forward Contracting",
        "rationale": "Lock in current prices to avoid market volatility",
        "action": "Negotiate advance purchase agreements with buyers",
        "timeline": "3-6 months for contract negotiation"
    })
    
    return recommendations

@router.post("/carbon-credit", response_model=CarbonCreditResponse)
async def calculate_carbon_credits(request: CarbonCreditRequest):
    """
    Calculate carbon credits and market value estimation
    
    **Calculation Process:**
    - 1 ton CO₂e saved = 1 carbon credit (baseline)
    - Apply methodology-specific factors
    - Calculate market value across different markets
    - Assess eligibility and risk factors
    - Provide market recommendations
    """
    
    try:
        # Calculate credit eligibility
        eligibility_info = calculate_credit_eligibility(
            request.co2_saved,
            request.waste_type,
            request.processing_method
        )
        
        if not eligibility_info["eligible"]:
            raise HTTPException(
                status_code=400,
                detail=f"Project does not meet minimum eligibility criteria. Minimum {ELIGIBILITY_CRITERIA['minimum_co2_saved']} tons CO₂e required."
            )
        
        # Calculate market values
        market_values = {}
        for market_type in CARBON_CREDIT_RATES.keys():
            market_values[market_type] = estimate_market_value(
                eligibility_info["verified_credits"], 
                market_type
            )
        
        # Determine project scale
        if request.co2_saved < 1.0:
            project_scale = "small"
        elif request.co2_saved < 10.0:
            project_scale = "medium"
        else:
            project_scale = "large"
        
        # Generate recommendations
        market_recommendations = generate_market_recommendations(
            eligibility_info["verified_credits"],
            project_scale
        )
        
        # Select best market option
        best_market = max(market_values.items(), key=lambda x: x[1]["net_value"])
        
        return CarbonCreditResponse(
            co2_saved=request.co2_saved,
            waste_type=request.waste_type,
            processing_method=request.processing_method,
            credits_earned=eligibility_info["verified_credits"],
            credits_unit="tCO₂e",
            market_value=best_market[1]["net_value"],
            currency="INR",
            market_info=MarketInfo(
                market_type=best_market[1]["market_type"],
                current_rate=best_market[1]["current_rate"],
                value_range=best_market[1]["value_range"],
                transaction_costs=best_market[1]["transaction_costs"]
            ),
            all_market_options=market_values,
            eligibility_status="Eligible" if eligibility_info["eligible"] else "Not Eligible",
            verification_methodology=eligibility_info["methodology"],
            risk_assessment={
                "confidence_level": eligibility_info["confidence_level"],
                "risk_factors": eligibility_info["risk_factors"],
                "mitigation_strategies": [
                    "Maintain detailed documentation of all activities",
                    "Implement robust monitoring and verification systems",
                    "Consider third-party validation early in the process",
                    "Ensure compliance with relevant carbon standards"
                ]
            },
            market_recommendations=market_recommendations,
            next_steps=[
                "Document baseline emissions and project activities",
                "Select appropriate carbon standard and methodology",
                "Develop monitoring and verification plan",
                "Engage qualified validation/verification body",
                "Submit project for registration and crediting"
            ],
            estimated_timeline="6-18 months depending on market and project scale",
            message=f"Carbon credit analysis completed for {request.co2_saved} tons CO₂e savings",
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Carbon credit calculation failed: {str(e)}"
        )

@router.get("/market-rates")
async def get_current_market_rates():
    """Get current carbon credit market rates and information"""
    return {
        "market_rates": CARBON_CREDIT_RATES,
        "last_updated": datetime.now(),
        "market_trends": {
            "voluntary_market": "Stable with slight upward trend",
            "compliance_market": "Strong demand, prices increasing",
            "indian_market": "Growing domestic demand, government support"
        },
        "factors_affecting_prices": [
            "Global climate policy developments",
            "Corporate net-zero commitments",
            "Supply-demand balance",
            "Verification and quality standards",
            "Regional market regulations"
        ]
    }

@router.get("/eligibility-criteria")
async def get_eligibility_criteria():
    """Get carbon credit eligibility criteria and requirements"""
    return {
        "eligibility_criteria": ELIGIBILITY_CRITERIA,
        "project_requirements": {
            "additionality": "Project must demonstrate that emissions reductions would not occur without carbon credit incentive",
            "permanence": "Emissions reductions must be permanent or have appropriate risk management",
            "monitoring": "Robust monitoring and verification system required",
            "documentation": "Comprehensive project documentation and reporting"
        },
        "verification_process": [
            "Project design and methodology selection",
            "Validation by accredited third party",
            "Implementation and monitoring",
            "Verification of emissions reductions", 
            "Credit issuance and registration"
        ]
    }
