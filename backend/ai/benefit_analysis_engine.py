from typing import Dict, Any

class BenefitAnalysisEngine:
    """
    Aggregates the total benefits of a simulation into a unified score.
    """

    @staticmethod
    def analyze(deltas: Dict[str, Any]) -> float:
        """
        Calculates an overall Benefit Score (0-100) indicating how impactful the intervention was.
        """
        score = 0.0
        
        # High impact if CSI drops significantly (e.g. 30 points)
        csi_drop = deltas['csi']['improvement']
        if csi_drop > 30:
            score += 40
        elif csi_drop > 15:
            score += 25
        elif csi_drop > 5:
            score += 10
            
        # Impact if delay is heavily reduced
        delay_saved = deltas['delay_hours']['improvement']
        if delay_saved > 500:
            score += 30
        elif delay_saved > 100:
            score += 15
        elif delay_saved > 0:
            score += 5
            
        # Impact if speed improves
        speed_imp = deltas['speed_kmh']['improvement']
        if speed_imp > 15:
            score += 30
        elif speed_imp > 5:
            score += 15
        elif speed_imp > 0:
            score += 5
            
        return min(100.0, score)
