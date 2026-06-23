class CongestionImpactEngine:
    """
    Computes a unified Congestion Impact Score (0-100) by aggregating
    multiple traffic degradation signals using weighted composition.
    
    This score answers the hackathon question: "How much does illegal parking
    at this location affect overall traffic flow?"
    
    Components and weights:
        1. Speed Reduction %      (weight: 0.30)  — Direct flow degradation
        2. Capacity Loss %        (weight: 0.25)  — Physical road blockage
        3. Lane Blockage Score    (weight: 0.20)  — Lane-level disruption
        4. Delay Severity Factor  (weight: 0.15)  — Time impact magnitude
        5. Road Priority Factor   (weight: 0.10)  — Higher-priority roads amplify impact
    """

    # Severity factor mapping for delay
    DELAY_SEVERITY_FACTOR = {
        "Critical":  100,
        "High":      75,
        "Moderate":  50,
        "Low":       25,
        "Minimal":   10,
    }

    # Road priority normalization (score / 100 since priority is already 0-100)
    @staticmethod
    def calculate_congestion_impact(
        speed_reduction_percentage: float,
        capacity_loss_percentage: float,
        lane_blockage_score: float,
        delay_severity: str,
        road_priority_score: int
    ) -> dict:
        """
        Produces the Congestion Impact Score from multi-signal aggregation.
        
        Args:
            speed_reduction_percentage: % speed reduction (0-100)
            capacity_loss_percentage: % capacity lost to parking (0-100)
            lane_blockage_score: Lane blockage score (0-100)
            delay_severity: Severity string from delay engine
            road_priority_score: Road priority (0-100)
            
        Returns:
            dict with:
                - congestion_impact_score: Weighted composite score (0-100)
                - congestion_severity: Categorical label
                - component_breakdown: Individual weighted contributions
        """
        # Normalize all inputs to 0-100 range
        speed_component = min(100.0, max(0.0, speed_reduction_percentage))
        capacity_component = min(100.0, max(0.0, capacity_loss_percentage))
        lane_component = min(100.0, max(0.0, lane_blockage_score))
        delay_component = CongestionImpactEngine.DELAY_SEVERITY_FACTOR.get(delay_severity, 10)
        priority_component = min(100.0, max(0.0, float(road_priority_score)))
        
        # Weighted aggregation
        w_speed = 0.30
        w_capacity = 0.25
        w_lane = 0.20
        w_delay = 0.15
        w_priority = 0.10
        
        score = (
            speed_component * w_speed +
            capacity_component * w_capacity +
            lane_component * w_lane +
            delay_component * w_delay +
            priority_component * w_priority
        )
        
        # Clamp final score
        score = min(100.0, max(0.0, score))
        
        # Severity classification
        if score >= 80:
            severity = "Critical"
        elif score >= 60:
            severity = "Severe"
        elif score >= 40:
            severity = "Moderate"
        elif score >= 20:
            severity = "Low"
        else:
            severity = "Minimal"
        
        return {
            "congestion_impact_score": round(score, 2),
            "congestion_severity": severity,
            "component_breakdown": {
                "speed_reduction": {"value": round(speed_component, 2), "weight": w_speed, "weighted": round(speed_component * w_speed, 2)},
                "capacity_loss": {"value": round(capacity_component, 2), "weight": w_capacity, "weighted": round(capacity_component * w_capacity, 2)},
                "lane_blockage": {"value": round(lane_component, 2), "weight": w_lane, "weighted": round(lane_component * w_lane, 2)},
                "delay_severity": {"value": delay_component, "weight": w_delay, "weighted": round(delay_component * w_delay, 2)},
                "road_priority": {"value": round(priority_component, 2), "weight": w_priority, "weighted": round(priority_component * w_priority, 2)},
            }
        }
