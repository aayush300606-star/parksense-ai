from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class SmartEnforcementIntelligence(BaseModel):
    """
    Standardized SEP Intelligence Object.
    Represents a single actionable enforcement order.
    """
    model_config = {"protected_namespaces": ()}

    hotspot_id: int
    road_name: str
    latitude: float
    longitude: float
    
    priority_rank: int
    priority_score: float
    priority_level: str
    
    recommended_team: str
    recommended_time: str
    
    recommended_action: str
    expected_csi_reduction: float
    expected_pis_reduction: float
    expected_capacity_recovery: float
    expected_delay_reduction: float
    roi_score: float
    confidence_score: float = 0.0
    
    explanation: str
    assignment_reasoning: str = ""
    timing_reasoning: str = ""
    scenario_reasoning: str = ""
    
    status: str = "Pending"
    generated_at: datetime
