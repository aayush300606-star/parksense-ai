from typing import Dict, Any


class AffectedVehicleEngine:
    """
    Estimates the number of vehicles impacted by a congestion hotspot.
    """

    # Baseline hourly capacity in Indian cities before congestion (per direction)
    HOURLY_CAPACITY = {
        "Expressway": 3600,
        "Major Arterial": 2400,
        "Minor Arterial": 1600,
        "Collector": 1000,
        "Secondary": 600,
        "Residential": 300,
        "Service": 150,
    }

    # Peak hour multiplier (how much of the daily traffic happens in one peak hour)
    PEAK_FACTOR = 0.12

    @staticmethod
    def estimate_vehicles(
        road_hierarchy: str,
        capacity_loss_percentage: float,
        csi_score: float
    ) -> Dict[str, Any]:
        """
        Estimates the number of vehicles impacted based on baseline capacity
        and the severity of the bottleneck.
        """
        base_capacity = AffectedVehicleEngine.HOURLY_CAPACITY.get(road_hierarchy, 600)
        
        # When capacity drops, throughput drops but queue builds up.
        # Affected vehicles = baseline volume * (CSI impact factor)
        # We assume baseline volume is running at 80% capacity during peak.
        peak_volume = base_capacity * 0.8
        
        # Impact factor scales with CSI. Higher CSI = more vehicles stuck in the bottleneck.
        impact_factor = max(0.2, csi_score / 100.0)
        
        vehicles_impacted_per_hour = peak_volume * impact_factor
        
        # Daily volume = peak / peak_factor. Assuming 14 active hours of impact.
        vehicles_impacted_per_day = vehicles_impacted_per_hour * 14
        
        return {
            "vehicles_impacted_per_hour": int(vehicles_impacted_per_hour),
            "vehicles_impacted_per_day": int(vehicles_impacted_per_day),
            "peak_hour_impacted_vehicles": int(vehicles_impacted_per_hour),
            "confidence": 0.85,
            "source": "AffectedVehicleEngine"
        }
