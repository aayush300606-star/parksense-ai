from typing import Dict, Any


class EconomicImpactEngine:
    """
    Estimates the economic burden of congestion (time lost + fuel wasted).
    """

    # Average Value of Time (VoT) for Indian commuters (INR per hour)
    VOT_INR_PER_HOUR = 120.0
    
    # Average fuel cost (INR per liter)
    FUEL_COST_INR = 100.0

    @staticmethod
    def estimate_economic_loss(
        daily_delay_hours: float,
        daily_commuters: int,
        fuel_wasted_per_day: float
    ) -> Dict[str, Any]:
        """
        Calculates lost productivity, time cost, and fuel cost.
        """
        # Average delay per commuter in hours
        avg_delay_hr = daily_delay_hours / max(1, daily_commuters)
        
        # Time cost = total delay hours * value of time
        # (Assuming all delay hours are commuter hours to simplify, ideally weighted by occupancy)
        # Better: Since daily_delay_hours is VEHICLE delay, we need PASSENGER delay.
        # Passenger delay = vehicle delay * average occupancy.
        # From earlier, average occupancy is roughly 1.5 across modes.
        passenger_delay_hours = daily_delay_hours * 1.5
        time_cost_per_day = passenger_delay_hours * EconomicImpactEngine.VOT_INR_PER_HOUR
        
        fuel_cost_per_day = fuel_wasted_per_day * EconomicImpactEngine.FUEL_COST_INR
        
        total_economic_loss_per_day = time_cost_per_day + fuel_cost_per_day
        total_economic_loss_per_year = total_economic_loss_per_day * 300
        
        # Score: 100 if loss > ₹10,00,000 per day
        economic_impact_score = min(100.0, (total_economic_loss_per_day / 1000000.0) * 100.0)
        
        return {
            "lost_productivity_inr_per_day": int(time_cost_per_day),
            "fuel_cost_inr_per_day": int(fuel_cost_per_day),
            "economic_burden_inr_per_day": int(total_economic_loss_per_day),
            "economic_burden_inr_per_year": int(total_economic_loss_per_year),
            "economic_impact_score": round(economic_impact_score, 2)
        }
