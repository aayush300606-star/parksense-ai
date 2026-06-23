from pydantic import BaseModel
from datetime import datetime

class Hotspot(BaseModel):
    """
    Standardized Hotspot Object for the AI Data Foundation.
    All future modules consume this object.
    """
    hotspot_id: int
    latitude: float
    longitude: float
    cluster_radius: float
    violations: int
    cluster_area: float
    violation_density: float
    violation_density_score: float
    created_at: datetime
    
    # Extra fields for frontend compatibility
    location_name: str
    top_violation: str
    vehicle_types: dict = {}
