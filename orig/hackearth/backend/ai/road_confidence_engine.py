class RoadConfidenceEngine:
    """
    Provides granular, attribute-level confidence percentages.
    """
    
    @staticmethod
    def calculate_confidence(source: str) -> dict:
        """
        Returns split confidence scores for different GIS attributes.
        """
        if source == "MapMyIndia API":
            return {
                "road_name_confidence": 0.99,
                "road_width_confidence": 0.95,
                "lane_count_confidence": 0.95,
                "road_category_confidence": 0.98,
                "road_hierarchy_confidence": 0.98,
                "speed_limit_confidence": 0.99,
                "geometry_confidence": 0.98
            }
        else:
            return {
                "road_name_confidence": 0.85,
                "road_width_confidence": 0.82,
                "lane_count_confidence": 0.80,
                "road_category_confidence": 0.88,
                "road_hierarchy_confidence": 0.88,
                "speed_limit_confidence": 0.85,
                "geometry_confidence": 0.75
            }
