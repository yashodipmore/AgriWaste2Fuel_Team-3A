# Farm-Waste Handling Recommendation System Integration
import os

# Weight range midpoints
weight_range_midpoints = {
    "<10kg": 5,
    "10–50kg": 30,
    "50–100kg": 75,
    "100–500kg": 300,
    ">500kg": 600
}

# Attribute profiles (can be expanded)
attribute_profiles = {
    "cow_dung": {"%C": 38, "%N": 0.5, "cn_ratio": 76, "decomposition_speed": "fast"},
    "fruit_veg_peels": {"%C": 28, "%N": 1.0, "cn_ratio": 28, "decomposition_speed": "fast"},
    "crop_residues": {"%C": 45, "%N": 0.7, "cn_ratio": 64, "decomposition_speed": "medium"},
    "rice_straw": {"%C": 45, "%N": 0.7, "cn_ratio": 64, "decomposition_speed": "medium"},
    "wheat_straw": {"%C": 45, "%N": 0.6, "cn_ratio": 75, "decomposition_speed": "medium"},
    "corn_stalks": {"%C": 42, "%N": 0.8, "cn_ratio": 53, "decomposition_speed": "medium"},
    "cotton_waste": {"%C": 40, "%N": 0.5, "cn_ratio": 80, "decomposition_speed": "slow"},
    "sugarcane_bagasse": {"%C": 48, "%N": 0.3, "cn_ratio": 160, "decomposition_speed": "slow"}
}

# GHG saving factors per (waste, method)
ghg_saving_factors = {
    ("cow_dung", "Biogas"): (0.36, 0.45),
    ("cow_dung", "Composting"): (0.12, 0.18),
    ("cow_dung", "Vermicompost"): (0.15, 0.22),
    ("fruit_veg_peels", "Biogas"): (0.32, 0.40),
    ("fruit_veg_peels", "Composting"): (0.14, 0.20),
    ("fruit_veg_peels", "Vermicompost"): (0.18, 0.24),
    ("crop_residues", "Biogas"): (0.34, 0.42),
    ("crop_residues", "Composting"): (0.10, 0.14),
    ("crop_residues", "Vermicompost"): (0.12, 0.16),
    ("crop_residues", "Mulching"): (0.80, 0.80),
    ("rice_straw", "Anaerobic Digestion"): (0.6, 0.7),
    ("rice_straw", "Gasification"): (0.8, 0.9),
    ("wheat_straw", "Gasification"): (0.7, 0.8),
    ("wheat_straw", "Composting"): (0.3, 0.4),
    ("corn_stalks", "Pyrolysis"): (0.9, 1.0),
    ("corn_stalks", "Biogas"): (0.5, 0.6),
    ("cotton_waste", "Composting"): (0.4, 0.5),
    ("cotton_waste", "Mulching"): (0.6, 0.7),
    ("sugarcane_bagasse", "Direct Combustion"): (1.2, 1.4),
    ("sugarcane_bagasse", "Biogas"): (0.7, 0.8)
}

# Carbon credit pricing tiers (₹ per kg CO₂e)
carbon_credit_prices = {
    "low": 0.50,
    "mid": 0.85,
    "high": 1.00
}

def get_weight_range_from_kg(weight_kg):
    """Convert weight in kg to weight range string"""
    if weight_kg < 10:
        return "<10kg"
    elif weight_kg <= 50:
        return "10–50kg"
    elif weight_kg <= 100:
        return "50–100kg"
    elif weight_kg <= 500:
        return "100–500kg"
    else:
        return ">500kg"

