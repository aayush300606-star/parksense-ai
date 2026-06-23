from typing import Dict, Any, List
import random

class ResourceAllocationEngine:
    """
    Simulates a constrained environment and assigns high-priority hotspots to specific teams.
    Assigns realistic operational teams based on context and priority.
    """

    OPERATIONAL_UNITS = [
        {"name": "Traffic Patrol Unit", "specialty": "flow_management", "description": "Specialized in unblocking active traffic flow."},
        {"name": "Parking Enforcement Unit", "specialty": "parking_violations", "description": "Equipped with towing and auto-challan capabilities."},
        {"name": "Rapid Response Team", "specialty": "emergency_routes", "description": "Quick deployment unit for clearing emergency corridors."},
        {"name": "Intersection Control Team", "specialty": "junction_management", "description": "Focused on signal compliance and junction blockades."},
        {"name": "Mobile Enforcement Team", "specialty": "general_patrol", "description": "General purpose roaming enforcement."}
    ]

    @staticmethod
    def allocate_teams(hotspots: List[Dict[str, Any]], available_teams: int) -> List[Dict[str, Any]]:
        """
        Assigns hotspots to patrol teams. 
        """
        sorted_hs = sorted(hotspots, key=lambda x: x['priority_score'], reverse=True)
        max_hotspots_per_team = 5
        total_capacity = available_teams * max_hotspots_per_team
        assigned_hs = sorted_hs[:total_capacity]
        
        allocations = []
        for hs in assigned_hs:
            hs_copy = dict(hs)
            
            # Intelligent assignment logic
            if hs.get('is_emergency'):
                unit = next(u for u in ResourceAllocationEngine.OPERATIONAL_UNITS if u['specialty'] == 'emergency_routes')
                reasoning = "Assigned Rapid Response Team because hotspot intersects an active emergency corridor requiring immediate clearance."
            elif 'Parking' in hs.get('recommended_action', ''):
                unit = next(u for u in ResourceAllocationEngine.OPERATIONAL_UNITS if u['specialty'] == 'parking_violations')
                reasoning = f"Assigned Parking Enforcement Unit due to high volume of actionable parking violations requiring towing or ticketing."
            elif hs.get('priority_score', 0) > 80:
                unit = next(u for u in ResourceAllocationEngine.OPERATIONAL_UNITS if u['specialty'] == 'flow_management')
                reasoning = "Assigned Traffic Patrol Unit to manage severe active congestion and manually direct traffic flow."
            else:
                unit = random.choice([u for u in ResourceAllocationEngine.OPERATIONAL_UNITS if u['specialty'] in ['general_patrol', 'junction_management']])
                reasoning = f"Assigned {unit['name']} for routine enforcement sweep and visibility."
                
            hs_copy['recommended_team'] = unit['name']
            hs_copy['assignment_reasoning'] = reasoning
            allocations.append(hs_copy)
            
        return allocations
