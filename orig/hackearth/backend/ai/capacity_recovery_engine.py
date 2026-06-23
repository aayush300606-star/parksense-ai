from typing import Dict, Any


class CapacityRecoveryEngine:
    """
    Simulates the 'enforced state' where illegal parking is removed
    to estimate capacity and speed recovery.
    """

    # Recovery potential based on road hierarchy
    RECOVERY_FACTOR = {
        "Expressway": 0.90,
        "Major Arterial": 0.85,
        "Minor Arterial": 0.80,
        "Collector": 0.75,
        "Secondary": 0.70,
        "Residential": 0.60,
        "Service": 0.50,
    }

    @staticmethod
    def simulate_recovery(
        capacity_loss_percentage: float,
        speed_reduction_percentage: float,
        road_hierarchy: str
    ) -> Dict[str, Any]:
        """
        Estimates the percentage of capacity and speed recovered if enforced.
        """
        factor = CapacityRecoveryEngine.RECOVERY_FACTOR.get(road_hierarchy, 0.75)
        
        capacity_recovered = capacity_loss_percentage * factor
        speed_recovered = speed_reduction_percentage * (factor * 0.9) # Speed recovery is slightly lower than capacity recovery
        
        delay_reduction_pct = speed_recovered # Proxy
        
        # Score: 100 if > 50% capacity recovered
        recovery_score = min(100.0, (capacity_recovered / 50.0) * 100.0)
        
        return {
            "capacity_recovered_pct": round(capacity_recovered, 1),
            "speed_recovered_pct": round(speed_recovered, 1),
            "delay_reduction_pct": round(delay_reduction_pct, 1),
            "travel_time_improvement_pct": round(delay_reduction_pct, 1), # Roughly equivalent
            "recovery_score": round(recovery_score, 2)
        }
