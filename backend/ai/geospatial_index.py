import numpy as np
from scipy.spatial import KDTree
from typing import List, Dict, Tuple, Optional


class GeospatialIndex:
    """
    KDTree-based spatial index for O(log n) radius and nearest-neighbor queries.
    
    Converts WGS84 lat/lon to a local flat-earth approximation in meters
    centered on the dataset centroid, then builds a KDTree for fast spatial lookups.
    
    This index is reused by:
        - Junction Intelligence Engine
        - POI Intelligence Engine
        - Future Digital Twin
        - Future Prediction Engine
        - Future Routing Engine
    """

    # Earth radius in meters
    EARTH_RADIUS_M = 6_371_000.0

    def __init__(self, hotspots: List[Dict]):
        """
        Build the spatial index from a list of hotspot dicts.
        Each hotspot must have 'latitude' and 'longitude' keys.
        """
        self._hotspots = hotspots
        self._lats = np.array([h['latitude'] for h in hotspots])
        self._lons = np.array([h['longitude'] for h in hotspots])

        # Compute centroid for flat-earth projection
        self._center_lat = np.mean(self._lats)
        self._center_lon = np.mean(self._lons)

        # Convert all hotspot coords to local meters
        self._coords_m = np.array([
            self._to_local_meters(lat, lon)
            for lat, lon in zip(self._lats, self._lons)
        ])

        # Build KDTree
        self._tree = KDTree(self._coords_m)

    def _to_local_meters(self, lat: float, lon: float) -> Tuple[float, float]:
        """
        Convert WGS84 lat/lon to flat-earth meters relative to the dataset centroid.
        Uses equirectangular approximation — accurate within ~100km of centroid.
        """
        dlat = np.radians(lat - self._center_lat)
        dlon = np.radians(lon - self._center_lon)
        cos_center = np.cos(np.radians(self._center_lat))

        x = dlon * cos_center * self.EARTH_RADIUS_M
        y = dlat * self.EARTH_RADIUS_M
        return (x, y)

    def query_radius(self, lat: float, lon: float, radius_m: float) -> List[Dict]:
        """
        Returns all hotspots within `radius_m` meters of (lat, lon).
        
        Each result dict contains:
            - hotspot: The original hotspot dict
            - distance_m: Distance in meters from query point
            - index: Index in the original hotspot list
        """
        point = self._to_local_meters(lat, lon)
        indices = self._tree.query_ball_point(point, r=radius_m)

        results = []
        for idx in indices:
            dist = np.sqrt(
                (self._coords_m[idx][0] - point[0]) ** 2 +
                (self._coords_m[idx][1] - point[1]) ** 2
            )
            results.append({
                "hotspot": self._hotspots[idx],
                "distance_m": round(float(dist), 2),
                "index": idx
            })

        results.sort(key=lambda r: r['distance_m'])
        return results

    def query_nearest(self, lat: float, lon: float, k: int = 5) -> List[Dict]:
        """
        Returns the k nearest hotspots to (lat, lon).
        """
        point = self._to_local_meters(lat, lon)
        k = min(k, len(self._hotspots))
        distances, indices = self._tree.query(point, k=k)

        # Handle single result (k=1 returns scalar)
        if k == 1:
            distances = [distances]
            indices = [indices]

        results = []
        for dist, idx in zip(distances, indices):
            results.append({
                "hotspot": self._hotspots[int(idx)],
                "distance_m": round(float(dist), 2),
                "index": int(idx)
            })

        return results

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Precise great-circle distance between two WGS84 points in meters.
        """
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        return float(GeospatialIndex.EARTH_RADIUS_M * c)

    def get_hotspot_count(self) -> int:
        return len(self._hotspots)

    def get_centroid(self) -> Tuple[float, float]:
        return (self._center_lat, self._center_lon)
