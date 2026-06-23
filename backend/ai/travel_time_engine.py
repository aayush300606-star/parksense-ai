class TravelTimeEngine:
    """
    Calculates normal and degraded travel times over the affected road segment.
    
    Uses the road segment length (derived from the DBSCAN cluster diameter)
    as the localized stretch over which the parking impact is felt.
    
    Formula:
        Time (seconds) = (Distance_m / Speed_kmh) * 3.6
        where 3.6 converts km/h to m/s (i.e., Time = Distance / (Speed * 1000/3600))
    """

    @staticmethod
    def calculate_travel_times(
        road_segment_length_m: float,
        base_speed_kmh: float,
        current_speed_kmh: float
    ) -> dict:
        """
        Computes normal and current travel times over the affected segment.
        
        Args:
            road_segment_length_m: Length of the road segment (meters)
            base_speed_kmh: Free-flow speed (km/h)
            current_speed_kmh: Degraded speed due to parking (km/h)
            
        Returns:
            dict with:
                - normal_travel_time_seconds: Time at free-flow speed
                - current_travel_time_seconds: Time at degraded speed
                - time_increase_factor: How many times slower
        """
        # Convert speeds to m/s for time calculation
        base_speed_ms = (base_speed_kmh * 1000.0) / 3600.0
        current_speed_ms = (current_speed_kmh * 1000.0) / 3600.0
        
        # Guard against division by zero
        if base_speed_ms <= 0:
            base_speed_ms = 0.1
        if current_speed_ms <= 0:
            current_speed_ms = 0.1
            
        normal_time = road_segment_length_m / base_speed_ms
        current_time = road_segment_length_m / current_speed_ms
        
        # Time increase factor (1.0 = no change, 2.0 = takes twice as long)
        if normal_time > 0:
            time_factor = current_time / normal_time
        else:
            time_factor = 1.0
        
        return {
            "normal_travel_time_seconds": round(normal_time, 2),
            "current_travel_time_seconds": round(current_time, 2),
            "time_increase_factor": round(time_factor, 2)
        }
