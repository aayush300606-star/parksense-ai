class CapacityLossEngine:
    """
    Quantifies the severity of road capacity reduction.
    """

    @staticmethod
    def calculate_capacity_loss(road_width: float, occupied_width: float) -> dict:
        """
        Formula: Capacity Loss = (Occupied Width / Original Road Width) * 100
        Returns score and categorical level.
        """
        if road_width <= 0:
            return {
                "capacity_loss_percentage": 100.0,
                "capacity_loss_score": 100.0,
                "capacity_loss_level": "Critical"
            }
            
        loss_percentage = (occupied_width / road_width) * 100.0
        
        # Cap loss at 100% physically
        if loss_percentage > 100.0:
            loss_percentage = 100.0
            
        # Determine Severity Level
        if loss_percentage >= 80:
            level = "Critical"
        elif loss_percentage >= 60:
            level = "High"
        elif loss_percentage >= 40:
            level = "Moderate"
        elif loss_percentage >= 20:
            level = "Low"
        else:
            level = "Minimal"
            
        return {
            "capacity_loss_percentage": round(loss_percentage, 2),
            "capacity_loss_score": round(loss_percentage, 2),
            "capacity_loss_level": level
        }
