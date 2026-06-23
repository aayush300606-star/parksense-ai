import os
import json
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from .preprocessing import CLEANED_DATA_PATH

HOTSPOTS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'hotspots.json')

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def detect_hotspots(df=None):
    """
    Detect spatial clusters using DBSCAN and calculate real area/radius metrics.
    """
    if df is None:
        print(f"Loading cleaned dataset from {CLEANED_DATA_PATH}...")
        df = pd.read_csv(CLEANED_DATA_PATH)
    
    # We might need to sample if the dataset is massive, otherwise DBSCAN is O(n^2)
    # If len is > 50000, take a random sample for DBSCAN for performance
    sample_df = df.sample(n=min(50000, len(df)), random_state=42) if len(df) > 50000 else df
    
    print("Extracting coordinates for clustering...")
    # DBSCAN using haversine metric requires radians
    coords = np.radians(sample_df[['latitude', 'longitude']].values)
    
    print("Running DBSCAN algorithm...")
    # eps = 300 meters = 0.3 km. In radians: 0.3 / 6371 = 0.000047
    kms_per_radian = 6371.0088
    eps = 0.3 / kms_per_radian 
    
    db = DBSCAN(eps=eps, min_samples=30, algorithm='ball_tree', metric='haversine').fit(coords)
    sample_df['cluster_id'] = db.labels_
    
    # Filter out noise
    clusters = sample_df[sample_df['cluster_id'] != -1]
    print(f"Detected {len(clusters['cluster_id'].unique())} valid clusters.")
    
    hotspots = []
    
    for cluster_id, group in clusters.groupby('cluster_id'):
        center_lat = group['latitude'].mean()
        center_lon = group['longitude'].mean()
        num_violations = len(group)
        
        # Aggregate vehicle types for the new occupancy engine
        vehicle_types = {}
        if 'vehicle_type' in group.columns:
            # Group by vehicle type and count
            vc = group['vehicle_type'].value_counts()
            for v_type, count in vc.items():
                if pd.notna(v_type):
                    vehicle_types[str(v_type).strip().upper()] = int(count)

        # Calculate cluster radius in meters (max distance from center to any point in cluster)
        distances = []
        for _, row in group.iterrows():
            dist = haversine_distance(center_lat, center_lon, row['latitude'], row['longitude'])
            distances.append(dist)
            
        radius_km = max(distances) if distances else 0.0
        # Give a minimum radius of 50 meters (0.05 km) to avoid 0 area for tight clusters
        radius_km = max(radius_km, 0.05) 
        
        cluster_radius_m = radius_km * 1000
        cluster_area_sqm = np.pi * (cluster_radius_m ** 2)
        
        # Density (violations per square meter)
        density = num_violations / cluster_area_sqm
        
        hotspot = {
            'cluster_id': int(cluster_id),
            'cluster_center_lat': float(center_lat),
            'cluster_center_lon': float(center_lon),
            'number_of_violations': int(num_violations),
            'cluster_radius': float(cluster_radius_m),
            'cluster_area': float(cluster_area_sqm),
            'density': float(density),
            'location_name': str(group['location'].mode().iloc[0] if 'location' in group.columns and not group['location'].empty and pd.notna(group['location'].mode().iloc[0]) else 'Unknown Area'),
            'top_violation': str(group['violation_type'].mode().iloc[0] if 'violation_type' in group.columns and not group['violation_type'].empty else 'Unknown'),
            'vehicle_types': vehicle_types
        }
        hotspots.append(hotspot)
        
    print(f"Saving {len(hotspots)} hotspots to {HOTSPOTS_JSON_PATH}")
    os.makedirs(os.path.dirname(HOTSPOTS_JSON_PATH), exist_ok=True)
    with open(HOTSPOTS_JSON_PATH, 'w') as f:
        json.dump(hotspots, f, indent=2)
        
    return hotspots

if __name__ == '__main__':
    detect_hotspots()
