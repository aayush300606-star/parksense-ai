from typing import Dict, Any
from .commuter_impact_engine import CommuterImpactEngine

class FuelWasteEngine:
    """
    Estimates fuel wasted due to congestion idling and slow movement.
    """

    # Fuel consumption rate while idling or moving < 10 km/h (Liters per Hour)
    IDLE_CONSUMPTION_LPH = {
        "Bike": 0.2,
        "Car": 1.2,
        "Auto": 0.6,
        "Bus": 4.0,
        "LCV": 2.0
    }

    @staticmethod
    def estimate_fuel_waste(
        daily_delay_hours: float,
        road_hierarchy: str
    ) -> Dict[str, Any]:
        """
        Estimates liters of fuel wasted based on delay hours and modal share.
        """
        share = CommuterImpactEngine.MODAL_SHARE.get(
            road_hierarchy, CommuterImpactEngine.MODAL_SHARE["Secondary"]
        )
        
        fuel_wasted_per_day = 0.0
        for v_type, pct in share.items():
            # Delay hours contributed by this vehicle type
            type_delay_hours = daily_delay_hours * pct
            consumption_rate = FuelWasteEngine.IDLE_CONSUMPTION_LPH.get(v_type, 1.0)
            fuel_wasted_per_day += type_delay_hours * consumption_rate
            
        fuel_wasted_per_month = fuel_wasted_per_day * 25 # Active days
        fuel_wasted_per_year = fuel_wasted_per_day * 300
        
        # Fuel score: 100 if > 2000 liters wasted daily
        fuel_impact_score = min(100.0, (fuel_wasted_per_day / 2000.0) * 100.0)
        
        return {
            "fuel_wasted_per_day": round(fuel_wasted_per_day, 1),
            "fuel_wasted_per_month": round(fuel_wasted_per_month, 1),
            "fuel_wasted_per_year": round(fuel_wasted_per_year, 1),
            "fuel_impact_score": round(fuel_impact_score, 2)
        }
