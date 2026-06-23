import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.prediction_intelligence import PredictionIntelligence
from ..services.csi_service import CSI_JSON_PATH
from ..services.pis_service import PIS_JSON_PATH

from ..ai.feature_store_engine import FeatureStoreEngine
from ..ai.temporal_feature_engine import TemporalFeatureEngine
from ..ai.model_engine import ModelEngine
from ..ai.feature_importance_engine import FeatureImportanceEngine
from ..ai.csi_forecast_engine import CSIForecastEngine
from ..ai.pis_forecast_engine import PISForecastEngine
from ..ai.hotspot_prediction_engine import HotspotPredictionEngine
from ..ai.prediction_explainability_engine import PredictionExplainabilityEngine
from ..ai.risk_forecast_engine import RiskForecastEngine
from ..ai.enforcement_forecast_engine import EnforcementForecastEngine
from ..ai.model_monitoring_engine import ModelMonitoringEngine

PREDICTIONS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'predictions.json')
FUTURE_HOTSPOTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'future_hotspots.json')
FUTURE_RISK_ZONES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'future_risk_zones.json')
ENFORCEMENT_FORECASTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'enforcement_forecasts.json')
PREDICTION_SUMMARY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'prediction_summary.json')

class PredictionService:
    """
    Orchestrator for the AI Prediction Engine.
    Trains ML models on synthetic historical data and forecasts future states.
    """

    @staticmethod
    def generate_all():
        """Executes the full prediction pipeline."""
        if not os.path.exists(CSI_JSON_PATH) or not os.path.exists(PIS_JSON_PATH):
            print("CSI or PIS data missing. Run those pipelines first.")
            return []

        with open(CSI_JSON_PATH, 'r') as f:
            csi_data = json.load(f)
        with open(PIS_JSON_PATH, 'r') as f:
            pis_data = json.load(f)

        print("  Bootstrapping synthetic historical dataset for ML training...")
        df_history = FeatureStoreEngine.build_synthetic_historical_dataset(csi_data, pis_data, days=14)
        
        print("  Training ML Models (Random Forest / Gradient Boosting)...")
        model_engine = ModelEngine()
        model_metrics = model_engine.train_models(df_history)
        
        # Get feature importances
        top_drivers = FeatureImportanceEngine.get_top_drivers(
            model_engine.csi_model, 
            df_history[model_engine.feature_cols],
            model_engine.feature_cols
        )
        
        # Generate predictions for different horizons
        current_time = datetime.now()
        horizons = TemporalFeatureEngine.get_forecast_timestamps(current_time)
        
        all_forecasts = {hid: {"forecasts": {}} for hid in [c['hotspot_id'] for c in csi_data]}
        
        for horizon_label, target_time in horizons.items():
            print(f"  Predicting horizon: {horizon_label}...")
            # Predict CSI
            csi_forecasts = CSIForecastEngine.forecast(model_engine, csi_data, pis_data, target_time)
            # Predict PIS
            pis_forecasts = PISForecastEngine.forecast(model_engine, csi_data, pis_data, target_time)
            
            for csi in csi_data:
                hid = csi['hotspot_id']
                pred_csi = csi_forecasts[hid]
                pred_pis = pis_forecasts[hid]
                
                hotspot_pred = HotspotPredictionEngine.predict_probability(pred_csi, csi['csi_score'])
                
                explanation = PredictionExplainabilityEngine.generate_explanation(
                    horizon=horizon_label,
                    predicted_csi=pred_csi,
                    current_csi=csi['csi_score'],
                    risk_level=hotspot_pred['hotspot_risk_level'],
                    top_drivers=top_drivers,
                    target_timestamp=target_time
                )
                
                all_forecasts[hid]["forecasts"][horizon_label] = {
                    "target_time": target_time.strftime("%Y-%m-%d %H:%M"),
                    "predicted_csi": pred_csi,
                    "predicted_pis": pred_pis,
                    "hotspot_probability": hotspot_pred['hotspot_probability'],
                    "hotspot_risk_level": hotspot_pred['hotspot_risk_level'],
                    "explanation": explanation
                }
                
        # Build Prediction Intelligence Objects
        prediction_objects = []
        for csi in csi_data:
            hid = csi['hotspot_id']
            obj = PredictionIntelligence(
                hotspot_id=hid,
                road_name=csi['road_name'],
                road_hierarchy=csi['road_hierarchy'],
                latitude=csi['latitude'],
                longitude=csi['longitude'],
                prediction_timestamp=current_time,
                forecasts=all_forecasts[hid]["forecasts"],
                key_prediction_drivers=top_drivers,
                generated_at=datetime.now()
            )
            prediction_objects.append(obj)
            
        os.makedirs(os.path.dirname(PREDICTIONS_JSON_PATH), exist_ok=True)
        
        json_data = [obj.dict() for obj in prediction_objects]
        with open(PREDICTIONS_JSON_PATH, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
            
        # Risk Zones
        risk_zones = RiskForecastEngine.extract_risk_zones(json_data)
        with open(FUTURE_RISK_ZONES_PATH, 'w') as f:
            json.dump(risk_zones, f, indent=2)
            
        # Enforcement Forecasts
        enf_forecasts = EnforcementForecastEngine.generate_patrol_recommendations(json_data)
        with open(ENFORCEMENT_FORECASTS_PATH, 'w') as f:
            json.dump(enf_forecasts, f, indent=2)
            
        # Future hotspots summary (just mapping the 24h horizon)
        future_hotspots = []
        for p in json_data:
            future_hotspots.append({
                "hotspot_id": p['hotspot_id'],
                "road_name": p['road_name'],
                "predicted_probability_24h": p['forecasts']['24h']['hotspot_probability'],
                "predicted_csi_24h": p['forecasts']['24h']['predicted_csi']
            })
        future_hotspots = sorted(future_hotspots, key=lambda x: x['predicted_csi_24h'], reverse=True)
        with open(FUTURE_HOTSPOTS_PATH, 'w') as f:
            json.dump(future_hotspots, f, indent=2)
            
        # Summary & Monitoring
        health_report = ModelMonitoringEngine.generate_health_report(model_metrics)
        
        summary = {
            "total_predictions": len(json_data),
            "high_risk_zones_identified": len(risk_zones),
            "patrol_recommendations_generated": len(enf_forecasts),
            "model_health": health_report,
            "top_global_drivers": top_drivers
        }
        with open(PREDICTION_SUMMARY_PATH, 'w') as f:
            json.dump(summary, f, indent=2)
            
        print(f"Prediction Engine generated forecasts for {len(prediction_objects)} locations.")
        return prediction_objects

    @staticmethod
    def get_all_predictions() -> List[Dict[str, Any]]:
        if not os.path.exists(PREDICTIONS_JSON_PATH):
            PredictionService.generate_all()
        with open(PREDICTIONS_JSON_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_prediction(hotspot_id: int) -> Dict[str, Any]:
        preds = PredictionService.get_all_predictions()
        for p in preds:
            if p['hotspot_id'] == hotspot_id:
                return p
        return {"error": "Prediction not found"}
        
    @staticmethod
    def get_predicted_hotspots() -> List[Dict[str, Any]]:
        if not os.path.exists(FUTURE_HOTSPOTS_PATH):
            PredictionService.generate_all()
        with open(FUTURE_HOTSPOTS_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_future_risk_zones() -> List[Dict[str, Any]]:
        if not os.path.exists(FUTURE_RISK_ZONES_PATH):
            PredictionService.generate_all()
        with open(FUTURE_RISK_ZONES_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_summary() -> Dict[str, Any]:
        if not os.path.exists(PREDICTION_SUMMARY_PATH):
            PredictionService.generate_all()
        with open(PREDICTION_SUMMARY_PATH, 'r') as f:
            return json.load(f)
