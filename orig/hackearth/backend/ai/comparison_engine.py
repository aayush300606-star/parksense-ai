from typing import Dict, Any

class ComparisonEngine:
    """
    Computes Before/After/Delta for simulation metrics.
    """

    @staticmethod
    def compare(baseline: Dict[str, Any], simulated: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a dictionary of deltas for the key metrics.
        """
        return {
            "csi": {
                "before": baseline['csi_score'],
                "after": simulated['csi_score'],
                "improvement": round(baseline['csi_score'] - simulated['csi_score'], 2)
            },
            "pis": {
                "before": baseline['pis_score'],
                "after": simulated['pis_score'],
                "improvement": round(baseline['pis_score'] - simulated['pis_score'], 2)
            },
            "capacity_loss_pct": {
                "before": baseline['capacity_loss_percentage'],
                "after": simulated['capacity_loss_percentage'],
                "improvement": round(baseline['capacity_loss_percentage'] - simulated['capacity_loss_percentage'], 1)
            },
            "speed_kmh": {
                "before": baseline['current_speed_kmh'],
                "after": simulated['current_speed_kmh'],
                "improvement": round(simulated['current_speed_kmh'] - baseline['current_speed_kmh'], 1)
            },
            "delay_hours": {
                "before": baseline['daily_delay_hours'],
                "after": simulated['daily_delay_hours'],
                "improvement": round(baseline['daily_delay_hours'] - simulated['daily_delay_hours'], 1)
            },
            "fuel_wasted_liters": {
                "before": baseline['fuel_wasted_per_day_liters'],
                "after": simulated['fuel_wasted_per_day_liters'],
                "improvement": round(baseline['fuel_wasted_per_day_liters'] - simulated['fuel_wasted_per_day_liters'], 1)
            },
            "economic_burden_inr": {
                "before": baseline['economic_burden_inr_per_day'],
                "after": simulated['economic_burden_inr_per_day'],
                "improvement": round(baseline['economic_burden_inr_per_day'] - simulated['economic_burden_inr_per_day'], 2)
            }
        }
