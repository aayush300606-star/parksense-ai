from typing import Dict, Any


class PISEngine:
    """
    Parking Impact Score (PIS™) Engine.
    
    Aggregates human, economic, and environmental impacts into a unified 0-100 score.
    While CSI measures congestion severity, PIS measures the real-world cost of that severity.
    """

    @staticmethod
    def calculate_pis(
        csi_score: float,
        commuter_impact_score: float,
        delay_impact_score: float,
        fuel_impact_score: float,
        environmental_impact_score: float,
        economic_impact_score: float,
        recovery_score: float
    ) -> Dict[str, Any]:
        """
        Calculates the final PIS score.
        """
        # Base weightings
        weights = {
            "csi_base": 0.20,             # Severity base
            "economic": 0.25,             # Economic burden (time + fuel cost)
            "commuter": 0.20,             # Number of people affected
            "environmental": 0.15,        # CO2 emissions
            "delay": 0.10,                # Total delay hours
            "recovery": 0.10              # Enforcement ROI potential
        }
        
        pis_score = (
            csi_score * weights["csi_base"] +
            economic_impact_score * weights["economic"] +
            commuter_impact_score * weights["commuter"] +
            environmental_impact_score * weights["environmental"] +
            delay_impact_score * weights["delay"] +
            recovery_score * weights["recovery"]
        )
        
        # PIS cannot be lower than CSI if CSI is very high (to ensure critical bottlenecks are flagged)
        if csi_score >= 80:
            pis_score = max(pis_score, csi_score * 0.95)
            
        pis_score = min(100.0, max(0.0, pis_score))
        
        return {
            "pis_score": round(pis_score, 2),
            "pis_components": {
                "csi_contribution": round(csi_score * weights["csi_base"], 2),
                "economic_contribution": round(economic_impact_score * weights["economic"], 2),
                "commuter_contribution": round(commuter_impact_score * weights["commuter"], 2),
                "environmental_contribution": round(environmental_impact_score * weights["environmental"], 2),
                "delay_contribution": round(delay_impact_score * weights["delay"], 2),
                "recovery_contribution": round(recovery_score * weights["recovery"], 2)
            }
        }
