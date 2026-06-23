from typing import Dict, List, Any


class AdaptiveWeightingEngine:
    """
    Context-dependent dynamic weight allocation for CSI™.
    
    Unlike fixed-weight systems, this engine adjusts component weights
    based on the urban context surrounding each hotspot:
    
        Near Hospital     → Boost emergency_impact weight
        Near Metro/Transit → Boost poi_density and critical_infrastructure weights
        Near Major Junction → Boost junction_influence weight
        High Violation Density → Boost violation_density weight
        Emergency Route → Amplify emergency_impact to dominant factor
    
    The base weight profile is modified by context multipliers.
    After adjustment, weights are renormalized to sum to 1.0.
    
    This makes CSI™ adaptive: two hotspots with identical traffic impact
    but different surroundings will receive different CSI scores.
    """

    # Base weights (default profile)
    BASE_WEIGHTS = {
        "violation_density":       0.15,
        "capacity_loss":           0.22,
        "traffic_impact":          0.25,
        "junction_influence":      0.12,
        "poi_density":             0.08,
        "critical_infrastructure": 0.10,
        "emergency_impact":        0.08,
    }

    # Context multiplier rules
    # Each rule checks a condition and applies multipliers to specific weights
    CONTEXT_RULES = [
        {
            "name": "Hospital Proximity",
            "condition": lambda ctx: any(
                p.get("poi_type") == "HOSPITAL" for p in ctx.get("critical_pois", [])
            ),
            "multipliers": {
                "emergency_impact": 1.8,
                "critical_infrastructure": 1.4,
            },
            "reasoning": "Hospital detected nearby — emergency access becomes critical",
        },
        {
            "name": "Transit Hub Proximity",
            "condition": lambda ctx: any(
                p.get("poi_type") in ("METRO_STATION", "BUS_STATION", "RAILWAY_STATION")
                for p in ctx.get("critical_pois", [])
            ),
            "multipliers": {
                "poi_density": 1.6,
                "critical_infrastructure": 1.3,
                "traffic_impact": 1.2,
            },
            "reasoning": "Transit hub nearby — public transport disruption amplified",
        },
        {
            "name": "Major Junction Proximity",
            "condition": lambda ctx: ctx.get("junction_distance_m", 999) <= 50,
            "multipliers": {
                "junction_influence": 2.0,
                "traffic_impact": 1.3,
            },
            "reasoning": "Major junction within 50m — intersection queue spillback risk",
        },
        {
            "name": "Critical Intersection",
            "condition": lambda ctx: ctx.get("junction_importance_level") == "Critical Intersection",
            "multipliers": {
                "junction_influence": 1.6,
                "capacity_loss": 1.2,
            },
            "reasoning": "Critical intersection — network-wide impact potential",
        },
        {
            "name": "Emergency Route Impact",
            "condition": lambda ctx: ctx.get("emergency_route_impact", False),
            "multipliers": {
                "emergency_impact": 2.5,
                "critical_infrastructure": 1.5,
                "capacity_loss": 1.3,
            },
            "reasoning": "Emergency route blocked — life-safety priority override",
        },
        {
            "name": "High Violation Density",
            "condition": lambda ctx: ctx.get("violation_density_score", 0) >= 70,
            "multipliers": {
                "violation_density": 1.5,
                "capacity_loss": 1.2,
            },
            "reasoning": "Extreme violation clustering — systemic enforcement failure",
        },
        {
            "name": "Major Arterial Road",
            "condition": lambda ctx: ctx.get("road_hierarchy") == "Major Arterial",
            "multipliers": {
                "traffic_impact": 1.3,
                "capacity_loss": 1.2,
            },
            "reasoning": "Major arterial — high traffic volume amplifies impact",
        },
        {
            "name": "Signalized Junction",
            "condition": lambda ctx: (
                ctx.get("junction_signalized", False) and
                ctx.get("junction_distance_m", 999) <= 100
            ),
            "multipliers": {
                "junction_influence": 1.4,
                "traffic_impact": 1.1,
            },
            "reasoning": "Signalized junction nearby — signal cycle failure risk",
        },
    ]

    @staticmethod
    def compute_weights(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes context-adaptive weights for the CSI formula.
        
        Args:
            context: Dict containing all upstream intelligence:
                - junction_distance_m, junction_importance_level, junction_signalized
                - critical_pois (list of POI dicts)
                - emergency_route_impact
                - violation_density_score
                - road_hierarchy
                
        Returns:
            dict with:
                - weights: dict of {component: weight} (sums to 1.0)
                - rules_applied: list of rule names that fired
                - reasoning: list of reasoning strings
                - weight_profile: "Adaptive" or "Base"
        """
        # Start with base weights
        adjusted = dict(AdaptiveWeightingEngine.BASE_WEIGHTS)
        rules_applied = []
        reasoning = []

        # Apply context rules
        for rule in AdaptiveWeightingEngine.CONTEXT_RULES:
            try:
                if rule["condition"](context):
                    for component, multiplier in rule["multipliers"].items():
                        if component in adjusted:
                            adjusted[component] *= multiplier
                    rules_applied.append(rule["name"])
                    reasoning.append(rule["reasoning"])
            except Exception:
                # Graceful degradation: if a rule fails, skip it
                continue

        # Renormalize to sum to 1.0
        total = sum(adjusted.values())
        if total > 0:
            normalized = {k: v / total for k, v in adjusted.items()}
        else:
            normalized = dict(AdaptiveWeightingEngine.BASE_WEIGHTS)

        # Round for readability
        normalized = {k: round(v, 4) for k, v in normalized.items()}

        # Verify sum ≈ 1.0 (fix floating point drift)
        weight_sum = sum(normalized.values())
        if abs(weight_sum - 1.0) > 0.001:
            # Adjust the largest weight to absorb the rounding error
            max_key = max(normalized, key=normalized.get)
            normalized[max_key] += round(1.0 - weight_sum, 4)

        return {
            "weights": normalized,
            "rules_applied": rules_applied,
            "rules_applied_count": len(rules_applied),
            "reasoning": reasoning,
            "weight_profile": "Adaptive" if rules_applied else "Base",
        }
