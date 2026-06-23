from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class RoadImpact(BaseModel):
    """
    Standardized Road Impact Object.
    Quantifies how illegal parking reduces effective road width and capacity.
    """
    hotspot_id: int
    road_name: str
    road_width: float
    occupied_width: float
    effective_width: float
    capacity_loss_percentage: float
    capacity_loss_score: float
    lane_blockage_score: float
    lane_utilization: float
    blocked_lanes: int
    remaining_lanes: int
    explainability: str
    road_confidence: float
    generated_at: datetime
