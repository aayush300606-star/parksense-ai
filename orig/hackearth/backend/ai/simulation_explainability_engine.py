from typing import Dict, Any

class SimulationExplainabilityEngine:
    """
    Generates natural language explanations for Digital Twin simulations.
    """

    @staticmethod
    def generate(scenario_name: str, deltas: Dict[str, Any], recovered_width: float) -> str:
        """
        Creates a readable explanation of the simulation.
        """
        csi_imp = deltas['csi']['improvement']
        if csi_imp <= 0:
            return f"Executing '{scenario_name}' yields no significant impact on this location."
            
        speed_before = deltas['speed_kmh']['before']
        speed_after = deltas['speed_kmh']['after']
        
        delay_saved = deltas['delay_hours']['improvement']
        fuel_saved = deltas['fuel_wasted_liters']['improvement']
        
        parts = [
            f"Executing '{scenario_name}' restored {recovered_width:.1f}m of usable carriageway.",
            f"Traffic speed improved from {speed_before:.1f} km/h to {speed_after:.1f} km/h.",
            f"CSI improved by {csi_imp:.1f} points.",
            f"Total daily delay reduced by {delay_saved:.1f} hours, saving {fuel_saved:.1f} liters of fuel."
        ]
        
        return " ".join(parts)
