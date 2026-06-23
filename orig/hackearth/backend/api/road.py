from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..services.road_service import RoadService

router = APIRouter(prefix="/api")

@router.get("/roads", response_model=List[Dict[str, Any]])
def get_all_roads():
    """
    Returns all Road Intelligence objects.
    """
    return RoadService.get_all_roads()

@router.get("/roads/{hotspot_id}", response_model=Dict[str, Any])
def get_road(hotspot_id: int):
    """
    Returns Road Intelligence for a specific hotspot.
    """
    road = RoadService.get_road_by_id(hotspot_id)
    if not road:
        raise HTTPException(status_code=404, detail="Road Intelligence not found")
    return road

@router.get("/road-summary", response_model=Dict[str, Any])
def get_road_summary():
    """
    Returns statistical summary of the Road Intelligence Layer.
    """
    return RoadService.get_statistics()
