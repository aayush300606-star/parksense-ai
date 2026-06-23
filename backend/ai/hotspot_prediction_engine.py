from typing import Dict, Any

class HotspotPredictionEngine:
    """
    Predicts the probability of a location becoming/remaining a severe hotspot.
    """

    @staticmethod
    def predict_probability(predicted_csi: float, current_csi: float) -> Dict[str, Any]:
        """
        Maps the forecasted CSI and delta into a raw probability (0-100%).
        """
        # Baseline probability tied to the forecasted CSI
        base_prob = predicted_csi
        
        # If the CSI is increasing sharply, probability of acute congestion goes up
        delta = predicted_csi - current_csi
        if delta > 10:
            prob = base_prob + 15
        elif delta > 5:
            prob = base_prob + 10
        elif delta < -10:
            prob = base_prob - 10
        else:
            prob = base_prob
            
        prob = min(99.0, max(1.0, prob))
        
        if prob >= 80:
            risk_level = "Critical Risk"
        elif prob >= 60:
            risk_level = "High Risk"
        elif prob >= 40:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"
            
        return {
            "hotspot_probability": round(prob, 1),
            "hotspot_risk_level": risk_level,
            "prediction_confidence": 0.88
        }
