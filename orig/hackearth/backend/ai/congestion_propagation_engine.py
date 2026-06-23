import networkx as nx
from typing import Dict, Any, List
from .road_network_graph_engine import RoadNetworkGraphEngine

class CongestionPropagationEngine:
    """
    Models how physical congestion spills over into adjacent network nodes.
    """

    @staticmethod
    def model_spillover(hotspot_id: int, base_congestion_radius: float = 1.0) -> Dict[str, Any]:
        """
        Uses BFS traversal to model traffic back-propagation.
        Congestion diminishes the further it travels from the epicenter.
        """
        G = RoadNetworkGraphEngine.load_graph()
        
        if not G.has_node(hotspot_id):
            return {"error": "Node not found"}
            
        primary_zone = []
        secondary_zone = []
        tertiary_zone = []
        
        # Calculate shortest path lengths from the epicenter to all other nodes (representing back-queue)
        lengths = nx.single_source_dijkstra_path_length(G, hotspot_id, weight='distance_km')
        
        for node, dist in lengths.items():
            if node == hotspot_id:
                continue
                
            # Spillover Decay function
            spillover_risk = max(0, 100 - (dist * 20)) # Decays by 20 points per KM
            
            impact_obj = {
                "affected_node": node,
                "distance_km": dist,
                "spillover_risk": spillover_risk
            }
            
            if dist <= 1.0:
                primary_zone.append(impact_obj)
            elif dist <= 2.5:
                secondary_zone.append(impact_obj)
            elif dist <= 5.0:
                tertiary_zone.append(impact_obj)
                
        ripple_score = len(primary_zone)*3 + len(secondary_zone)*2 + len(tertiary_zone)
        
        return {
            "epicenter": hotspot_id,
            "primary_impact_zone": primary_zone,
            "secondary_impact_zone": secondary_zone,
            "tertiary_impact_zone": tertiary_zone,
            "influence_radius_km": max(lengths.values()) if lengths else 0,
            "ripple_effect_score": ripple_score
        }
