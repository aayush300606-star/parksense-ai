from typing import Dict, Any


class EnvironmentalImpactEngine:
    """
    Translates fuel waste into CO2 emissions and environmental burden.
    """

    # kg of CO2 per liter of mixed urban fuel (Petrol/Diesel mix)
    CO2_PER_LITER = 2.35 

    @staticmethod
    def estimate_emissions(fuel_wasted_per_day: float) -> Dict[str, Any]:
        """
        Estimates CO2 emissions based on fuel wasted.
        """
        co2_per_day_kg = fuel_wasted_per_day * EnvironmentalImpactEngine.CO2_PER_LITER
        co2_per_year_kg = co2_per_day_kg * 300
        co2_per_year_tons = co2_per_year_kg / 1000.0
        
        # Environmental score: 100 if > 5000 kg CO2 daily
        environmental_impact_score = min(100.0, (co2_per_day_kg / 5000.0) * 100.0)
        
        if environmental_impact_score >= 80:
            level = "Severe"
        elif environmental_impact_score >= 60:
            level = "High"
        elif environmental_impact_score >= 40:
            level = "Moderate"
        elif environmental_impact_score >= 20:
            level = "Low"
        else:
            level = "Minimal"
            
        return {
            "co2_emissions_kg_per_day": round(co2_per_day_kg, 1),
            "co2_emissions_tons_per_year": round(co2_per_year_tons, 1),
            "pollution_increase_factor": round(1.0 + (environmental_impact_score / 200.0), 2),
            "environmental_impact_score": round(environmental_impact_score, 2),
            "environmental_level": level
        }
