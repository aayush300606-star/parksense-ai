from typing import Dict, List


class HotspotRankingEngine:
    """
    Produces a unified city-wide ranking of hotspots by CSI and PIS.
    
    Features:
        - Overall ranking by CSI (primary) and PIS (secondary)
        - Percentile classification
        - Category-filtered rankings (road hierarchy, emergency priority)
        - Top-N extraction
    """

    @staticmethod
    def generate_rankings(csi_data: List[Dict]) -> List[Dict]:
        """
        Ranks all hotspots by CSI score and adds percentile/rank metadata.
        
        Args:
            csi_data: List of dicts with at least csi_score, priority_score, hotspot_id
            
        Returns:
            Sorted list with rank, percentile, and tier added
        """
        if not csi_data:
            return []

        # Sort by CSI descending, then Priority descending for ties
        sorted_data = sorted(
            csi_data,
            key=lambda x: (x.get('csi_score', 0), x.get('priority_score', 0)),
            reverse=True
        )

        total = len(sorted_data)

        for i, item in enumerate(sorted_data):
            rank = i + 1
            # Percentile: what % of hotspots score LOWER than this one
            percentile = ((total - rank) / total) * 100.0

            item['rank'] = rank
            item['percentile'] = round(percentile, 1)

            # Tier classification
            if percentile >= 90:
                item['tier'] = "Top 10%"
            elif percentile >= 75:
                item['tier'] = "Top 25%"
            elif percentile >= 50:
                item['tier'] = "Top 50%"
            elif percentile >= 25:
                item['tier'] = "Bottom 50%"
            else:
                item['tier'] = "Bottom 25%"

        return sorted_data

    @staticmethod
    def get_top_n(ranked_data: List[Dict], n: int = 10) -> List[Dict]:
        """Returns top N hotspots by CSI rank."""
        return ranked_data[:min(n, len(ranked_data))]

    @staticmethod
    def filter_by_priority(ranked_data: List[Dict], priority: str) -> List[Dict]:
        """Filters ranked hotspots by priority level."""
        return [d for d in ranked_data if d.get('priority_level') == priority]

    @staticmethod
    def filter_by_hierarchy(ranked_data: List[Dict], hierarchy: str) -> List[Dict]:
        """Filters ranked hotspots by road hierarchy."""
        return [d for d in ranked_data if d.get('road_hierarchy') == hierarchy]

    @staticmethod
    def generate_city_analytics(ranked_data: List[Dict]) -> Dict:
        """
        Produces city-wide aggregate statistics from ranked CSI data.
        
        Returns a comprehensive analytics object for dashboard rendering.
        """
        if not ranked_data:
            return {}

        total = len(ranked_data)
        csi_scores = [d['csi_score'] for d in ranked_data]
        priority_scores = [d['priority_score'] for d in ranked_data]

        # CSI distribution
        csi_severity_dist = {}
        for d in ranked_data:
            s = d.get('csi_severity', 'Unknown')
            csi_severity_dist[s] = csi_severity_dist.get(s, 0) + 1

        # Priority distribution
        priority_dist = {}
        for d in ranked_data:
            p = d.get('priority_level', 'Unknown')
            priority_dist[p] = priority_dist.get(p, 0) + 1

        # Road hierarchy distribution
        hierarchy_dist = {}
        for d in ranked_data:
            h = d.get('road_hierarchy', 'Unknown')
            if h not in hierarchy_dist:
                hierarchy_dist[h] = {"count": 0, "avg_csi": 0, "total_csi": 0}
            hierarchy_dist[h]["count"] += 1
            hierarchy_dist[h]["total_csi"] += d['csi_score']
        for h in hierarchy_dist:
            hierarchy_dist[h]["avg_csi"] = round(
                hierarchy_dist[h]["total_csi"] / hierarchy_dist[h]["count"], 2
            )
            del hierarchy_dist[h]["total_csi"]

        # Annual impact
        total_annual_delay = sum(d.get('annual_delay_vehicle_hours', 0) for d in ranked_data)

        # Emergency hotspots
        emergency_count = sum(
            1 for d in ranked_data
            if d.get('emergency_route_impact', False)
        )

        return {
            "total_hotspots_analyzed": total,
            "csi_statistics": {
                "mean": round(sum(csi_scores) / total, 2),
                "median": round(sorted(csi_scores)[total // 2], 2),
                "min": round(min(csi_scores), 2),
                "max": round(max(csi_scores), 2),
                "std_dev": round(
                    (sum((x - sum(csi_scores)/total)**2 for x in csi_scores) / total) ** 0.5, 2
                ),
            },
            "priority_statistics": {
                "mean": round(sum(priority_scores) / total, 2),
                "median": round(sorted(priority_scores)[total // 2], 2),
                "min": round(min(priority_scores), 2),
                "max": round(max(priority_scores), 2),
            },
            "csi_severity_distribution": csi_severity_dist,
            "priority_distribution": priority_dist,
            "road_hierarchy_analysis": hierarchy_dist,
            "total_annual_delay_vehicle_hours": round(total_annual_delay, 0),
            "emergency_route_hotspots": emergency_count,
            "top_5_worst_hotspots": [
                {
                    "rank": d['rank'],
                    "hotspot_id": d['hotspot_id'],
                    "road_name": d['road_name'],
                    "csi_score": d['csi_score'],
                    "priority_level": d['priority_level'],
                }
                for d in ranked_data[:5]
            ],
        }
