from fastapi import APIRouter
from typing import Dict, Any

from ..services.csi_service import CSIService
from ..services.pis_service import PISService
from ..services.prediction_service import PredictionService
from ..services.digital_twin_service import DigitalTwinService
from ..services.smart_enforcement_service import SmartEnforcementService
from ..ai.copilot_orchestrator import CopilotOrchestrator
from ..ai.hotspot_dna_engine import HotspotDNAEngine
import json
import os

router = APIRouter(prefix="/api/demo")

@router.get("/presentation")
def get_presentation_mode() -> Dict[str, Any]:
    """
    1-Click Judge Walkthrough Mode.
    Assembles a narrative payload of the most critical hotspot in the city,
    combining its CSI, Economic Impact (PIS), Predictive Risk, Digital Twin ROI,
    and Enforcement Plan, wrapped in an AI Copilot narrative.
    """
    
    # 1. Identify the most critical hotspot (Highest CSI)
    top_csi = CSIService.get_top_critical()
    if not top_csi:
        return {"error": "Pipeline must be run first."}
        
    target = top_csi[0]
    hid = target['hotspot_id']
    
    # 2. Get its PIS
    pis_data = PISService.get_all_pis()
    target_pis = next((p for p in pis_data if p['hotspot_id'] == hid), None)
    
    # 3. Get its Predictions
    pred_data = PredictionService.get_all_predictions()
    target_pred = next((p for p in pred_data if p['hotspot_id'] == hid), None)
    
    # 4. Get its Digital Twin Results
    dt_data = DigitalTwinService.get_all_simulations()
    target_dts = [s for s in dt_data if s['hotspot_id'] == hid]
    best_dt = next((s for s in DigitalTwinService.get_best_scenarios() if s['hotspot_id'] == hid), target_dts[0] if target_dts else None)
    
    # 5. Get Enforcement Plan
    sep_data = SmartEnforcementService.get_enforcement_plan()
    target_sep = next((p for p in sep_data if p['hotspot_id'] == hid), None)
    
    # 5.1 Get Enforcement DNA
    target_dna = HotspotDNAEngine.get_dna(hid)
    
    # 5.2 Get Network Intelligence
    network_data = None
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'network_csi.json')) as f:
            n_data = json.load(f)
            network_data = next((n for n in n_data if n['hotspot_id'] == hid), None)
    except:
        pass
    
    # 6. Ask AI Copilot to generate a narrative presentation
    narrative_query = f"Provide a complete executive presentation summary for {target['road_name']}. Why is it critical, what will happen tomorrow, and what should we do?"
    narrative = CopilotOrchestrator.process_query(narrative_query)
    
    return {
        "presentation_title": f"Smart City Intelligence Briefing: {target['road_name']}",
        "narrative_summary": narrative['response'],
        "ai_evidence": narrative['evidence'],
        "ai_recommendations": narrative['recommendations'],
        "intelligence_layers": {
            "descriptive": {
                "csi_score": target['csi_score'],
                "csi_level": target['csi_level'],
                "dominant_factor": target['dominant_factor'],
                "pis_score": target_pis['pis_score'] if target_pis else None,
                "economic_loss_inr": target_pis['economic_burden_inr_per_day'] if target_pis else None
            },
            "predictive": {
                "risk_1h": target_pred['forecasts']['1h'].get('hotspot_probability') if target_pred and '1h' in target_pred.get('forecasts', {}) else None,
                "risk_24h": target_pred['forecasts']['24h'].get('hotspot_probability') if target_pred and '24h' in target_pred.get('forecasts', {}) else None,
                "trend_24h": target_pred['forecasts']['24h'].get('trend_direction') if target_pred and '24h' in target_pred.get('forecasts', {}) else None
            },
            "prescriptive": {
                "best_simulation": best_dt.get('scenario_name') if best_dt else None,
                "expected_csi_reduction": best_dt.get('csi_improvement') if best_dt else None,
                "roi_score": best_dt.get('roi') if best_dt else None
            },
            "operational": {
                "recommended_team": target_sep.get('recommended_team') if target_sep else None,
                "recommended_time": target_sep.get('recommended_time') if target_sep else None,
                "action": target_sep.get('recommended_action') if target_sep else None
            },
            "root_cause_dna": {
                "dna_signature": target_dna.get('dna_signature') if 'error' not in target_dna else None,
                "primary_cause": target_dna.get('primary_cause') if 'error' not in target_dna else None,
                "infrastructure_fix": target_dna.get('recommended_infrastructure_fix') if 'error' not in target_dna else None
            },
            "network_intelligence": {
                "network_csi": network_data.get('network_csi_score') if network_data else None,
                "ripple_effect_multiplier": network_data.get('ripple_effect_multiplier') if network_data else None
            }
        }
    }
