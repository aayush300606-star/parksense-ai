class KPIMetadataEngine:
    """
    Acts as the single source of truth for the definitions and methodologies of all system KPIs.
    Frontend 'Why?' buttons pull from this registry to provide immediate explainability to users.
    """

    METADATA_REGISTRY = {
        "CSI": {
            "definition": "Adaptive Congestion Severity Index. A universal score (0-100) representing the severity of a traffic bottleneck.",
            "methodology": "Min-max normalized weighted sum of Violation Density, Effective Width Loss, Traffic Delay, and Contextual Importance.",
            "formula": "w1*Density + w2*WidthLoss + w3*Delay + w4*POI_Penalty",
            "data_sources": ["Police Ticketing Data", "OpenStreetMap", "TomTom Traffic Proxies"],
            "confidence": "High (0.95)"
        },
        "PIS": {
            "definition": "Parking Impact Score. Translates traffic delay into physical Rupees lost and CO2 emitted.",
            "methodology": "Calculates total commuter hours wasted per day and multiplies by average hourly wage. Adds idling fuel waste.",
            "formula": "(Delay_Hrs * Wage) + (Wasted_Fuel_Liters * Fuel_Cost)",
            "data_sources": ["Economic Indicators", "Vehicle Emission Standards"],
            "confidence": "Medium (0.85) - Dependent on wage estimations"
        },
        "Effective_Width": {
            "definition": "The actual drivable width of the road after accounting for illegally parked vehicles.",
            "methodology": "Subtracts standard vehicle width (e.g., 2.5m for a car) from the total road capacity for each parked vehicle in a cross-section.",
            "formula": "Total_Width - (Num_Parked_Vehicles * Avg_Vehicle_Width)",
            "data_sources": ["Road Hierarchy DB", "Violation Clusters"],
            "confidence": "High (0.92)"
        },
        "Prediction_Risk": {
            "definition": "The probability that a hotspot will cross the 'Severe' CSI threshold in the future.",
            "methodology": "Random Forest ML classification based on temporal trends, peak hour proximity, and historical frequency.",
            "formula": "Ensemble_Tree_Output(Temporal_Features)",
            "data_sources": ["Historical CSI Data", "Time-of-day features"],
            "confidence": "High (0.88 for 24h, 0.75 for 7d)"
        },
        "Digital_Twin_ROI": {
            "definition": "The expected return on investment for a physical enforcement action.",
            "methodology": "Simulates removing vehicles and recalculates the CSI. ROI is the ratio of CSI improvement to the operational cost of the action.",
            "formula": "(CSI_Before - CSI_After) / Intervention_Cost_Weight",
            "data_sources": ["Physics Simulator", "Enforcement Resource Matrix"],
            "confidence": "High (0.90)"
        }
    }

    @staticmethod
    def get_kpi_metadata(kpi_key: str) -> dict:
        return KPIMetadataEngine.METADATA_REGISTRY.get(kpi_key, {
            "error": "KPI metadata not found. Please consult the engineering team."
        })
