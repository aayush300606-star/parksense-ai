import os
import json
from typing import Dict, Any

CONTEXT_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'context.json')

class HotspotSegmentationEngine:
    """
    Classifies a hotspot into an operational Archetype based on its geospatial Context Intelligence.
    A hotspot surrounded by hospitals behaves differently than one surrounded by pubs.
    """

    @staticmethod
    def classify_archetype(hotspot_id: int) -> Dict[str, Any]:
        if not os.path.exists(CONTEXT_JSON_PATH):
            return {"error": "Context data missing"}
            
        with open(CONTEXT_JSON_PATH, 'r') as f:
            context_data = json.load(f)
            
        target = next((c for c in context_data if c['hotspot_id'] == hotspot_id), None)
        if not target:
            return {"archetype": "Residential/Mixed-Use", "confidence": 0.5}
            
        # Analyze POI density to classify archetype deterministically
        poi_counts = target.get('nearby_poi_counts', {})
        
        archetype = "Mixed-Use"
        confidence = 0.6
        
        # Dominant Archetype Logic
        if poi_counts.get('transit', 0) > 0:
            archetype = "Metro-Oriented"
            confidence = 0.95
        elif poi_counts.get('school', 0) > 0:
            archetype = "School-Oriented"
            confidence = 0.90
        elif poi_counts.get('hospital', 0) > 0:
            archetype = "Hospital-Oriented"
            confidence = 0.98
        elif poi_counts.get('commercial', 0) > 5:
            archetype = "Commercial/Retail"
            confidence = 0.85
        elif poi_counts.get('restaurant', 0) > 5:
            archetype = "Nightlife/Dining"
            confidence = 0.80
            
        return {
            "hotspot_id": hotspot_id,
            "archetype": archetype,
            "archetype_confidence": confidence,
            "context_drivers": poi_counts
        }
