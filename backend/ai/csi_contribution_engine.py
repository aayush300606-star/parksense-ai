from typing import Dict, Any, List


class CSIContributionEngine:
    """
    Analyzes the percentage contribution of each component to the final CSI score.
    
    This engine makes CSI™ fully transparent:
        "Violation Density drives 28% of this CSI score,
         Traffic Impact drives 22%, Capacity Loss drives 18%..."
    
    Critical for:
        - Dashboard pie charts
        - LLM Agent reasoning
        - Judicial defensibility
        - Enforcement justification reports
    """

    @staticmethod
    def analyze_contributions(
        csi_score: float,
        component_contributions: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """
        Computes percentage contribution of each component.
        
        Args:
            csi_score: The final CSI score (0-100)
            component_contributions: From CSIEngine.calculate_csi()
            
        Returns:
            dict with:
                - contributions: list of {name, label, percentage, weighted_value}
                  sorted by percentage descending
                - dominant_factor: name of the highest-contributing component
                - top_3_factors: names of the top 3 contributors
        """
        if csi_score <= 0:
            return {
                "contributions": [],
                "dominant_factor": "None",
                "top_3_factors": [],
            }

        contrib_list = []
        for name, data in component_contributions.items():
            weighted = data.get("weighted_value", 0)
            percentage = (weighted / csi_score * 100.0) if csi_score > 0 else 0.0

            contrib_list.append({
                "name": name,
                "label": data.get("label", name),
                "raw_value": data.get("raw_value", 0),
                "weight": data.get("weight", 0),
                "weighted_value": round(weighted, 2),
                "percentage": round(percentage, 1),
            })

        # Sort by percentage descending
        contrib_list.sort(key=lambda x: x["percentage"], reverse=True)

        dominant = contrib_list[0]["name"] if contrib_list else "None"
        top_3 = [c["name"] for c in contrib_list[:3]]

        return {
            "contributions": contrib_list,
            "dominant_factor": dominant,
            "top_3_factors": top_3,
        }
