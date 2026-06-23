class BaseSpeedEngine:
    """
    Maps Road Hierarchy classifications to standard free-flow speeds (km/h).
    
    Based on Indian Roads Congress (IRC) guidelines and urban planning norms:
    - IRC:SP:84-2014 (Manual of Specifications & Standards for Expressways)
    - IRC:64-1990 (Capacity of Roads in Rural Areas)
    - Typical urban Indian city observed free-flow speeds.
    
    These are the maximum expected speeds under zero-congestion, no-parking conditions.
    """

    # Free-flow speed mapping (km/h) by road hierarchy
    SPEED_MAP = {
        "Expressway":       80,
        "Major Arterial":   60,
        "Minor Arterial":   50,
        "Collector":        40,
        "Secondary":        35,
        "Residential":      25,
        "Service":          20,
    }

    # Volume-to-capacity ratio under free-flow (baseline α for BPR)
    BASELINE_VC_RATIO = {
        "Expressway":       0.30,
        "Major Arterial":   0.45,
        "Minor Arterial":   0.50,
        "Collector":        0.55,
        "Secondary":        0.60,
        "Residential":      0.65,
        "Service":          0.70,
    }

    @staticmethod
    def get_base_speed(road_hierarchy: str) -> dict:
        """
        Returns the deterministic free-flow speed for a given road hierarchy.
        
        Returns:
            dict with:
                - base_speed_kmh: Free-flow speed in km/h
                - base_vc_ratio: Baseline volume-to-capacity ratio
                - source: Attribution string
        """
        speed = BaseSpeedEngine.SPEED_MAP.get(road_hierarchy, 30)
        vc = BaseSpeedEngine.BASELINE_VC_RATIO.get(road_hierarchy, 0.60)

        return {
            "base_speed_kmh": speed,
            "base_vc_ratio": vc,
            "source": "IRC Urban Design Standards"
        }
