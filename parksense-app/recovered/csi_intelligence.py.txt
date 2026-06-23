from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class CSIIntelligence(BaseModel):
    """
    Standardized Adaptive CSI™ Intelligence Object.
    
    The primary intelligence output of ParkSense AI.
    Every downstream module consumes this object:
        - Parking Impact Score (PIS™)
        - Enforcement Planner
        - Prediction Engine
        - Digital Twin
        - Executive Dashboard
        - LLM Smart City Agent
    """
    model_config = {"protected_namespaces": ()}

    hotspot_id: int
    road_name: str
    road_hierarchy: str
    latitude: float
    longitude: float

    # === Adaptive CSI™ ===
    csi_score: float
    csi_level: str
    csi_color: str
    csi_color_name: str
    csi_priority: str
    csi_priority_label: str

    # === Component Scores ===
    component_scores: Dict[str, Any]

    # === Adaptive Weights ===
    component_weights: Dict[str, float]
    weight_profile: str
    rules_applied: List[str]
    adaptive_reasoning: List[str]

    # === Contribution Analysis ===
    component_contributions: List[Dict[str, Any]]
    dominant_factor: str
    top_3_factors: List[str]

    # === Enforcement Priority ===
    priority_score: float
    priority_level: str
    expected_capacity_recovery: float
    expected_speed_improvement: float
    daily_vehicles_affected: int
    annual_delay_savings_hours: float
    enforcement_recommendation: str

    # === Ranking ===
    rank: int
    percentile: float
    tier: str

    # === Upstream References ===
    violation_density_score: float
    capacity_loss_percentage: float
    speed_reduction_percentage: float
    congestion_impact_score: float
    annual_delay_vehicle_hours: float
    junction_type: str
    junction_distance_m: float
    emergency_route_impact: bool
    violations: int

    # === Temporal ===
    peak_hour: int
    peak_hour_label: str
    peak_day: str
    temporal_recurrence_score: float

    # === Explainability ===
    human_explanation: str
    key_factors: List[str]
    recommendation: str

    # === Metadata ===
    confidence: float
    generated_at: datetime
