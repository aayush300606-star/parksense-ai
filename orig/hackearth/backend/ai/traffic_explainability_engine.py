class TrafficExplainabilityEngine:
    """
    Generates human-readable traffic impact narratives.
    
    These explanations are designed to be directly consumable by:
    - Dashboard UIs showing impact cards
    - LLM-based city planning agents
    - PDF/report generation modules
    - Decision-makers who need plain-language justifications
    """

    @staticmethod
    def generate_traffic_explanation(
        road_name: str,
        road_hierarchy: str,
        base_speed_kmh: float,
        current_speed_kmh: float,
        speed_reduction_percentage: float,
        capacity_loss_percentage: float,
        delay_seconds: float,
        annual_delay_vehicle_hours: float,
        congestion_impact_score: float,
        congestion_severity: str
    ) -> str:
        """
        Produces a structured, multi-sentence explanation of the traffic impact.
        """
        # Format delay for readability
        if delay_seconds >= 60:
            delay_str = f"{delay_seconds / 60:.1f} minutes"
        else:
            delay_str = f"{delay_seconds:.0f} seconds"
        
        # Format annual delay
        if annual_delay_vehicle_hours >= 1000:
            annual_str = f"{annual_delay_vehicle_hours / 1000:.1f}K vehicle-hours"
        else:
            annual_str = f"{annual_delay_vehicle_hours:.0f} vehicle-hours"
        
        # Build explanation
        explanation_parts = []
        
        # Speed impact
        explanation_parts.append(
            f"Illegal parking at {road_name} ({road_hierarchy}) has caused "
            f"a {speed_reduction_percentage:.1f}% speed reduction, "
            f"dropping traffic flow from {base_speed_kmh:.0f} km/h to {current_speed_kmh:.1f} km/h."
        )
        
        # Capacity context
        explanation_parts.append(
            f"This is driven by a {capacity_loss_percentage:.1f}% loss in effective road capacity."
        )
        
        # Delay impact
        explanation_parts.append(
            f"Each vehicle traversing this segment experiences an additional {delay_str} of delay."
        )
        
        # Annual projection
        if annual_delay_vehicle_hours > 0:
            explanation_parts.append(
                f"Projected annually, this translates to {annual_str} of cumulative delay across all vehicles."
            )
        
        # Overall severity
        explanation_parts.append(
            f"Congestion Impact Score: {congestion_impact_score:.1f}/100 ({congestion_severity})."
        )
        
        # Actionable recommendation
        if congestion_severity in ("Critical", "Severe"):
            explanation_parts.append(
                "RECOMMENDATION: Immediate enforcement action required. "
                "Consider deploying tow trucks and no-parking signage at this location."
            )
        elif congestion_severity == "Moderate":
            explanation_parts.append(
                "RECOMMENDATION: Schedule periodic enforcement patrols. "
                "Monitor for escalation during peak hours."
            )
        elif congestion_severity == "Low":
            explanation_parts.append(
                "RECOMMENDATION: Flag for awareness. Low-priority enforcement action."
            )
        
        return " ".join(explanation_parts)
