from typing import Dict, Any

class ToolRegistry:
    """
    Maps intents to the specific backend data services needed to answer them.
    """
    
    @staticmethod
    def get_tools_for_intent(intent: str) -> list[str]:
        registry = {
            "HOTSPOT_INQUIRY": ["CSIService", "PISService"],
            "SIMULATION_REQUEST": ["DigitalTwinService"],
            "PREDICTION_INQUIRY": ["PredictionService"],
            "ENFORCEMENT_PLAN": ["SmartEnforcementService"],
            "EXECUTIVE_SUMMARY": ["CSIService", "SmartEnforcementService", "PredictionService"],
            "NETWORK_INQUIRY": ["UTGIService"],
            "ROOT_CAUSE_INQUIRY": ["REIService"],
            "PIS_INQUIRY": ["PISService"],
            "GENERAL_INQUIRY": ["CSIService"]
        }
        return registry.get(intent, ["CSIService", "UTGIService", "REIService"])
