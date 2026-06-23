from fastapi import APIRouter
from typing import List, Dict, Any
import os
import json
from ..services.prediction_service import PredictionService

router = APIRouter(prefix="/api")

@router.get("/predictions", response_model=List[Dict[str, Any]])
def get_all_predictions():
    """Returns AI forecasts (1h, 6h, 24h, 7d) for all hotspots."""
    return PredictionService.get_all_predictions()

@router.get("/predictions/shap")
def get_shap_values():
    """Returns SHAP values for explainable AI."""
    shap_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'shap_values.json')
    if os.path.exists(shap_path):
        with open(shap_path, 'r') as f:
            return json.load(f)
    return {"error": "SHAP values not found"}

@router.get("/predictions/{hotspot_id}")
def get_prediction_by_id(hotspot_id: int):
    """Returns detailed AI forecast for a specific hotspot."""
    return PredictionService.get_prediction(hotspot_id)

@router.get("/predicted-hotspots")
def get_predicted_hotspots():
    """Returns future hotspots sorted by 24h predicted severity."""
    return PredictionService.get_predicted_hotspots()

@router.get("/future-risk-zones")
def get_future_risk_zones():
    """Returns zones flagged with critical or high risk in the future."""
    return PredictionService.get_future_risk_zones()

@router.get("/prediction-summary")
def get_prediction_summary():
    """Returns ML model health and prediction aggregate summary."""
    return PredictionService.get_summary()


