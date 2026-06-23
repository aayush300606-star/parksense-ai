class CauseCongestionMapper:
    """
    Deterministic mapping engine that connects behavioral Root Causes to their physical 
    manifestations on the road network (Capacity Loss -> Traffic Slowdown -> CSI).
    """

    @staticmethod
    def map_pathway(root_cause_key: str) -> dict:
        pathways = {
            "RC_COMMERCIAL": {
                "behavior": "Heavy goods vehicles double-parking for 15-45 minutes.",
                "capacity_impact": "Loss of 1 full traffic lane.",
                "flow_impact": "High turbulence as vehicles merge into adjacent lanes.",
                "csi_driver": "Effective Width Loss",
                "pis_driver": "Idling Fuel Waste"
            },
            "RC_RIDE_HAIL": {
                "behavior": "Frequent, short-duration (1-3 min) stopping near POI entrances.",
                "capacity_impact": "Intermittent blockage of the left-most lane.",
                "flow_impact": "Stop-and-go shockwaves propagating upstream.",
                "csi_driver": "Temporal Violation Frequency",
                "pis_driver": "Commuter Delay"
            },
            "RC_SCHOOL": {
                "behavior": "Extreme clustering of vehicles during two 45-minute daily windows.",
                "capacity_impact": "Loss of 1-2 lanes, severe pedestrian conflict.",
                "flow_impact": "Total localized gridlock during peak windows.",
                "csi_driver": "Peak Context Density",
                "pis_driver": "Idling Fuel Waste"
            },
            "RC_METRO": {
                "behavior": "Long-term (8+ hours) parallel and perpendicular parking spillover.",
                "capacity_impact": "Permanent structural loss of lane capacity.",
                "flow_impact": "Continuous speed reduction on the corridor.",
                "csi_driver": "Effective Width Loss",
                "pis_driver": "Commuter Delay"
            }
        }
        
        # Default fallback mapping
        default_mapping = {
            "behavior": "Unauthorized parking blocking right-of-way.",
            "capacity_impact": "Reduction of usable road width.",
            "flow_impact": "Speed reduction and queuing.",
            "csi_driver": "Violation Density",
            "pis_driver": "Economic Loss"
        }
        
        return pathways.get(root_cause_key, default_mapping)
