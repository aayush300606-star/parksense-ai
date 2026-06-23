class JunctionImportanceEngine:
    """
    Classifies junction importance on a 0-100 scale based on junction type
    and connected road hierarchy.
    
    The importance score reflects how critical the junction is to the city's
    traffic network — blocking a major arterial circle causes far greater
    disruption than blocking a residential T-junction.
    
    Classification:
        Critical Intersection (100): Major circles, flyovers on arterials
        Major Arterial Junction (80): Signal junctions on major roads
        Minor Arterial Junction (60): Junctions on collector/minor arterial roads
        Collector Junction (40): Junctions in commercial/collector areas
        Local Junction (20): Residential cross/T-junctions
    """

    # Base importance by junction type
    JUNCTION_TYPE_BASE = {
        "Traffic Circle":       85,
        "Signal Junction":      75,
        "Flyover Junction":     70,
        "Underpass Junction":   65,
        "Cross Junction":       50,
        "T-Junction":           40,
        "Uncontrolled Junction": 25,
    }

    # Road hierarchy multiplier (applied to base score)
    HIERARCHY_MULTIPLIER = {
        "Expressway":       1.20,
        "Major Arterial":   1.10,
        "Minor Arterial":   1.00,
        "Collector":        0.90,
        "Secondary":        0.80,
        "Residential":      0.65,
        "Service":          0.50,
    }

    # Classification thresholds
    IMPORTANCE_LEVELS = [
        (80, "Critical Intersection"),
        (60, "Major Arterial Junction"),
        (40, "Minor Arterial Junction"),
        (25, "Collector Junction"),
        (0,  "Local Junction"),
    ]

    @staticmethod
    def calculate_importance(
        junction_type: str,
        road_hierarchy: str,
        road_count_connected: int,
        signalized: bool
    ) -> dict:
        """
        Calculates junction importance score.
        
        Args:
            junction_type: Type classification from JunctionIntelligenceEngine
            road_hierarchy: Road hierarchy of the hotspot
            road_count_connected: Number of roads meeting at the junction
            signalized: Whether the junction has traffic signals
            
        Returns:
            dict with junction_importance_score, junction_importance_level
        """
        # Base score from junction type
        base = JunctionImportanceEngine.JUNCTION_TYPE_BASE.get(junction_type, 25)

        # Road hierarchy multiplier
        multiplier = JunctionImportanceEngine.HIERARCHY_MULTIPLIER.get(road_hierarchy, 0.80)
        score = base * multiplier

        # Road count bonus: more connected roads = more important junction
        if road_count_connected >= 5:
            score += 12
        elif road_count_connected >= 4:
            score += 8
        elif road_count_connected >= 3:
            score += 4

        # Signal bonus: signalized junctions handle more traffic
        if signalized:
            score += 5

        # Clamp to 0-100
        score = min(100.0, max(0.0, score))

        # Determine classification level
        level = "Local Junction"
        for threshold, label in JunctionImportanceEngine.IMPORTANCE_LEVELS:
            if score >= threshold:
                level = label
                break

        return {
            "junction_importance_score": round(score, 2),
            "junction_importance_level": level
        }
