from typing import Dict, Any, List
import math

class PatrolOptimizationEngine:
    """
    Sequences the assigned hotspots geographically to minimize travel time.
    """

    @staticmethod
    def optimize_routes(allocated_hotspots: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups hotspots by assigned team and sequences them using a simple nearest-neighbor TSP heuristic.
        """
        routes = {}
        
        # Group by team
        for hs in allocated_hotspots:
            team = hs['recommended_team']
            if team not in routes:
                routes[team] = []
            routes[team].append(hs)
            
        # Optimize sequence for each team
        for team, points in routes.items():
            if not points:
                continue
                
            optimized = []
            unvisited = list(points)
            
            # Start with highest priority in this group
            current = max(unvisited, key=lambda x: x['priority_score'])
            optimized.append(current)
            unvisited.remove(current)
            
            while unvisited:
                # Find nearest neighbor
                nearest = None
                min_dist = float('inf')
                for node in unvisited:
                    # Haversine or simple Euclidean approximation
                    dx = node['latitude'] - current['latitude']
                    dy = node['longitude'] - current['longitude']
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = node
                        
                optimized.append(nearest)
                unvisited.remove(nearest)
                current = nearest
                
            routes[team] = optimized
            
        return routes