def estimate_ghg_savings_and_credits(waste_type, method, weight_kg, price_tier="mid"):
    """Estimate GHG savings and carbon credits"""
    # Normalize waste type
    waste_type_normalized = waste_type.lower().replace(" ", "_")
    
    key = (waste_type_normalized, method)
    if key not in ghg_saving_factors:
        # Try with generic crop_residues if specific type not found
        key = ("crop_residues", method)
        if key not in ghg_saving_factors:
            return {
                "ghg_savings_range": "N/A",
                "carbon_credit_value": "N/A",
                "credit_rate_used": "N/A"
            }

    min_factor, max_factor = ghg_saving_factors[key]
    min_saving = round(weight_kg * min_factor, 2)
    max_saving = round(weight_kg * max_factor, 2)
    credit_rate_per_kg = carbon_credit_prices.get(price_tier, 0.85)
    min_credit = round(min_saving * credit_rate_per_kg, 2)
    max_credit = round(max_saving * credit_rate_per_kg, 2)

    return {
        "ghg_savings_range": f"{min_saving} – {max_saving} kg CO₂e",
        "carbon_credit_value": f"₹{min_credit} – ₹{max_credit}",
        "credit_rate_used": f"{credit_rate_per_kg} ₹/kg CO₂e ({price_tier})",
        "co2_saved": (min_saving + max_saving) / 2,  # Average for calculations
        "carbon_credits": (min_credit + max_credit) / 2,  # Average for calculations
        "estimated_value": (min_credit + max_credit) / 2 * 15  # Estimated market value
    }

def get_optimal_processing_method(waste_type, weight_kg, moisture_content="moist", climate_zone="moderate"):
    """Get optimal processing method for waste type"""
    waste_type_normalized = waste_type.lower().replace(" ", "_")
    
    # Method selection logic based on waste type and conditions
    method_preferences = {
        "rice_straw": "Anaerobic Digestion",
        "wheat_straw": "Gasification",
        "corn_stalks": "Pyrolysis",
        "cotton_waste": "Composting",
        "sugarcane_bagasse": "Direct Combustion",
        "cow_dung": "Biogas" if weight_kg >= 50 else "Vermicompost",
        "fruit_veg_peels": "Vermicompost" if weight_kg <= 50 else "Composting",
        "crop_residues": "Mulching" if moisture_content == "dry" else "Composting"
    }
    
    return method_preferences.get(waste_type_normalized, "Anaerobic Digestion")

def full_farm_waste_recommendation(waste_type, weight_kg, moisture_content="moist", climate_zone="moderate", price_tier="mid"):
    """Main recommendation function integrated for our system"""
    
    # Get optimal processing method
    method = get_optimal_processing_method(waste_type, weight_kg, moisture_content, climate_zone)
    
    # Calculate expected output based on method and waste type
    output_factors = {
        "Biogas": (0.20, 0.30, "m³ of biogas"),
        "Anaerobic Digestion": (0.25, 0.35, "m³ of biogas"),
        "Gasification": (0.40, 0.50, "m³ of syngas"),
        "Pyrolysis": (0.30, 0.40, "liters of bio-oil"),
        "Direct Combustion": (0.80, 0.90, "kWh of energy"),
        "Composting": (0.30, 0.45, "kg of compost"),
        "Vermicompost": (0.60, 0.85, "kg of vermicompost"),
        "Mulching": (1.0, 1.0, "kg of mulch")
    }
    
    output_min, output_max, output_unit = output_factors.get(method, (0.3, 0.4, "units of processed waste"))
    output_min = round(weight_kg * output_min, 2)
    output_max = round(weight_kg * output_max, 2)
    
    # Generate reason based on method
    reasons = {
        "Biogas": f"Biogas production is optimal for {waste_type} of this quantity. The organic matter will generate methane gas suitable for cooking and heating.",
        "Anaerobic Digestion": f"Anaerobic digestion is ideal for {waste_type}. This process breaks down organic matter without oxygen, producing biogas and nutrient-rich slurry.",
        "Gasification": f"Gasification converts {waste_type} into synthetic gas (syngas) through high-temperature processing with limited oxygen.",
        "Pyrolysis": f"Pyrolysis breaks down {waste_type} at high temperatures without oxygen, producing bio-oil, biochar, and gases.",
        "Direct Combustion": f"Direct combustion of {waste_type} efficiently converts biomass directly into heat and electricity.",
        "Composting": f"Composting is suitable for {waste_type}. Microorganisms break down organic matter into nutrient-rich compost.",
        "Vermicompost": f"Vermicomposting uses earthworms to break down {waste_type} into high-quality organic fertilizer.",
        "Mulching": f"Using {waste_type} as mulch helps retain soil moisture, suppress weeds, and improve soil health."
    }
    
    reason = reasons.get(method, f"Processing {waste_type} using {method} is recommended for optimal resource utilization.")
    
    # Estimate GHG and carbon credits
    ghg_info = estimate_ghg_savings_and_credits(waste_type, method, weight_kg, price_tier)
    
    return {
        "recommended_method": method,
        "reason": reason,
        "expected_output_range": f"{output_min} – {output_max} {output_unit}",
        "ghg_savings_range": ghg_info["ghg_savings_range"],
        "carbon_credit_value": ghg_info["carbon_credit_value"],
        "credit_rate_used": ghg_info["credit_rate_used"],
        "co2_saved": ghg_info.get("co2_saved", 0),
        "carbon_credits": ghg_info.get("carbon_credits", 0),
        "estimated_value": ghg_info.get("estimated_value", 0),
        "processing_time": estimate_processing_time(method, weight_kg),
        "efficiency": min(95, 70 + (weight_kg / 100))  # Efficiency based on scale
    }

