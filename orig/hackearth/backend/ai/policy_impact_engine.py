from typing import Dict, Any
from .enforcement_effectiveness_engine import EnforcementEffectivenessEngine

class PolicyImpactEngine:
    """
    A lightweight Digital Twin expansion. Calculates the macro-economic and physical improvements 
    expected if long-term policy interventions (like creating a Loading Zone) are executed.
    """

    @staticmethod
    def simulate_policy(hotspot_id: int) -> Dict[str, Any]:
        effect_data = EnforcementEffectivenessEngine.estimate_roi(hotspot_id)
        
        csi_improvement = effect_data.get('expected_csi_reduction_points', 0)
        
        # If CSI drops by 30 points, that roughly correlates to a 30% reduction in Economic Loss (PIS)
        # and a significant recovery of effective lane width.
        
        return {
            "hotspot_id": hotspot_id,
            "simulated_policy": effect_data.get('optimal_longterm_action', {}).get('details', {}).get('name', 'Unknown Policy'),
            "expected_csi_improvement": csi_improvement,
            "expected_pis_reduction_percent": csi_improvement, # 1:1 rough proxy for hackathon
            "capacity_recovery_lanes": round(csi_improvement / 20.0, 1) # ~20 CSI = 1 full lane lost
        }
