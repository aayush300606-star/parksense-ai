from typing import Dict, Any

class EnforcementExplainabilityEngine:
    """
    Generates natural language reasoning for the operational commands.
    """

    @staticmethod
    def generate(
        priority_rank: int,
        csi_score: float,
        pis_score: float,
        is_emergency: bool,
        recommended_action: str,
        cap_rec: float,
        delay_rec: float
    ) -> str:
        """
        Produces human-readable operational reasoning.
        """
        parts = [f"Priority #{priority_rank}."]
        parts.append(f"Reason: CSI={csi_score:.1f}, PIS={pis_score:.1f}.")
        
        if is_emergency:
            parts.append("Critical Emergency Route.")
            
        parts.append(f"Action: {recommended_action}.")
        
        if cap_rec > 0:
            parts.append(f"Expected Capacity Recovery = {cap_rec:.1f}%.")
            parts.append(f"Expected Delay Reduction = {delay_rec:.1f} hours.")
            
        return " ".join(parts)
