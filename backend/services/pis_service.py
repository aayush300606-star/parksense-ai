import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.pis_intelligence import PISIntelligence
from ..services.csi_service import CSI_JSON_PATH

from ..ai.affected_vehicle_engine import AffectedVehicleEngine
from ..ai.commuter_impact_engine import CommuterImpactEngine
from ..ai.delay_impact_engine import DelayImpactEngine
from ..ai.fuel_waste_engine import FuelWasteEngine
from ..ai.environmental_impact_engine import EnvironmentalImpactEngine
from ..ai.economic_impact_engine import EconomicImpactEngine
from ..ai.capacity_recovery_engine import CapacityRecoveryEngine
from ..ai.pis_engine import PISEngine
from ..ai.pis_classification_engine import PISClassificationEngine
from ..ai.pis_explainability_engine import PISExplainabilityEngine
from ..ai.enforcement_benefit_engine import EnforcementBenefitEngine

PIS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'pis_results.json')
IMPACT_ANALYSIS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'impact_analysis.json')
ENVIRONMENTAL_IMPACT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'environmental_impact.json')
ECONOMIC_IMPACT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'economic_impact.json')
ENFORCEMENT_BENEFITS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'enforcement_benefits.json')
PIS_SUMMARY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'pis_summary.json')

class PISService:
    """
    Orchestrator for the Parking Impact Score (PIS™) Engine.
    
    Transforms CSI congestion severity into real-world impact metrics.
    """

    @staticmethod
    def generate_all():
        """Executes the full PIS™ pipeline."""
        if not os.path.exists(CSI_JSON_PATH):
            print(f"CSI data missing at {CSI_JSON_PATH}. Run CSI pipeline first.")
            return []

        with open(CSI_JSON_PATH, 'r') as f:
            csi_data = json.load(f)

        pis_objects = []
        
        for csi in csi_data:
            hid = csi['hotspot_id']
            road_name = csi['road_name']
            road_hierarchy = csi['road_hierarchy']
            lat = csi['latitude']
            lng = csi['longitude']
            
            csi_score = csi['csi_score']
            capacity_loss = csi.get('capacity_loss_percentage', 0)
            speed_reduction = csi.get('speed_reduction_percentage', 0)
            # Extrapolate average delay per vehicle (seconds). If not explicitly available, 
            # estimate from annual_delay_vehicle_hours roughly. Or use a reasonable proxy.
            annual_delay = csi.get('annual_delay_vehicle_hours', 0)
            
            # --- 1. Affected Vehicles ---
            veh_result = AffectedVehicleEngine.estimate_vehicles(
                road_hierarchy=road_hierarchy,
                capacity_loss_percentage=capacity_loss,
                csi_score=csi_score
            )
            
            # Estimate delay seconds per vehicle
            # daily delay hours = annual / 300
            # daily delay seconds = daily delay hours * 3600
            # delay per vehicle = daily delay seconds / daily vehicles
            daily_delay_hours_rough = annual_delay / 300.0
            daily_vehicles = veh_result["vehicles_impacted_per_day"]
            delay_seconds = (daily_delay_hours_rough * 3600.0) / max(1, daily_vehicles)
            
            # --- 2. Commuter Impact ---
            com_result = CommuterImpactEngine.estimate_commuters(
                vehicles_per_day=daily_vehicles,
                road_hierarchy=road_hierarchy
            )
            
            # --- 3. Delay Impact ---
            delay_result = DelayImpactEngine.calculate_delay(
                delay_seconds=delay_seconds,
                vehicles_per_day=daily_vehicles
            )
            
            # --- 4. Fuel Waste ---
            fuel_result = FuelWasteEngine.estimate_fuel_waste(
                daily_delay_hours=delay_result["daily_delay_hours"],
                road_hierarchy=road_hierarchy
            )
            
            # --- 5. Environmental Impact ---
            env_result = EnvironmentalImpactEngine.estimate_emissions(
                fuel_wasted_per_day=fuel_result["fuel_wasted_per_day"]
            )
            
            # --- 6. Economic Impact ---
            econ_result = EconomicImpactEngine.estimate_economic_loss(
                daily_delay_hours=delay_result["daily_delay_hours"],
                daily_commuters=com_result["daily_commuters_affected"],
                fuel_wasted_per_day=fuel_result["fuel_wasted_per_day"]
            )
            
            # --- 7. Capacity Recovery ---
            rec_result = CapacityRecoveryEngine.simulate_recovery(
                capacity_loss_percentage=capacity_loss,
                speed_reduction_percentage=speed_reduction,
                road_hierarchy=road_hierarchy
            )
            
            # --- 8. PIS Engine ---
            pis_result = PISEngine.calculate_pis(
                csi_score=csi_score,
                commuter_impact_score=com_result["commuter_impact_score"],
                delay_impact_score=delay_result["delay_impact_score"],
                fuel_impact_score=fuel_result["fuel_impact_score"],
                environmental_impact_score=env_result["environmental_impact_score"],
                economic_impact_score=econ_result["economic_impact_score"],
                recovery_score=rec_result["recovery_score"]
            )
            
            # --- 9. Classification ---
            class_result = PISClassificationEngine.classify(pis_result["pis_score"])
            
            # --- 11. Enforcement Benefit ---
            bene_result = EnforcementBenefitEngine.calculate_benefits(
                daily_delay_hours=delay_result["daily_delay_hours"],
                daily_commuters=com_result["daily_commuters_affected"],
                co2_kg_per_day=env_result["co2_emissions_kg_per_day"],
                economic_loss_per_day=econ_result["economic_burden_inr_per_day"],
                delay_reduction_pct=rec_result["delay_reduction_pct"]
            )
            
            # --- 10. Explainability ---
            exp_result = PISExplainabilityEngine.generate_explanation(
                pis_score=pis_result["pis_score"],
                pis_level=class_result["pis_level"],
                daily_commuters=com_result["daily_commuters_affected"],
                daily_delay_hours=delay_result["daily_delay_hours"],
                fuel_wasted_per_day=fuel_result["fuel_wasted_per_day"],
                co2_emissions_kg_per_day=env_result["co2_emissions_kg_per_day"],
                economic_burden_inr_per_day=econ_result["economic_burden_inr_per_day"],
                enforcement_benefit_score=bene_result["enforcement_benefit_score"]
            )
            
            # Create Intelligence Object
            obj = PISIntelligence(
                hotspot_id=hid,
                latitude=lat,
                longitude=lng,
                road_name=road_name,
                road_hierarchy=road_hierarchy,
                
                csi_score=csi_score,
                pis_score=pis_result["pis_score"],
                pis_level=class_result["pis_level"],
                pis_priority=class_result["pis_priority"],
                pis_color=class_result["pis_color"],
                pis_color_name=class_result["pis_color_name"],
                
                vehicles_impacted_per_day=veh_result["vehicles_impacted_per_day"],
                peak_hour_impacted_vehicles=veh_result["peak_hour_impacted_vehicles"],
                daily_commuters_affected=com_result["daily_commuters_affected"],
                daily_delay_hours=delay_result["daily_delay_hours"],
                annual_delay_hours=delay_result["annual_delay_hours"],
                
                fuel_wasted_per_day_liters=fuel_result["fuel_wasted_per_day"],
                fuel_wasted_per_year_liters=fuel_result["fuel_wasted_per_year"],
                co2_emissions_kg_per_day=env_result["co2_emissions_kg_per_day"],
                co2_emissions_tons_per_year=env_result["co2_emissions_tons_per_year"],
                environmental_level=env_result["environmental_level"],
                
                lost_productivity_inr_per_day=econ_result["lost_productivity_inr_per_day"],
                fuel_cost_inr_per_day=econ_result["fuel_cost_inr_per_day"],
                economic_burden_inr_per_day=econ_result["economic_burden_inr_per_day"],
                economic_burden_inr_per_year=econ_result["economic_burden_inr_per_year"],
                
                capacity_recovered_pct=rec_result["capacity_recovered_pct"],
                speed_recovered_pct=rec_result["speed_recovered_pct"],
                expected_delay_reduction_hours_per_day=bene_result["expected_delay_reduction_hours_per_day"],
                expected_commuter_benefit_hours_per_day=bene_result["expected_commuter_benefit_hours_per_day"],
                expected_economic_benefit_inr_per_day=bene_result["expected_economic_benefit_inr_per_day"],
                enforcement_benefit_score=bene_result["enforcement_benefit_score"],
                
                explanation=exp_result["explanation"],
                generated_at=datetime.now()
            )
            pis_objects.append(obj)

        os.makedirs(os.path.dirname(PIS_JSON_PATH), exist_ok=True)

        json_data = [obj.dict() for obj in pis_objects]
        with open(PIS_JSON_PATH, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
            
        # Impact Analysis (Aggregated for frontend)
        impact_analysis = []
        for d in json_data:
            impact_analysis.append({
                "hotspot_id": d["hotspot_id"],
                "road_name": d["road_name"],
                "csi_score": d["csi_score"],
                "pis_score": d["pis_score"],
                "pis_level": d["pis_level"],
                "daily_commuters": d["daily_commuters_affected"],
                "daily_delay_hours": d["daily_delay_hours"]
            })
        with open(IMPACT_ANALYSIS_PATH, 'w') as f:
            json.dump(impact_analysis, f, indent=2)
            
        # Environmental Impact
        env_impact = []
        for d in json_data:
            env_impact.append({
                "hotspot_id": d["hotspot_id"],
                "road_name": d["road_name"],
                "fuel_wasted_liters": d["fuel_wasted_per_day_liters"],
                "co2_emissions_kg": d["co2_emissions_kg_per_day"],
                "environmental_level": d["environmental_level"]
            })
        with open(ENVIRONMENTAL_IMPACT_PATH, 'w') as f:
            json.dump(env_impact, f, indent=2)
            
        # Economic Impact
        econ_impact = []
        for d in json_data:
            econ_impact.append({
                "hotspot_id": d["hotspot_id"],
                "road_name": d["road_name"],
                "lost_productivity_inr": d["lost_productivity_inr_per_day"],
                "fuel_cost_inr": d["fuel_cost_inr_per_day"],
                "total_economic_burden_inr": d["economic_burden_inr_per_day"]
            })
        with open(ECONOMIC_IMPACT_PATH, 'w') as f:
            json.dump(econ_impact, f, indent=2)
            
        # Enforcement Benefits
        enf_benefits = []
        for d in json_data:
            enf_benefits.append({
                "hotspot_id": d["hotspot_id"],
                "road_name": d["road_name"],
                "capacity_recovered_pct": d["capacity_recovered_pct"],
                "expected_delay_reduction_hours": d["expected_delay_reduction_hours_per_day"],
                "expected_economic_benefit_inr": d["expected_economic_benefit_inr_per_day"],
                "enforcement_benefit_score": d["enforcement_benefit_score"]
            })
        with open(ENFORCEMENT_BENEFITS_PATH, 'w') as f:
            json.dump(enf_benefits, f, indent=2)

        # Summary
        total_fuel = sum(d["fuel_wasted_per_day_liters"] for d in json_data)
        total_co2 = sum(d["co2_emissions_kg_per_day"] for d in json_data)
        total_econ = sum(d["economic_burden_inr_per_day"] for d in json_data)
        total_commuters = sum(d["daily_commuters_affected"] for d in json_data)
        
        summary = {
            "total_hotspots_analyzed": len(json_data),
            "city_wide_daily_impact": {
                "fuel_wasted_liters": round(total_fuel, 0),
                "co2_emissions_kg": round(total_co2, 0),
                "economic_burden_inr": round(total_econ, 0),
                "commuters_affected": round(total_commuters, 0)
            }
        }
        with open(PIS_SUMMARY_PATH, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"Parking Impact Score (PIS) Intelligence generated for {len(pis_objects)} hotspots.")
        return pis_objects

    @staticmethod
    def get_all_pis() -> List[Dict[str, Any]]:
        if not os.path.exists(PIS_JSON_PATH):
            PISService.generate_all()
        with open(PIS_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        if not os.path.exists(PIS_SUMMARY_PATH):
            PISService.generate_all()
        with open(PIS_SUMMARY_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_impact_analysis() -> List[Dict[str, Any]]:
        if not os.path.exists(IMPACT_ANALYSIS_PATH):
            PISService.generate_all()
        with open(IMPACT_ANALYSIS_PATH, 'r') as f:
            return json.load(f)
            
    @staticmethod
    def get_enforcement_benefits() -> List[Dict[str, Any]]:
        if not os.path.exists(ENFORCEMENT_BENEFITS_PATH):
            PISService.generate_all()
        with open(ENFORCEMENT_BENEFITS_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_top_impact() -> List[Dict[str, Any]]:
        data = PISService.get_all_pis()
        sorted_data = sorted(data, key=lambda x: x["pis_score"], reverse=True)
        return sorted_data[:20]
