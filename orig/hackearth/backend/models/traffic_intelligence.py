from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class TrafficIntelligence(BaseModel):
    """
    Standardized Traffic Intelligence Object.
    Quantifies how illegal parking degrades traffic flow using macroscopic traffic models.
    """
    model_config = {"protected_namespaces": ()}
    hotspot_id: int
    road_name: str
    road_hierarchy: str

    # Speed Intelligence
    base_speed_kmh: float
    current_speed_kmh: float
    speed_reduction_percentage: float
    speed_reduction_severity: str

    # Travel Time Intelligence (over the affected road segment)
    road_segment_length_m: float
    normal_travel_time_seconds: float
    current_travel_time_seconds: float

    # Delay Intelligence
    delay_seconds: float
    delay_severity: str
    annual_delay_vehicle_hours: float

    # Congestion Impact Intelligence
    congestion_impact_score: float
    congestion_severity: str

    # Upstream data references
    capacity_loss_percentage: float
    lane_blockage_score: float

    # Explainability
    traffic_explainability: str
    model_used: str

    # Metadata
    confidence: float
    generated_at: datetime
