import os
import pandas as pd
import numpy as np
from typing import Dict, List
from collections import Counter


class TemporalPatternEngine:
    """
    Extracts time-of-day and day-of-week violation patterns from raw data.
    
    For each hotspot, determines:
        - Peak violation hours
        - Day-of-week distribution
        - Month-over-month consistency (recurrence)
        - Temporal recurrence score (0-100)
    
    A hotspot with violations consistently across all months and peak hours
    scores higher recurrence than one with sporadic bursts.
    """

    CLEANED_DATA_PATH = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'processed', 'cleaned_dataset.csv'
    )

    @staticmethod
    def analyze_temporal_patterns(hotspots: List[Dict]) -> List[Dict]:
        """
        Analyzes temporal patterns for all hotspots using the cleaned dataset.
        
        Args:
            hotspots: List of hotspot dicts with hotspot_id, latitude, longitude
            
        Returns:
            List of temporal pattern dicts per hotspot
        """
        # Load cleaned dataset
        if not os.path.exists(TemporalPatternEngine.CLEANED_DATA_PATH):
            print("Cleaned dataset not found. Returning default temporal patterns.")
            return [TemporalPatternEngine._default_pattern(h['hotspot_id']) for h in hotspots]

        try:
            df = pd.read_csv(TemporalPatternEngine.CLEANED_DATA_PATH)
        except Exception as e:
            print(f"Failed to load temporal data: {e}")
            return [TemporalPatternEngine._default_pattern(h['hotspot_id']) for h in hotspots]

        # Parse datetime columns
        date_col = None
        for col in ['violation_date', 'date', 'challan_date', 'created_at', 'timestamp']:
            if col in df.columns:
                date_col = col
                break

        time_col = None
        for col in ['violation_time', 'time', 'challan_time']:
            if col in df.columns:
                time_col = col
                break

        # Try to extract temporal features
        has_hour = False
        has_month = False
        has_dow = False

        if date_col:
            try:
                df['_parsed_date'] = pd.to_datetime(df[date_col], errors='coerce')
                df['_month'] = df['_parsed_date'].dt.month
                df['_dow'] = df['_parsed_date'].dt.dayofweek  # 0=Monday
                has_month = df['_month'].notna().sum() > 0
                has_dow = df['_dow'].notna().sum() > 0
            except Exception:
                pass

        if time_col:
            try:
                df['_hour'] = pd.to_datetime(df[time_col], format='mixed', errors='coerce').dt.hour
                has_hour = df['_hour'].notna().sum() > 0
            except Exception:
                pass

        # If no temporal columns found, use coordinate-based assignment
        if not has_hour and not has_month:
            return TemporalPatternEngine._coordinate_based_patterns(hotspots, df)

        # Build spatial assignment: assign each row to nearest hotspot
        # For performance, use a simple bounding-box approach
        results = []
        for h in hotspots:
            hid = h['hotspot_id']
            lat = h['latitude']
            lon = h['longitude']
            radius_deg = h.get('cluster_radius', 500) / 111000.0  # meters to degrees

            # Filter violations near this hotspot
            mask = (
                (df['latitude'] >= lat - radius_deg) &
                (df['latitude'] <= lat + radius_deg) &
                (df['longitude'] >= lon - radius_deg) &
                (df['longitude'] <= lon + radius_deg)
            )
            local_df = df[mask]

            if len(local_df) == 0:
                results.append(TemporalPatternEngine._default_pattern(hid))
                continue

            pattern = {"hotspot_id": hid}

            # Hour-of-day distribution
            if has_hour:
                hour_counts = local_df['_hour'].dropna().astype(int).value_counts().sort_index()
                hour_dist = {int(h): int(c) for h, c in hour_counts.items()}
                pattern["hourly_distribution"] = hour_dist

                if hour_dist:
                    peak_hour = max(hour_dist, key=hour_dist.get)
                    pattern["peak_hour"] = int(peak_hour)
                    pattern["peak_hour_label"] = f"{peak_hour:02d}:00 - {(peak_hour+1)%24:02d}:00"
                else:
                    pattern["peak_hour"] = 10
                    pattern["peak_hour_label"] = "10:00 - 11:00"
            else:
                pattern["hourly_distribution"] = {}
                pattern["peak_hour"] = 10
                pattern["peak_hour_label"] = "10:00 - 11:00"

            # Day-of-week distribution
            if has_dow:
                dow_counts = local_df['_dow'].dropna().astype(int).value_counts().sort_index()
                dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                dow_dist = {dow_names[int(d)]: int(c) for d, c in dow_counts.items() if int(d) < 7}
                pattern["daily_distribution"] = dow_dist

                if dow_dist:
                    peak_day = max(dow_dist, key=dow_dist.get)
                    pattern["peak_day"] = peak_day
                else:
                    pattern["peak_day"] = "Wednesday"
            else:
                pattern["daily_distribution"] = {}
                pattern["peak_day"] = "Wednesday"

            # Month distribution & recurrence
            if has_month:
                month_counts = local_df['_month'].dropna().astype(int).value_counts()
                months_active = len(month_counts)
                total_months_possible = max(1, df['_month'].dropna().nunique())

                # Recurrence = fraction of months with violations × consistency
                month_coverage = months_active / total_months_possible
                
                # Consistency: coefficient of variation (lower = more consistent)
                if months_active > 1:
                    cv = month_counts.std() / max(1, month_counts.mean())
                    consistency = max(0, 1 - cv)  # 1 = perfectly consistent
                else:
                    consistency = 0.5

                recurrence = (month_coverage * 0.60 + consistency * 0.40) * 100.0
                pattern["months_active"] = int(months_active)
                pattern["month_coverage"] = round(month_coverage, 2)
            else:
                recurrence = 50.0
                pattern["months_active"] = 3
                pattern["month_coverage"] = 0.60

            pattern["temporal_recurrence_score"] = round(min(100.0, max(0.0, recurrence)), 2)
            pattern["violation_count_local"] = int(len(local_df))

            results.append(pattern)

        return results

    @staticmethod
    def _coordinate_based_patterns(hotspots: List[Dict], df: pd.DataFrame) -> List[Dict]:
        """
        Fallback when no temporal columns exist.
        Uses violation count as a proxy for recurrence.
        """
        results = []
        max_violations = max((h.get('violations', 1) for h in hotspots), default=1)

        for h in hotspots:
            hid = h['hotspot_id']
            violations = h.get('violations', 0)

            # Recurrence proportional to violation count
            recurrence = (violations / max(1, max_violations)) * 100.0

            results.append({
                "hotspot_id": hid,
                "hourly_distribution": {},
                "peak_hour": 10,
                "peak_hour_label": "10:00 - 11:00",
                "daily_distribution": {},
                "peak_day": "Wednesday",
                "months_active": 5,
                "month_coverage": 1.0,
                "temporal_recurrence_score": round(min(100.0, recurrence), 2),
                "violation_count_local": int(violations)
            })

        return results

    @staticmethod
    def _default_pattern(hotspot_id: int) -> Dict:
        """Returns a default temporal pattern when no data is available."""
        return {
            "hotspot_id": hotspot_id,
            "hourly_distribution": {},
            "peak_hour": 10,
            "peak_hour_label": "10:00 - 11:00",
            "daily_distribution": {},
            "peak_day": "Wednesday",
            "months_active": 1,
            "month_coverage": 0.20,
            "temporal_recurrence_score": 20.0,
            "violation_count_local": 0
        }
