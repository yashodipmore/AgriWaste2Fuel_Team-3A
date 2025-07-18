# Farm-Waste Handling Recommendation System with GHG + Carbon Credit Estimation

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
    "crop_residues": {"%C": 45, "%N": 0.7, "cn_ratio": 64, "decomposition_speed": "medium"}
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
}

# Carbon credit pricing tiers (₹ per kg CO₂e)
carbon_credit_prices = {
    "low": 0.50,
    "mid": 0.85,
    "high": 1.00
}

# GHG savings + credit estimator
def estimate_ghg_savings_and_credits(waste_type, method, weight_kg, price_tier="mid"):
    key = (waste_type, method)
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
        "credit_rate_used": f"{credit_rate_per_kg} ₹/kg CO₂e ({price_tier})"
    }

# Main recommendation function
def full_farm_waste_recommendation(waste_type, weight_range, moisture_content, climate_zone, price_tier="mid"):
    weight = weight_range_midpoints[weight_range]
    method = ""
    reason = ""
    output_min = 0
    output_max = 0
    output_unit = ""

    # Recommendation logic
    if waste_type == "cow_dung":
        if weight >= 50 and moisture_content in ["moist", "wet"]:
            method = "Biogas"
            reason = (
                "You have enough cow dung and it is wet — this is great for making gas at home. "
                "The gas can be used for cooking or lighting. After making gas, a leftover liquid comes out, "
                "which is good for farming. This setup works well for families or groups of farmers."
            )
            output_min = round(weight * 0.20, 2)
            output_max = round(weight * 0.30, 2)
            output_unit = "m³ of biogas"
        else:
            method = "Vermicompost"
            reason = (
                "With less dung or if it’s a bit dry, making vermicompost is a good idea. "
                "Just mix dung with worms in a box or pit. After 30–40 days, it turns into black compost "
                "that is very good for crops."
            )
            output_min = round(weight * 0.60, 2)
            output_max = round(weight * 0.75, 2)
            output_unit = "kg of vermicompost"

    elif waste_type == "fruit_veg_peels":
        if moisture_content == "wet" and weight <= 50:
            method = "Vermicompost"
            reason = (
                "Wet kitchen waste like fruit or vegetable peels is best for making compost with worms. "
                "You don’t need much space — even a small bin is enough. The final compost is soft and good "
                "for home gardens or crops."
            )
            output_min = round(weight * 0.60, 2)
            output_max = round(weight * 0.85, 2)
            output_unit = "kg of vermicompost"
        else:
            method = "Composting"
            reason = (
                "If you have a lot of peels or if it’s too wet or dry, you can compost it. "
                "Just make a pile with dry waste or cow dung and turn it sometimes. After a few weeks, "
                "it becomes healthy soil compost."
            )
            output_min = round(weight * 0.35, 2)
            output_max = round(weight * 0.45, 2)
            output_unit = "kg of compost"

    elif waste_type == "crop_residues":
        if moisture_content == "dry" and climate_zone == "dry_hot":
            method = "Mulching"
            reason = (
                "Dry crop waste is best used as mulch in dry or hot areas. Just spread it on your soil. "
                "It saves water, keeps the soil cool, and stops weeds from growing."
            )
            output_min = output_max = weight
            output_unit = "kg of mulch"
        else:
            method = "Composting"
            reason = (
                "Dry crop waste can be composted by mixing it with cow dung or wet waste. "
                "Keep it moist and turn it sometimes. After 6–8 weeks, it becomes soft compost that is good for farms."
            )
            output_min = round(weight * 0.30, 2)
            output_max = round(weight * 0.45, 2)
            output_unit = "kg of compost"

    # Estimate GHG and credit
    ghg_info = estimate_ghg_savings_and_credits(waste_type, method, weight, price_tier)

    return {
        "recommended_method": method,
        "reason": reason,
        "expected_output_range": f"{output_min} – {output_max} {output_unit}",
        "ghg_savings_range": ghg_info["ghg_savings_range"],
        "carbon_credit_value": ghg_info["carbon_credit_value"],
        "credit_rate_used": ghg_info["credit_rate_used"]
    }
