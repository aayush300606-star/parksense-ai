from typing import Dict, Any


class PISExplainabilityEngine:
    """
    Generates human-readable narratives explaining the real-world impact of the hotspot.
    """

    @staticmethod
    def generate_explanation(
        pis_score: float,
        pis_level: str,
        daily_commuters: int,
        daily_delay_hours: float,
        fuel_wasted_per_day: float,
        co2_emissions_kg_per_day: float,
        economic_burden_inr_per_day: float,
        enforcement_benefit_score: float
    ) -> Dict[str, Any]:
        """
        Generates narrative summarizing the exact economic, environmental, and human toll.
        """
        parts = []
        
        parts.append(f"PIS = {pis_score:.0f}/100 ({pis_level} Impact). Reason: ")
        
        # Human Toll
        if daily_commuters >= 1000:
            commuters_str = f"{daily_commuters/1000:.1f}k"
        else:
            commuters_str = str(daily_commuters)
        parts.append(f"{commuters_str} commuters affected daily, suffering {daily_delay_hours:.0f} hours of collective delay.")
        
        # Economic Toll
        if economic_burden_inr_per_day >= 100000:
            econ_str = f"Lakhs"
            val = economic_burden_inr_per_day / 100000.0
            parts.append(f"Economic burden is roughly ₹{val:.1f} Lakhs/day due to lost productivity and wasted fuel.")
        else:
            parts.append(f"Economic burden is roughly ₹{economic_burden_inr_per_day:,.0f}/day.")
            
        # Environmental Toll
        parts.append(f"{fuel_wasted_per_day:.0f} liters of fuel wasted daily, generating {co2_emissions_kg_per_day:.0f}kg of CO₂ emissions.")
        
        # Enforcement Benefit
        if enforcement_benefit_score >= 80:
            parts.append("Expected enforcement benefit is critical.")
        elif enforcement_benefit_score >= 60:
            parts.append("Expected enforcement benefit is high.")
        elif enforcement_benefit_score >= 40:
            parts.append("Expected enforcement benefit is moderate.")
        else:
            parts.append("Expected enforcement benefit is low.")
            
        explanation_str = " ".join(parts)
        
        return {
            "explanation": explanation_str
        }
