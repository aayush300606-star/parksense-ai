from typing import Dict, List, Any


class CSIExplainabilityEngine:
    """
    Generates both human-readable and machine-readable explanations
    for every CSI™ score.
    
    Every CSI value must explain itself. This is non-negotiable for:
        - Judicial defensibility
        - Municipal decision-making
        - LLM Agent reasoning
        - Public transparency
    """

    @staticmethod
    def generate_explanation(
        hotspot_id: int,
        road_name: str,
        road_hierarchy: str,
        csi_score: float,
        csi_level: str,
        csi_color_name: str,
        rank: int,
        total_hotspots: int,
        percentile: float,
        contributions: List[Dict],
        adaptive_reasoning: List[str],
        weight_profile: str,
        speed_reduction_percentage: float,
        capacity_loss_percentage: float,
        annual_delay_vehicle_hours: float,
        junction_type: str,
        junction_distance_m: float,
        emergency_route_impact: bool,
        critical_pois: List[Dict] = None,
        pis_score: float = 0,
        pis_priority: str = "",
    ) -> Dict[str, Any]:
        """
        Generates both human-readable and machine-readable explanations.
        
        Returns:
            dict with:
                - human_explanation: Multi-sentence narrative
                - machine_explanation: Structured dict for programmatic consumption
                - key_factors: Top contributing factors as bullet points
                - recommendation: Enforcement recommendation
        """
        # === Machine-readable explanation ===
        machine = {
            "hotspot_id": hotspot_id,
            "csi_score": csi_score,
            "csi_level": csi_level,
            "rank": rank,
            "total_hotspots": total_hotspots,
            "percentile": percentile,
            "top_contributions": [
                {
                    "factor": c["label"],
                    "contribution_percentage": c["percentage"],
                    "raw_value": c["raw_value"],
                }
                for c in contributions[:5]
            ],
            "weight_profile": weight_profile,
            "adaptive_rules_applied": adaptive_reasoning,
            "speed_reduction": speed_reduction_percentage,
            "capacity_loss": capacity_loss_percentage,
            "emergency_route_blocked": emergency_route_impact,
        }

        # === Key factors (bullet points) ===
        key_factors = []

        if capacity_loss_percentage >= 30:
            key_factors.append(f"{capacity_loss_percentage:.0f}% Road Capacity Loss")
        if speed_reduction_percentage >= 20:
            key_factors.append(f"{speed_reduction_percentage:.1f}% Traffic Slowdown")
        if junction_type and junction_distance_m <= 100:
            key_factors.append(f"{junction_type} {junction_distance_m:.0f}m Away")
        if emergency_route_impact:
            key_factors.append("Emergency Route Impact")

        if critical_pois:
            for poi in critical_pois[:3]:
                poi_label = poi.get("poi_type", "").replace("_", " ").title()
                dist = poi.get("distance_m", 0)
                if dist > 0:
                    key_factors.append(f"{poi_label} Within {dist:.0f}m")
                else:
                    key_factors.append(f"{poi_label} Nearby")

        # Add top contribution factors
        for c in contributions[:3]:
            factor_str = f"{c['label']}: {c['percentage']:.0f}% of CSI"
            if factor_str not in key_factors:
                key_factors.append(factor_str)

        # === Human-readable explanation ===
        parts = []

        # Score and rank
        parts.append(
            f"CSI = {csi_score:.0f}/100 ({csi_level}, {csi_color_name})."
        )
        parts.append(
            f"Ranked #{rank} of {total_hotspots} citywide "
            f"(top {100 - percentile:.0f}%)."
        )

        # Reason header
        parts.append("Reason:")

        # Impact metrics
        if speed_reduction_percentage >= 20:
            parts.append(
                f"{speed_reduction_percentage:.1f}% traffic slowdown on "
                f"{road_name} ({road_hierarchy})."
            )
        if capacity_loss_percentage >= 30:
            parts.append(f"{capacity_loss_percentage:.0f}% road capacity loss.")

        # Annual impact
        if annual_delay_vehicle_hours >= 1000:
            delay_str = f"{annual_delay_vehicle_hours / 1000:.1f}K"
        else:
            delay_str = f"{annual_delay_vehicle_hours:.0f}"
        parts.append(f"Projected annual delay: {delay_str} vehicle-hours.")

        # Junction
        if junction_type and junction_distance_m <= 100:
            parts.append(f"{junction_type} {junction_distance_m:.0f}m away.")

        # Critical infrastructure
        if critical_pois:
            for poi in critical_pois[:3]:
                poi_label = poi.get("poi_type", "").replace("_", " ").title()
                dist = poi.get("distance_m", 0)
                if dist > 0:
                    parts.append(f"{poi_label} within {dist:.0f}m.")

        # Emergency
        if emergency_route_impact:
            parts.append("EMERGENCY ROUTE IMPACT: Blocks likely emergency vehicle corridor.")

        # Adaptive weighting
        if adaptive_reasoning:
            parts.append(
                f"Adaptive weighting applied ({weight_profile}): "
                + "; ".join(adaptive_reasoning[:3]) + "."
            )

        # PIS
        if pis_score > 0 and pis_priority:
            parts.append(f"Enforcement Priority: {pis_score:.0f}/100 ({pis_priority}).")

        # === Recommendation ===
        if csi_level == "Critical":
            recommendation = (
                "IMMEDIATE ACTION: Deploy enforcement within 24 hours. "
                "Install permanent no-parking barriers. "
                "Coordinate with traffic police for sustained operations. "
                "Consider CCTV-based automated challan enforcement."
            )
        elif csi_level == "High":
            recommendation = (
                "HIGH PRIORITY: Schedule enforcement this week. "
                "Install warning signage. Consider peak-hour barriers."
            )
        elif csi_level == "Moderate":
            recommendation = (
                "Include in monthly enforcement rotation. "
                "Deploy awareness campaigns. Monitor for escalation."
            )
        elif csi_level == "Low":
            recommendation = (
                "Periodic monitoring. Record for trend analysis."
            )
        else:
            recommendation = (
                "Passive observation. No active enforcement required."
            )

        return {
            "human_explanation": " ".join(parts),
            "machine_explanation": machine,
            "key_factors": key_factors,
            "recommendation": recommendation,
        }
