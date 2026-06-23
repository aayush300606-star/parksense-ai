import networkx as nx
from typing import Dict, Any, List
from .road_network_graph_engine import RoadNetworkGraphEngine
from .graph_feature_engine import GraphFeatureEngine

class CorridorIntelligenceEngine:
    """
    Identifies contiguous chains of highly vulnerable edges to define 'Corridors'.
    """

    @staticmethod
    def identify_corridors() -> List[Dict[str, Any]]:
        G = RoadNetworkGraphEngine.load_graph()
        features = GraphFeatureEngine.compute_features()
        
        corridors = []
        
        # Simple heuristic: Group nodes with high betweenness centrality into contiguous corridors
        # (For this hackathon, we will extract the top 3 subgraphs of critical nodes)
        
        critical_nodes = [n for n, feat in features.items() if feat['betweenness_centrality'] > 0.05]
        
        if not critical_nodes:
            return []
            
        # Create subgraph of only critical bottlenecks
        H = G.subgraph(critical_nodes)
        
        # Find weakly connected components (contiguous segments of road)
        components = list(nx.weakly_connected_components(H))
        
        for idx, comp in enumerate(components):
            if len(comp) < 2: continue # Ignore isolated nodes
            
            # Calculate health
            avg_pagerank = sum([features[n]['pagerank'] for n in comp]) / len(comp)
            
            corridors.append({
                "corridor_id": f"CORR-{idx+1}",
                "nodes_involved": list(comp),
                "length_nodes": len(comp),
                "corridor_importance_score": avg_pagerank * 1000,
                "corridor_risk_level": "Severe" if len(comp) > 3 else "High"
            })
            
        return sorted(corridors, key=lambda x: x['length_nodes'], reverse=True)
