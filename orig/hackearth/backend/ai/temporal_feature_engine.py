import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TemporalFeatureEngine:
    """
    Generates temporal features for machine learning models.
    Provides cyclic encoding for time-based features to preserve periodicity.
    """

    @staticmethod
    def generate_features(timestamp: datetime) -> Dict[str, float]:
        """
        Extracts temporal features from a given timestamp.
        Uses sine/cosine transformations for cyclical features like hour and day_of_week.
        """
        hour = timestamp.hour
        day_of_week = timestamp.weekday() # 0 = Monday, 6 = Sunday
        month = timestamp.month
        
        is_weekend = 1.0 if day_of_week >= 5 else 0.0
        
        # Peak hours: 8-11 AM, 5-8 PM
        is_peak_hour = 1.0 if (8 <= hour <= 11) or (17 <= hour <= 20) else 0.0
        
        # Cyclic encoding for hour (0-23)
        hour_sin = np.sin(2 * np.pi * hour / 24.0)
        hour_cos = np.cos(2 * np.pi * hour / 24.0)
        
        # Cyclic encoding for day of week (0-6)
        dow_sin = np.sin(2 * np.pi * day_of_week / 7.0)
        dow_cos = np.cos(2 * np.pi * day_of_week / 7.0)
        
        return {
            "hour_sin": round(hour_sin, 4),
            "hour_cos": round(hour_cos, 4),
            "dow_sin": round(dow_sin, 4),
            "dow_cos": round(dow_cos, 4),
            "is_weekend": is_weekend,
            "is_peak_hour": is_peak_hour,
            "month": float(month)
        }

    @staticmethod
    def get_forecast_timestamps(base_time: datetime) -> Dict[str, datetime]:
        """Returns target timestamps for the 4 forecast horizons."""
        return {
            "1h": base_time + timedelta(hours=1),
            "6h": base_time + timedelta(hours=6),
            "24h": base_time + timedelta(hours=24),
            "7d": base_time + timedelta(days=7)
        }
