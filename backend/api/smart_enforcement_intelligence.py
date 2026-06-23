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

@router.post("/enforcement-plan/{hotspot_id}/dispatch")
def dispatch_enforcement(hotspot_id: int):
    """
    Approves and dispatches the recommended enforcement action.
    Updates the plan record with 'Dispatched' status.
    """
    plans = SmartEnforcementService.get_enforcement_plan()
    updated = False
    for p in plans:
        if p.get('hotspot_id') == hotspot_id:
            p['status'] = 'Dispatched'
            updated = True
            break
            
    if updated:
        import os, json
        from ..services.smart_enforcement_service import ENFORCEMENT_PLAN_PATH
        with open(ENFORCEMENT_PLAN_PATH, 'w') as f:
            json.dump(plans, f, indent=2, default=str)
        return {"status": "success", "message": f"Team dispatched to hotspot {hotspot_id}"}
        
    return {"status": "error", "message": "Hotspot not found"}, 404
