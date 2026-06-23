from typing import Dict, Any

class TrafficRecoverySimulation:
    """
    Simulates the improvement in traffic flow (speed, delay) based on capacity recovery.
    """

    @staticmethod
    def simulate(baseline: Dict[str, Any], new_capacity_loss_pct: float) -> Dict[str, Any]:
        """
        Uses a modified BPR (Bureau of Public Roads) function heuristic 
        to map capacity loss back to speed reduction.
        """
        ffs = baseline['free_flow_speed_kmh']
        
        # If capacity loss is 0, speed is free flow.
        # If capacity loss is 50%, speed drops significantly.
        # Speed = FFS * (1 - (CapacityLoss/100)^1.5) -> basic heuristic
        
        # Normalize the loss
        loss_factor = min(1.0, new_capacity_loss_pct / 100.0)
        
        speed_factor = 1.0 - (loss_factor ** 1.5)
        new_speed = ffs * max(0.1, speed_factor) # Minimum 10% of FFS to avoid 0
        
        # Calculate speed improvement
        speed_improvement = new_speed - baseline['current_speed_kmh']
        
        return {
            "current_speed_kmh": round(new_speed, 1),
            "speed_improvement_kmh": round(speed_improvement, 1)
        }
