from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from ..services.csi_service import CSIService

router = APIRouter(prefix="/api")


@router.get("/csi", response_model=List[Dict[str, Any]])
def get_all_csi():
    """
    Returns full Adaptive CSI™ intelligence for all hotspots,
    ordered by rank (highest severity first).
    Includes: CSI score, level, color, adaptive weights, contribution analysis,
    enforcement priority, expected benefits, ranking, and explainability.
    """
    return CSIService.get_all_csi()


@router.get("/csi-summary")
def get_csi_summary():
    """
    Returns city-wide CSI™ summary analytics:
    severity distributions, dominant factor analysis, adaptive weighting stats,
    annual delay totals, and top-5 worst hotspots.
    """
    return CSIService.get_summary()


@router.get("/priority-ranking")
def get_priority_ranking(top: Optional[int] = Query(None, description="Return only top N hotspots")):
    """
    Returns enforcement priority rankings with expected capacity recovery
    and speed improvement projections. Supports ?top=N for top-N filtering.
    """
    return CSIService.get_rankings(top=top)


@router.get("/top-critical-hotspots")
def get_top_critical():
    """
    Returns the most critical hotspots (CSI >= 60 or top 20)
    with full intelligence for focused enforcement planning.
    """
    return CSIService.get_top_critical()


@router.get("/top-high-impact-roads")
def get_top_roads():
    """
    Returns roads ranked by aggregate parking impact:
    hotspot count, average/max CSI, total annual delay per road.
    """
    return CSIService.get_top_roads()


@router.get("/csi-heatmap-layer")
def get_heatmap_layer():
    """
    Lightweight heatmap layer data for frontend map rendering.
    Returns lat/lng/weight/color for each hotspot.
    """
    return CSIService.get_heatmap_layer()


@router.get("/csi-priority-layer")
def get_priority_layer():
    """
    Lightweight priority marker layer for frontend map rendering.
    Returns lat/lng/priority/color/expected_recovery for each hotspot.
    """
    return CSIService.get_priority_layer()


@router.get("/temporal-patterns")
def get_temporal_patterns():
    """
    Returns temporal violation patterns: hourly/daily distributions,
    peak hours, recurrence scores for all hotspots.
    """
    return CSIService.get_temporal_patterns()


# Backward compatibility endpoints
@router.get("/csi-rankings")
def get_csi_rankings(top: Optional[int] = Query(None)):
    """Legacy endpoint — redirects to priority-ranking."""
    return CSIService.get_rankings(top=top)


@router.get("/pis")
def get_pis():
    """
    Returns Parking Impact Scores with enforcement priorities
    and expected benefit projections.
    """
    return CSIService.get_pis()


@router.get("/city-analytics")
def get_city_analytics():
    """Legacy endpoint — returns CSI summary analytics."""
    return CSIService.get_summary()


@router.get("/csi/{hotspot_id}")
def get_csi_by_hotspot(hotspot_id: int):
    """Returns full Adaptive CSI™ intelligence for a specific hotspot."""
    all_csi = CSIService.get_all_csi()
    for c in all_csi:
        if c['hotspot_id'] == hotspot_id:
            return c
    return {"error": f"Hotspot {hotspot_id} not found in CSI intelligence."}
