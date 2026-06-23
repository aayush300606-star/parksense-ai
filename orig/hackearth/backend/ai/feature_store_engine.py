import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
from .temporal_feature_engine import TemporalFeatureEngine

class FeatureStoreEngine:
    """
    Centralized Feature Store for ML Models.
    Aggregates data from CSI, PIS, Traffic, Road, and Context intelligence.
    
    In a real production environment, this would connect to Feast or Vertex AI Feature Store.
    Here we dynamically generate a synthetic historical dataset using our 100 hotspots
    to train real ML models without 'fake' predictions.
    """

    @staticmethod
    def build_current_features(csi_data: List[Dict], pis_data: List[Dict], current_time: datetime) -> pd.DataFrame:
        """
        Builds the current feature state for all hotspots for inference.
        """
        pis_map = {p['hotspot_id']: p for p in pis_data}
        
        features = []
        for csi in csi_data:
            hid = csi['hotspot_id']
            pis = pis_map.get(hid, {})
            
            # Base features
            f = {
                "hotspot_id": hid,
                "current_csi": csi['csi_score'],
                "current_pis": pis.get('pis_score', 0),
                "capacity_loss": csi['capacity_loss_percentage'],
                "speed_reduction": csi['speed_reduction_percentage'],
                "violation_density": csi['violation_density_score'],
                "junction_influence": csi.get('component_scores', {}).get('Junction Influence', 0),
                "poi_density": csi.get('component_scores', {}).get('POI Density', 0),
                "road_hierarchy_encoded": FeatureStoreEngine._encode_hierarchy(csi['road_hierarchy'])
            }
            
            # Add temporal features for current time
            temp_f = TemporalFeatureEngine.generate_features(current_time)
            f.update(temp_f)
            
            features.append(f)
            
        return pd.DataFrame(features)

    @staticmethod
    def build_synthetic_historical_dataset(csi_data: List[Dict], pis_data: List[Dict], days: int = 14) -> pd.DataFrame:
        """
        Bootstraps a realistic historical dataset by taking the current state and 
        perturbing it across time using known temporal rules (e.g., lower at night, higher at peak).
        This provides data to train standard ML regressors.
        """
        current_df = FeatureStoreEngine.build_current_features(csi_data, pis_data, datetime.now())
        
        historical_rows = []
        base_time = datetime.now() - timedelta(days=days)
        
        # Generate 4 samples per day per hotspot
        for day in range(days):
            for hour in [2, 9, 14, 18]: # Night, Morning Peak, Afternoon, Evening Peak
                timestamp = base_time + timedelta(days=day, hours=hour)
                temp_f = TemporalFeatureEngine.generate_features(timestamp)
                
                # Baseline multiplier based on time
                multiplier = 1.0
                if temp_f["is_peak_hour"] == 1.0:
                    multiplier = np.random.uniform(1.1, 1.4)
                elif hour == 2:
                    multiplier = np.random.uniform(0.1, 0.3)
                else:
                    multiplier = np.random.uniform(0.7, 1.0)
                    
                if temp_f["is_weekend"] == 1.0 and hour in [9, 18]:
                    multiplier *= 0.8 # Less intense peaks on weekend
                elif temp_f["is_weekend"] == 1.0 and hour == 14:
                    multiplier *= 1.2 # More afternoon traffic on weekend
                    
                for _, row in current_df.iterrows():
                    # Perturb features
                    hist_row = row.copy()
                    
                    hist_row['hour_sin'] = temp_f['hour_sin']
                    hist_row['hour_cos'] = temp_f['hour_cos']
                    hist_row['dow_sin'] = temp_f['dow_sin']
                    hist_row['dow_cos'] = temp_f['dow_cos']
                    hist_row['is_weekend'] = temp_f['is_weekend']
                    hist_row['is_peak_hour'] = temp_f['is_peak_hour']
                    
                    # Target variables (what the model will predict)
                    # We add some noise to make it realistic
                    noise = np.random.normal(0, 5)
                    hist_row['target_csi'] = np.clip(row['current_csi'] * multiplier + noise, 0, 100)
                    hist_row['target_pis'] = np.clip(row['current_pis'] * multiplier + noise, 0, 100)
                    
                    historical_rows.append(hist_row)
                    
        return pd.DataFrame(historical_rows)

    @staticmethod
    def _encode_hierarchy(hierarchy: str) -> float:
        mapping = {
            "Expressway": 1.0,
            "Major Arterial": 0.8,
            "Minor Arterial": 0.6,
            "Collector": 0.4,
            "Secondary": 0.3,
            "Residential": 0.2,
            "Service": 0.1
        }
        return mapping.get(hierarchy, 0.5)
