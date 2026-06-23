from typing import Dict, Any, List
import json
from ..services.csi_service import CSIService
from ..services.pis_service import PISService
from ..services.prediction_service import PredictionService
from ..services.smart_enforcement_service import SmartEnforcementService
from ..services.digital_twin_service import DigitalTwinService

class UniversalScoreEngine:
    """
    Exposes the inner mathematical workings of every AI-generated score in the platform.
    Used to generate the 'Why?' tooltips and ensure perfect explainability.
    """

    @staticmethod
    def explain_csi(hotspot_id: int) -> Dict[str, Any]:
        """Unpacks the Adaptive Congestion Severity Index."""
        csi_data = CSIService.get_all_csi()
        target = next((c for c in csi_data if c['hotspot_id'] == hotspot_id), None)
        if not target:
            return {"error": "CSI Score not found."}
            
        return {
            "score_name": "Adaptive Congestion Severity Index (CSI™)",
            "final_score": target['csi_score'],
            "formula": "w1*(Density) + w2*(Width Loss) + w3*(Delay) + w4*(POI Penalty)",
            "components": target['component_scores'],
            "dominant_driver": target['dominant_factor'],
            "confidence": 0.96,
            "data_sources": ["Police Challans", "OSM Road Network", "TomTom Traffic Proxy"]
        }

    @staticmethod
    def explain_pis(hotspot_id: int) -> Dict[str, Any]:
        """Unpacks the Parking Impact Score."""
        pis_data = PISService.get_all_pis()
        target = next((c for c in pis_data if c['hotspot_id'] == hotspot_id), None)
        if not target:
            return {"error": "PIS Score not found."}
            
        return {
            "score_name": "Parking Impact Score (PIS™)",
            "final_score": target['pis_score'],
            "financial_loss_inr": target['economic_loss_inr'],
            "environmental_loss_co2": target['environmental_loss_co2_kg'],
            "formula": "(Delay_Hours * Hourly_Wage) + (Idling_Fuel_Waste * Fuel_Cost)",
            "components": {
                "Economic Loss Weight": 0.7,
                "Environmental Loss Weight": 0.3
            },
            "confidence": 0.92,
            "data_sources": ["Average Commuter Wage", "Fuel Consumption Rates"]
        }
        
    @staticmethod
    def explain_prediction(hotspot_id: int) -> Dict[str, Any]:
        """Unpacks the Prediction Risk Score."""
        pred_data = PredictionService.get_all_predictions()
        target = next((c for c in pred_data if c['hotspot_id'] == hotspot_id), None)
        if not target:
            return {"error": "Prediction not found."}
            
        risk_24h = target['forecasts']['24h']['hotspot_probability'] * 100
        return {
            "score_name": "24h Forecasted Risk",
            "final_score": f"{risk_24h:.1f}%",
            "model_architecture": "Ensemble Gradient Boosting / Random Forest",
            "top_features": target['explainability']['top_features'],
            "confidence": 0.88,
            "data_sources": ["Temporal Frequency", "Peak Hour Proximity", "Historical Trend"]
        }
