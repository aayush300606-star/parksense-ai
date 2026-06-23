from typing import Dict, Any


class DelayImpactEngine:
    """
    Calculates aggregate delay hours caused by the hotspot.
    """

    @staticmethod
    def calculate_delay(
        delay_seconds: float,
        vehicles_per_day: int
    ) -> Dict[str, Any]:
        """
        Calculates daily, weekly, and annual delay hours.
        """
        # delay_seconds is the average delay PER vehicle passing through
        daily_delay_seconds = delay_seconds * vehicles_per_day
        daily_delay_hours = daily_delay_seconds / 3600.0
        
        weekly_delay_hours = daily_delay_hours * 6  # Assuming 6 heavy traffic days
        annual_delay_hours = daily_delay_hours * 300 # Excluding some holidays/Sundays
        
        # Delay score: 100 if > 5000 hours daily delay
        delay_impact_score = min(100.0, (daily_delay_hours / 5000.0) * 100.0)
        
        return {
            "daily_delay_hours": round(daily_delay_hours, 1),
            "weekly_delay_hours": round(weekly_delay_hours, 1),
            "annual_delay_hours": round(annual_delay_hours, 1),
            "delay_impact_score": round(delay_impact_score, 2)
        }
