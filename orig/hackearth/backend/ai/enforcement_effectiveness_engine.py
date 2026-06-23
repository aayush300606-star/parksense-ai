from typing import Dict, Any
from .root_cause_engine import RootCauseEngine
from .enforcement_knowledge_base import EnforcementKnowledgeBase

class EnforcementEffectivenessEngine:
    """
    Evaluates how effective specific physical interventions will be against a known Root Cause.
    (e.g., Towing works well for Metro spillover, but Barricades work better for Market vendors).
    """

    @staticmethod
    def estimate_roi(hotspot_id: int) -> Dict[str, Any]:
        cause_data = RootCauseEngine.analyze_root_cause(hotspot_id)
        primary_key = cause_data.get('primary_cause_key', 'UNKNOWN')
        
        # Hardcoded effectiveness matrix mapping Root Cause to the best Intervention
        # In production this would learn via ML from past enforcement success data
        
        if primary_key == "RC_METRO":
            best_immediate = "INT_TOWING"
            best_longterm = "INT_BARRICADES"
            expected_csi_reduction = 45 # Massive reduction
        elif primary_key == "RC_RIDE_HAIL" or primary_key == "RC_NIGHTLIFE":
            best_immediate = "INT_MARSHAL"
            best_longterm = "INT_PICKUP_ZONE"
            expected_csi_reduction = 30
        elif primary_key == "RC_COMMERCIAL":
            best_immediate = "INT_PATROL"
            best_longterm = "INT_LOADING_BAY"
            expected_csi_reduction = 25
        elif primary_key == "RC_SCHOOL":
            best_immediate = "INT_MARSHAL"
            best_longterm = "INT_PICKUP_ZONE"
            expected_csi_reduction = 40
        else:
            best_immediate = "INT_TOWING"
            best_longterm = "INT_PATROL"
            expected_csi_reduction = 20
            
        immediate_details = EnforcementKnowledgeBase.get_intervention_details(best_immediate)
        longterm_details = EnforcementKnowledgeBase.get_intervention_details(best_longterm)
        
        return {
            "hotspot_id": hotspot_id,
            "expected_csi_reduction_points": expected_csi_reduction,
            "expected_compliance_rate": "85%" if expected_csi_reduction > 30 else "60%",
            "optimal_immediate_action": {
                "key": best_immediate,
                "details": immediate_details
            },
            "optimal_longterm_action": {
                "key": best_longterm,
                "details": longterm_details
            }
        }
