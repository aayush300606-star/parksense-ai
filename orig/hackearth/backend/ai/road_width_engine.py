class RoadWidthEngine:
    """
    Estimates road width using documented transportation engineering rules.
    """
    
    WIDTH_MAPPING = {
        "Expressway": 30.0,
        "Major Arterial": 20.0,
        "Minor Arterial": 18.0,
        "Collector": 15.0,
        "Secondary": 12.0,
        "Residential": 8.0,
        "Service": 6.0
    }

    @staticmethod
    def estimate_width(road_hierarchy: str) -> float:
        """
        Returns estimated road width in meters based on the hierarchy.
        Never generates random values.
        """
        # Default to a secondary road if not explicitly matched
        return RoadWidthEngine.WIDTH_MAPPING.get(road_hierarchy, 12.0)
