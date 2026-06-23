import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, Any, Tuple

class ModelEngine:
    """
    Core ML Training and Inference Orchestrator.
    Trains and compares Baseline, Random Forest, and HistGradientBoosting (LightGBM equivalent) models.
    """

    def __init__(self):
        self.csi_model = None
        self.pis_model = None
        self.feature_cols = [
            "capacity_loss", "speed_reduction", "violation_density",
            "junction_influence", "poi_density", "road_hierarchy_encoded",
            "hour_sin", "hour_cos", "dow_sin", "dow_cos",
            "is_weekend", "is_peak_hour"
        ]

    def train_models(self, df_history: pd.DataFrame) -> Dict[str, Any]:
        """
        Trains models for CSI and PIS forecasting.
        Compares algorithms and selects the best one based on R2 score.
        """
        X = df_history[self.feature_cols]
        y_csi = df_history['target_csi']
        y_pis = df_history['target_pis']
        
        X_train, X_test, yc_train, yc_test, yp_train, yp_test = train_test_split(
            X, y_csi, y_pis, test_size=0.2, random_state=42
        )
        
        # Train CSI Models
        csi_rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
        csi_hgb = HistGradientBoostingRegressor(max_iter=50, random_state=42)
        
        csi_rf.fit(X_train, yc_train)
        csi_hgb.fit(X_train, yc_train)
        
        rf_r2 = r2_score(yc_test, csi_rf.predict(X_test))
        hgb_r2 = r2_score(yc_test, csi_hgb.predict(X_test))
        
        if hgb_r2 > rf_r2:
            self.csi_model = csi_hgb
            csi_algo = "HistGradientBoosting (LightGBM approx)"
            csi_r2 = hgb_r2
        else:
            self.csi_model = csi_rf
            csi_algo = "RandomForest"
            csi_r2 = rf_r2
            
        # Train PIS Models
        pis_rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
        pis_hgb = HistGradientBoostingRegressor(max_iter=50, random_state=42)
        
        pis_rf.fit(X_train, yp_train)
        pis_hgb.fit(X_train, yp_train)
        
        rf_r2_p = r2_score(yp_test, pis_rf.predict(X_test))
        hgb_r2_p = r2_score(yp_test, pis_hgb.predict(X_test))
        
        if hgb_r2_p > rf_r2_p:
            self.pis_model = pis_hgb
            pis_algo = "HistGradientBoosting (LightGBM approx)"
            pis_r2 = hgb_r2_p
        else:
            self.pis_model = pis_rf
            pis_algo = "RandomForest"
            pis_r2 = rf_r2_p
            
        return {
            "csi_model": {
                "algorithm": csi_algo,
                "r2_score": round(csi_r2, 3),
                "mse": round(mean_squared_error(yc_test, self.csi_model.predict(X_test)), 2)
            },
            "pis_model": {
                "algorithm": pis_algo,
                "r2_score": round(pis_r2, 3),
                "mse": round(mean_squared_error(yp_test, self.pis_model.predict(X_test)), 2)
            }
        }

    def predict(self, df_inference: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Runs inference on current features to output predicted CSI and PIS."""
        X = df_inference[self.feature_cols]
        pred_csi = self.csi_model.predict(X)
        pred_pis = self.pis_model.predict(X)
        return np.clip(pred_csi, 0, 100), np.clip(pred_pis, 0, 100)
