from typing import Dict, Any

class CSIRecalculationEngine:
    """
    Recalculates the Congestion Severity Index (CSI) based on simulated physical conditions.
    """

    @staticmethod
    def recalculate(baseline_csi: float, baseline_cap_loss: float, new_cap_loss: float) -> float:
        """
        Estimates the new CSI. Since CSI is heavily driven by capacity loss, 
        we scale the physical components of CSI downwards.
        """
        # If we recovered 100% of the lost capacity, the physical component of CSI drops to 0.
        # However, volume/junction influence still exist.
        # We assume capacity loss accounts for roughly 60% of the CSI variance.
        
        if baseline_cap_loss == 0:
            return baseline_csi
            
        recovery_ratio = (baseline_cap_loss - new_cap_loss) / baseline_cap_loss
        
        # Max CSI reduction is 60% of original (due to base traffic volume remaining)
        max_reduction = baseline_csi * 0.60
        
        actual_reduction = max_reduction * recovery_ratio
        
        new_csi = baseline_csi - actual_reduction
        
        return round(max(0.0, new_csi), 2)
