from typing import Dict, Any, List

class ScenarioSelectionEngine:
    """
    Pulls data from the Digital Twin to recommend the specific intervention 
    that provides the best ROI for a location, scaling outputs to realistic compliance models.
    """

    @staticmethod
    def select_best_scenario(digital_twin_scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Given the A/B/C/D scenarios simulated for a hotspot,
        returns the one with the highest practical benefit score, adjusted for real-world compliance.
        """
        best_sim = max(digital_twin_scenarios, key=lambda x: x['benefit_score'])
        
        if best_sim['benefit_score'] < 10.0:
            return {
                "recommended_action": "No Action (Monitor)",
                "expected_csi_reduction": 0.0,
                "expected_pis_reduction": 0.0,
                "expected_capacity_recovery": 0.0,
                "expected_delay_reduction": 0.0,
                "roi_score": best_sim['benefit_score'],
                "confidence_score": 100.0,
                "scenario_reasoning": "Minimal benefit predicted for any active intervention. Recommending passive monitoring."
            }
            
        # Realistic Compliance Modeling
        # If the Digital Twin suggests 100% removal, we know realistic operational compliance is usually ~65-80%.
        # We scale the expected improvements accordingly to set realistic expectations.
        is_max_scenario = "100%" in best_sim['scenario_name']
        compliance_discount = 0.75 if is_max_scenario else 0.90
        
        # We also want to display a realistic intervention target rather than "100%"
        action_name = best_sim['scenario_name']
        if is_max_scenario:
            action_name = "Intensive Patrol (Target: >75% Clearance)"
        elif "75%" in action_name:
            action_name = "Targeted Patrol (Target: >50% Clearance)"
            
        reasoning = f"Digital Twin '{best_sim['scenario_name']}' selected as base. Applied {int(compliance_discount*100)}% compliance discount to theoretical max limits to produce realistic expected improvements."
            
        return {
            "recommended_action": action_name,
            "expected_csi_reduction": round(best_sim['deltas']['csi']['improvement'] * compliance_discount, 2),
            "expected_pis_reduction": round(best_sim['deltas']['pis']['improvement'] * compliance_discount, 2),
            "expected_capacity_recovery": round(best_sim['deltas']['capacity_loss_pct']['improvement'] * compliance_discount, 2),
            "expected_delay_reduction": round(best_sim['deltas']['delay_hours']['improvement'] * compliance_discount, 1),
            "roi_score": round(best_sim['benefit_score'] * compliance_discount, 1),
            "confidence_score": round(compliance_discount * 100, 1),
            "scenario_reasoning": reasoning
        }
