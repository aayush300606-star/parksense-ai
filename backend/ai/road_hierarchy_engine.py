class RoadHierarchyEngine:
    """
    Determines Road Hierarchy and assigns priority scores.
    """
    
    HIERARCHY_MAPPING = {
        "Expressway": {"hierarchy": "Expressway", "score": 100},
        "Highway": {"hierarchy": "Major Arterial", "score": 90},
        "Arterial": {"hierarchy": "Major Arterial", "score": 90},
        "Collector Road": {"hierarchy": "Collector", "score": 60},
        "Commercial": {"hierarchy": "Collector", "score": 60},
        "Minor Road": {"hierarchy": "Secondary", "score": 50},
        "Residential": {"hierarchy": "Residential", "score": 40},
        "Service Road": {"hierarchy": "Service", "score": 20},
        "Service": {"hierarchy": "Service", "score": 20},
        "Local": {"hierarchy": "Residential", "score": 40} # Default fallback
    }

    @staticmethod
    def calculate_hierarchy(road_category: str) -> dict:
        """
        Takes a road category and returns the strict hierarchy and priority score.
        """
        mapping = RoadHierarchyEngine.HIERARCHY_MAPPING.get(road_category, RoadHierarchyEngine.HIERARCHY_MAPPING["Local"])
        
        return {
            "road_hierarchy": mapping["hierarchy"],
            "road_priority_score": mapping["score"]
        }
