from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.digital_twin_service import DigitalTwinService

router = APIRouter(prefix="/api")

class SimulationRequest(BaseModel):
    hotspot_id: int
    removal_pct: float

@router.get("/digital-twin", response_model=List[Dict[str, Any]])
def get_all_simulations():
    """Returns pre-calculated A/B/C/D scenarios for all hotspots."""
    return DigitalTwinService.get_all_simulations()

@router.post("/simulate")
def simulate_custom_scenario(req: SimulationRequest):
    """Runs a real-time custom simulation for a single hotspot."""
    return DigitalTwinService.simulate_custom(req.hotspot_id, req.removal_pct)

@router.get("/best-scenarios")
def get_best_scenarios():
    """Returns the recommended intervention scenario for each hotspot based on ROI."""
    return DigitalTwinService.get_best_scenarios()
