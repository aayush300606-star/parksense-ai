from fastapi import APIRouter
from typing import List, Dict, Any
from ..services.road_impact_service import RoadImpactService

router = APIRouter(prefix="/api")

@router.get("/road-impact", response_model=List[Dict[str, Any]])
def get_all_road_impacts():
    """
    Returns full Road Impact Intelligence objects quantifying capacity loss.
    """
    return RoadImpactService.get_all_impacts()

@router.get("/effective-width")
def get_effective_width():
    """
    Returns isolated effective width data for visualization rendering.
    """
    impacts = RoadImpactService.get_all_impacts()
    return [{'id': x['hotspot_id'], 'effective_width': x['effective_width']} for x in impacts]

@router.get("/capacity-loss")
def get_capacity_loss():
    """
    Returns isolated capacity loss metrics.
    """
    impacts = RoadImpactService.get_all_impacts()
    return [{'id': x['hotspot_id'], 'capacity_loss_score': x['capacity_loss_score']} for x in impacts]

@router.get("/lane-blockage")
def get_lane_blockage():
    """
    Returns isolated lane blockage metrics.
    """
    impacts = RoadImpactService.get_all_impacts()
    return [{'id': x['hotspot_id'], 'blocked_lanes': x['blocked_lanes'], 'remaining_lanes': x['remaining_lanes']} for x in impacts]
