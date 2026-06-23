from typing import Dict, List, Any

class ScenarioEngine:
    """
    Defines standard intervention scenarios for the Digital Twin.
    """

    SCENARIOS = {
        "A": {"name": "100% Illegal Parking Removal", "removal_pct": 100},
        "B": {"name": "75% Removal (High Enforcement)", "removal_pct": 75},
        "C": {"name": "50% Removal (Moderate Enforcement)", "removal_pct": 50},
        "D": {"name": "25% Removal (Low Enforcement)", "removal_pct": 25}
    }

    @staticmethod
    def get_scenario(scenario_id: str) -> Dict[str, Any]:
        if scenario_id in ScenarioEngine.SCENARIOS:
            return ScenarioEngine.SCENARIOS[scenario_id]
        return {"name": "Custom Intervention", "removal_pct": 0} # Default no-op
