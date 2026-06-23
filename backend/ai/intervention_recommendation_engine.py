from typing import Dict, Any
from .enforcement_effectiveness_engine import EnforcementEffectivenessEngine
from .policy_impact_engine import PolicyImpactEngine

class InterventionRecommendationEngine:
    """
    Packages the final prescriptive intelligence for the Executive UI.
    Includes comprehensive explainability logic.
    """

    @staticmethod
    def recommend(hotspot_id: int) -> Dict[str, Any]:
        effect_data = EnforcementEffectivenessEngine.estimate_roi(hotspot_id)
        policy_data = PolicyImpactEngine.simulate_policy(hotspot_id)
        
        immediate = effect_data.get('optimal_immediate_action', {})
        longterm = effect_data.get('optimal_longterm_action', {})
        
        csi_improvement = policy_data.get('expected_csi_improvement', 20)
        
        return {
            "hotspot_id": hotspot_id,
            "intervention_priority": "Critical" if csi_improvement > 30 else "High" if csi_improvement > 15 else "Standard",
            "immediate_action": immediate.get('name', 'General Patrol'),
            "immediate_action_reasoning": immediate.get('reasoning', ''),
            "long_term_action": longterm.get('name', 'Infrastructure Review'),
            "long_term_action_reasoning": longterm.get('reasoning', ''),
            "expected_capacity_recovered": f"{policy_data.get('capacity_recovery_lanes', 1)} Lanes",
            "implementation_complexity": "High" if "Infrastructure" in longterm.get('name', '') or "Redesign" in longterm.get('name', '') else "Medium"
        }
