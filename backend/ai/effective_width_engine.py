class EffectiveWidthEngine:
    """
    Calculates the usable carriageway remaining after illegal parking intrusion.
    """

    @staticmethod
    def calculate_effective_width(road_width: float, occupied_width: float) -> dict:
        """
        Formula: Effective Width = Road Width - Occupied Width.
        Ensures widths are clamped safely (cannot be negative).
        """
        effective_width = road_width - occupied_width
        
        # Clamp negative values to 0 (road completely blocked)
        if effective_width < 0:
            effective_width = 0.0
            
        # Calculate percentage of road remaining
        if road_width > 0:
            remaining_percentage = (effective_width / road_width) * 100.0
        else:
            remaining_percentage = 0.0
            
        return {
            "effective_width": round(effective_width, 2),
            "effective_width_percentage": round(remaining_percentage, 2)
        }
