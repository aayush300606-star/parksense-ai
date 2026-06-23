from typing import Dict, Any

class BaselineStateEngine:
    """
    Captures the current state of a hotspot before any digital twin simulations.
    """

    @staticmethod
    def capture_baseline(csi_data: Dict, pis_data: Dict) -> Dict[str, Any]:
        """
        Extracts the essential metrics from the current intelligence pipelines.
        """
        return {
            "csi_score": csi_data['csi_score'],
            "pis_score": pis_data.get('pis_score', 0),
            "effective_width_m": csi_data['effective_width_m'],
            "capacity_loss_percentage": csi_data['capacity_loss_percentage'],
            "current_speed_kmh": csi_data.get('current_speed_kmh', 15), # Fallback if missing
            "free_flow_speed_kmh": csi_data.get('free_flow_speed_kmh', 40),
            "daily_delay_hours": pis_data.get('daily_delay_hours', 0),
            "fuel_wasted_per_day_liters": pis_data.get('fuel_wasted_per_day_liters', 0),
            "co2_emissions_kg_per_day": pis_data.get('co2_emissions_kg_per_day', 0),
            "economic_burden_inr_per_day": pis_data.get('economic_burden_inr_per_day', 0)
        }
