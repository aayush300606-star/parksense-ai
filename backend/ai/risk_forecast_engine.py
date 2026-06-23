from typing import Dict, List, Any

class RiskForecastEngine:
    """
    Identifies future high-risk zones across the city.
    """

    @staticmethod
    def extract_risk_zones(predictions_data: List[Dict]) -> List[Dict]:
        """
        Filters the predictions to return only critical future risks.
        """
        high_risks = []
        for p in predictions_data:
            # If any horizon predicts high risk
            for horizon, fcast in p['forecasts'].items():
                if fcast['hotspot_probability'] >= 75:
                    high_risks.append({
                        "hotspot_id": p['hotspot_id'],
                        "road_name": p['road_name'],
                        "horizon": horizon,
                        "predicted_csi": fcast['predicted_csi'],
                        "risk_level": fcast['hotspot_risk_level'],
                        "explanation": fcast['explanation']
                    })
                    break # Record once per hotspot
                    
        return sorted(high_risks, key=lambda x: x['predicted_csi'], reverse=True)
