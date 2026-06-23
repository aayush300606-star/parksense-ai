import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.road_impact import RoadImpact
from ..services.road_service import ROAD_JSON_PATH

from ..ai.occupied_width_engine import OccupiedWidthEngine
from ..ai.effective_width_engine import EffectiveWidthEngine
from ..ai.capacity_loss_engine import CapacityLossEngine
from ..ai.lane_blockage_engine import LaneBlockageEngine
from ..ai.explainability_engine import ExplainabilityEngine
from ..ai.violation_density import DENSITY_JSON_PATH

ROAD_IMPACT_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'road_impact.json')
EFFECTIVE_WIDTH_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'effective_width.json')
CAPACITY_LOSS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'capacity_loss.json')
LANE_BLOCKAGE_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'lane_blockage.json')

class RoadImpactService:
    """
    Orchestrator for the Effective Road Width Loss Engine.
    Combines Hotspot Vehicle Data with Road Intelligence Data.
    """
    
    @staticmethod
    def generate_all():
        """
        Executes the flagship AI capacity loss pipeline.
        """
        if not os.path.exists(ROAD_JSON_PATH) or not os.path.exists(DENSITY_JSON_PATH):
            print("Dependencies missing for Road Impact Pipeline. Run Road Intelligence first.")
            return []
            
        with open(ROAD_JSON_PATH, 'r') as f:
            roads = json.load(f)
            
        with open(DENSITY_JSON_PATH, 'r') as f:
            hotspots = {h['hotspot_id']: h for h in json.load(f)}
            
        impact_objects = []
        
        for r in roads:
            hotspot_id = r['hotspot_id']
            hotspot = hotspots.get(hotspot_id, {})
            vehicle_types = hotspot.get('vehicle_types', {})
            
            # 1. Occupied Width Engine
            occ_data = OccupiedWidthEngine.calculate_occupied_width(vehicle_types)
            occupied_width = occ_data['occupied_width']
            
            road_width = r['estimated_road_width']
            original_lanes = r['lane_count']
            
            # 2. Effective Width Engine
            eff_data = EffectiveWidthEngine.calculate_effective_width(road_width, occupied_width)
            effective_width = eff_data['effective_width']
            
            # 3. Capacity Loss Engine
            cap_loss_data = CapacityLossEngine.calculate_capacity_loss(road_width, occupied_width)
            
            # 4. Lane Blockage Engine
            lane_data = LaneBlockageEngine.calculate_lane_blockage(original_lanes, occupied_width)
            
            # 5. Explainability Engine
            explanation = ExplainabilityEngine.generate_explanation(
                vehicle_types=vehicle_types,
                road_width=road_width,
                occupied_width=occupied_width,
                effective_width=effective_width,
                capacity_loss=cap_loss_data['capacity_loss_percentage']
            )
            
            impact_obj = RoadImpact(
                hotspot_id=hotspot_id,
                road_name=r['road_name'],
                road_width=road_width,
                occupied_width=occupied_width,
                effective_width=effective_width,
                capacity_loss_percentage=cap_loss_data['capacity_loss_percentage'],
                capacity_loss_score=cap_loss_data['capacity_loss_score'],
                lane_blockage_score=lane_data['lane_blockage_score'],
                lane_utilization=lane_data['lane_utilization'],
                blocked_lanes=lane_data['blocked_lanes'],
                remaining_lanes=lane_data['remaining_lanes'],
                explainability=explanation,
                road_confidence=r['confidence_scores'].get('road_width_confidence', 0.80),
                generated_at=datetime.now()
            )
            impact_objects.append(impact_obj)
            
        # Serialize and Save all visualization variants
        os.makedirs(os.path.dirname(ROAD_IMPACT_JSON_PATH), exist_ok=True)
        
        json_data = [obj.dict() for obj in impact_objects]
        with open(ROAD_IMPACT_JSON_PATH, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
            
        # Extract subset lists for specialized dashboard visualizers
        with open(EFFECTIVE_WIDTH_JSON_PATH, 'w') as f:
            json.dump([{'id': x['hotspot_id'], 'effective_width': x['effective_width']} for x in json_data], f, indent=2)
            
        with open(CAPACITY_LOSS_JSON_PATH, 'w') as f:
            json.dump([{'id': x['hotspot_id'], 'capacity_loss_score': x['capacity_loss_score']} for x in json_data], f, indent=2)
            
        with open(LANE_BLOCKAGE_JSON_PATH, 'w') as f:
            json.dump([{'id': x['hotspot_id'], 'blocked_lanes': x['blocked_lanes']} for x in json_data], f, indent=2)
            
        print(f"Road Impact Intelligence generated for {len(impact_objects)} roads.")
        return impact_objects

    @staticmethod
    def get_all_impacts() -> List[Dict[str, Any]]:
        if not os.path.exists(ROAD_IMPACT_JSON_PATH):
            RoadImpactService.generate_all()
        with open(ROAD_IMPACT_JSON_PATH, 'r') as f:
            return json.load(f)
