from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime


class ContextIntelligence(BaseModel):
    """
    Standardized Context Intelligence Object.
    
    Captures the full location-awareness profile of a hotspot:
    junction proximity, POI landscape, critical infrastructure,
    emergency access impact, and overall context importance.
    
    This object is a primary input for:
        - Adaptive Congestion Severity Index (CSI)
        - Parking Impact Score (PIS)
        - Enforcement Priority Planner
        - Smart City LLM Agent
    """
    model_config = {"protected_namespaces": ()}

    hotspot_id: int
    road_name: str

    # Junction Intelligence
    junction_id: str
    junction_distance_m: float
    junction_type: str
    junction_signalized: bool
    junction_road_count: int
    junction_score: float
    junction_importance_score: float
    junction_importance_level: str
    junction_influence_score: float
    junction_influence_level: str

    # POI Intelligence (multi-radius)
    poi_count_300m: int
    poi_count_500m: int
    poi_count_1000m: int
    poi_density_score: float
    poi_density_level: str

    # Critical Infrastructure
    critical_infrastructure_score: float
    critical_infrastructure_level: str
    critical_poi_count: int

    # Emergency Access
    emergency_impact_score: float
    emergency_priority: str
    emergency_route_impact: bool

    # Context Importance (aggregate)
    context_importance_score: float
    context_importance_level: str

    # Explainability
    context_explainability: str

    # Metadata
    source: str
    confidence: float
    generated_at: datetime
