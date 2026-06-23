from typing import Dict, Any, List

class ScenarioSelectionEngine:
    """
    Pulls data from the Digital Twin to recommend the specific intervention 
    that provides the best ROI for a location.
    """

    @staticmethod
    def select_best_scenario(digital_twin_scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Given the A/B/C/D scenarios simulated for a hotspot,
        returns the one with the highest benefit score.
        If benefit is minimal even at 100%, returns 'No Action'.
        """
        best_sim = max(digital_twin_scenarios, key=lambda x: x['benefit_score'])
        
        if best_sim['benefit_score'] < 10.0:
            return {
                "recommended_action": "No Action (Monitor)",
                "expected_csi_reduction": 0.0,
                "expected_pis_reduction": 0.0,
                "expected_capacity_recovery": 0.0,
                "expected_delay_reduction": 0.0,
                "roi_score": best_sim['benefit_score']
            }
            
        return {
            "recommended_action": best_sim['scenario_name'],
            "expected_csi_reduction": best_sim['deltas']['csi']['improvement'],
            "expected_pis_reduction": best_sim['deltas']['pis']['improvement'],
            "expected_capacity_recovery": best_sim['deltas']['capacity_loss_pct']['improvement'],
            "expected_delay_reduction": best_sim['deltas']['delay_hours']['improvement'],
            "roi_score": best_sim['benefit_score']
        }
