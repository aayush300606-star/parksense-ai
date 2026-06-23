from typing import Dict, Any


class EnforcementBenefitEngine:
    """
    Quantifies the real-world benefits (delay reduction, economic savings)
    achieved if enforcement is executed.
    """

    @staticmethod
    def calculate_benefits(
        daily_delay_hours: float,
        daily_commuters: int,
        co2_kg_per_day: float,
        economic_loss_per_day: float,
        delay_reduction_pct: float
    ) -> Dict[str, Any]:
        """
        Projects the exact quantitative benefits of enforcement.
        """
        reduction_factor = delay_reduction_pct / 100.0
        
        expected_delay_reduction_hours = daily_delay_hours * reduction_factor
        expected_commuter_benefit_hours = expected_delay_reduction_hours * 1.5 # 1.5 occupancy
        expected_environmental_benefit_co2_kg = co2_kg_per_day * reduction_factor
        expected_economic_benefit_inr = economic_loss_per_day * reduction_factor
        
        # Score out of 100 based on economic benefit (100 if > ₹5L daily saved)
        enforcement_benefit_score = min(100.0, (expected_economic_benefit_inr / 500000.0) * 100.0)
        
        return {
            "expected_delay_reduction_hours_per_day": round(expected_delay_reduction_hours, 1),
            "expected_commuter_benefit_hours_per_day": round(expected_commuter_benefit_hours, 1),
            "expected_environmental_benefit_co2_kg_per_day": round(expected_environmental_benefit_co2_kg, 1),
            "expected_economic_benefit_inr_per_day": int(expected_economic_benefit_inr),
            "enforcement_benefit_score": round(enforcement_benefit_score, 2)
        }
