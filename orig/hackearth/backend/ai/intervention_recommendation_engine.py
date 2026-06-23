from typing import Dict, Any
from .enforcement_effectiveness_engine import EnforcementEffectivenessEngine
from .policy_impact_engine import PolicyImpactEngine

class InterventionRecommendationEngine:
    """
    Packages the final prescriptive intelligence for the Executive UI.
    """

    @staticmethod
    def recommend(hotspot_id: int) -> Dict[str, Any]:
        effect_data = EnforcementEffectivenessEngine.estimate_roi(hotspot_id)
        policy_data = PolicyImpactEngine.simulate_policy(hotspot_id)
        
        immediate = effect_data.get('optimal_immediate_action', {})
        longterm = effect_data.get('optimal_longterm_action', {})
        
        return {
            "hotspot_id": hotspot_id,
            "intervention_priority": "Critical" if policy_data['expected_csi_improvement'] > 30 else "High",
            "immediate_action": immediate.get('details', {}).get('name', 'Unknown'),
            "short_term_action": "Increase Patrol Frequency",
            "long_term_action": longterm.get('details', {}).get('name', 'Unknown'),
            "expected_capacity_recovered": f"{policy_data['capacity_recovery_lanes']} Lanes",
            "implementation_complexity": longterm.get('details', {}).get('implementation_complexity', 'High')
        }
