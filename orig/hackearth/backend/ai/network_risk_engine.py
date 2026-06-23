from typing import Dict, Any, List
from .graph_feature_engine import GraphFeatureEngine
from .gnn_engine import GNNEngine
from .congestion_propagation_engine import CongestionPropagationEngine

class NetworkRiskEngine:
    """
    Fuses Graph theory, GNN predictions, and physical propagation to identify the absolute 
    most fragile infrastructure nodes in the city network.
    """

    @staticmethod
    def calculate_vulnerability() -> List[Dict[str, Any]]:
        features = GraphFeatureEngine.compute_features()
        gnn_results = GNNEngine.train_and_predict()
        
        risk_profile = []
        
        for node, feat in features.items():
            gnn_score = gnn_results['predictions'][node]['gnn_vulnerability_score']
            betweenness = feat['betweenness_centrality']
            pagerank = feat['pagerank']
            
            # Propagation Math
            prop_data = CongestionPropagationEngine.model_spillover(node)
            ripple_score = prop_data.get('ripple_effect_score', 0)
            
            # Total Network Fragility Score (0-100)
            # High GNN Vulnerability + High Betweenness = Critical Point of Failure
            normalized_betweenness = min(100, betweenness * 1000) # Scale roughly to 100
            fragility = (gnn_score * 0.5) + (normalized_betweenness * 0.3) + (min(100, ripple_score) * 0.2)
            
            risk_profile.append({
                "hotspot_id": node,
                "gnn_risk": gnn_score,
                "betweenness": betweenness,
                "ripple_score": ripple_score,
                "network_fragility_score": min(100, fragility),
                "risk_level": "Critical" if fragility > 80 else "High" if fragility > 60 else "Moderate"
            })
            
        # Sort by most fragile
        return sorted(risk_profile, key=lambda x: x['network_fragility_score'], reverse=True)
