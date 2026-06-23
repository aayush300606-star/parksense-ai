class VehicleOccupancyEngine:
    """
    Estimates the physical width footprint of different vehicle types.
    """
    
    VEHICLE_WIDTH_MAPPING = {
        "BIKE": 1.0,
        "SCOOTER": 1.0,
        "MOTORCYCLE": 1.0,
        "TWO WHEELER": 1.0,
        "AUTO": 1.5,
        "PASSENGER AUTO": 1.5,
        "CAR": 2.2,
        "TAXI": 2.2,
        "JEEP": 2.4,
        "SUV": 2.4,
        "BUS": 2.8,
        "MINI BUS": 2.8,
        "TRUCK": 3.0,
        "HGV": 3.0,
        "LCV": 2.6
    }
    
    DEFAULT_WIDTH = 2.0 # Fallback average width if type is unknown

    @staticmethod
    def get_vehicle_width(vehicle_type: str) -> float:
        """
        Returns the standard lateral width in meters for a given vehicle type.
        """
        v_type = str(vehicle_type).strip().upper()
        
        # Exact match
        if v_type in VehicleOccupancyEngine.VEHICLE_WIDTH_MAPPING:
            return VehicleOccupancyEngine.VEHICLE_WIDTH_MAPPING[v_type]
            
        # Substring match (e.g. "TATA TRUCK")
        for key, width in VehicleOccupancyEngine.VEHICLE_WIDTH_MAPPING.items():
            if key in v_type:
                return width
                
        # Graceful fallback
        return VehicleOccupancyEngine.DEFAULT_WIDTH
