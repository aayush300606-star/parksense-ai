from .vehicle_occupancy_engine import VehicleOccupancyEngine

class OccupiedWidthEngine:
    """
    Calculates the total effective width blocked by illegally parked vehicles.
    """

    @staticmethod
    def calculate_occupied_width(vehicle_types: dict) -> dict:
        """
        Aggregates the physical width taken by all vehicles in the cluster.
        According to the defined formula: Occupied Width = sum(vehicle_width).
        To prevent absurdly high widths from long linear clusters, we can 
        assume a lateral stacking factor, but the core formula remains driven
        by vehicle widths.
        """
        total_occupied_width = 0.0
        
        # If no vehicle types are present, we assume an average car footprint
        # based on the total violations count, but ideally we have the dict.
        if not vehicle_types:
            return {
                "occupied_width": 2.2,
                "occupied_width_source": "Fallback Estimation (No Vehicle Data)",
                "occupied_width_confidence": 0.50
            }
            
        for v_type, count in vehicle_types.items():
            width_per_vehicle = VehicleOccupancyEngine.get_vehicle_width(v_type)
            # The user requested sum(vehicle_width).
            # To make it realistic for physical roads, if there are 100 bikes, they aren't all 
            # parked laterally blocking a 100m wide road. They park in clusters.
            # We'll calculate the raw sum.
            total_occupied_width += (width_per_vehicle * count)
            
        # In reality, vehicles park linearly. To represent lateral intrusion, we 
        # simulate double/triple parking severity logarithmically or capped, 
        # but to strictly follow "sum(vehicle_width)" as instructed, we compute the raw sum.
        # To keep it bounded within realistic city bounds, we might cap it during capacity loss.
        # However, for pure sum:
        raw_sum = total_occupied_width
        
        # Since the prompt requires `Occupied Width = sum(vehicle_width)`, we will use it directly.
        # (Though we will clamp it in the Effective Width engine to not exceed Road Width).
        
        return {
            "occupied_width": round(raw_sum, 2),
            "occupied_width_source": "Aggregated Vehicle Data",
            "occupied_width_confidence": 0.95
        }
