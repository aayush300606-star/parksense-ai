import networkx as nx
from typing import Dict, Any
from .road_network_graph_engine import RoadNetworkGraphEngine

class GraphFeatureEngine:
    """
    Computes mathematical network topology metrics to identify structurally vulnerable corridors.
    """

    @staticmethod
    def compute_features() -> Dict[str, Any]:
        G = RoadNetworkGraphEngine.load_graph()
        
        # Centrality Metrics
        # Degree: How many roads connect here?
        degree_cent = nx.degree_centrality(G)
        
        # Betweenness: How often is this junction on the shortest path between two points?
        betweenness_cent = nx.betweenness_centrality(G, weight='weight')
        
        # Eigenvector: Is this junction connected to other highly connected junctions?
        try:
            eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000)
        except nx.PowerIterationFailedConvergence:
            eigenvector_cent = {n: 0 for n in G.nodes()}
            
        # PageRank: Overall traffic flow importance
        pagerank = nx.pagerank(G, alpha=0.85, weight='weight')
        
        features = {}
        for node in G.nodes():
            features[node] = {
                "degree_centrality": degree_cent.get(node, 0),
                "betweenness_centrality": betweenness_cent.get(node, 0),
                "eigenvector_centrality": eigenvector_cent.get(node, 0),
                "pagerank": pagerank.get(node, 0),
                # Aggregate influence
                "network_influence_score": (betweenness_cent.get(node, 0) * 0.5) + (pagerank.get(node, 0) * 0.5)
            }
            
        return features
