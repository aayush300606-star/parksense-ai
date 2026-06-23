import math
from typing import Dict, List


class EmergencyAccessEngine:
    """
    Evaluates whether illegal parking at a hotspot impedes emergency vehicle access.
    
    Emergency access impact is highest when:
        1. A hospital/fire station/police station is nearby
        2. The road is a high-hierarchy road (emergency routes typically use arterials)
        3. The capacity loss is significant (blocking >50% capacity)
        4. The hotspot is on a likely emergency route (between emergency facilities)
    
    This engine produces an emergency_impact_score and emergency_priority.
    """

    # Emergency-relevant POI types and their urgency weights
    EMERGENCY_POI_WEIGHTS = {
        "HOSPITAL":        100,  # Highest — ambulance access is life-critical
        "FIRE_STATION":     90,
        "POLICE_STATION":   75,
        "METRO_STATION":    40,  # Transit disruption can delay emergency personnel
        "RAILWAY_STATION":  35,
        "BUS_STATION":      30,
    }

    # Road hierarchy contribution to emergency route likelihood
    EMERGENCY_ROUTE_PROBABILITY = {
        "Expressway":       1.00,
        "Major Arterial":   0.90,
        "Minor Arterial":   0.70,
        "Collector":        0.50,
        "Secondary":        0.35,
        "Residential":      0.20,
        "Service":          0.10,
    }

    # Distance decay for emergency access (meters)
    # Emergency impact drops rapidly beyond 500m
    @staticmethod
    def _distance_factor(distance_m: float) -> float:
        """Inverse-distance factor with rapid decay."""
        if distance_m <= 50:
            return 1.0
        elif distance_m <= 150:
            return 0.85
        elif distance_m <= 300:
            return 0.65
        elif distance_m <= 500:
            return 0.40
        elif distance_m <= 1000:
            return 0.20
        else:
            return 0.05

    @staticmethod
    def calculate_emergency_impact(
        all_pois: List[Dict],
        road_hierarchy: str,
        capacity_loss_percentage: float
    ) -> Dict:
        """
        Calculates the emergency access impact score.
        
        Args:
            all_pois: All POIs detected around the hotspot
            road_hierarchy: Road classification
            capacity_loss_percentage: Capacity loss from Road Impact Engine
            
        Returns:
            dict with:
                - emergency_impact_score: 0-100
                - emergency_priority: P1 (Critical) to P5 (Informational)
                - emergency_pois_affected: list of emergency POIs impacted
                - emergency_route_impact: whether this blocks a likely emergency route
        """
        emergency_pois = []
        raw_impact_sum = 0.0

        for poi in all_pois:
            poi_type = poi.get("poi_type", "")
            if poi_type not in EmergencyAccessEngine.EMERGENCY_POI_WEIGHTS:
                continue

            emergency_pois.append(poi)

            # Weight × distance factor
            weight = EmergencyAccessEngine.EMERGENCY_POI_WEIGHTS[poi_type]
            dist = poi.get("distance_m", 1000)
            dist_factor = EmergencyAccessEngine._distance_factor(dist)

            raw_impact_sum += weight * dist_factor

        # Road hierarchy factor: arterials are more likely emergency routes
        route_probability = EmergencyAccessEngine.EMERGENCY_ROUTE_PROBABILITY.get(
            road_hierarchy, 0.30
        )

        # Capacity loss factor: higher blockage = worse for emergency vehicles
        # Normalize to 0-1 range, with amplification above 50%
        capacity_factor = min(1.0, capacity_loss_percentage / 80.0)

        # Composite score: infrastructure proximity × route likelihood × blockage severity
        if raw_impact_sum > 0:
            # Logarithmic saturation for the infrastructure component
            infra_score = 100.0 * (1 - math.exp(-raw_impact_sum / 120.0))
        else:
            infra_score = 0.0

        # Final score: weighted combination
        score = (
            infra_score * 0.50 +
            route_probability * 100.0 * 0.25 +
            capacity_factor * 100.0 * 0.25
        )

        score = min(100.0, max(0.0, score))

        # Emergency route impact flag
        emergency_route_impact = (
            route_probability >= 0.70 and
            capacity_loss_percentage >= 40.0 and
            len(emergency_pois) > 0
        )

        # Priority classification (P1 = most urgent)
        if score >= 80:
            priority = "P1-Critical"
        elif score >= 60:
            priority = "P2-High"
        elif score >= 40:
            priority = "P3-Moderate"
        elif score >= 20:
            priority = "P4-Low"
        else:
            priority = "P5-Informational"

        return {
            "emergency_impact_score": round(score, 2),
            "emergency_priority": priority,
            "emergency_pois_affected": emergency_pois,
            "emergency_pois_count": len(emergency_pois),
            "emergency_route_impact": emergency_route_impact,
            "route_probability": round(route_probability, 2)
        }
