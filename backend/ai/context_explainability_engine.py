from typing import Dict, List


class ContextExplainabilityEngine:
    """
    Generates structured, human-readable explanations for context intelligence scores.
    
    Outputs are consumable by:
        - Dashboard UI cards
        - LLM Smart City Agents
        - PDF enforcement reports
        - Decision-maker briefings
    """

    @staticmethod
    def generate_explanation(
        road_name: str,
        context_importance_score: float,
        context_importance_level: str,
        junction_type: str,
        junction_distance_m: float,
        junction_importance_level: str,
        junction_influence_level: str,
        poi_count_300m: int,
        poi_count_500m: int,
        poi_count_1000m: int,
        poi_density_level: str,
        critical_infrastructure_score: float,
        critical_infrastructure_level: str,
        critical_pois: List[Dict],
        emergency_impact_score: float,
        emergency_priority: str,
        emergency_route_impact: bool
    ) -> str:
        """
        Produces a structured multi-sentence context explanation.
        """
        parts = []

        # Header
        parts.append(
            f"Context Importance = {context_importance_score:.1f}/100 ({context_importance_level})."
        )

        # Junction context
        if junction_distance_m <= 100:
            parts.append(
                f"{junction_type} within {junction_distance_m:.0f}m "
                f"({junction_importance_level}, {junction_influence_level} influence)."
            )
        else:
            parts.append(
                f"Nearest junction ({junction_type}) at {junction_distance_m:.0f}m distance."
            )

        # Critical infrastructure highlights
        if critical_pois:
            poi_descriptions = []
            for poi in critical_pois[:4]:  # Top 4 most relevant
                poi_type_label = poi["poi_type"].replace("_", " ").title()
                dist = poi.get("distance_m", 0)
                name = poi.get("poi_name", poi_type_label)
                if dist > 0:
                    poi_descriptions.append(f"{name} within {dist:.0f}m")
                else:
                    poi_descriptions.append(f"{name} in immediate vicinity")
            parts.append("Nearby critical infrastructure: " + "; ".join(poi_descriptions) + ".")

        # POI density
        parts.append(
            f"POI density: {poi_count_300m} within 300m, "
            f"{poi_count_500m} within 500m, "
            f"{poi_count_1000m} within 1000m ({poi_density_level} density)."
        )

        # Emergency access
        if emergency_route_impact:
            parts.append(
                f"⚠ HIGH EMERGENCY IMPACT: Parking here blocks a likely emergency vehicle route. "
                f"Emergency priority: {emergency_priority}."
            )
        elif emergency_impact_score >= 40:
            parts.append(
                f"Emergency access impact: {emergency_impact_score:.0f}/100 ({emergency_priority})."
            )

        # Recommendation
        if context_importance_level == "Critical":
            parts.append(
                "RECOMMENDATION: Designate as Priority Enforcement Zone. "
                "Deploy permanent no-parking infrastructure. "
                "Coordinate with traffic police for sustained enforcement."
            )
        elif context_importance_level == "High":
            parts.append(
                "RECOMMENDATION: Schedule regular enforcement patrols. "
                "Install warning signage near critical infrastructure."
            )
        elif context_importance_level == "Moderate":
            parts.append(
                "RECOMMENDATION: Monitor during peak hours. "
                "Consider parking management interventions."
            )
        else:
            parts.append(
                "RECOMMENDATION: Standard enforcement level. "
                "Low contextual urgency."
            )

        return " ".join(parts)
