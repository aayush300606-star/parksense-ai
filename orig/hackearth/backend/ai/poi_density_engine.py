from typing import Dict, List


class POIDensityEngine:
    """
    Calculates POI density metrics across the three analysis radii.
    
    Density scoring uses min-max normalization across all hotspots
    to produce a relative density score (0-100).
    
    Individual hotspot density is calculated as:
        Raw Density = weighted sum of POI counts per radius band
        (300m POIs weighted highest, 1000m POIs weighted lowest)
    """

    # Radius weights: closer POIs contribute more to density perception
    RADIUS_WEIGHTS = {
        300:  3.0,
        500:  2.0,
        1000: 1.0,
    }

    @staticmethod
    def calculate_density(
        poi_count_300m: int,
        poi_count_500m: int,
        poi_count_1000m: int
    ) -> Dict:
        """
        Calculates the weighted POI density for a single hotspot.
        This returns a raw weighted density — normalization happens at the service level.
        
        Args:
            poi_count_300m: Number of unique POIs within 300m
            poi_count_500m: Number of unique POIs within 500m
            poi_count_1000m: Number of unique POIs within 1000m
            
        Returns:
            dict with raw density metrics
        """
        weighted_density = (
            poi_count_300m * POIDensityEngine.RADIUS_WEIGHTS[300] +
            poi_count_500m * POIDensityEngine.RADIUS_WEIGHTS[500] +
            poi_count_1000m * POIDensityEngine.RADIUS_WEIGHTS[1000]
        )

        return {
            "poi_count_300m": poi_count_300m,
            "poi_count_500m": poi_count_500m,
            "poi_count_1000m": poi_count_1000m,
            "weighted_poi_density": round(weighted_density, 2)
        }

    @staticmethod
    def normalize_density_scores(all_densities: List[Dict]) -> List[Dict]:
        """
        Min-max normalizes the weighted densities across all hotspots
        to produce a 0-100 poi_density_score.
        
        Args:
            all_densities: List of density dicts from calculate_density()
            
        Returns:
            Updated list with poi_density_score and poi_density_level added
        """
        if not all_densities:
            return all_densities

        raw_values = [d["weighted_poi_density"] for d in all_densities]
        min_val = min(raw_values)
        max_val = max(raw_values)
        range_val = max_val - min_val if max_val > min_val else 1.0

        for d in all_densities:
            normalized = ((d["weighted_poi_density"] - min_val) / range_val) * 100.0
            d["poi_density_score"] = round(normalized, 2)

            # Level classification
            if normalized >= 75:
                d["poi_density_level"] = "Very High"
            elif normalized >= 50:
                d["poi_density_level"] = "High"
            elif normalized >= 25:
                d["poi_density_level"] = "Medium"
            else:
                d["poi_density_level"] = "Low"

        return all_densities
