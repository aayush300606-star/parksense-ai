import os
import json
import numpy as np
from datetime import datetime

HOTSPOTS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'hotspots.json')
DENSITY_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'hotspots_with_density.json')

def calculate_violation_density(hotspots=None):
    """
    Calculates normalized violation density score (0-100) for all hotspots.
    """
    if hotspots is None:
        if not os.path.exists(HOTSPOTS_JSON_PATH):
            print("No hotspots data found. Please run hotspot_detection.py first.")
            return []
        with open(HOTSPOTS_JSON_PATH, 'r') as f:
            hotspots = json.load(f)
            
    if not hotspots:
        return []
        
    # Extract raw densities
    raw_densities = [h['density'] for h in hotspots]
    min_density = min(raw_densities)
    max_density = max(raw_densities)
    
    # Avoid division by zero
    range_density = max_density - min_density if max_density > min_density else 1.0
    
    processed_hotspots = []
    
    for h in hotspots:
        raw_density = h['density']
        
        # Min-Max Normalization to 0-100 scale
        normalized_score = ((raw_density - min_density) / range_density) * 100.0
        
        # Format the standardized hotspot object
        standardized_hotspot = {
            "hotspot_id": h['cluster_id'],
            "latitude": h['cluster_center_lat'],
            "longitude": h['cluster_center_lon'],
            "cluster_radius": h['cluster_radius'],
            "violations": h['number_of_violations'],
            "cluster_area": h['cluster_area'],
            "violation_density": raw_density,
            "violation_density_score": normalized_score,
            "created_at": datetime.now().isoformat(),
            # Legacy fields to keep frontend backwards compatible
            "location_name": h.get('location_name', 'Unknown'),
            "top_violation": h.get('top_violation', 'Unknown'),
            # New Field for Effective Width Engine
            "vehicle_types": h.get('vehicle_types', {})
        }
        processed_hotspots.append(standardized_hotspot)
        
    print(f"Saving {len(processed_hotspots)} density-scored hotspots to {DENSITY_JSON_PATH}")
    os.makedirs(os.path.dirname(DENSITY_JSON_PATH), exist_ok=True)
    with open(DENSITY_JSON_PATH, 'w') as f:
        json.dump(processed_hotspots, f, indent=2)
        
    return processed_hotspots

if __name__ == '__main__':
    calculate_violation_density()
