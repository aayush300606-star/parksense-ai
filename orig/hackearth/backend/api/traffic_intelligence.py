from fastapi import APIRouter
from typing import List, Dict, Any
from ..services.traffic_intelligence_service import TrafficIntelligenceService

router = APIRouter(prefix="/api")


@router.get("/traffic-intelligence", response_model=List[Dict[str, Any]])
def get_all_traffic_intelligence():
    """
    Returns full Traffic Intelligence objects with speed, delay, congestion impact,
    and explainability for every hotspot.
    """
    return TrafficIntelligenceService.get_all_traffic()


@router.get("/speed-analysis")
def get_speed_analysis():
    """
    Returns speed reduction analysis: base speed vs current speed, severity.
    Optimized for speed heatmap and chart visualizations.
    """
    return TrafficIntelligenceService.get_speed_analysis()


@router.get("/delay-analysis")
def get_delay_analysis():
    """
    Returns delay estimation data: per-vehicle delay, annual vehicle-hours lost.
    Optimized for delay ranking tables and bar charts.
    """
    return TrafficIntelligenceService.get_delay_analysis()


@router.get("/congestion-impact")
def get_congestion_impact():
    """
    Returns Congestion Impact Scores (0-100) with severity classification.
    Optimized for the primary congestion dashboard widget.
    """
    return TrafficIntelligenceService.get_congestion_impact()


@router.get("/traffic-intelligence/{hotspot_id}")
def get_traffic_by_hotspot(hotspot_id: int):
    """
    Returns traffic intelligence for a specific hotspot.
    """
    all_traffic = TrafficIntelligenceService.get_all_traffic()
    for t in all_traffic:
        if t['hotspot_id'] == hotspot_id:
            return t
    return {"error": f"Hotspot {hotspot_id} not found in traffic intelligence."}
