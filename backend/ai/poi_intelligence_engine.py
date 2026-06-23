import os
import re
import requests
from typing import Dict, List, Optional


class POIIntelligenceEngine:
    """
    Multi-radius Point of Interest discovery around each hotspot.
    
    Searches at 300m, 500m, and 1000m radii.
    
    Strategy 1: MapMyIndia Nearby Search API (when API key available)
    Strategy 2: Deterministic extraction from location names and
                nearby hotspot location contexts via KDTree.
    
    POI Categories:
        HOSPITAL, SCHOOL, COLLEGE, METRO_STATION, BUS_STATION,
        RAILWAY_STATION, MARKET, MALL, GOVERNMENT_OFFICE,
        POLICE_STATION, FIRE_STATION, INDUSTRIAL_AREA,
        BUSINESS_DISTRICT, RELIGIOUS_PLACE, PARK, TRANSIT_HUB
    """

    SEARCH_RADII = [300, 500, 1000]

    # Keyword patterns for deterministic POI extraction from Indian location names
    POI_KEYWORD_MAP = {
        "HOSPITAL": [
            "hospital", "medical", "clinic", "health centre", "nursing home",
            "trauma centre", "icu"
        ],
        "SCHOOL": [
            "school", "vidyalaya", "academy", "convent", "public school"
        ],
        "COLLEGE": [
            "college", "university", "institute", "iit", "iim", "iisc",
            "polytechnic", "engineering"
        ],
        "METRO_STATION": [
            "metro", "metro station", "namma metro"
        ],
        "BUS_STATION": [
            "bus stand", "bus station", "bus stop", "bmtc", "ksrtc",
            "bus terminal", "majestic"
        ],
        "RAILWAY_STATION": [
            "railway", "railway station", "train station", "rail",
            "cantonment"
        ],
        "MARKET": [
            "market", "bazaar", "bazar", "mandi", "commercial street",
            "avenue road", "chickpet", "gandhi bazaar", "malleswaram market"
        ],
        "MALL": [
            "mall", "forum", "orion", "phoenix", "garuda", "mantri",
            "brigade gateway", "central", "inorbit", "total mall",
            "gopalan", "lulu"
        ],
        "GOVERNMENT_OFFICE": [
            "government", "govt", "vidhana soudha", "municipal",
            "bbmp", "bda", "taluk office", "tahsildar", "sub-registrar",
            "court", "collectorate", "secretariat"
        ],
        "POLICE_STATION": [
            "police", "police station", "thana"
        ],
        "FIRE_STATION": [
            "fire station", "fire brigade", "fire department"
        ],
        "INDUSTRIAL_AREA": [
            "industrial", "factory", "manufacturing", "industrial area",
            "industrial layout", "industrial estate", "peenya"
        ],
        "BUSINESS_DISTRICT": [
            "tech park", "it park", "software", "business park",
            "electronic city", "whitefield", "manyata", "embassy",
            "bagmane", "ecospace", "prestige tech", "rmz"
        ],
        "RELIGIOUS_PLACE": [
            "temple", "church", "mosque", "masjid", "gurudwara",
            "dargah", "ashram", "math", "mandir"
        ],
        "PARK": [
            "park", "garden", "lalbagh", "cubbon", "botanical",
            "playground", "stadium"
        ],
        "TRANSIT_HUB": [
            "interchange", "terminal", "hub", "depot", "stand"
        ],
    }

    # MapMyIndia category keywords for API search
    MAPMYINDIA_CATEGORIES = {
        "HOSPITAL": "hospital clinic nursing",
        "SCHOOL": "school academy",
        "COLLEGE": "college university institute",
        "METRO_STATION": "metro station",
        "BUS_STATION": "bus stand station terminal",
        "RAILWAY_STATION": "railway station",
        "MARKET": "market bazaar",
        "MALL": "mall shopping",
        "GOVERNMENT_OFFICE": "government office court",
        "POLICE_STATION": "police station",
        "FIRE_STATION": "fire station",
    }

    @staticmethod
    def discover_pois(
        hotspot_id: int,
        latitude: float,
        longitude: float,
        location_name: str,
        nearby_hotspot_locations: List[Dict] = None
    ) -> Dict:
        """
        Discovers POIs around a hotspot at multiple radii.
        
        Args:
            hotspot_id: Hotspot identifier
            latitude: Hotspot latitude
            longitude: Hotspot longitude
            location_name: Full location string
            nearby_hotspot_locations: List of dicts with 'location_name' and 'distance_m'
                                     from the geospatial index
                                     
        Returns:
            dict with POIs organized by radius band
        """
        # Strategy 1: Try MapMyIndia
        api_pois = POIIntelligenceEngine._try_mapmyindia(latitude, longitude)

        # Strategy 2: Deterministic analysis
        deterministic_pois = POIIntelligenceEngine._deterministic_discovery(
            hotspot_id, latitude, longitude, location_name, nearby_hotspot_locations
        )

        # Merge: API results take priority, deterministic fills gaps
        if api_pois:
            all_pois = api_pois + deterministic_pois
        else:
            all_pois = deterministic_pois

        # Deduplicate by type+radius_band
        seen = set()
        unique_pois = []
        for poi in all_pois:
            key = (poi["poi_type"], poi["radius_band"])
            if key not in seen:
                seen.add(key)
                unique_pois.append(poi)

        # Organize by radius
        pois_300m = [p for p in unique_pois if p["radius_band"] == 300]
        pois_500m = [p for p in unique_pois if p["radius_band"] <= 500]
        pois_1000m = [p for p in unique_pois if p["radius_band"] <= 1000]

        return {
            "hotspot_id": hotspot_id,
            "pois_300m": pois_300m,
            "pois_500m": pois_500m,
            "pois_1000m": pois_1000m,
            "poi_count_300m": len(pois_300m),
            "poi_count_500m": len(pois_500m),
            "poi_count_1000m": len(pois_1000m),
            "total_unique_pois": len(unique_pois),
            "all_pois": unique_pois,
            "source": "MapMyIndia API + Deterministic" if api_pois else "Deterministic Geospatial Analysis"
        }

    @staticmethod
    def _try_mapmyindia(lat: float, lon: float) -> List[Dict]:
        """Attempts POI discovery via MapMyIndia Nearby Search API."""
        api_key = os.environ.get("MAPMYINDIA_API_KEY")
        if not api_key:
            return []

        pois = []
        try:
            for poi_type, keywords in POIIntelligenceEngine.MAPMYINDIA_CATEGORIES.items():
                response = requests.get(
                    "https://atlas.mappls.com/api/places/nearby/json",
                    params={
                        "keywords": keywords,
                        "refLocation": f"{lat},{lon}",
                        "radius": 1000,
                        "sortBy": "dist:asc",
                        "page": 1,
                    },
                    headers={"Authorization": f"bearer {api_key}"},
                    timeout=3
                )
                if response.status_code == 200:
                    data = response.json()
                    for loc in data.get("suggestedLocations", [])[:3]:
                        dist_m = float(loc.get("distance", 0)) * 1000
                        radius_band = 300 if dist_m <= 300 else (500 if dist_m <= 500 else 1000)
                        if dist_m <= 1000:
                            pois.append({
                                "poi_type": poi_type,
                                "poi_name": loc.get("placeName", poi_type),
                                "distance_m": round(dist_m, 2),
                                "radius_band": radius_band,
                                "latitude": float(loc.get("latitude", lat)),
                                "longitude": float(loc.get("longitude", lon)),
                                "source": "MapMyIndia API",
                                "confidence": 0.95
                            })
        except Exception as e:
            print(f"MapMyIndia POI query failed: {e}")

        return pois

    @staticmethod
    def _deterministic_discovery(
        hotspot_id: int,
        latitude: float,
        longitude: float,
        location_name: str,
        nearby_hotspot_locations: List[Dict] = None
    ) -> List[Dict]:
        """
        Deterministic POI detection from location name keywords.
        Analyzes both the hotspot's own location name and nearby hotspot locations.
        """
        pois = []

        # Analyze the hotspot's own location name (these POIs are closest)
        own_pois = POIIntelligenceEngine._extract_pois_from_text(
            location_name, distance_m=0.0, radius_band=300
        )
        pois.extend(own_pois)

        # Analyze nearby hotspot locations at their actual distances
        if nearby_hotspot_locations:
            for nearby in nearby_hotspot_locations:
                nearby_loc = nearby.get("location_name", "")
                nearby_dist = nearby.get("distance_m", 0)

                if nearby_dist <= 0 or not nearby_loc:
                    continue

                radius_band = 300 if nearby_dist <= 300 else (500 if nearby_dist <= 500 else 1000)

                if nearby_dist <= 1000:
                    nearby_pois = POIIntelligenceEngine._extract_pois_from_text(
                        nearby_loc, distance_m=nearby_dist, radius_band=radius_band
                    )
                    pois.extend(nearby_pois)

        return pois

    @staticmethod
    def _extract_pois_from_text(
        text: str,
        distance_m: float,
        radius_band: int
    ) -> List[Dict]:
        """
        Extracts POI types from a text string using keyword matching.
        """
        text_lower = str(text).lower()
        found_pois = []

        for poi_type, keywords in POIIntelligenceEngine.POI_KEYWORD_MAP.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Extract POI name from the text (use the keyword context)
                    poi_name = POIIntelligenceEngine._extract_poi_name(text, keyword)

                    found_pois.append({
                        "poi_type": poi_type,
                        "poi_name": poi_name,
                        "distance_m": round(distance_m, 2),
                        "radius_band": radius_band,
                        "latitude": 0.0,  # Not available from text
                        "longitude": 0.0,
                        "source": "Deterministic Geospatial Analysis",
                        "confidence": 0.80 if distance_m == 0 else 0.70
                    })
                    break  # Only one match per category per text

        return found_pois

    @staticmethod
    def _extract_poi_name(text: str, keyword: str) -> str:
        """
        Extracts a readable POI name from the location text near the keyword.
        """
        parts = str(text).split(",")
        for part in parts:
            if keyword.lower() in part.lower():
                return part.strip()
        return keyword.title()
