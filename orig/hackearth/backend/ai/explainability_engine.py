class ExplainabilityEngine:
    """
    Translates mathematical telemetry into human-readable GIS intelligence reasoning.
    """

    @staticmethod
    def generate_explanation(vehicle_types: dict, road_width: float, occupied_width: float, effective_width: float, capacity_loss: float) -> str:
        """
        Constructs an AI explanation sentence.
        Example: 14 illegally parked SCOOTERs and 2 PASSENGER AUTOS occupying 8.8 meters reduced usable carriageway to 11.2 meters.
        """
        # Format the vehicle breakdown
        if not vehicle_types:
            vehicle_string = "Illegally parked vehicles"
        else:
            parts = []
            for v_type, count in vehicle_types.items():
                parts.append(f"{count} {v_type}(s)")
            vehicle_string = " and ".join(parts)
            
        explanation = (
            f"{vehicle_string} occupying {occupied_width} meters laterally "
            f"reduced the usable carriageway from {road_width}m to {effective_width}m, "
            f"resulting in a {capacity_loss}% loss in road capacity."
        )
        
        return explanation
