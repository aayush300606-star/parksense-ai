from typing import Dict, List, Any
from .digital_twin_engine import DigitalTwinEngine

class MultiScenarioEngine:
    """
    Runs a hotspot through multiple scenarios simultaneously and ranks them.
    """

    @staticmethod
    def run_all_scenarios(csi_data: Dict, pis_data: Dict, total_road_width: float) -> List[Dict[str, Any]]:
        """
        Executes scenarios A, B, C, D and ranks them by ROI and Benefit Score.
        """
        results = []
        for s_id in ["A", "B", "C", "D"]:
            sim = DigitalTwinEngine.simulate(csi_data, pis_data, total_road_width, s_id)
            results.append(sim)
            
        # Rank by benefit score
        return sorted(results, key=lambda x: x['benefit_score'], reverse=True)
