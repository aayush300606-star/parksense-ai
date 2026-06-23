import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.road import RoadIntelligence
from ..ai.violation_density import DENSITY_JSON_PATH

from ..ai.road_information import RoadInformationEngine
from ..ai.road_hierarchy_engine import RoadHierarchyEngine
from ..ai.road_width_engine import RoadWidthEngine
from ..ai.road_capacity_engine import RoadCapacityEngine
from ..ai.road_geometry_engine import RoadGeometryEngine
from ..ai.road_confidence_engine import RoadConfidenceEngine

ROAD_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'road_intelligence.json')
STATS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'road_statistics.json')

class RoadService:
    """
    Orchestrator for the Road Intelligence Layer.
    Loads hotspots, extracts AI attributes, and generates standard objects.
    """
    
    @staticmethod
    def generate_all():
        """
        Processes all hotspots and calculates road intelligence.
        """
        if not os.path.exists(DENSITY_JSON_PATH):
            print("No hotspots data found. Pipeline dependency missing.")
            return []
            
        with open(DENSITY_JSON_PATH, 'r') as f:
            hotspots = json.load(f)
            
        road_objects = []
        
        for h in hotspots:
            # 1. Road Information Extraction (MapMyIndia stub / Deterministic Fallback)
            info = RoadInformationEngine.extract_information(h.get('location_name', ''), h['latitude'], h['longitude'])
            source = "Deterministic Algorithm"
            
            # 2. Road Hierarchy Assignment
            hierarchy = RoadHierarchyEngine.calculate_hierarchy(info['road_category'])
            
            # 3. Road Width Estimation
            width = RoadWidthEngine.estimate_width(hierarchy['road_hierarchy'])
            
            # 4. Road Capacity Estimation
            capacity = RoadCapacityEngine.calculate_capacity(width, hierarchy['road_priority_score'])
            
            # 5. Road Geometry Generation
            geometry = RoadGeometryEngine.generate_geometry(h['latitude'], h['longitude'], h['cluster_radius'])
            
            # 6. Road Confidence
            confidence = RoadConfidenceEngine.calculate_confidence(source)
            
            # Map to standard Pydantic model
            road_obj = RoadIntelligence(
                hotspot_id=h['hotspot_id'],
                road_name=info['road_name'],
                road_category=info['road_category'],
                road_hierarchy=hierarchy['road_hierarchy'],
                road_type=info['road_type'],
                road_priority_score=hierarchy['road_priority_score'],
                lane_count=capacity['lane_count'],
                estimated_road_width=width,
                speed_limit=info['speed_limit'],
                capacity_factor=capacity['capacity_factor'],
                capacity_score=capacity['capacity_score'],
                geometry=geometry,
                confidence_scores=confidence,
                source=source,
                generated_at=datetime.now()
            )
            
            road_objects.append(road_obj)
            
        # Serialize and Save
        os.makedirs(os.path.dirname(ROAD_JSON_PATH), exist_ok=True)
        with open(ROAD_JSON_PATH, 'w') as f:
            json.dump([obj.dict() for obj in road_objects], f, indent=2, default=str)
            
        print(f"Road Intelligence layer generated for {len(road_objects)} locations.")
        RoadService.generate_statistics(road_objects)
        return road_objects
        
    @staticmethod
    def generate_statistics(road_objects: List[RoadIntelligence]):
        """
        Calculates and stores analytics payload.
        """
        if not road_objects:
            return
            
        stats = {
            "total_roads": len(road_objects),
            "road_categories": {},
            "lane_distribution": {},
            "hierarchy_distribution": {},
            "average_width_meters": 0.0,
            "average_capacity_score": 0.0
        }
        
        total_width = 0
        total_capacity = 0
        
        for r in road_objects:
            # Categories
            stats["road_categories"][r.road_category] = stats["road_categories"].get(r.road_category, 0) + 1
            # Lanes
            lane_key = f"{r.lane_count} Lanes"
            stats["lane_distribution"][lane_key] = stats["lane_distribution"].get(lane_key, 0) + 1
            # Hierarchy
            stats["hierarchy_distribution"][r.road_hierarchy] = stats["hierarchy_distribution"].get(r.road_hierarchy, 0) + 1
            
            total_width += r.estimated_road_width
            total_capacity += r.capacity_score
            
        stats["average_width_meters"] = round(total_width / len(road_objects), 2)
        stats["average_capacity_score"] = round(total_capacity / len(road_objects), 2)
        
        with open(STATS_JSON_PATH, 'w') as f:
            json.dump(stats, f, indent=2)
            
    @staticmethod
    def get_all_roads() -> List[Dict[str, Any]]:
        if not os.path.exists(ROAD_JSON_PATH):
            RoadService.generate_all()
        with open(ROAD_JSON_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_road_by_id(hotspot_id: int) -> Dict[str, Any]:
        roads = RoadService.get_all_roads()
        for r in roads:
            if r['hotspot_id'] == hotspot_id:
                return r
        return None
        
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        if not os.path.exists(STATS_JSON_PATH):
            RoadService.generate_all()
        with open(STATS_JSON_PATH, 'r') as f:
            return json.load(f)
