from typing import Dict, Any

class TimeWindowEngine:
    """
    Identifies the optimal time window to deploy enforcement personnel,
    based on prediction forecasts and hotspot severity.
    """

    @staticmethod
    def get_optimal_window(predicted_peak_hour: int, csi_score: float = 0.0) -> Dict[str, Any]:
        """
        Calculates the best impact window and explains the reasoning.
        """
        # If severity is high (CSI > 60), we need a wider 3-hour pre-emptive window.
        # Otherwise, a 2-hour window is sufficient.
        window_duration = 3 if csi_score > 60 else 2
        
        # We deploy enforcement *before* the peak hits.
        start_hour = (predicted_peak_hour - window_duration + 1) % 24
        end_hour = (predicted_peak_hour + 1) % 24
        
        start_str = f"{start_hour:02d}:00"
        end_str = f"{end_hour:02d}:00"
        peak_str = f"{predicted_peak_hour:02d}:00"
        
        if window_duration == 3:
            reasoning = f"Extended {window_duration}-hour deployment selected starting at {start_str} to pre-emptively manage the severe predicted peak at {peak_str} (CSI: {csi_score:.1f})."
        else:
            reasoning = f"Standard {window_duration}-hour deployment starting at {start_str} to clear blockages prior to the {peak_str} peak congestion."
        
        return {
            "peak_congestion_period": peak_str,
            "recommended_intervention_window": f"{start_str} - {end_str}",
            "start_hour": start_hour,
            "timing_reasoning": reasoning
        }
