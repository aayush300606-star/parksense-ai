from typing import Dict, Any


class PISClassificationEngine:
    """
    Classifies the continuous 0-100 PIS score into distinct impact levels.
    """

    @staticmethod
    def classify(pis_score: float) -> Dict[str, str]:
        """
        Maps score to level, priority, and hex color code.
        """
        if pis_score >= 80:
            return {
                "pis_level": "Critical",
                "pis_priority": "P1",
                "pis_color": "#FF0000",
                "pis_color_name": "Red"
            }
        elif pis_score >= 60:
            return {
                "pis_level": "High",
                "pis_priority": "P2",
                "pis_color": "#FF8C00",
                "pis_color_name": "Orange"
            }
        elif pis_score >= 40:
            return {
                "pis_level": "Moderate",
                "pis_priority": "P3",
                "pis_color": "#FFD700",
                "pis_color_name": "Yellow"
            }
        elif pis_score >= 20:
            return {
                "pis_level": "Low",
                "pis_priority": "P4",
                "pis_color": "#9ACD32",
                "pis_color_name": "Yellow-Green"
            }
        else:
            return {
                "pis_level": "Minimal",
                "pis_priority": "P5",
                "pis_color": "#32CD32",
                "pis_color_name": "Green"
            }
