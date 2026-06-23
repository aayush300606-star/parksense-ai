class DelayEstimationEngine:
    """
    Estimates the per-vehicle delay and extrapolates to annual vehicle-hours lost.
    
    Delay is the additional time each vehicle spends traversing the affected segment
    compared to free-flow conditions.
    
    Annual impact estimation uses assumed Average Daily Traffic (ADT) volumes
    based on road hierarchy to project total delay across all vehicles.
    """

    # Assumed Average Daily Traffic by road hierarchy (vehicles/day)
    # Based on Indian urban traffic survey norms
    ADT_MAP = {
        "Expressway":       40000,
        "Major Arterial":   25000,
        "Minor Arterial":   15000,
        "Collector":        8000,
        "Secondary":        5000,
        "Residential":      2000,
        "Service":          800,
    }
    
    # Fraction of the day during which parking violations create congestion
    # Typically peak hours (morning + evening) = ~6 hours out of 24
    CONGESTION_HOURS_FRACTION = 6.0 / 24.0

    @staticmethod
    def calculate_delay(
        normal_travel_time_seconds: float,
        current_travel_time_seconds: float,
        road_hierarchy: str
    ) -> dict:
        """
        Calculates per-vehicle delay and annualized impact.
        
        Args:
            normal_travel_time_seconds: Free-flow travel time (seconds)
            current_travel_time_seconds: Degraded travel time (seconds)
            road_hierarchy: Road classification for ADT lookup
            
        Returns:
            dict with:
                - delay_seconds: Per-vehicle delay
                - delay_severity: Categorical severity
                - daily_vehicle_delay_hours: Total daily delay across all vehicles
                - annual_delay_vehicle_hours: Projected annual impact
        """
        delay = current_travel_time_seconds - normal_travel_time_seconds
        delay = max(0.0, delay)  # Delay cannot be negative
        
        # Severity classification (per-vehicle delay thresholds)
        if delay >= 60:
            severity = "Critical"
        elif delay >= 30:
            severity = "High"
        elif delay >= 15:
            severity = "Moderate"
        elif delay >= 5:
            severity = "Low"
        else:
            severity = "Minimal"
        
        # Annualized impact estimation
        adt = DelayEstimationEngine.ADT_MAP.get(road_hierarchy, 3000)
        
        # Only vehicles passing during congested hours experience the full delay
        affected_vehicles_per_day = adt * DelayEstimationEngine.CONGESTION_HOURS_FRACTION
        
        # Daily delay in vehicle-hours
        daily_delay_hours = (affected_vehicles_per_day * delay) / 3600.0
        
        # Annual delay (365 days, but parking violations may not occur every day)
        # Assume violations are persistent ~300 days/year for chronic hotspots
        annual_delay_hours = daily_delay_hours * 300
        
        return {
            "delay_seconds": round(delay, 2),
            "delay_severity": severity,
            "daily_vehicle_delay_hours": round(daily_delay_hours, 2),
            "annual_delay_vehicle_hours": round(annual_delay_hours, 2)
        }
