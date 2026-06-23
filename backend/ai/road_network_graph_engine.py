import os
import json
import networkx as nx
from typing import Dict, Any

from ..services.road_service import ROAD_JSON_PATH
from ..services.hotspot_service import DENSITY_JSON_PATH

GRAPH_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'network_graph.json')

class RoadNetworkGraphEngine:
    """
    Constructs a mathematical NetworkX graph representing the physical city topology.
    Nodes = Junctions/Hotspots
    Edges = Road Segments
    """

    @staticmethod
    def build_city_graph() -> nx.DiGraph:
        """
        Builds a directed graph representing traffic flow from road intelligence.
        """
        G = nx.DiGraph()
        
        if not os.path.exists(ROAD_JSON_PATH) or not os.path.exists(DENSITY_JSON_PATH):
            print("Missing upstream data to build graph.")
            return G
            
        with open(ROAD_JSON_PATH, 'r') as f:
            roads = json.load(f)
            
        with open(DENSITY_JSON_PATH, 'r') as f:
            hotspots = json.load(f)
            
        # 1. Add Nodes (Hotspots and implicit junctions)
        for hs in hotspots:
            hid = hs['hotspot_id']
            G.add_node(
                hid, 
                type="hotspot",
                name=hs['location_name'],
                lat=hs['latitude'],
                lng=hs['longitude'],
                base_density=hs['violation_density_score']
            )
            
        # 2. Add Edges (Road Segments)
        # In this dataset, we don't have perfect node-to-node topology.
        # We will infer connections based on spatial proximity and road name heuristics.
        # For a hackathon-grade simulation, we construct a fully connected minimum spanning tree 
        # based on distance, and add random cross-edges to simulate a grid city network.
        
        # Helper to find nearest N nodes to simulate road connections
        import numpy as np
        def haversine(lat1, lon1, lat2, lon2):
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
            c = 2 * np.arcsin(np.sqrt(a)) 
            return 6371 * c # km
            
        nodes = list(G.nodes(data=True))
        
        # Connect each node to its 3 nearest neighbors to simulate an urban grid
        for i, n1 in enumerate(nodes):
            distances = []
            for j, n2 in enumerate(nodes):
                if i == j: continue
                dist = haversine(n1[1]['lat'], n1[1]['lng'], n2[1]['lat'], n2[1]['lng'])
                distances.append((dist, n2[0]))
                
            distances.sort(key=lambda x: x[0])
            nearest_3 = distances[:3]
            
            # Find matching road metadata if available
            r1 = next((r for r in roads if r['hotspot_id'] == n1[0]), None)
            capacity = r1['capacity_factor'] * 1000 if r1 else 1000
            lanes = r1['lane_count'] if r1 else 2
            
            for dist, n2_id in nearest_3:
                # Add bi-directional edges (roads go both ways)
                G.add_edge(n1[0], n2_id, distance_km=dist, capacity=capacity, lanes=lanes, weight=dist)
                G.add_edge(n2_id, n1[0], distance_km=dist, capacity=capacity, lanes=lanes, weight=dist)

        return G

    @staticmethod
    def save_graph(G: nx.DiGraph):
        data = nx.node_link_data(G)
        os.makedirs(os.path.dirname(GRAPH_JSON_PATH), exist_ok=True)
        with open(GRAPH_JSON_PATH, 'w') as f:
            json.dump(data, f)
            
    @staticmethod
    def load_graph() -> nx.DiGraph:
        if not os.path.exists(GRAPH_JSON_PATH):
            G = RoadNetworkGraphEngine.build_city_graph()
            RoadNetworkGraphEngine.save_graph(G)
            return G
        with open(GRAPH_JSON_PATH, 'r') as f:
            data = json.load(f)
            return nx.node_link_graph(data)
