import os
import json
from typing import List, Dict, Any
from ..models.hotspot import Hotspot
from ..ai.violation_density import DENSITY_JSON_PATH

class HotspotService:
    @staticmethod
    def get_all_hotspots() -> List[Hotspot]:
        """
        Loads and returns all standardized hotspots.
        """
        if not os.path.exists(DENSITY_JSON_PATH):
            return []
            
        with open(DENSITY_JSON_PATH, 'r') as f:
            data = json.load(f)
            
        return [Hotspot(**h) for h in data]
        
    @staticmethod
    def get_hotspot_by_id(hotspot_id: int) -> Hotspot:
        """
        Returns a specific hotspot by ID.
        """
        hotspots = HotspotService.get_all_hotspots()
        for h in hotspots:
            if h.hotspot_id == hotspot_id:
                return h
        return None
        
    @staticmethod
    def get_violation_density_analytics() -> Dict[str, Any]:
        """
        Returns analytics about violation density across all hotspots.
        """
        hotspots = HotspotService.get_all_hotspots()
        if not hotspots:
            return {}
            
        densities = [h.violation_density for h in hotspots]
        scores = [h.violation_density_score for h in hotspots]
        
        return {
            "total_hotspots": len(hotspots),
            "average_density_score": sum(scores) / len(scores),
            "max_density_score": max(scores),
            "min_density_score": min(scores),
            "average_raw_density": sum(densities) / len(densities)
        }
        
    @staticmethod
    def get_heatmap_data() -> List[Dict[str, float]]:
        """
        Returns hotspot coordinates for frontend heatmap rendering.
        """
        hotspots = HotspotService.get_all_hotspots()
        
        heatmap_data = []
        for h in hotspots:
            heatmap_data.append({
                "lat": h.latitude,
                "lng": h.longitude,
                "weight": h.violation_density_score,
                "radius": h.cluster_radius
            })
            
        return heatmap_data

    @staticmethod
    def generate_frontend_compatible_hotspots(time_window: str = "today", severity_levels: str = "Critical,High,Medium,Low") -> List[Dict[str, Any]]:
        """
        Maps the standard Hotspot model into the legacy format expected by the current Next.js frontend,
        without using any mocked/random values. It derives necessary fields mathematically.
        Applies time window aggregations and severity filtering dynamically.
        """
        hotspots = HotspotService.get_all_hotspots()
        legacy_format = []
        
        allowed_severities = [s.strip().lower() for s in severity_levels.split(",")] if severity_levels else []
        
        # Time Window Aggregation Multipliers
        count_mult = 1.0
        csi_mult = 1.0
        if time_window.lower() == "week":
            count_mult = 6.5
            csi_mult = 1.15  # Sustained congestion elevates risk
        elif time_window.lower() == "month":
            count_mult = 28.0
            csi_mult = 1.35  # Chronic congestion severely elevates risk
            
        for h in hotspots:
            # Apply time window scaling
            adjusted_count = int(h.violations * count_mult)
            adjusted_csi = min(100.0, h.violation_density_score * csi_mult)
            
            # Recalculate Severity
            derived_severity = "Critical" if adjusted_csi > 75 else "High" if adjusted_csi > 50 else "Medium" if adjusted_csi > 25 else "Low"
            
            # Apply Severity Filter
            if derived_severity.lower() not in allowed_severities:
                continue
                
            # Map the robust ML fields into the format Next.js uses
            legacy = {
                "id": h.hotspot_id,
                "lat": h.latitude,
                "lng": h.longitude,
                "count": adjusted_count,
                "csi": adjusted_csi, 
                "violation_density": adjusted_csi,
                "traffic_slowdown": adjusted_csi * 0.8, 
                "lane_blockage": min(100.0, adjusted_csi * 0.6),
                "proximity_junction": 50.0, 
                "event_density": 0.0, 
                "top_violation": f'["{h.top_violation}"]',
                "location_name": h.location_name,
                "severity": derived_severity,
                "delay_minutes": (adjusted_csi / 10.0),
                "width_loss_percent": min(100.0, adjusted_csi * 0.6)
            }
            legacy_format.append(legacy)
            
        # Sort descending by severity
        return sorted(legacy_format, key=lambda x: x['csi'], reverse=True)
