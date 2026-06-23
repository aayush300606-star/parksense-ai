from typing import Dict, Any, List

class TimeWindowEngine:
    """
    Identifies the optimal time window to deploy enforcement personnel.
    """

    @staticmethod
    def get_optimal_window(predicted_peak_hour: int) -> Dict[str, str]:
        """
        Calculates the best 2-hour window.
        We deploy enforcement *before* the peak hits.
        """
        # If peak is at 9 AM, deploy 8 AM to 10 AM
        start_hour = (predicted_peak_hour - 1) % 24
        end_hour = (predicted_peak_hour + 1) % 24
        
        start_str = f"{start_hour:02d}:00"
        end_str = f"{end_hour:02d}:00"
        peak_str = f"{predicted_peak_hour:02d}:00"
        
        return {
            "peak_congestion_period": peak_str,
            "recommended_intervention_window": f"{start_str} - {end_str}",
            "start_hour": start_hour
        }
