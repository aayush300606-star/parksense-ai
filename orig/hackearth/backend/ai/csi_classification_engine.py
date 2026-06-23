from typing import Dict


class CSIClassificationEngine:
    """
    Classifies CSI scores into severity levels with color codes
    and priority designations.
    
    Levels:
        0-20   Very Low   Green        P5
        20-40  Low        Light Green  P4
        40-60  Moderate   Yellow       P3
        60-80  High       Orange       P2
        80-100 Critical   Red          P1
    """

    SEVERITY_BANDS = [
        {"min": 80, "max": 100, "level": "Critical",  "color": "#DC2626", "color_name": "Red",         "priority": "P1", "priority_label": "P1-Immediate"},
        {"min": 60, "max": 80,  "level": "High",      "color": "#F97316", "color_name": "Orange",      "priority": "P2", "priority_label": "P2-High"},
        {"min": 40, "max": 60,  "level": "Moderate",   "color": "#EAB308", "color_name": "Yellow",      "priority": "P3", "priority_label": "P3-Moderate"},
        {"min": 20, "max": 40,  "level": "Low",        "color": "#84CC16", "color_name": "Light Green", "priority": "P4", "priority_label": "P4-Low"},
        {"min": 0,  "max": 20,  "level": "Very Low",   "color": "#22C55E", "color_name": "Green",       "priority": "P5", "priority_label": "P5-Monitor"},
    ]

    @staticmethod
    def classify(csi_score: float) -> Dict:
        """
        Classifies a CSI score into severity level, color, and priority.
        
        Args:
            csi_score: The CSI score (0-100)
            
        Returns:
            dict with csi_level, csi_color, csi_color_name, csi_priority,
            csi_priority_label
        """
        score = min(100.0, max(0.0, csi_score))

        for band in CSIClassificationEngine.SEVERITY_BANDS:
            if score >= band["min"]:
                return {
                    "csi_level": band["level"],
                    "csi_color": band["color"],
                    "csi_color_name": band["color_name"],
                    "csi_priority": band["priority"],
                    "csi_priority_label": band["priority_label"],
                }

        # Fallback (should never reach)
        return {
            "csi_level": "Very Low",
            "csi_color": "#22C55E",
            "csi_color_name": "Green",
            "csi_priority": "P5",
            "csi_priority_label": "P5-Monitor",
        }
