class EnforcementKnowledgeBase:
    """
    Central repository of known violation behaviors, root causes, and standard enforcement strategies.
    Used deterministically by the recommendation engines to generate physical solutions.
    """

    ROOT_CAUSES = {
        "RC_METRO": "Metro Station Commuter Spillover",
        "RC_RIDE_HAIL": "Ride-Hailing Pickup/Drop-off",
        "RC_COMMERCIAL": "Commercial/Freight Loading",
        "RC_HOSPITAL": "Emergency & Patient Drop-off",
        "RC_MARKET": "Informal Street Market/Vending",
        "RC_SCHOOL": "School Drop-off/Pick-up Blocking",
        "RC_NIGHTLIFE": "Nightlife/Restaurant Valet Spillover",
        "RC_RESIDENTIAL": "Overnight Residential Parking Overflow",
        "RC_EVENT": "Sporadic Event/Stadium Congestion"
    }

    INTERVENTIONS = {
        "INT_TOWING": {
            "type": "Immediate",
            "name": "Rapid Towing Dispatch",
            "effectiveness": "High",
            "implementation_complexity": "Low",
            "description": "Immediate removal of the physical blockage to recover capacity."
        },
        "INT_MARSHAL": {
            "type": "Immediate",
            "name": "Deploy Traffic Marshal",
            "effectiveness": "Medium",
            "implementation_complexity": "Low",
            "description": "Manual traffic direction to prevent localized stopping."
        },
        "INT_PATROL": {
            "type": "Short-Term",
            "name": "Increased Frequency Patrols",
            "effectiveness": "High",
            "implementation_complexity": "Medium",
            "description": "Routing regular police patrols through the corridor to deter long-term violations."
        },
        "INT_PICKUP_ZONE": {
            "type": "Long-Term",
            "name": "Establish Dedicated Pickup/Drop-off Zone",
            "effectiveness": "Very High",
            "implementation_complexity": "High",
            "description": "Re-architect the curbside to legalize and structure short-term stops, eliminating road blockage."
        },
        "INT_LOADING_BAY": {
            "type": "Long-Term",
            "name": "Designate Commercial Loading Bay",
            "effectiveness": "Very High",
            "implementation_complexity": "High",
            "description": "Dedicate physical space for freight delivery vehicles, restricting hours of operation."
        },
        "INT_BARRICADES": {
            "type": "Short-Term",
            "name": "Install Physical Barricades/Bollards",
            "effectiveness": "High",
            "implementation_complexity": "Medium",
            "description": "Physically prevent vehicles from mounting the curb or parking on critical junctions."
        }
    }

    @classmethod
    def get_root_cause_label(cls, key: str) -> str:
        return cls.ROOT_CAUSES.get(key, "Unknown Root Cause")

    @classmethod
    def get_intervention_details(cls, key: str) -> dict:
        return cls.INTERVENTIONS.get(key, {})
