class ContextImportanceEngine:
    """
    Aggregates all context signals into a unified Context Importance Score (0-100).
    
    This score answers: "How location-critical is enforcement at this hotspot?"
    
    A high Context Importance Score means illegal parking here causes outsized
    harm due to the surrounding urban context (proximity to junctions, hospitals,
    transit, government buildings, emergency routes).
    
    Component Weights:
        Junction Importance     0.20  — Network topology impact
        Junction Influence      0.20  — Proximity-based amplification
        POI Density             0.20  — Activity center density
        Critical Infrastructure 0.25  — Emergency/transit/government
        Emergency Access        0.15  — Emergency vehicle route impact
    """

    @staticmethod
    def calculate_context_importance(
        junction_importance_score: float,
        junction_influence_score: float,
        poi_density_score: float,
        critical_infrastructure_score: float,
        emergency_impact_score: float
    ) -> dict:
        """
        Weighted aggregation of context signals.
        
        Returns:
            dict with:
                - context_importance_score: 0-100
                - context_importance_level: categorical
                - component_breakdown: individual weighted contributions
        """
        # Clamp all inputs
        ji = min(100.0, max(0.0, junction_importance_score))
        jinf = min(100.0, max(0.0, junction_influence_score))
        pd = min(100.0, max(0.0, poi_density_score))
        ci = min(100.0, max(0.0, critical_infrastructure_score))
        ea = min(100.0, max(0.0, emergency_impact_score))

        # Weights
        w_ji = 0.20
        w_jinf = 0.20
        w_pd = 0.20
        w_ci = 0.25
        w_ea = 0.15

        score = (
            ji * w_ji +
            jinf * w_jinf +
            pd * w_pd +
            ci * w_ci +
            ea * w_ea
        )

        score = min(100.0, max(0.0, score))

        # Level classification
        if score >= 80:
            level = "Critical"
        elif score >= 60:
            level = "High"
        elif score >= 40:
            level = "Moderate"
        elif score >= 20:
            level = "Low"
        else:
            level = "Very Low"

        return {
            "context_importance_score": round(score, 2),
            "context_importance_level": level,
            "component_breakdown": {
                "junction_importance": {
                    "value": round(ji, 2), "weight": w_ji,
                    "weighted": round(ji * w_ji, 2)
                },
                "junction_influence": {
                    "value": round(jinf, 2), "weight": w_jinf,
                    "weighted": round(jinf * w_jinf, 2)
                },
                "poi_density": {
                    "value": round(pd, 2), "weight": w_pd,
                    "weighted": round(pd * w_pd, 2)
                },
                "critical_infrastructure": {
                    "value": round(ci, 2), "weight": w_ci,
                    "weighted": round(ci * w_ci, 2)
                },
                "emergency_access": {
                    "value": round(ea, 2), "weight": w_ea,
                    "weighted": round(ea * w_ea, 2)
                },
            }
        }
