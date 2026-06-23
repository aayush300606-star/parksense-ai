from fastapi import APIRouter
from typing import List, Dict, Any
from ..services.pis_service import PISService

router = APIRouter(prefix="/api")

@router.get("/pis", response_model=List[Dict[str, Any]])
def get_all_pis():
    """Returns the full Parking Impact Score (PIS) intelligence for all hotspots."""
    return PISService.get_all_pis()

@router.get("/pis-summary")
def get_pis_summary():
    """Returns city-wide aggregated impact statistics."""
    return PISService.get_summary()

@router.get("/impact-analysis")
def get_impact_analysis():
    """Returns general impact analysis details."""
    return PISService.get_impact_analysis()

@router.get("/enforcement-benefit")
def get_enforcement_benefit():
    """Returns enforcement benefits projection data."""
    return PISService.get_enforcement_benefits()

@router.get("/top-impact-hotspots")
def get_top_impact_hotspots():
    """Returns the top 20 hotspots sorted by PIS score."""
    return PISService.get_top_impact()
