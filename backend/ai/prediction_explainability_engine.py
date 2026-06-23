from typing import Dict, List, Any
from datetime import datetime

class PredictionExplainabilityEngine:
    """
    Natural Language Generation explaining ML forecasts.
    """

    @staticmethod
    def generate_explanation(
        horizon: str,
        predicted_csi: float,
        current_csi: float,
        risk_level: str,
        top_drivers: List[Dict[str, Any]],
        target_timestamp: datetime
    ) -> str:
        """
        Explains *why* the ML model made a specific forecast.
        """
        delta = predicted_csi - current_csi
        
        time_str = target_timestamp.strftime("%I:%M %p")
        day_str = target_timestamp.strftime("%A")
        
        parts = []
        
        if delta >= 5:
            parts.append(f"Predicted CSI Increase (+{delta:.1f}) in {horizon}.")
        elif delta <= -5:
            parts.append(f"Predicted CSI Decrease ({delta:.1f}) in {horizon}.")
        else:
            parts.append(f"CSI expected to remain stable (~{predicted_csi:.0f}) in {horizon}.")
            
        parts.append(f"Reason: Approaching {day_str} {time_str} conditions.")
        
        driver_names = []
        for d in top_drivers[:3]:
            # Clean up raw feature names for human readability
            feat = d['feature'].replace('_', ' ').title()
            if "Sin" in feat or "Cos" in feat:
                continue # Skip cyclic encoders in text
            if "Hierarchy" in feat:
                feat = "Road Capacity Constraints"
            if "Peak Hour" in feat:
                feat = "Peak Hour Traffic Growth"
                
            driver_names.append(f"{feat}")
            
        if driver_names:
            parts.append("Key drivers: " + ", ".join(driver_names) + ".")
            
        if risk_level in ["Critical Risk", "High Risk"]:
            parts.append("High likelihood of severe bottleneck forming.")
            
        return " ".join(parts)
