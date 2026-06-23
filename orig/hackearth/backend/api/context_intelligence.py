from fastapi import APIRouter
from typing import List, Dict, Any
from ..services.context_intelligence_service import ContextIntelligenceService

router = APIRouter(prefix="/api")


@router.get("/junction-intelligence", response_model=List[Dict[str, Any]])
def get_junction_intelligence():
    """
    Returns junction intelligence for all hotspots:
    junction type, distance, importance, influence scores.
    """
    return ContextIntelligenceService.get_junction_intelligence()


@router.get("/poi-intelligence", response_model=List[Dict[str, Any]])
def get_poi_intelligence():
    """
    Returns multi-radius POI intelligence for all hotspots:
    POI counts at 300m/500m/1000m, identified POIs with types and distances.
    """
    return ContextIntelligenceService.get_poi_intelligence()


@router.get("/context-intelligence", response_model=List[Dict[str, Any]])
def get_context_intelligence():
    """
    Returns full context intelligence objects with junction, POI, infrastructure,
    emergency, and aggregate context importance for every hotspot.
    """
    return ContextIntelligenceService.get_all_context()


@router.get("/emergency-impact", response_model=List[Dict[str, Any]])
def get_emergency_impact():
    """
    Returns emergency access impact analysis for all hotspots:
    emergency scores, priorities (P1-P5), and route impact flags.
    """
    return ContextIntelligenceService.get_emergency_impact()


@router.get("/context-summary")
def get_context_summary():
    """
    Returns aggregate context intelligence statistics:
    distribution of importance levels, emergency priorities,
    and critical infrastructure counts.
    """
    return ContextIntelligenceService.get_context_summary()


@router.get("/context-intelligence/{hotspot_id}")
def get_context_by_hotspot(hotspot_id: int):
    """
    Returns context intelligence for a specific hotspot.
    """
    all_context = ContextIntelligenceService.get_all_context()
    for ctx in all_context:
        if ctx['hotspot_id'] == hotspot_id:
            return ctx
    return {"error": f"Hotspot {hotspot_id} not found in context intelligence."}
