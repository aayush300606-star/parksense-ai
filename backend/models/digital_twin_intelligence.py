from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class DigitalTwinIntelligence(BaseModel):
    """
    Standardized AI Digital Twin Simulation Object.
    Contains Before/After metrics and deltas for a specific scenario.
    """
    model_config = {"protected_namespaces": ()}

    hotspot_id: int
    road_name: str
    
    scenario_id: str
    scenario_name: str
    
    baseline_state: Dict[str, Any]
    simulated_state: Dict[str, Any]
    
    deltas: Dict[str, Any]
    
    benefit_score: float
    roi: str
    explanation: str
    
    generated_at: datetime
