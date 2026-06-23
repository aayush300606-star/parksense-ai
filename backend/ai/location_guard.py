import json
import os
from typing import List, Set

from ..services.hotspot_service import DENSITY_JSON_PATH
from ..services.road_service import ROAD_JSON_PATH

class LocationGuard:
    """
    Generates a dynamic whitelist of every valid physical entity in the city.
    The AI is absolutely forbidden from referencing a location not on this list.
    """

    @staticmethod
    def get_approved_entities() -> Set[str]:
        approved = set()
        
        # 1. Add Hotspot Locations
        if os.path.exists(DENSITY_JSON_PATH):
            with open(DENSITY_JSON_PATH, 'r') as f:
                data = json.load(f)
                for h in data:
                    name = h.get('location_name')
                    if name and name != 'Unknown':
                        approved.add(name.lower().strip())
        
        # 2. Add Road Names
        if os.path.exists(ROAD_JSON_PATH):
            with open(ROAD_JSON_PATH, 'r') as f:
                data = json.load(f)
                for r in data:
                    name = r.get('road_name')
                    if name and name != 'Unknown':
                        approved.add(name.lower().strip())
                        
        # Manually add the city name bounds
        approved.update(['bengaluru', 'bangalore', 'unknown'])
        
        return approved

    @staticmethod
    def is_location_valid(location_string: str) -> bool:
        """Checks if a named location exists in the whitelist."""
        whitelist = LocationGuard.get_approved_entities()
        if not whitelist:
            return True # If no data, bypass to prevent crashes
            
        loc = location_string.lower().strip()
        # Substring search (e.g. "Koramangala" is valid if "Koramangala Main Road" is in whitelist)
        for valid_loc in whitelist:
            if loc in valid_loc or valid_loc in loc:
                return True
        return False
