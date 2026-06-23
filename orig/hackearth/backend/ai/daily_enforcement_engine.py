from typing import Dict, Any, List

class DailyEnforcementEngine:
    """
    Generates the final daily operational plan.
    """

    @staticmethod
    def compile_plan(routes: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Takes the optimized routes and wraps them into a daily plan object.
        """
        total_hotspots = 0
        expected_csi_total = 0.0
        
        team_plans = []
        for team, hotspots in routes.items():
            total_hotspots += len(hotspots)
            team_csi_red = sum([h['expected_csi_reduction'] for h in hotspots])
            expected_csi_total += team_csi_red
            
            team_plans.append({
                "team_name": team,
                "assigned_interventions": len(hotspots),
                "expected_team_csi_reduction": round(team_csi_red, 1),
                "route": hotspots
            })
            
        return {
            "total_teams_deployed": len(routes),
            "total_interventions_planned": total_hotspots,
            "expected_city_csi_reduction": round(expected_csi_total, 1),
            "team_schedules": team_plans
        }
