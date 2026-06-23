from typing import Dict, Any


class CSIEngine:
    """
    Adaptive Congestion Severity Index (CSI™) — Core Calculation Engine.
    
    The flagship intelligence engine of ParkSense AI.
    
    Formula:
        CSI = Σ(W_i × S_i)  for i in [1..7]
    
    Where:
        W_i = Adaptive weight from AdaptiveWeightingEngine (context-dependent)
        S_i = Normalized component score from CSIComponentEngine (0-100)
        Σ(W_i) = 1.0 (guaranteed by weight normalization)
    
    The CSI is NOT a fixed formula — it adapts to urban context:
        - Near a hospital: emergency weight amplified → higher CSI
        - On a quiet residential street: traffic weight dominates
        - At a major junction on an emergency route: junction + emergency dominate
    
    This adaptive behavior is what makes CSI™ a Smart City innovation,
    not merely a weighted average.
    """

    @staticmethod
    def calculate_csi(
        components: Dict[str, Dict],
        weights: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Computes the Adaptive Congestion Severity Index.
        
        Args:
            components: Dict from CSIComponentEngine.gather_components()["components"]
                        Each entry has {"value": float, "label": str, "confidence": float}
            weights: Dict from AdaptiveWeightingEngine.compute_weights()["weights"]
                     Keys match component names, values sum to 1.0
                     
        Returns:
            dict with:
                - csi_score: float (0-100)
                - component_contributions: dict of {name: weighted_value}
                - confidence: float (weighted average of component confidences)
        """
        csi = 0.0
        contributions = {}
        confidence_sum = 0.0

        for name, comp in components.items():
            value = comp["value"]
            weight = weights.get(name, 0.0)
            weighted_value = value * weight

            csi += weighted_value
            contributions[name] = {
                "raw_value": round(value, 2),
                "weight": round(weight, 4),
                "weighted_value": round(weighted_value, 2),
                "label": comp["label"],
            }

            # Weighted confidence
            confidence_sum += comp["confidence"] * weight

        csi = min(100.0, max(0.0, csi))

        return {
            "csi_score": round(csi, 2),
            "component_contributions": contributions,
            "confidence": round(confidence_sum, 2),
        }
