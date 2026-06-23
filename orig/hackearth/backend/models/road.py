from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class RoadIntelligence(BaseModel):
    """
    Standardized Road Intelligence Object.
    Contains rich spatial and hierarchical metadata for a specific hotspot.
    """
    hotspot_id: int
    road_name: str
    road_category: str
    road_hierarchy: str
    road_type: str
    road_priority_score: int
    lane_count: int
    estimated_road_width: float
    speed_limit: int
    capacity_factor: str
    capacity_score: float
    geometry: Dict[str, Any]
    confidence_scores: Dict[str, float]
    source: str
    generated_at: datetime
