import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.smart_enforcement_intelligence import SmartEnforcementIntelligence
from ..services.csi_service import CSI_JSON_PATH
from ..services.pis_service import PIS_JSON_PATH
from ..services.prediction_service import PREDICTIONS_JSON_PATH
from ..services.digital_twin_service import SIMULATION_RESULTS_PATH

from ..ai.enforcement_priority_engine import EnforcementPriorityEngine
from ..ai.time_window_engine import TimeWindowEngine
from ..ai.scenario_selection_engine import ScenarioSelectionEngine
from ..ai.resource_allocation_engine import ResourceAllocationEngine
from ..ai.patrol_optimization_engine import PatrolOptimizationEngine
from ..ai.enforcement_explainability_engine import EnforcementExplainabilityEngine
from ..ai.daily_enforcement_engine import DailyEnforcementEngine
from ..ai.weekly_strategy_engine import WeeklyStrategyEngine

ENFORCEMENT_PLAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'enforcement_plan.json')
DAILY_PLAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'daily_plan.json')
WEEKLY_STRATEGY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'weekly_strategy.json')

class SmartEnforcementService:
    """
    Orchestrator for the Smart Enforcement Planner (SEP).
    Combines intelligence to build physical patrol schedules.
    """

    @staticmethod
    def generate_all(available_teams: int = 5):
        """Executes the full SEP pipeline."""
        if not all(os.path.exists(p) for p in [CSI_JSON_PATH, PIS_JSON_PATH, PREDICTIONS_JSON_PATH, SIMULATION_RESULTS_PATH]):
            print("Upstream intelligence missing. Run CSI, PIS, Predictions, and Digital Twin first.")
            return []

        with open(CSI_JSON_PATH, 'r') as f:
            csi_data = json.load(f)
        with open(PIS_JSON_PATH, 'r') as f:
            pis_data = json.load(f)
        with open(PREDICTIONS_JSON_PATH, 'r') as f:
            pred_data = json.load(f)
        with open(SIMULATION_RESULTS_PATH, 'r') as f:
            dt_data = json.load(f)

        pis_map = {p['hotspot_id']: p for p in pis_data}
        pred_map = {p['hotspot_id']: p for p in pred_data}
        
        # Group DT scenarios by hotspot
        dt_map = {}
        for sim in dt_data:
            hid = sim['hotspot_id']
            if hid not in dt_map:
                dt_map[hid] = []
            dt_map[hid].append(sim)

        print("  Running Enforcement Optimization...")
        
        raw_hotspots = []
        
        for csi in csi_data:
            hid = csi['hotspot_id']
            pis = pis_map.get(hid, {})
            pred = pred_map.get(hid, {})
            dt_scenarios = dt_map.get(hid, [])
            
            # 1. Priority
            pred_risk = pred.get('forecasts', {}).get('1h', {}).get('hotspot_probability', 0)
            is_emergency = csi.get('emergency_route_impact', False)
            # Context importance approximation
            is_high_context = csi.get('component_scores', {}).get('Context Intelligence', 0) > 60
            
            priority = EnforcementPriorityEngine.calculate_priority(
                csi['csi_score'], 
                pis.get('pis_score', 0),
                pred_risk,
                is_emergency,
                is_high_context
            )
            
            # 2. Time Window
            peak_hour = csi.get('peak_hour', 17)
            time_window = TimeWindowEngine.get_optimal_window(peak_hour, csi['csi_score'])
            
            # 3. Scenario Selection
            if dt_scenarios:
                best_scenario = ScenarioSelectionEngine.select_best_scenario(dt_scenarios)
            else:
                best_scenario = {
                    "recommended_action": "Monitor",
                    "expected_csi_reduction": 0, "expected_pis_reduction": 0,
                    "expected_capacity_recovery": 0, "expected_delay_reduction": 0,
                    "roi_score": 0, "confidence_score": 0.0, "scenario_reasoning": "No simulated data."
                }
                
            raw_hotspots.append({
                "hotspot_id": hid,
                "road_name": csi['road_name'],
                "latitude": csi['latitude'],
                "longitude": csi['longitude'],
                "priority_score": priority['priority_score'],
                "priority_level": priority['priority_level'],
                "recommended_time": time_window['recommended_intervention_window'],
                "timing_reasoning": time_window.get('timing_reasoning', ''),
                "is_emergency": is_emergency,
                **best_scenario
            })
            
        # 4. Resource Allocation
        allocated = ResourceAllocationEngine.allocate_teams(raw_hotspots, available_teams)
        
        # Give them ranks
        for idx, item in enumerate(allocated):
            item['priority_rank'] = idx + 1
            item['explanation'] = EnforcementExplainabilityEngine.generate(
                item['priority_rank'],
                csi_map(csi_data, item['hotspot_id'])['csi_score'],
                pis_map.get(item['hotspot_id'], {}).get('pis_score', 0),
                item['is_emergency'],
                item['recommended_action'],
                item['expected_capacity_recovery'],
                item['expected_delay_reduction']
            )
            
        # Build Intelligence Objects
        enforcement_objects = []
        for hs in allocated:
            obj = SmartEnforcementIntelligence(
                hotspot_id=hs['hotspot_id'],
                road_name=hs['road_name'],
                latitude=hs['latitude'],
                longitude=hs['longitude'],
                priority_rank=hs['priority_rank'],
                priority_score=hs['priority_score'],
                priority_level=hs['priority_level'],
                recommended_team=hs['recommended_team'],
                recommended_time=hs['recommended_time'],
                recommended_action=hs['recommended_action'],
                expected_csi_reduction=hs['expected_csi_reduction'],
                expected_pis_reduction=hs['expected_pis_reduction'],
                expected_capacity_recovery=hs['expected_capacity_recovery'],
                expected_delay_reduction=hs['expected_delay_reduction'],
                roi_score=hs['roi_score'],
                confidence_score=hs.get('confidence_score', 0.0),
                explanation=hs['explanation'],
                assignment_reasoning=hs.get('assignment_reasoning', ''),
                timing_reasoning=hs.get('timing_reasoning', ''),
                scenario_reasoning=hs.get('scenario_reasoning', ''),
                status="Pending",
                generated_at=datetime.now()
            )
            enforcement_objects.append(obj.dict())
            
        # 5. Route Optimization
        optimized_routes = PatrolOptimizationEngine.optimize_routes(enforcement_objects)
        
        # 6. Daily Plan
        daily_plan = DailyEnforcementEngine.compile_plan(optimized_routes)
        
        # 7. Weekly Strategy
        weekly_plan = WeeklyStrategyEngine.compile_strategy([daily_plan])
        
        # Save Outputs
        os.makedirs(os.path.dirname(ENFORCEMENT_PLAN_PATH), exist_ok=True)
        
        with open(ENFORCEMENT_PLAN_PATH, 'w') as f:
            json.dump(enforcement_objects, f, indent=2, default=str)
        with open(DAILY_PLAN_PATH, 'w') as f:
            json.dump(daily_plan, f, indent=2, default=str)
        with open(WEEKLY_STRATEGY_PATH, 'w') as f:
            json.dump(weekly_plan, f, indent=2, default=str)
            
        print(f"Smart Enforcement Planner generated {len(enforcement_objects)} prioritized orders across {available_teams} teams.")
        return enforcement_objects

    @staticmethod
    def get_enforcement_plan() -> List[Dict[str, Any]]:
        if not os.path.exists(ENFORCEMENT_PLAN_PATH):
            SmartEnforcementService.generate_all()
        with open(ENFORCEMENT_PLAN_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_daily_plan() -> Dict[str, Any]:
        if not os.path.exists(DAILY_PLAN_PATH):
            SmartEnforcementService.generate_all()
        with open(DAILY_PLAN_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_weekly_plan() -> Dict[str, Any]:
        if not os.path.exists(WEEKLY_STRATEGY_PATH):
            SmartEnforcementService.generate_all()
        with open(WEEKLY_STRATEGY_PATH, 'r') as f:
            return json.load(f)

def csi_map(csi_data, hid):
    for c in csi_data:
        if c['hotspot_id'] == hid:
            return c
    return {}
