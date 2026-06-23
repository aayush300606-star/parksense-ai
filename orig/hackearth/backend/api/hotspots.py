from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.hotspot import Hotspot
from ..services.hotspot_service import HotspotService

router = APIRouter(prefix="/api")

@router.get("/hotspots", response_model=List[Hotspot])
def get_hotspots():
    """
    Returns a list of all standard hotspot objects.
    """
    return HotspotService.get_all_hotspots()

@router.get("/hotspots/{hotspot_id}", response_model=Hotspot)
def get_hotspot(hotspot_id: int):
    """
    Returns details for a specific hotspot.
    """
    hotspot = HotspotService.get_hotspot_by_id(hotspot_id)
    if not hotspot:
        raise HTTPException(status_code=404, detail="Hotspot not found")
    return hotspot

@router.get("/violation-density")
def get_violation_density():
    """
    Returns violation density analytics.
    """
    return HotspotService.get_violation_density_analytics()

@router.get("/heatmap")
def get_heatmap():
    """
    Returns hotspot coordinates for frontend heatmap rendering.
    """
    return HotspotService.get_heatmap_data()

# --- Legacy Support Endpoint ---
@router.get("/legacy/hotspots.json")
def get_legacy_hotspots():
    """
    Returns the legacy JSON structure expected by the Next.js frontend,
    populated with real, un-mocked data.
    """
    return HotspotService.generate_frontend_compatible_hotspots()
