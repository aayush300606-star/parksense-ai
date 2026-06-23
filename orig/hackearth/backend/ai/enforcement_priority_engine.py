from typing import Dict, Any

class EnforcementPriorityEngine:
    """
    Ranks hotspots for enforcement action by fusing multiple intelligence layers.
    Also handles legacy PIS/CSI priority calculations.
    """

    @staticmethod
    def calculate_enforcement_priority(
        csi_score: float,
        csi_level: str,
        capacity_loss_percentage: float,
        speed_reduction_percentage: float,
        road_hierarchy: str,
        emergency_route_impact: bool,
        violation_count: int,
        annual_delay_vehicle_hours: float
    ) -> Dict[str, Any]:
        """
        Legacy method used by CSI Service to calculate expected benefits.
        """
        priority_score = (csi_score * 0.4) + (capacity_loss_percentage * 0.3) + (speed_reduction_percentage * 0.3)
        if emergency_route_impact:
            priority_score *= 1.2
            
        priority_score = min(100.0, priority_score)
        
        if priority_score >= 80:
            level = "P1 - Critical Priority"
            rec = "Deploy active towing and high-visibility patrols."
        elif priority_score >= 60:
            level = "P2 - High Priority"
            rec = "Deploy ticketing patrols during peak hours."
        elif priority_score >= 40:
            level = "P3 - Moderate Priority"
            rec = "Monitor and deploy automated enforcement (ANPR)."
        else:
            level = "P4 - Low Priority"
            rec = "No active enforcement required."
            
        cap_rec = capacity_loss_percentage * 0.8
        spd_imp = speed_reduction_percentage * 0.7
        daily_veh = int(annual_delay_vehicle_hours / 365)
        del_sav = annual_delay_vehicle_hours * 0.6
        
        return {
            "priority_score": round(priority_score, 1),
            "priority_level": level,
            "expected_capacity_recovery": round(cap_rec, 1),
            "expected_speed_improvement": round(spd_imp, 1),
            "daily_vehicles_affected": daily_veh,
            "annual_delay_savings_hours": round(del_sav, 1),
            "enforcement_recommendation": rec
        }

    @staticmethod
    def calculate_priority(
        csi_score: float, 
        pis_score: float, 
        prediction_risk_score: float, 
        is_emergency_route: bool, 
        is_high_context: bool
    ) -> Dict[str, Any]:
        """
        Calculates an absolute Priority Score (0-100).
        """
        # Base weightings
        score = (csi_score * 0.35) + (pis_score * 0.35) + (prediction_risk_score * 0.30)
        
        # Context multipliers
        if is_emergency_route:
            score *= 1.25
        if is_high_context:
            score *= 1.10
            
        score = min(100.0, score)
        
        if score >= 85:
            level = "P1 - Critical Priority"
        elif score >= 70:
            level = "P2 - High Priority"
        elif score >= 50:
            level = "P3 - Moderate Priority"
        else:
            level = "P4 - Low Priority"
            
        return {
            "priority_score": round(score, 1),
            "priority_level": level
        }
