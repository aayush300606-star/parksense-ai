from typing import Dict, List, Any

class EnforcementForecastEngine:
    """
    Translates predictions into actionable patrol recommendations.
    """

    @staticmethod
    def generate_patrol_recommendations(predictions_data: List[Dict]) -> List[Dict]:
        """
        Generates a list of recommended patrol zones and optimal times.
        """
        recommendations = []
        
        for p in predictions_data:
            # Find the horizon with the highest predicted PIS
            worst_horizon = None
            max_pis = -1
            
            for horizon, fcast in p['forecasts'].items():
                if fcast['predicted_pis'] > max_pis:
                    max_pis = fcast['predicted_pis']
                    worst_horizon = horizon
                    
            if max_pis >= 60:
                reco = {
                    "hotspot_id": p['hotspot_id'],
                    "road_name": p['road_name'],
                    "recommended_patrol_time": p['forecasts'][worst_horizon]['target_time'],
                    "priority_forecast": p['forecasts'][worst_horizon]['hotspot_risk_level'],
                    "expected_intervention_benefit": "High" if max_pis >= 80 else "Moderate"
                }
                recommendations.append(reco)
                
        return sorted(recommendations, key=lambda x: x['priority_forecast'])
