from typing import Dict, Any

class PISRecalculationEngine:
    """
    Recalculates the Parking Impact Score (PIS) metrics based on the new simulated speed.
    """

    @staticmethod
    def recalculate(baseline: Dict[str, Any], simulated_speed: float) -> Dict[str, Any]:
        """
        Recomputes delay, fuel, emissions, and economic burden based on the ratio of speed improvement.
        """
        old_speed = baseline['current_speed_kmh']
        
        if simulated_speed <= old_speed:
            speed_ratio = 1.0
        else:
            # If speed doubles, delay halves.
            speed_ratio = old_speed / simulated_speed
            
        new_delay_hours = baseline['daily_delay_hours'] * speed_ratio
        new_fuel = baseline['fuel_wasted_per_day_liters'] * speed_ratio
        new_co2 = baseline['co2_emissions_kg_per_day'] * speed_ratio
        new_econ = baseline['economic_burden_inr_per_day'] * speed_ratio
        
        new_pis = baseline['pis_score'] * speed_ratio
        
        return {
            "pis_score": round(new_pis, 2),
            "daily_delay_hours": round(new_delay_hours, 1),
            "fuel_wasted_per_day_liters": round(new_fuel, 1),
            "co2_emissions_kg_per_day": round(new_co2, 1),
            "economic_burden_inr_per_day": round(new_econ, 2)
        }
