import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.traffic_intelligence import TrafficIntelligence
from ..services.road_service import ROAD_JSON_PATH
from ..services.road_impact_service import ROAD_IMPACT_JSON_PATH

from ..ai.base_speed_engine import BaseSpeedEngine
from ..ai.traffic_speed_engine import TrafficSpeedEngine
from ..ai.travel_time_engine import TravelTimeEngine
from ..ai.delay_estimation_engine import DelayEstimationEngine
from ..ai.congestion_impact_engine import CongestionImpactEngine
from ..ai.traffic_explainability_engine import TrafficExplainabilityEngine

TRAFFIC_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'traffic_intelligence.json')
SPEED_ANALYSIS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'speed_analysis.json')
DELAY_ANALYSIS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'delay_analysis.json')
CONGESTION_IMPACT_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'congestion_impact.json')


class TrafficIntelligenceService:
    """
    Orchestrator for the Traffic Intelligence Engine.
    
    Pipeline:
        Road Intelligence + Road Impact
            → Base Speed Engine
            → Traffic Speed Engine (BPR model)
            → Travel Time Engine
            → Delay Estimation Engine
            → Congestion Impact Engine
            → Traffic Explainability Engine
            → Structured JSON Outputs
    """

    @staticmethod
    def generate_all():
        """
        Executes the full traffic intelligence pipeline.
        Depends on Road Intelligence and Road Impact having been generated first.
        """
        if not os.path.exists(ROAD_JSON_PATH):
            print("Road Intelligence data missing. Run Road Intelligence pipeline first.")
            return []
        if not os.path.exists(ROAD_IMPACT_JSON_PATH):
            print("Road Impact data missing. Run Effective Width Engine first.")
            return []

        with open(ROAD_JSON_PATH, 'r') as f:
            roads = json.load(f)

        with open(ROAD_IMPACT_JSON_PATH, 'r') as f:
            impacts = {imp['hotspot_id']: imp for imp in json.load(f)}

        traffic_objects = []

        for road in roads:
            hotspot_id = road['hotspot_id']
            impact = impacts.get(hotspot_id)

            if not impact:
                continue

            road_hierarchy = road['road_hierarchy']
            road_name = road['road_name']
            road_priority_score = road['road_priority_score']

            # Extract road segment length from geometry
            geometry = road.get('geometry', {})
            road_segment_length_m = geometry.get('properties', {}).get('road_segment_length_m', 200.0)

            capacity_loss_pct = impact['capacity_loss_percentage']
            lane_blockage_score = impact['lane_blockage_score']

            # === PIPELINE STAGE 1: Base Speed ===
            base_data = BaseSpeedEngine.get_base_speed(road_hierarchy)
            base_speed = base_data['base_speed_kmh']
            base_vc = base_data['base_vc_ratio']

            # === PIPELINE STAGE 2: Traffic Speed (BPR Model) ===
            speed_data = TrafficSpeedEngine.calculate_current_speed(
                base_speed_kmh=base_speed,
                base_vc_ratio=base_vc,
                capacity_loss_percentage=capacity_loss_pct
            )
            current_speed = speed_data['current_speed_kmh']

            # === PIPELINE STAGE 3: Travel Time ===
            time_data = TravelTimeEngine.calculate_travel_times(
                road_segment_length_m=road_segment_length_m,
                base_speed_kmh=base_speed,
                current_speed_kmh=current_speed
            )

            # === PIPELINE STAGE 4: Delay Estimation ===
            delay_data = DelayEstimationEngine.calculate_delay(
                normal_travel_time_seconds=time_data['normal_travel_time_seconds'],
                current_travel_time_seconds=time_data['current_travel_time_seconds'],
                road_hierarchy=road_hierarchy
            )

            # === PIPELINE STAGE 5: Congestion Impact Score ===
            congestion_data = CongestionImpactEngine.calculate_congestion_impact(
                speed_reduction_percentage=speed_data['speed_reduction_percentage'],
                capacity_loss_percentage=capacity_loss_pct,
                lane_blockage_score=lane_blockage_score,
                delay_severity=delay_data['delay_severity'],
                road_priority_score=road_priority_score
            )

            # === PIPELINE STAGE 6: Explainability ===
            explanation = TrafficExplainabilityEngine.generate_traffic_explanation(
                road_name=road_name,
                road_hierarchy=road_hierarchy,
                base_speed_kmh=base_speed,
                current_speed_kmh=current_speed,
                speed_reduction_percentage=speed_data['speed_reduction_percentage'],
                capacity_loss_percentage=capacity_loss_pct,
                delay_seconds=delay_data['delay_seconds'],
                annual_delay_vehicle_hours=delay_data['annual_delay_vehicle_hours'],
                congestion_impact_score=congestion_data['congestion_impact_score'],
                congestion_severity=congestion_data['congestion_severity']
            )

            # === Build Standardized Object ===
            traffic_obj = TrafficIntelligence(
                hotspot_id=hotspot_id,
                road_name=road_name,
                road_hierarchy=road_hierarchy,
                base_speed_kmh=base_speed,
                current_speed_kmh=current_speed,
                speed_reduction_percentage=speed_data['speed_reduction_percentage'],
                speed_reduction_severity=speed_data['speed_reduction_severity'],
                road_segment_length_m=road_segment_length_m,
                normal_travel_time_seconds=time_data['normal_travel_time_seconds'],
                current_travel_time_seconds=time_data['current_travel_time_seconds'],
                delay_seconds=delay_data['delay_seconds'],
                delay_severity=delay_data['delay_severity'],
                annual_delay_vehicle_hours=delay_data['annual_delay_vehicle_hours'],
                congestion_impact_score=congestion_data['congestion_impact_score'],
                congestion_severity=congestion_data['congestion_severity'],
                capacity_loss_percentage=capacity_loss_pct,
                lane_blockage_score=lane_blockage_score,
                traffic_explainability=explanation,
                model_used=speed_data['model_used'],
                confidence=road.get('confidence_scores', {}).get('speed_limit_confidence', 0.85),
                generated_at=datetime.now()
            )
            traffic_objects.append(traffic_obj)

        # === Serialize and Save ===
        os.makedirs(os.path.dirname(TRAFFIC_JSON_PATH), exist_ok=True)

        json_data = [obj.dict() for obj in traffic_objects]
        with open(TRAFFIC_JSON_PATH, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)

        # === Generate specialized dashboard JSONs ===
        TrafficIntelligenceService._save_speed_analysis(json_data)
        TrafficIntelligenceService._save_delay_analysis(json_data)
        TrafficIntelligenceService._save_congestion_impact(json_data)

        print(f"Traffic Intelligence generated for {len(traffic_objects)} hotspots.")
        return traffic_objects

    @staticmethod
    def _save_speed_analysis(data: List[Dict]):
        """Extracts speed-focused subset for visualization."""
        speed_data = [{
            "hotspot_id": d["hotspot_id"],
            "road_name": d["road_name"],
            "road_hierarchy": d["road_hierarchy"],
            "base_speed_kmh": d["base_speed_kmh"],
            "current_speed_kmh": d["current_speed_kmh"],
            "speed_reduction_percentage": d["speed_reduction_percentage"],
            "speed_reduction_severity": d["speed_reduction_severity"],
        } for d in data]
        with open(SPEED_ANALYSIS_JSON_PATH, 'w') as f:
            json.dump(speed_data, f, indent=2)

    @staticmethod
    def _save_delay_analysis(data: List[Dict]):
        """Extracts delay-focused subset for visualization."""
        delay_data = [{
            "hotspot_id": d["hotspot_id"],
            "road_name": d["road_name"],
            "delay_seconds": d["delay_seconds"],
            "delay_severity": d["delay_severity"],
            "annual_delay_vehicle_hours": d["annual_delay_vehicle_hours"],
            "normal_travel_time_seconds": d["normal_travel_time_seconds"],
            "current_travel_time_seconds": d["current_travel_time_seconds"],
        } for d in data]
        with open(DELAY_ANALYSIS_JSON_PATH, 'w') as f:
            json.dump(delay_data, f, indent=2)

    @staticmethod
    def _save_congestion_impact(data: List[Dict]):
        """Extracts congestion impact subset for visualization."""
        congestion_data = [{
            "hotspot_id": d["hotspot_id"],
            "road_name": d["road_name"],
            "congestion_impact_score": d["congestion_impact_score"],
            "congestion_severity": d["congestion_severity"],
            "capacity_loss_percentage": d["capacity_loss_percentage"],
            "speed_reduction_percentage": d["speed_reduction_percentage"],
        } for d in data]
        with open(CONGESTION_IMPACT_JSON_PATH, 'w') as f:
            json.dump(congestion_data, f, indent=2)

    @staticmethod
    def get_all_traffic() -> List[Dict[str, Any]]:
        if not os.path.exists(TRAFFIC_JSON_PATH):
            TrafficIntelligenceService.generate_all()
        with open(TRAFFIC_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_speed_analysis() -> List[Dict[str, Any]]:
        if not os.path.exists(SPEED_ANALYSIS_JSON_PATH):
            TrafficIntelligenceService.generate_all()
        with open(SPEED_ANALYSIS_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_delay_analysis() -> List[Dict[str, Any]]:
        if not os.path.exists(DELAY_ANALYSIS_JSON_PATH):
            TrafficIntelligenceService.generate_all()
        with open(DELAY_ANALYSIS_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_congestion_impact() -> List[Dict[str, Any]]:
        if not os.path.exists(CONGESTION_IMPACT_JSON_PATH):
            TrafficIntelligenceService.generate_all()
        with open(CONGESTION_IMPACT_JSON_PATH, 'r') as f:
            return json.load(f)
