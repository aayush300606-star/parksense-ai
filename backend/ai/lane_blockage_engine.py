class LaneBlockageEngine:
    """
    Translates metric width loss into lane-level blockage analytics.
    """
    
    LANE_WIDTH_METERS = 3.5

    @staticmethod
    def calculate_lane_blockage(original_lanes: int, occupied_width: float) -> dict:
        """
        Calculates how many full/partial lanes are rendered unusable.
        """
        # Blocked lanes calculated by how many 3.5m chunks are occupied
        blocked_lanes_raw = occupied_width / LaneBlockageEngine.LANE_WIDTH_METERS
        blocked_lanes = round(blocked_lanes_raw)
        
        # Ensure we don't block more lanes than exist
        if blocked_lanes > original_lanes:
            blocked_lanes = original_lanes
            
        remaining_lanes = original_lanes - blocked_lanes
        
        # Lane utilization score: 100% means all lanes open. 0% means all blocked.
        if original_lanes > 0:
            lane_utilization = (remaining_lanes / original_lanes) * 100.0
        else:
            lane_utilization = 0.0
            
        return {
            "blocked_lanes": int(blocked_lanes),
            "remaining_lanes": int(remaining_lanes),
            "lane_utilization": round(lane_utilization, 2),
            "lane_blockage_score": round((blocked_lanes / max(1, original_lanes)) * 100.0, 2)
        }
