from typing import Dict, Any
from .network_risk_engine import NetworkRiskEngine
from .congestion_propagation_engine import CongestionPropagationEngine

class NetworkExplainabilityEngine:
    """
    Translates complex Graph Neural Network features and NetworkX centralities into
    deterministic, human-readable explanations.
    """

    @staticmethod
    def explain_node(hotspot_id: int) -> Dict[str, Any]:
        risks = NetworkRiskEngine.calculate_vulnerability()
        target = next((r for r in risks if r['hotspot_id'] == hotspot_id), None)
        
        if not target:
            return {"error": "Node not found."}
            
        prop_data = CongestionPropagationEngine.model_spillover(hotspot_id)
        
        explanation = []
        explanation.append(f"Network Risk Level is {target['risk_level']}.")
        
        if target['betweenness'] > 0.05:
            explanation.append("This junction acts as a critical transit bridge (High Betweenness Centrality).")
            
        if target['gnn_risk'] > 60:
            explanation.append("The Graph Neural Network predicts a high probability of cascade failure.")
            
        if target['ripple_score'] > 10:
            explanation.append(f"Congestion here will ripple outwards, directly impacting {len(prop_data['primary_impact_zone'])} primary adjacent roads and {len(prop_data['secondary_impact_zone'])} secondary roads.")
            
        explanation.append(f"The maximum propagation radius for congestion at this node is {prop_data['influence_radius_km']:.1f} kilometers.")
        
        return {
            "hotspot_id": hotspot_id,
            "machine_readable": {
                "gnn_risk": target['gnn_risk'],
                "betweenness": target['betweenness'],
                "ripple_score": target['ripple_score'],
                "propagation_radius": prop_data['influence_radius_km']
            },
            "human_readable": " ".join(explanation)
        }
