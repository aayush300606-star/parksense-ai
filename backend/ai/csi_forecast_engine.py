import pandas as pd
from typing import Dict, List, Any
from datetime import datetime

class CSIForecastEngine:
    """
    Generates CSI predictions for future time horizons.
    """

    @staticmethod
    def forecast(
        model_engine,
        csi_data: List[Dict],
        pis_data: List[Dict],
        target_timestamp: datetime
    ) -> Dict[int, float]:
        """
        Predicts future CSI for all hotspots at a specific future timestamp.
        Returns a mapping of hotspot_id -> predicted_csi.
        """
        from .feature_store_engine import FeatureStoreEngine
        
        df_inference = FeatureStoreEngine.build_current_features(csi_data, pis_data, target_timestamp)
        pred_csi, _ = model_engine.predict(df_inference)
        
        forecasts = {}
        for idx, row in df_inference.iterrows():
            hid = int(row['hotspot_id'])
            forecasts[hid] = round(pred_csi[idx], 2)
            
        return forecasts
