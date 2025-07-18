"""
Recommendation engine for biogas/compost processing
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import random

from app.models.schemas import (
    RecommendationRequest, 
    RecommendationResponse, 
    ProcessingStep
)

router = APIRouter()

# Decision matrix for processing method selection
PROCESSING_DECISION_MATRIX = {
    # High moisture content (>60%) -> Biogas
    "biogas_conditions": {
        "moisture_threshold": 60,
        "preferred_waste_types": [
            "cow dung", "buffalo dung", "chicken manure", "banana leaves",
            "vegetable scraps", "food waste", "sugarcane bagasse"
        ],
        "efficiency": 85
    },
    # Low moisture content (<40%) -> Compost  
    "compost_conditions": {
        "moisture_threshold": 40,
        "preferred_waste_types": [
            "rice straw", "wheat straw", "cotton stalks", "corn husks",
            "coconut husk", "mustard stalks", "sunflower stalks"
        ],
        "efficiency": 75
    }
}

# Processing steps templates
BIOGAS_STEPS = [
    ProcessingStep(
        step_number=1,
        title="Waste Collection & Sorting",
        description="Collect fresh organic waste and sort by type. Remove any non-organic materials.",
        duration="1-2 hours",
        tools_required=["Collection containers", "Sorting area", "Gloves"]
    ),
    ProcessingStep(
        step_number=2,
        title="Feedstock Preparation",
        description="Chop/shred waste into small pieces (2-5 cm) for better digestion. Mix with water if needed.",
        duration="2-3 hours", 
        tools_required=["Chopping machine", "Water source", "Mixing equipment"]
    ),
    ProcessingStep(
        step_number=3,
        title="Biogas Digester Loading",
        description="Load prepared feedstock into biogas digester. Maintain C:N ratio of 25-30:1.",
        duration="1 hour",
        tools_required=["Biogas digester", "Loading equipment", "pH meter"]
    ),
    ProcessingStep(
        step_number=4,
        title="Fermentation Monitoring",
        description="Monitor temperature (35-40°C), pH (6.8-7.2), and gas production daily.",
        duration="30-45 days",
        tools_required=["Thermometer", "pH meter", "Gas flow meter"]
    ),
    ProcessingStep(
        step_number=5,
        title="Biogas Collection",
        description="Collect biogas through pipeline system. Store in gas holder or use directly.",
        duration="Daily collection",
        tools_required=["Gas pipeline", "Gas holder", "Safety equipment"]
    ),
    ProcessingStep(
        step_number=6,
        title="Slurry Management", 
        description="Remove digested slurry and use as high-quality organic fertilizer.",
        duration="Weekly",
        tools_required=["Slurry outlet", "Storage tanks", "Application equipment"]
    )
]

COMPOST_STEPS = [
    ProcessingStep(
        step_number=1,
        title="Raw Material Collection",
        description="Collect dry organic waste materials. Ensure carbon-rich materials dominate.",
        duration="1-2 hours",
        tools_required=["Collection area", "Tarpaulin", "Storage containers"]
    ),
    ProcessingStep(
        step_number=2,
        title="Material Preparation",
        description="Shred materials to 2-5 cm pieces. Mix carbon and nitrogen sources in 30:1 ratio.",
        duration="3-4 hours",
        tools_required=["Shredding machine", "Mixing area", "Measuring tools"]
    ),
    ProcessingStep(
        step_number=3,
        title="Pile Construction",
        description="Build compost pile in layers. Maintain pile height of 1-1.5 meters.",
        duration="2-3 hours",
        tools_required=["Pitchfork", "Measuring tape", "Water sprayer"]
    ),
    ProcessingStep(
        step_number=4,
        title="Moisture Management",
        description="Maintain moisture level at 40-60%. Add water or dry materials as needed.",
        duration="Weekly",
        tools_required=["Moisture meter", "Water source", "Dry materials"]
    ),
    ProcessingStep(
        step_number=5,
        title="Turning & Aeration",
        description="Turn pile every 2-3 weeks to ensure proper aeration and decomposition.",
        duration="2-3 months",
        tools_required=["Pitchfork", "Shovel", "Thermometer"]
    ),
    ProcessingStep(
        step_number=6,
        title="Maturation & Harvesting",
        description="Allow compost to mature. Harvest when dark, crumbly, and earthy-smelling.", 
        duration="1-2 weeks",
        tools_required=["Sieve", "Storage bags", "Quality testing kit"]
    )
]

def determine_processing_method(waste_type: str, quantity: float, moisture_content: float = None) -> str:
    """Determine optimal processing method based on waste characteristics"""
    
    waste_type_lower = waste_type.lower()
    
    # Check for high-moisture waste types
    biogas_wastes = PROCESSING_DECISION_MATRIX["biogas_conditions"]["preferred_waste_types"]
    if any(waste in waste_type_lower for waste in biogas_wastes):
        return "biogas"
    
    # Check for low-moisture waste types
    compost_wastes = PROCESSING_DECISION_MATRIX["compost_conditions"]["preferred_waste_types"]
    if any(waste in waste_type_lower for waste in compost_wastes):
        return "compost"
    
    # If moisture content is provided, use it as deciding factor
    if moisture_content is not None:
        if moisture_content > PROCESSING_DECISION_MATRIX["biogas_conditions"]["moisture_threshold"]:
            return "biogas"
        elif moisture_content < PROCESSING_DECISION_MATRIX["compost_conditions"]["moisture_threshold"]:
            return "compost"
    
    # Default decision based on common waste types
    if any(keyword in waste_type_lower for keyword in ["straw", "stalks", "husks"]):
        return "compost"
    elif any(keyword in waste_type_lower for keyword in ["dung", "manure", "scraps", "leaves"]):
        return "biogas"
    
    # Default to compost for unknown types
    return "compost"

def calculate_expected_output(method: str, quantity: float, waste_type: str) -> dict:
    """Calculate expected output based on processing method and quantity"""
    
    if method == "biogas":
        # Biogas yield: 20-40 m³ per ton of waste
        biogas_yield = random.uniform(20, 40) * (quantity / 1000)
        # Energy content: ~6 kWh per m³ of biogas
        energy_output = biogas_yield * 6
        # Slurry output: ~60-70% of input weight
        slurry_output = quantity * random.uniform(0.6, 0.7)
        
        return {
            "biogas_volume": f"{biogas_yield:.1f} m³",
            "energy_equivalent": f"{energy_output:.1f} kWh", 
            "organic_slurry": f"{slurry_output:.0f} kg",
            "cooking_hours": f"{energy_output / 2:.1f} hours", # Assuming 2 kWh per hour cooking
            "carbon_reduction": f"{quantity * 0.0025:.2f} tons CO₂e"
        }
    else:  # compost
        # Compost yield: 30-40% of input weight
        compost_yield = quantity * random.uniform(0.3, 0.4)
        # Fertilizer value calculation
        fertilizer_equivalent = compost_yield * 2  # 1 kg compost = 2 kg chemical fertilizer
        
        return {
            "compost_quantity": f"{compost_yield:.0f} kg",
            "fertilizer_equivalent": f"{fertilizer_equivalent:.0f} kg chemical fertilizer",
            "soil_coverage": f"{compost_yield / 5:.1f} acres", # 5 kg per acre
            "nutrient_content": "2-3% N, 1-2% P, 1-2% K",
            "carbon_sequestration": f"{quantity * 0.0015:.2f} tons CO₂e"
        }

@router.post("/recommend", response_model=RecommendationResponse) 
async def get_processing_recommendation(request: RecommendationRequest):
    """
    Get processing method recommendation (biogas or compost) based on waste characteristics
    
    **Decision Factors:**
    - Waste type and characteristics
    - Moisture content
    - Quantity available
    - Processing efficiency
    - Expected output
    """
    
    try:
        # Determine optimal processing method
        recommended_method = determine_processing_method(
            request.waste_type, 
            request.quantity,
            request.moisture_content
        )
        
        # Generate reasoning
        if recommended_method == "biogas":
            reasoning = f"Biogas production recommended for {request.waste_type} due to high organic content and moisture. Optimal for energy generation and liquid fertilizer production."
            processing_steps = BIOGAS_STEPS
            tools_required = [
                "Biogas digester (5-10 m³ capacity)",
                "Gas collection system",
                "pH and temperature monitoring tools",
                "Safety equipment",
                "Slurry storage tanks"
            ]
            processing_time = "30-45 days initial fermentation + ongoing production"
            efficiency = PROCESSING_DECISION_MATRIX["biogas_conditions"]["efficiency"]
        else:
            reasoning = f"Composting recommended for {request.waste_type} due to suitable carbon content and lower moisture. Ideal for solid fertilizer production."
            processing_steps = COMPOST_STEPS
            tools_required = [
                "Composting area (covered)",
                "Shredding/chopping equipment", 
                "Turning tools (pitchfork, shovel)",
                "Moisture monitoring equipment",
                "Thermometer for temperature monitoring"
            ]
            processing_time = "2-4 months for complete decomposition"
            efficiency = PROCESSING_DECISION_MATRIX["compost_conditions"]["efficiency"]
        
        # Calculate expected output
        expected_output = calculate_expected_output(
            recommended_method, 
            request.quantity, 
            request.waste_type
        )
        
        return RecommendationResponse(
            recommended_method=recommended_method.title(),
            processing_method=recommended_method.title(),  # Add for compatibility
            reasoning=reasoning,
            processing_steps=processing_steps,
            tools_required=tools_required,
            expected_output=expected_output,
            processing_time=processing_time,
            efficiency=efficiency,
            message=f"Processing recommendation generated for {request.quantity}kg of {request.waste_type}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation generation failed: {str(e)}"
        )

@router.get("/processing-methods")
async def get_processing_methods():
    """Get information about available processing methods"""
    return {
        "methods": {
            "biogas": {
                "description": "Anaerobic digestion for energy production",
                "suitable_for": PROCESSING_DECISION_MATRIX["biogas_conditions"]["preferred_waste_types"],
                "output": "Biogas + Liquid fertilizer",
                "time_required": "30-45 days",
                "efficiency": f"{PROCESSING_DECISION_MATRIX['biogas_conditions']['efficiency']}%"
            },
            "compost": {
                "description": "Aerobic decomposition for fertilizer production", 
                "suitable_for": PROCESSING_DECISION_MATRIX["compost_conditions"]["preferred_waste_types"],
                "output": "Solid organic fertilizer",
                "time_required": "2-4 months",
                "efficiency": f"{PROCESSING_DECISION_MATRIX['compost_conditions']['efficiency']}%"
            }
        },
        "selection_criteria": [
            "Moisture content of waste",
            "Carbon to nitrogen ratio",
            "Available infrastructure",
            "Desired output type",
            "Processing timeline"
        ]
    }
