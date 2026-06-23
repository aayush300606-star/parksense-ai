class RoadGeometryEngine:
    """
    Generates deterministic spatial geometry representing the road segment.
    """
    
    @staticmethod
    def generate_geometry(lat: float, lon: float, radius_m: float) -> dict:
        """
        Creates a GeoJSON-compatible bounding box and pseudo-centerline 
        around the hotspot coordinate without any random variables.
        """
        # Roughly 1 degree of latitude is ~111,000 meters
        lat_offset = (radius_m / 111000.0)
        lon_offset = (radius_m / 111000.0) # Approximation, good enough for near equator/India
        
        bbox = [
            round(lon - lon_offset, 6),
            round(lat - lat_offset, 6),
            round(lon + lon_offset, 6),
            round(lat + lat_offset, 6)
        ]
        
        # Create a deterministic horizontal or vertical line based on coordinate parity
        # (This is just an algorithmic fallback since we don't have real map vectors)
        is_horizontal = int(lat * 1000) % 2 == 0
        
        if is_horizontal:
            line_coords = [
                [round(lon - lon_offset, 6), lat],
                [round(lon + lon_offset, 6), lat]
            ]
            direction = "East-West"
        else:
            line_coords = [
                [lon, round(lat - lat_offset, 6)],
                [lon, round(lat + lat_offset, 6)]
            ]
            direction = "North-South"

        return {
            "type": "Feature",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "geometry": {
                "type": "LineString",
                "coordinates": line_coords
            },
            "properties": {
                "bbox": bbox,
                "direction_metadata": direction,
                "road_segment_length_m": round(radius_m * 2, 2)
            }
        }
