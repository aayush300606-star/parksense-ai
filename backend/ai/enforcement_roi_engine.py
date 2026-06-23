from typing import Dict, Any

class EnforcementROIEngine:
    """
    Calculates the Return on Investment for deploying enforcement personnel.
    """

    @staticmethod
    def calculate_roi(scenario_pct: float, benefit_score: float) -> str:
        """
        Determines ROI string. 
        If removing 50% parking gives 90% benefit, the ROI is Excellent.
        If removing 100% parking only gives 10% benefit, the ROI is Poor.
        """
        if scenario_pct == 0:
            return "N/A"
            
        ratio = benefit_score / scenario_pct
        
        if ratio >= 1.2:
            return "Excellent ROI"
        elif ratio >= 0.8:
            return "Good ROI"
        elif ratio >= 0.4:
            return "Moderate ROI"
        else:
            return "Poor ROI"
