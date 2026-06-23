from typing import Dict, Any, List

class ContextAggregator:
    """
    Pulls intelligence from the registered tools to build the LLM Context Window.
    """

    @staticmethod
    def build_context(tools: List[str]) -> Dict[str, Any]:
        """
        Dynamically fetches the latest JSON data from the requested services.
        To avoid massive context windows, it fetches summaries or top N results.
        """
        context = {}
        
        if "CSIService" in tools:
            from ..services.csi_service import CSIService
            context["top_critical_hotspots"] = CSIService.get_top_critical()[:5]
            context["city_summary"] = CSIService.get_summary()
            
        if "PISService" in tools:
            # PIS is heavily tied to CSI, we just pass the top economic burdens
            from ..services.pis_service import PISService
            context["highest_impact_zones"] = sorted(PISService.get_all_pis(), key=lambda x: x['pis_score'], reverse=True)[:5]
            
        if "DigitalTwinService" in tools:
            from ..services.digital_twin_service import DigitalTwinService
            context["best_simulations"] = DigitalTwinService.get_best_scenarios()[:5]
            
        if "PredictionService" in tools:
            from ..services.prediction_service import PredictionService
            preds = PredictionService.get_all_predictions()
            # Find hotspots that are predicted to get significantly worse in 24h
            high_risk = []
            for p in preds:
                h24 = p['forecasts'].get('24h', {})
                if h24.get('trend_direction') == 'Increasing' and h24.get('severity_level') in ['Critical', 'Severe']:
                    high_risk.append(p)
            context["predicted_high_risk_tomorrow"] = high_risk[:5]
            
        if "SmartEnforcementService" in tools:
            from ..services.smart_enforcement_service import SmartEnforcementService
            context["daily_enforcement_plan"] = SmartEnforcementService.get_daily_plan()
            context["top_enforcement_targets"] = SmartEnforcementService.get_enforcement_plan()[:5]
            
        if "UTGIService" in tools:
            import json
            import os
            try:
                with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'network_csi.json')) as f:
                    context["network_csi_map"] = json.load(f)[:5]
                with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'ripple_effects.json')) as f:
                    context["top_ripple_effects"] = json.load(f)[:3]
            except:
                pass
                
        if "REIService" in tools:
            import json
            import os
            try:
                with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'hotspot_dna.json')) as f:
                    context["top_root_causes"] = json.load(f)[:5]
            except:
                pass
            
        return context
