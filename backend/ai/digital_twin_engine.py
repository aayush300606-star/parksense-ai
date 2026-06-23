from typing import Dict, Any, List
from .scenario_engine import ScenarioEngine
from .baseline_state_engine import BaselineStateEngine
from .capacity_recovery_simulation import CapacityRecoverySimulation
from .traffic_recovery_simulation import TrafficRecoverySimulation
from .csi_recalculation_engine import CSIRecalculationEngine
from .pis_recalculation_engine import PISRecalculationEngine
from .comparison_engine import ComparisonEngine
from .benefit_analysis_engine import BenefitAnalysisEngine
from .enforcement_roi_engine import EnforcementROIEngine
from .simulation_explainability_engine import SimulationExplainabilityEngine
from datetime import datetime

class DigitalTwinEngine:
    """
    Core orchestrator for a single scenario simulation.
    """

    @staticmethod
    def simulate(csi_data: Dict, pis_data: Dict, total_road_width: float, scenario_id: str) -> Dict[str, Any]:
        """
        Runs the full Digital Twin pipeline for one hotspot against one scenario.
        """
        scenario = ScenarioEngine.get_scenario(scenario_id)
        removal_pct = scenario['removal_pct']
        
        # 1. Capture Baseline
        baseline = BaselineStateEngine.capture_baseline(csi_data, pis_data)
        
        # 2. Simulate Physical Recovery
        cap_sim = CapacityRecoverySimulation.simulate(baseline, removal_pct, total_road_width)
        
        # 3. Simulate Traffic Flow Recovery
        traffic_sim = TrafficRecoverySimulation.simulate(baseline, cap_sim['capacity_loss_percentage'])
        
        # 4. Recalculate Index Scores
        new_csi = CSIRecalculationEngine.recalculate(
            baseline['csi_score'], 
            baseline['capacity_loss_percentage'], 
            cap_sim['capacity_loss_percentage']
        )
        
        pis_sim = PISRecalculationEngine.recalculate(baseline, traffic_sim['current_speed_kmh'])
        
        # Combine simulated state
        simulated_state = {
            "csi_score": new_csi,
            "pis_score": pis_sim['pis_score'],
            "effective_width_m": cap_sim['effective_width_m'],
            "capacity_loss_percentage": cap_sim['capacity_loss_percentage'],
            "current_speed_kmh": traffic_sim['current_speed_kmh'],
            "daily_delay_hours": pis_sim['daily_delay_hours'],
            "fuel_wasted_per_day_liters": pis_sim['fuel_wasted_per_day_liters'],
            "co2_emissions_kg_per_day": pis_sim['co2_emissions_kg_per_day'],
            "economic_burden_inr_per_day": pis_sim['economic_burden_inr_per_day']
        }
        
        # 5. Analysis & Explainability
        deltas = ComparisonEngine.compare(baseline, simulated_state)
        benefit_score = BenefitAnalysisEngine.analyze(deltas)
        roi_string = EnforcementROIEngine.calculate_roi(removal_pct, benefit_score)
        explanation = SimulationExplainabilityEngine.generate(scenario['name'], deltas, cap_sim['width_recovered_m'])
        
        return {
            "scenario_id": scenario_id,
            "scenario_name": scenario['name'],
            "baseline_state": baseline,
            "simulated_state": simulated_state,
            "deltas": deltas,
            "benefit_score": benefit_score,
            "roi": roi_string,
            "explanation": explanation,
            "generated_at": datetime.now()
        }
