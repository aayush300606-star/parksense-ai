class JunctionInfluenceEngine:
    """
    Calculates how much a hotspot's proximity to a junction amplifies
    its congestion impact.
    
    Physics: Illegal parking near junctions is disproportionately disruptive
    because it reduces the approach/departure capacity of the intersection,
    causing queue spillback and signal cycle failures.
    
    The influence score uses an inverse-distance decay function:
        influence = 100 * e^(-distance / decay_constant)
    
    Discretized into severity bands for classification.
    """

    import math

    # Decay constant in meters (controls how fast influence drops with distance)
    # At 1 decay constant distance, influence drops to ~37% of max
    DECAY_CONSTANT_M = 80.0

    # Severity band thresholds (meters)
    INFLUENCE_BANDS = [
        (5,   "Very High", 100),
        (20,  "High",       80),
        (50,  "Medium",     60),
        (100, "Low",        40),
        (300, "Minimal",    20),
    ]

    @staticmethod
    def calculate_influence(junction_distance_m: float) -> dict:
        """
        Calculates junction influence based on distance.
        
        Args:
            junction_distance_m: Distance from hotspot to nearest junction (meters)
            
        Returns:
            dict with:
                - junction_influence_score: Continuous 0-100 score (exponential decay)
                - junction_influence_level: Categorical severity band
                - junction_influence_band_score: Discrete band score
        """
        import math

        # Continuous exponential decay score
        distance = max(0.0, junction_distance_m)
        continuous_score = 100.0 * math.exp(-distance / JunctionInfluenceEngine.DECAY_CONSTANT_M)
        continuous_score = min(100.0, max(0.0, continuous_score))

        # Determine discrete band
        band_level = "None"
        band_score = 5
        for threshold, level, score in JunctionInfluenceEngine.INFLUENCE_BANDS:
            if distance <= threshold:
                band_level = level
                band_score = score
                break
        else:
            band_level = "None"
            band_score = 5

        return {
            "junction_influence_score": round(continuous_score, 2),
            "junction_influence_level": band_level,
            "junction_influence_band_score": band_score
        }
