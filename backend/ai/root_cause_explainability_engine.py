from typing import Dict, Any
from .hotspot_dna_engine import HotspotDNAEngine
from .root_cause_engine import RootCauseEngine

class RootCauseExplainabilityEngine:
    """
    Translates complex Root Cause and Intervention Logic into plain-English answers
    for the AI Copilot (SCAC) and Executive Dashboards.
    """

    @staticmethod
    def explain_root_cause(hotspot_id: int) -> Dict[str, Any]:
        dna = HotspotDNAEngine.get_dna(hotspot_id)
        if "error" in dna:
            return dna
            
        cause_data = RootCauseEngine.analyze_root_cause(hotspot_id)
        pathway = cause_data.get('physical_manifestation', {})
        
        explanation = [
            f"This hotspot is primarily driven by {dna['primary_cause']}.",
            f"Vehicles exhibit {pathway.get('behavior', 'unauthorized parking behavior')}.",
            f"This directly results in a {pathway.get('capacity_impact', 'loss of road capacity')}, leading to {pathway.get('flow_impact', 'traffic slowdowns')}."
        ]
        
        if dna['predictability'] == "High":
            explanation.append(f"Because the behavior is Highly Predictable (peaking precisely at {dna['peak_violation_time']}), targeted enforcement will be highly effective.")
        else:
            explanation.append(f"The violation behavior has Low Predictability, making scheduled patrols difficult. Structural infrastructure changes are required.")
            
        explanation.append(f"Immediate Recommendation: {dna['recommended_immediate_action']}.")
        explanation.append(f"Long-Term Solution: {dna['recommended_infrastructure_fix']}.")
        
        return {
            "hotspot_id": hotspot_id,
            "explanation": " ".join(explanation),
            "confidence": cause_data.get('confidence', 0.8)
        }
