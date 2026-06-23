class RoadCapacityEngine:
    """
    Estimates road capacity and lane counts.
    """
    
    LANE_WIDTH_METERS = 3.5
    BASE_CAPACITY_PER_LANE_PER_HOUR = 1200 # PCU/hr

    @staticmethod
    def calculate_capacity(road_width: float, road_priority_score: int) -> dict:
        """
        Determines lane count and calculates capacity mathematically.
        """
        # Determine number of lanes (minimum 1, even for narrow residential roads)
        # Using 3.5 meters as the standard lane width.
        lane_count = max(1, round(road_width / RoadCapacityEngine.LANE_WIDTH_METERS))
        
        # Adjust per-lane capacity based on hierarchy score (Expressways are more efficient)
        efficiency_modifier = road_priority_score / 100.0
        adjusted_lane_capacity = RoadCapacityEngine.BASE_CAPACITY_PER_LANE_PER_HOUR * (0.6 + (0.4 * efficiency_modifier))
        
        total_capacity_pcu = lane_count * adjusted_lane_capacity
        
        # Max reasonable capacity for an 8-lane expressway might be around 9600
        # Min reasonable capacity is for a 1-lane residential road ~720
        # Normalize to 0-100
        capacity_score = min(100.0, (total_capacity_pcu / 10000.0) * 100.0)
        
        if capacity_score >= 80:
            capacity_factor = "Very High"
        elif capacity_score >= 60:
            capacity_factor = "High"
        elif capacity_score >= 40:
            capacity_factor = "Medium"
        elif capacity_score >= 20:
            capacity_factor = "Low"
        else:
            capacity_factor = "Very Low"
            
        return {
            "lane_count": int(lane_count),
            "capacity_factor": capacity_factor,
            "capacity_score": round(capacity_score, 2),
            "theoretical_pcu_hr": round(total_capacity_pcu, 2)
        }
