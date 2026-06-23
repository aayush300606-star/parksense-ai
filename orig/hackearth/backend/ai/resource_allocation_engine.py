from typing import Dict, Any, List

class ResourceAllocationEngine:
    """
    Simulates a constrained environment and assigns high-priority hotspots to specific teams.
    """

    @staticmethod
    def allocate_teams(hotspots: List[Dict[str, Any]], available_teams: int) -> List[Dict[str, Any]]:
        """
        Assigns hotspots to patrol teams. 
        Each team can handle ~4-5 hotspots per shift depending on geography.
        """
        # Sort hotspots by absolute priority
        sorted_hs = sorted(hotspots, key=lambda x: x['priority_score'], reverse=True)
        
        # Max capacity per team
        max_hotspots_per_team = 5
        total_capacity = available_teams * max_hotspots_per_team
        
        # We only assign the top N hotspots that fit within capacity
        assigned_hs = sorted_hs[:total_capacity]
        
        allocations = []
        for i, hs in enumerate(assigned_hs):
            team_id = (i % available_teams) + 1
            hs_copy = dict(hs)
            hs_copy['recommended_team'] = f"Patrol Team Alpha-{team_id}"
            allocations.append(hs_copy)
            
        return allocations
