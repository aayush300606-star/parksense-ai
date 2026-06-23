from typing import Dict, Any


class CommuterImpactEngine:
    """
    Translates vehicle counts into human impact using Indian modal share and occupancy assumptions.
    """

    # Average occupancy per vehicle type
    OCCUPANCY = {
        "Bike": 1.2,
        "Car": 1.5,
        "Auto": 2.5,
        "Bus": 30.0,
        "LCV": 1.1 # Light commercial vehicle
    }

    # Typical modal share on Indian arterial/city roads
    MODAL_SHARE = {
        "Expressway": {"Car": 0.60, "Bike": 0.10, "Bus": 0.10, "Auto": 0.05, "LCV": 0.15},
        "Major Arterial": {"Car": 0.40, "Bike": 0.35, "Bus": 0.10, "Auto": 0.10, "LCV": 0.05},
        "Minor Arterial": {"Car": 0.35, "Bike": 0.40, "Bus": 0.05, "Auto": 0.15, "LCV": 0.05},
        "Collector": {"Car": 0.30, "Bike": 0.45, "Bus": 0.02, "Auto": 0.20, "LCV": 0.03},
        "Secondary": {"Car": 0.25, "Bike": 0.50, "Bus": 0.01, "Auto": 0.22, "LCV": 0.02},
        "Residential": {"Car": 0.20, "Bike": 0.60, "Bus": 0.00, "Auto": 0.18, "LCV": 0.02},
        "Service": {"Car": 0.10, "Bike": 0.70, "Bus": 0.00, "Auto": 0.15, "LCV": 0.05},
    }

    @staticmethod
    def estimate_commuters(
        vehicles_per_day: int,
        road_hierarchy: str
    ) -> Dict[str, Any]:
        """
        Estimates the number of daily commuters affected by the bottleneck.
        """
        share = CommuterImpactEngine.MODAL_SHARE.get(
            road_hierarchy, CommuterImpactEngine.MODAL_SHARE["Secondary"]
        )
        
        daily_commuters = 0
        for v_type, pct in share.items():
            count = vehicles_per_day * pct
            occupancy = CommuterImpactEngine.OCCUPANCY.get(v_type, 1.2)
            daily_commuters += count * occupancy
            
        peak_commuters = daily_commuters / 14  # Assuming 14 active hours
        
        # Score out of 100 based on severity of commuter impact (cap at 100k daily)
        commuter_impact_score = min(100.0, (daily_commuters / 100000.0) * 100.0)
        
        return {
            "people_affected": int(daily_commuters),
            "daily_commuters_affected": int(daily_commuters),
            "peak_hour_commuters": int(peak_commuters),
            "commuter_impact_score": round(commuter_impact_score, 2)
        }
