from fastapi import APIRouter
from typing import List, Dict, Any
from ..services.smart_enforcement_service import SmartEnforcementService

router = APIRouter(prefix="/api")

@router.get("/enforcement-plan", response_model=List[Dict[str, Any]])
def get_enforcement_plan():
    """Returns the prioritized list of hotspots mapped to teams."""
    return SmartEnforcementService.get_enforcement_plan()

@router.get("/daily-plan")
def get_daily_plan():
    """Returns the compiled daily patrol schedules grouped by team."""
    return SmartEnforcementService.get_daily_plan()

@router.get("/weekly-plan")
def get_weekly_plan():
    """Returns strategic macro-level enforcement trends."""
    return SmartEnforcementService.get_weekly_plan()
