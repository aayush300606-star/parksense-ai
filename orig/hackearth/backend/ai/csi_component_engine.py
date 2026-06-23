from typing import Dict, Any, Optional


class CSIComponentEngine:
    """
    Gathers, validates, and normalizes all 7 component scores
    that feed into the Adaptive CSI™ formula.
    
    Every score is:
        1. Validated (not None, not NaN)
        2. Clamped to [0, 100]
        3. Stored with its source and confidence
    
    Components:
        1. Violation Density Score     — Clustering intensity
        2. Capacity Loss Score         — Physical road blockage
        3. Traffic Impact Score        — BPR flow degradation
        4. Junction Influence Score    — Proximity × junction importance
        5. POI Density Score           — Activity center concentration
        6. Critical Infrastructure Score — Emergency/transit/government
        7. Emergency Impact Score      — Emergency vehicle route impact
    """

    COMPONENT_NAMES = [
        "violation_density",
        "capacity_loss",
        "traffic_impact",
        "junction_influence",
        "poi_density",
        "critical_infrastructure",
        "emergency_impact",
    ]

    COMPONENT_LABELS = {
        "violation_density":        "Violation Density",
        "capacity_loss":            "Road Capacity Loss",
        "traffic_impact":           "Traffic Flow Impact",
        "junction_influence":       "Junction Influence",
        "poi_density":              "POI Density",
        "critical_infrastructure":  "Critical Infrastructure",
        "emergency_impact":         "Emergency Access Impact",
    }

    @staticmethod
    def gather_components(
        violation_density_score: float,
        capacity_loss_percentage: float,
        congestion_impact_score: float,
        junction_influence_score: float,
        poi_density_score: float,
        critical_infrastructure_score: float,
        emergency_impact_score: float,
        # Confidence scores for provenance
        density_confidence: float = 0.90,
        road_confidence: float = 0.80,
        traffic_confidence: float = 0.85,
        junction_confidence: float = 0.75,
        poi_confidence: float = 0.70,
        infra_confidence: float = 0.70,
        emergency_confidence: float = 0.75,
    ) -> Dict[str, Any]:
        """
        Validates, normalizes, and packages all 7 component scores.
        
        Returns:
            dict with:
                - components: dict of {name: {value, label, confidence}}
                - valid: bool (True if all components present)
                - component_count: int
        """
        raw_values = {
            "violation_density":       violation_density_score,
            "capacity_loss":           capacity_loss_percentage,
            "traffic_impact":          congestion_impact_score,
            "junction_influence":      junction_influence_score,
            "poi_density":             poi_density_score,
            "critical_infrastructure": critical_infrastructure_score,
            "emergency_impact":        emergency_impact_score,
        }

        confidences = {
            "violation_density":       density_confidence,
            "capacity_loss":           road_confidence,
            "traffic_impact":          traffic_confidence,
            "junction_influence":      junction_confidence,
            "poi_density":             poi_confidence,
            "critical_infrastructure": infra_confidence,
            "emergency_impact":        emergency_confidence,
        }

        components = {}
        all_valid = True

        for name in CSIComponentEngine.COMPONENT_NAMES:
            raw = raw_values.get(name)

            # Validate
            if raw is None:
                raw = 0.0
                all_valid = False

            try:
                val = float(raw)
            except (TypeError, ValueError):
                val = 0.0
                all_valid = False

            # Check for NaN
            if val != val:  # NaN check
                val = 0.0
                all_valid = False

            # Clamp to 0-100
            val = min(100.0, max(0.0, val))

            components[name] = {
                "value": round(val, 2),
                "label": CSIComponentEngine.COMPONENT_LABELS[name],
                "confidence": round(min(1.0, max(0.0, confidences.get(name, 0.70))), 2),
            }

        return {
            "components": components,
            "valid": all_valid,
            "component_count": len(components),
        }
