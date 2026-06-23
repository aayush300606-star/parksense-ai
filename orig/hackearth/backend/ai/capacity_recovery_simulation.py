from typing import Dict, Any

class CapacityRecoverySimulation:
    """
    Simulates the physical recovery of road width when illegal parking is removed.
    """

    @staticmethod
    def simulate(baseline: Dict[str, Any], removal_pct: float, total_road_width: float) -> Dict[str, Any]:
        """
        Calculates the new effective road width and capacity loss.
        """
        # How much width was lost to parking?
        width_lost_to_parking = total_road_width - baseline['effective_width_m']
        
        # Recover width based on removal percentage
        width_recovered = width_lost_to_parking * (removal_pct / 100.0)
        
        new_effective_width = baseline['effective_width_m'] + width_recovered
        
        # Recalculate capacity loss percentage
        new_capacity_loss_pct = ((total_road_width - new_effective_width) / total_road_width) * 100.0
        
        return {
            "effective_width_m": round(new_effective_width, 2),
            "width_recovered_m": round(width_recovered, 2),
            "capacity_loss_percentage": round(max(0.0, new_capacity_loss_pct), 1)
        }
