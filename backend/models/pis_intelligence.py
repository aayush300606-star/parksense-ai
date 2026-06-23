from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class PISIntelligence(BaseModel):
    """
    Standardized Parking Impact Score (PIS™) Intelligence Object.
    
    Translates CSI congestion severity into real-world impact metrics:
    human, economic, environmental, and enforcement ROI.
    """
    model_config = {"protected_namespaces": ()}

    hotspot_id: int
    latitude: float
    longitude: float
    road_name: str
    road_hierarchy: str

    # === Scores ===
    csi_score: float
    pis_score: float
    pis_level: str
    pis_priority: str
    pis_color: str
    pis_color_name: str

    # === Human Impact ===
    vehicles_impacted_per_day: int
    peak_hour_impacted_vehicles: int
    daily_commuters_affected: int
    daily_delay_hours: float
    annual_delay_hours: float

    # === Environmental & Fuel Impact ===
    fuel_wasted_per_day_liters: float
    fuel_wasted_per_year_liters: float
    co2_emissions_kg_per_day: float
    co2_emissions_tons_per_year: float
    environmental_level: str

    # === Economic Impact ===
    lost_productivity_inr_per_day: int
    fuel_cost_inr_per_day: int
    economic_burden_inr_per_day: int
    economic_burden_inr_per_year: int

    # === Capacity & Enforcement ROI ===
    capacity_recovered_pct: float
    speed_recovered_pct: float
    expected_delay_reduction_hours_per_day: float
    expected_commuter_benefit_hours_per_day: float
    expected_economic_benefit_inr_per_day: int
    enforcement_benefit_score: float

    # === Explainability ===
    explanation: str

    # === Metadata ===
    generated_at: datetime
