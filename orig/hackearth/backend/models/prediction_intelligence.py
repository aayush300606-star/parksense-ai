from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class PredictionIntelligence(BaseModel):
    """
    Standardized AI Prediction Intelligence Object.
    Contains ML forecasts for future CSI, PIS, and hotspot probability across multiple time horizons.
    """
    model_config = {"protected_namespaces": ()}

    hotspot_id: int
    road_name: str
    road_hierarchy: str
    latitude: float
    longitude: float

    prediction_timestamp: datetime
    
    # Mapping of horizon ("1h", "6h", "24h", "7d") to forecast data
    forecasts: Dict[str, Dict[str, Any]]
    
    # ML model explainability
    key_prediction_drivers: List[Dict[str, Any]]
    
    generated_at: datetime
