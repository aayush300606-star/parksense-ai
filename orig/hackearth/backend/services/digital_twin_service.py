import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.digital_twin_intelligence import DigitalTwinIntelligence
from ..services.csi_service import CSI_JSON_PATH
from ..services.pis_service import PIS_JSON_PATH
from ..services.road_impact_service import ROAD_IMPACT_JSON_PATH
from ..services.traffic_intelligence_service import TRAFFIC_JSON_PATH

from ..ai.digital_twin_engine import DigitalTwinEngine
from ..ai.multi_scenario_engine import MultiScenarioEngine

SIMULATION_RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'simulation_results.json')
SCENARIO_ANALYSIS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'scenario_analysis.json')

class DigitalTwinService:
    """
    Orchestrator for the Digital Twin Simulation Engine.
    Simulates all standard scenarios for all hotspots and saves outputs.
    """

    @staticmethod
    def generate_all():
        """Executes the standard simulation pipelines for all hotspots."""
        if not os.path.exists(CSI_JSON_PATH) or not os.path.exists(PIS_JSON_PATH):
            print("CSI or PIS data missing. Run those pipelines first.")
            return []

        with open(CSI_JSON_PATH, 'r') as f:
            csi_data = json.load(f)
        with open(PIS_JSON_PATH, 'r') as f:
            pis_data = json.load(f)
        with open(ROAD_IMPACT_JSON_PATH, 'r') as f:
            road_data = json.load(f)
        with open(TRAFFIC_JSON_PATH, 'r') as f:
            traffic_data = json.load(f)

        pis_map = {p['hotspot_id']: p for p in pis_data}
        road_map = {r['hotspot_id']: r for r in road_data}
        traffic_map = {t['hotspot_id']: t for t in traffic_data}
        
        all_simulations = []
        best_scenarios = []
        
        print("  Running multi-scenario simulations for all hotspots...")
        
        for csi in csi_data:
            hid = csi['hotspot_id']
            pis = pis_map.get(hid, {})
            road = road_map.get(hid, {})
            traffic = traffic_map.get(hid, {})
            
            # Inject physical features into csi object for baseline capture
            csi['effective_width_m'] = road.get('effective_width', 7.5)
            csi['current_speed_kmh'] = traffic.get('current_speed_kmh', 15)
            csi['free_flow_speed_kmh'] = traffic.get('free_flow_speed_kmh', 40)
            
            total_road_width = road.get('road_width', csi['effective_width_m'] * 2)
                
            # Run all scenarios
            hotspot_scenarios = MultiScenarioEngine.run_all_scenarios(csi, pis, total_road_width)
            
            # Save the best scenario (highest benefit score)
            best_scenarios.append({
                "hotspot_id": hid,
                "road_name": csi['road_name'],
                "best_scenario": hotspot_scenarios[0]['scenario_name'],
                "roi": hotspot_scenarios[0]['roi'],
                "csi_improvement": hotspot_scenarios[0]['deltas']['csi']['improvement'],
                "benefit_score": hotspot_scenarios[0]['benefit_score']
            })
            
            for sim in hotspot_scenarios:
                obj = DigitalTwinIntelligence(
                    hotspot_id=hid,
                    road_name=csi['road_name'],
                    scenario_id=sim['scenario_id'],
                    scenario_name=sim['scenario_name'],
                    baseline_state=sim['baseline_state'],
                    simulated_state=sim['simulated_state'],
                    deltas=sim['deltas'],
                    benefit_score=sim['benefit_score'],
                    roi=sim['roi'],
                    explanation=sim['explanation'],
                    generated_at=sim['generated_at']
                )
                all_simulations.append(obj.dict())
                
        os.makedirs(os.path.dirname(SIMULATION_RESULTS_PATH), exist_ok=True)
        
        with open(SIMULATION_RESULTS_PATH, 'w') as f:
            json.dump(all_simulations, f, indent=2, default=str)
            
        with open(SCENARIO_ANALYSIS_PATH, 'w') as f:
            json.dump(best_scenarios, f, indent=2)
            
        print(f"Digital Twin Engine completed {len(all_simulations)} scenario simulations.")
        return all_simulations

    @staticmethod
    def get_all_simulations() -> List[Dict[str, Any]]:
        if not os.path.exists(SIMULATION_RESULTS_PATH):
            DigitalTwinService.generate_all()
        with open(SIMULATION_RESULTS_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def simulate_custom(hotspot_id: int, removal_pct: float) -> Dict[str, Any]:
        """Runs an on-the-fly custom simulation for a single hotspot."""
        with open(CSI_JSON_PATH, 'r') as f:
            csi_data = json.load(f)
        with open(PIS_JSON_PATH, 'r') as f:
            pis_data = json.load(f)
        with open(ROAD_IMPACT_JSON_PATH, 'r') as f:
            road_data = json.load(f)
        with open(TRAFFIC_JSON_PATH, 'r') as f:
            traffic_data = json.load(f)
            
        pis_map = {p['hotspot_id']: p for p in pis_data}
        road_map = {r['hotspot_id']: r for r in road_data}
        traffic_map = {t['hotspot_id']: t for t in traffic_data}
        
        csi = next((c for c in csi_data if c['hotspot_id'] == hotspot_id), None)
        if not csi:
            return {"error": "Hotspot not found"}
            
        pis = pis_map.get(hotspot_id, {})
        road = road_map.get(hotspot_id, {})
        traffic = traffic_map.get(hotspot_id, {})
        
        csi['effective_width_m'] = road.get('effective_width', 7.5)
        csi['current_speed_kmh'] = traffic.get('current_speed_kmh', 15)
        csi['free_flow_speed_kmh'] = traffic.get('free_flow_speed_kmh', 40)
        
        total_road_width = road.get('road_width', csi['effective_width_m'] * 2)
        
        from ..ai.scenario_engine import ScenarioEngine
        ScenarioEngine.SCENARIOS["CUSTOM"] = {"name": f"{removal_pct}% Custom Removal", "removal_pct": removal_pct}
        
        sim = DigitalTwinEngine.simulate(csi, pis, total_road_width, "CUSTOM")
        
        obj = DigitalTwinIntelligence(
            hotspot_id=hotspot_id,
            road_name=csi['road_name'],
            scenario_id=sim['scenario_id'],
            scenario_name=sim['scenario_name'],
            baseline_state=sim['baseline_state'],
            simulated_state=sim['simulated_state'],
            deltas=sim['deltas'],
            benefit_score=sim['benefit_score'],
            roi=sim['roi'],
            explanation=sim['explanation'],
            generated_at=sim['generated_at']
        )
        return obj.dict()

    @staticmethod
    def get_best_scenarios() -> List[Dict[str, Any]]:
        if not os.path.exists(SCENARIO_ANALYSIS_PATH):
            DigitalTwinService.generate_all()
        with open(SCENARIO_ANALYSIS_PATH, 'r') as f:
            return json.load(f)