def estimate_processing_time(method, weight_kg):
    """Estimate processing time based on method and quantity"""
    base_times = {
        "Biogas": 15,  # days
        "Anaerobic Digestion": 20,
        "Gasification": 1,  # hours
        "Pyrolysis": 2,  # hours  
        "Direct Combustion": 0.5,  # hours
        "Composting": 45,  # days
        "Vermicompost": 60,  # days
        "Mulching": 0.1  # immediate
    }
    
    base_time = base_times.get(method, 10)
    scale_factor = (weight_kg / 1000) + 1
    
    if method in ["Gasification", "Pyrolysis", "Direct Combustion"]:
        return f"{round(base_time * scale_factor, 1)} hours"
    elif method == "Mulching":
        return "Immediate application"
    else:
        return f"{round(base_time * scale_factor)} days"

def get_waste_recommendations(waste_type: str, quantity: int, location: str = "Maharashtra"):
    """
    Wrapper function for full_farm_waste_recommendation to maintain API compatibility
    
    Args:
        waste_type: Type of agricultural waste
        quantity: Quantity in kg
        location: Location (used for climate zone inference)
        
    Returns:
        List of processing recommendations with details
    """
    try:
        # Map location to climate zone (simplified)
        climate_map = {
            "maharashtra": "moderate",
            "rajasthan": "hot_dry", 
            "kerala": "humid",
            "punjab": "moderate",
            "gujarat": "hot_dry"
        }
        
        climate_zone = climate_map.get(location.lower(), "moderate")
        
        # Get full recommendation
        result = full_farm_waste_recommendation(
            waste_type=waste_type.lower().replace(" ", "_"),
            weight_kg=quantity,
            climate_zone=climate_zone
        )
        
        # Convert to list format expected by API
        recommendations = []
        
        if "recommendations" in result:
            for rec in result["recommendations"]:
                recommendations.append({
                    "method": rec["method"],
                    "suitability": rec["suitability_score"],
                    "benefits": rec.get("benefits", []),
                    "processing_time": rec.get("processing_time", "Variable"),
                    "cost_estimate": rec.get("cost_range", "Moderate"),
                    "ghg_reduction": rec.get("ghg_savings", {}).get("co2_tons", 0)
                })
        
        return recommendations
        
    except Exception as e:
        # Fallback recommendations
        return [
            {
                "method": "Composting",
                "suitability": 80,
                "benefits": ["Soil improvement", "Nutrient recycling"],
                "processing_time": "30-45 days",
                "cost_estimate": "Low",
                "ghg_reduction": 0.5
            },
            {
                "method": "Biogas",
                "suitability": 70,
                "benefits": ["Clean energy", "Digestate fertilizer"],
                "processing_time": "15-30 days",
                "cost_estimate": "Medium",
                "ghg_reduction": 1.2
            }
        ]
