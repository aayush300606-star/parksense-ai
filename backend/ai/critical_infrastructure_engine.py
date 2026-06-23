from typing import Dict, List


class CriticalInfrastructureEngine:
    """
    Identifies and scores critical infrastructure near hotspots.
    
    Critical infrastructure categories:
        1. Emergency Medical (Hospitals, Clinics)
        2. Emergency Services (Police, Fire)
        3. Transit Hubs (Metro, Bus, Railway)
        4. Government (Courts, Offices)
    
    Scoring:
        Each category has a base weight reflecting its criticality.
        Proximity amplifies the score (closer = more critical).
        Multiple critical POIs compound the score.
    """

    # Category weights (how critical each type is)
    CATEGORY_WEIGHTS = {
        "HOSPITAL":          100,
        "FIRE_STATION":       95,
        "POLICE_STATION":     85,
        "METRO_STATION":      80,
        "RAILWAY_STATION":    80,
        "BUS_STATION":        70,
        "GOVERNMENT_OFFICE":  60,
        "TRANSIT_HUB":        70,
        "SCHOOL":             65,
        "COLLEGE":            55,
    }

    # Critical types (subset that constitutes "critical infrastructure")
    CRITICAL_TYPES = {
        "HOSPITAL", "FIRE_STATION", "POLICE_STATION",
        "METRO_STATION", "RAILWAY_STATION", "BUS_STATION",
        "GOVERNMENT_OFFICE", "TRANSIT_HUB"
    }

    # Proximity multiplier: closer POIs have more impact
    PROXIMITY_MULTIPLIER = {
        300:  1.0,   # Within 300m — full impact
        500:  0.70,  # Within 500m — moderate impact
        1000: 0.40,  # Within 1000m — lower impact
    }

    @staticmethod
    def calculate_critical_infrastructure(all_pois: List[Dict]) -> Dict:
        """
        Scores the critical infrastructure density around a hotspot.
        
        Args:
            all_pois: List of POI dicts from POIIntelligenceEngine
            
        Returns:
            dict with:
                - critical_infrastructure_score: 0-100
                - critical_infrastructure_level: categorical
                - critical_pois: list of identified critical POIs
                - critical_poi_count: number of critical infrastructure POIs
        """
        critical_pois = []
        weighted_score_sum = 0.0
        max_possible = 0.0

        for poi in all_pois:
            poi_type = poi.get("poi_type", "")
            if poi_type not in CriticalInfrastructureEngine.CRITICAL_TYPES:
                continue

            critical_pois.append(poi)

            # Get category weight
            weight = CriticalInfrastructureEngine.CATEGORY_WEIGHTS.get(poi_type, 50)

            # Get proximity multiplier
            radius_band = poi.get("radius_band", 1000)
            proximity = CriticalInfrastructureEngine.PROXIMITY_MULTIPLIER.get(radius_band, 0.40)

            weighted_score_sum += weight * proximity

        # Normalize: a single hospital within 300m scores ~60.
        # Multiple critical POIs can push toward 100.
        # Use logarithmic saturation to prevent unbounded growth
        if weighted_score_sum > 0:
            import math
            # log curve: 100 * (1 - e^(-sum/150))
            # At sum=150, score ≈ 63. At sum=300, score ≈ 86. At sum=500, score ≈ 96.
            score = 100.0 * (1 - math.exp(-weighted_score_sum / 150.0))
        else:
            score = 0.0

        score = min(100.0, max(0.0, score))

        # Severity level
        if score >= 80:
            level = "Critical"
        elif score >= 60:
            level = "High"
        elif score >= 40:
            level = "Moderate"
        elif score >= 20:
            level = "Low"
        else:
            level = "Minimal"

        return {
            "critical_infrastructure_score": round(score, 2),
            "critical_infrastructure_level": level,
            "critical_pois": critical_pois,
            "critical_poi_count": len(critical_pois)
        }
