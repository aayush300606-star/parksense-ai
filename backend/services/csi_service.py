import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.csi_intelligence import CSIIntelligence
from ..ai.violation_density import DENSITY_JSON_PATH
from ..services.road_service import ROAD_JSON_PATH
from ..services.road_impact_service import ROAD_IMPACT_JSON_PATH
from ..services.traffic_intelligence_service import TRAFFIC_JSON_PATH
from ..services.context_intelligence_service import CONTEXT_JSON_PATH

from ..ai.csi_component_engine import CSIComponentEngine
from ..ai.adaptive_weighting_engine import AdaptiveWeightingEngine
from ..ai.csi_engine import CSIEngine
from ..ai.csi_contribution_engine import CSIContributionEngine
from ..ai.csi_classification_engine import CSIClassificationEngine
from ..ai.csi_explainability_engine import CSIExplainabilityEngine
from ..ai.enforcement_priority_engine import EnforcementPriorityEngine
from ..ai.temporal_pattern_engine import TemporalPatternEngine
from ..ai.hotspot_ranking_engine import HotspotRankingEngine

CSI_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'csi_results.json')
CSI_SUMMARY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'csi_summary.json')
PRIORITY_RANKING_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'priority_ranking.json')
TOP_CRITICAL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'top_critical_hotspots.json')
TOP_ROADS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'top_high_impact_roads.json')
TEMPORAL_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'temporal_patterns.json')

# Keep backward compat with old paths
CSI_RANKINGS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'csi_rankings.json')
CSI_CITY_ANALYTICS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'csi_city_analytics.json')


class CSIService:
    """
    Orchestrator for the Adaptive CSI™ Engine.
    
    Pipeline:
        All 5 Upstream Intelligence Layers
            → Stage 1: Temporal Pattern Analysis
            → Stage 2: CSI Component Validation (7 signals)
            → Stage 3: Adaptive Weighting (context-dependent)
            → Stage 4: CSI Calculation (weighted aggregation)
            → Stage 5: Contribution Analysis (percentage breakdown)
            → Stage 6: CSI Classification (level, color, priority)
            → Stage 7: Enforcement Priority (expected benefits)
            → Stage 8: Ranking (city-wide ordering)
            → Stage 9: Explainability (human + machine)
            → Stage 10: JSON Output Generation (5 files)
    """

    @staticmethod
    def generate_all():
        """Executes the full Adaptive CSI™ pipeline."""
        deps = {
            "Density": DENSITY_JSON_PATH,
            "Road Intelligence": ROAD_JSON_PATH,
            "Road Impact": ROAD_IMPACT_JSON_PATH,
            "Traffic Intelligence": TRAFFIC_JSON_PATH,
            "Context Intelligence": CONTEXT_JSON_PATH,
        }
        for name, path in deps.items():
            if not os.path.exists(path):
                print(f"{name} data missing at {path}. Run upstream pipeline first.")
                return []

        with open(DENSITY_JSON_PATH, 'r') as f:
            hotspots = json.load(f)
        with open(ROAD_JSON_PATH, 'r') as f:
            roads = {r['hotspot_id']: r for r in json.load(f)}
        with open(ROAD_IMPACT_JSON_PATH, 'r') as f:
            impacts = {imp['hotspot_id']: imp for imp in json.load(f)}
        with open(TRAFFIC_JSON_PATH, 'r') as f:
            traffic = {t['hotspot_id']: t for t in json.load(f)}
        with open(CONTEXT_JSON_PATH, 'r') as f:
            context = {c['hotspot_id']: c for c in json.load(f)}

        # Load POI intelligence for critical_pois in context
        poi_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'poi_intelligence.json')
        poi_map = {}
        if os.path.exists(poi_path):
            with open(poi_path, 'r') as f:
                for p in json.load(f):
                    poi_map[p['hotspot_id']] = p.get('pois', [])

        # === STAGE 1: Temporal Pattern Analysis ===
        print("  Analyzing temporal violation patterns...")
        temporal_patterns = TemporalPatternEngine.analyze_temporal_patterns(hotspots)
        temporal_map = {t['hotspot_id']: t for t in temporal_patterns}

        os.makedirs(os.path.dirname(TEMPORAL_JSON_PATH), exist_ok=True)
        with open(TEMPORAL_JSON_PATH, 'w') as f:
            json.dump(temporal_patterns, f, indent=2)

        # Pre-process: build raw data for ranking
        raw_csi_data = []

        for hotspot in hotspots:
            hid = hotspot['hotspot_id']
            road = roads.get(hid, {})
            impact = impacts.get(hid, {})
            traf = traffic.get(hid, {})
            ctx = context.get(hid, {})
            temporal = temporal_map.get(hid, {})
            critical_pois = poi_map.get(hid, [])

            road_name = road.get('road_name', 'Unknown Road')
            road_hierarchy = road.get('road_hierarchy', 'Residential')
            road_priority = road.get('road_priority_score', 40)

            # Upstream signal values
            violation_density_score = hotspot.get('violation_density_score', 0)
            capacity_loss = impact.get('capacity_loss_percentage', 0)
            congestion_impact = traf.get('congestion_impact_score', 0)
            junction_influence = ctx.get('junction_influence_score', 0)
            poi_density = ctx.get('poi_density_score', 0)
            critical_infra = ctx.get('critical_infrastructure_score', 0)
            emergency_impact = ctx.get('emergency_impact_score', 0)

            speed_reduction = traf.get('speed_reduction_percentage', 0)
            annual_delay = traf.get('annual_delay_vehicle_hours', 0)
            junction_type = ctx.get('junction_type', '')
            junction_distance = ctx.get('junction_distance_m', 999)
            junction_signalized = ctx.get('junction_signalized', False)
            junction_importance_level = ctx.get('junction_importance_level', '')
            emergency_route = ctx.get('emergency_route_impact', False)
            violations = hotspot.get('violations', 0)

            road_confidence = min(
                road.get('confidence_scores', {}).values() or [0.80]
            ) if road.get('confidence_scores') else 0.80

            # === STAGE 2: Component Validation ===
            comp_result = CSIComponentEngine.gather_components(
                violation_density_score=violation_density_score,
                capacity_loss_percentage=capacity_loss,
                congestion_impact_score=congestion_impact,
                junction_influence_score=junction_influence,
                poi_density_score=poi_density,
                critical_infrastructure_score=critical_infra,
                emergency_impact_score=emergency_impact,
                density_confidence=0.90,
                road_confidence=road_confidence,
                traffic_confidence=traf.get('confidence', 0.85),
                junction_confidence=ctx.get('confidence', 0.75),
                poi_confidence=0.70,
                infra_confidence=0.70,
                emergency_confidence=0.75,
            )

            # === STAGE 3: Adaptive Weighting ===
            weight_context = {
                "junction_distance_m": junction_distance,
                "junction_importance_level": junction_importance_level,
                "junction_signalized": junction_signalized,
                "critical_pois": critical_pois,
                "emergency_route_impact": emergency_route,
                "violation_density_score": violation_density_score,
                "road_hierarchy": road_hierarchy,
            }
            weight_result = AdaptiveWeightingEngine.compute_weights(weight_context)

            # === STAGE 4: CSI Calculation ===
            csi_result = CSIEngine.calculate_csi(
                components=comp_result["components"],
                weights=weight_result["weights"]
            )

            # === STAGE 5: Contribution Analysis ===
            contrib_result = CSIContributionEngine.analyze_contributions(
                csi_score=csi_result["csi_score"],
                component_contributions=csi_result["component_contributions"]
            )

            # === STAGE 6: Classification ===
            class_result = CSIClassificationEngine.classify(csi_result["csi_score"])

            # === STAGE 7: Enforcement Priority ===
            enforce_result = EnforcementPriorityEngine.calculate_enforcement_priority(
                csi_score=csi_result["csi_score"],
                csi_level=class_result["csi_level"],
                capacity_loss_percentage=capacity_loss,
                speed_reduction_percentage=speed_reduction,
                road_hierarchy=road_hierarchy,
                emergency_route_impact=emergency_route,
                violation_count=violations,
                annual_delay_vehicle_hours=annual_delay,
            )

            raw_csi_data.append({
                "hotspot_id": hid,
                "road_name": road_name,
                "road_hierarchy": road_hierarchy,
                "latitude": hotspot.get('latitude', 0),
                "longitude": hotspot.get('longitude', 0),
                "csi_score": csi_result["csi_score"],
                **class_result,
                "component_scores": {
                    k: v["value"] for k, v in comp_result["components"].items()
                },
                "component_weights": weight_result["weights"],
                "weight_profile": weight_result["weight_profile"],
                "rules_applied": weight_result["rules_applied"],
                "adaptive_reasoning": weight_result["reasoning"],
                "component_contributions": contrib_result["contributions"],
                "dominant_factor": contrib_result["dominant_factor"],
                "top_3_factors": contrib_result["top_3_factors"],
                **enforce_result,
                "violation_density_score": violation_density_score,
                "capacity_loss_percentage": capacity_loss,
                "speed_reduction_percentage": speed_reduction,
                "congestion_impact_score": congestion_impact,
                "annual_delay_vehicle_hours": annual_delay,
                "junction_type": junction_type,
                "junction_distance_m": junction_distance,
                "emergency_route_impact": emergency_route,
                "violations": violations,
                "peak_hour": temporal.get('peak_hour', 10),
                "peak_hour_label": temporal.get('peak_hour_label', '10:00 - 11:00'),
                "peak_day": temporal.get('peak_day', 'Wednesday'),
                "temporal_recurrence_score": temporal.get('temporal_recurrence_score', 50),
                "critical_pois": critical_pois,
                "confidence": csi_result["confidence"],
            })

        # === STAGE 8: Ranking ===
        ranked = HotspotRankingEngine.generate_rankings(raw_csi_data)

        # === STAGE 9: Explainability ===
        csi_objects = []
        for item in ranked:
            explain = CSIExplainabilityEngine.generate_explanation(
                hotspot_id=item["hotspot_id"],
                road_name=item["road_name"],
                road_hierarchy=item["road_hierarchy"],
                csi_score=item["csi_score"],
                csi_level=item["csi_level"],
                csi_color_name=item["csi_color_name"],
                rank=item["rank"],
                total_hotspots=len(ranked),
                percentile=item["percentile"],
                contributions=item["component_contributions"],
                adaptive_reasoning=item["adaptive_reasoning"],
                weight_profile=item["weight_profile"],
                speed_reduction_percentage=item["speed_reduction_percentage"],
                capacity_loss_percentage=item["capacity_loss_percentage"],
                annual_delay_vehicle_hours=item["annual_delay_vehicle_hours"],
                junction_type=item.get("junction_type", ""),
                junction_distance_m=item.get("junction_distance_m", 999),
                emergency_route_impact=item["emergency_route_impact"],
                critical_pois=item.get("critical_pois", []),
                pis_score=item["priority_score"],
                pis_priority=item["priority_level"],
            )

            obj = CSIIntelligence(
                hotspot_id=item["hotspot_id"],
                road_name=item["road_name"],
                road_hierarchy=item["road_hierarchy"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                csi_score=item["csi_score"],
                csi_level=item["csi_level"],
                csi_color=item["csi_color"],
                csi_color_name=item["csi_color_name"],
                csi_priority=item["csi_priority"],
                csi_priority_label=item["csi_priority_label"],
                component_scores=item["component_scores"],
                component_weights=item["component_weights"],
                weight_profile=item["weight_profile"],
                rules_applied=item["rules_applied"],
                adaptive_reasoning=item["adaptive_reasoning"],
                component_contributions=item["component_contributions"],
                dominant_factor=item["dominant_factor"],
                top_3_factors=item["top_3_factors"],
                priority_score=item["priority_score"],
                priority_level=item["priority_level"],
                expected_capacity_recovery=item["expected_capacity_recovery"],
                expected_speed_improvement=item["expected_speed_improvement"],
                daily_vehicles_affected=item["daily_vehicles_affected"],
                annual_delay_savings_hours=item["annual_delay_savings_hours"],
                enforcement_recommendation=item["enforcement_recommendation"],
                rank=item["rank"],
                percentile=item["percentile"],
                tier=item["tier"],
                violation_density_score=item["violation_density_score"],
                capacity_loss_percentage=item["capacity_loss_percentage"],
                speed_reduction_percentage=item["speed_reduction_percentage"],
                congestion_impact_score=item["congestion_impact_score"],
                annual_delay_vehicle_hours=item["annual_delay_vehicle_hours"],
                junction_type=item.get("junction_type", ""),
                junction_distance_m=item.get("junction_distance_m", 0),
                emergency_route_impact=item["emergency_route_impact"],
                violations=item["violations"],
                peak_hour=item["peak_hour"],
                peak_hour_label=item["peak_hour_label"],
                peak_day=item["peak_day"],
                temporal_recurrence_score=item["temporal_recurrence_score"],
                human_explanation=explain["human_explanation"],
                key_factors=explain["key_factors"],
                recommendation=explain["recommendation"],
                confidence=item["confidence"],
                generated_at=datetime.now(),
            )
            csi_objects.append(obj)

        # === STAGE 10: JSON Output Generation ===
        os.makedirs(os.path.dirname(CSI_JSON_PATH), exist_ok=True)

        # 1. Full CSI results
        json_data = [obj.dict() for obj in csi_objects]
        with open(CSI_JSON_PATH, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)

        # 2. Priority ranking (compact)
        rankings = [{
            "rank": d["rank"],
            "hotspot_id": d["hotspot_id"],
            "road_name": d["road_name"],
            "road_hierarchy": d["road_hierarchy"],
            "csi_score": d["csi_score"],
            "csi_level": d["csi_level"],
            "csi_color": d["csi_color"],
            "priority_score": d["priority_score"],
            "priority_level": d["priority_level"],
            "expected_capacity_recovery": d["expected_capacity_recovery"],
            "expected_speed_improvement": d["expected_speed_improvement"],
            "percentile": d["percentile"],
            "tier": d["tier"],
        } for d in json_data]
        with open(PRIORITY_RANKING_PATH, 'w') as f:
            json.dump(rankings, f, indent=2)
        # Backward compat
        with open(CSI_RANKINGS_JSON_PATH, 'w') as f:
            json.dump(rankings, f, indent=2)

        # 3. Top critical hotspots (CSI >= 60 or top 20)
        critical = [d for d in json_data if d["csi_score"] >= 60][:20]
        if len(critical) < 10:
            critical = json_data[:20]  # Fall back to top 20
        with open(TOP_CRITICAL_PATH, 'w') as f:
            json.dump(critical, f, indent=2, default=str)

        # 4. Top high-impact roads (grouped by road name)
        road_scores = {}
        for d in json_data:
            rn = d["road_name"]
            if rn not in road_scores:
                road_scores[rn] = {
                    "road_name": rn,
                    "road_hierarchy": d["road_hierarchy"],
                    "hotspot_count": 0,
                    "avg_csi": 0,
                    "max_csi": 0,
                    "total_annual_delay": 0,
                }
            road_scores[rn]["hotspot_count"] += 1
            road_scores[rn]["avg_csi"] += d["csi_score"]
            road_scores[rn]["max_csi"] = max(road_scores[rn]["max_csi"], d["csi_score"])
            road_scores[rn]["total_annual_delay"] += d["annual_delay_vehicle_hours"]

        for rn in road_scores:
            road_scores[rn]["avg_csi"] = round(
                road_scores[rn]["avg_csi"] / road_scores[rn]["hotspot_count"], 2
            )
            road_scores[rn]["total_annual_delay"] = round(road_scores[rn]["total_annual_delay"], 0)

        top_roads = sorted(road_scores.values(), key=lambda x: x["max_csi"], reverse=True)[:20]
        with open(TOP_ROADS_PATH, 'w') as f:
            json.dump(top_roads, f, indent=2)

        # 5. CSI Summary (city-wide analytics)
        city_analytics = HotspotRankingEngine.generate_city_analytics(ranked)
        # Enrich with adaptive weighting stats
        adaptive_count = sum(1 for d in json_data if d["weight_profile"] == "Adaptive")
        city_analytics["adaptive_weighting_stats"] = {
            "adaptive_profiles": adaptive_count,
            "base_profiles": len(json_data) - adaptive_count,
            "adaptive_percentage": round(adaptive_count / max(1, len(json_data)) * 100, 1),
        }
        # Dominant factor distribution
        factor_dist = {}
        for d in json_data:
            f = d.get("dominant_factor", "Unknown")
            factor_dist[f] = factor_dist.get(f, 0) + 1
        city_analytics["dominant_factor_distribution"] = factor_dist

        with open(CSI_SUMMARY_PATH, 'w') as f:
            json.dump(city_analytics, f, indent=2, default=str)
        # Backward compat
        with open(CSI_CITY_ANALYTICS_JSON_PATH, 'w') as f:
            json.dump(city_analytics, f, indent=2, default=str)

        print(f"Adaptive CSI Intelligence generated for {len(csi_objects)} hotspots.")
        return csi_objects

    # === Data Access Methods ===

    @staticmethod
    def get_all_csi() -> List[Dict[str, Any]]:
        if not os.path.exists(CSI_JSON_PATH):
            CSIService.generate_all()
        with open(CSI_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_rankings(top: int = None) -> List[Dict[str, Any]]:
        if not os.path.exists(PRIORITY_RANKING_PATH):
            CSIService.generate_all()
        with open(PRIORITY_RANKING_PATH, 'r') as f:
            data = json.load(f)
        if top:
            return data[:min(top, len(data))]
        return data

    @staticmethod
    def get_pis() -> List[Dict[str, Any]]:
        all_csi = CSIService.get_all_csi()
        return [{
            "hotspot_id": d["hotspot_id"],
            "road_name": d["road_name"],
            "priority_score": d["priority_score"],
            "priority_level": d["priority_level"],
            "expected_capacity_recovery": d["expected_capacity_recovery"],
            "expected_speed_improvement": d["expected_speed_improvement"],
            "enforcement_recommendation": d["enforcement_recommendation"],
            "csi_score": d["csi_score"],
            "csi_level": d["csi_level"],
            "emergency_route_impact": d["emergency_route_impact"],
        } for d in all_csi]

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        if not os.path.exists(CSI_SUMMARY_PATH):
            CSIService.generate_all()
        with open(CSI_SUMMARY_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_top_critical() -> List[Dict[str, Any]]:
        if not os.path.exists(TOP_CRITICAL_PATH):
            CSIService.generate_all()
        with open(TOP_CRITICAL_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_temporal_patterns() -> List[Dict[str, Any]]:
        if not os.path.exists(TEMPORAL_JSON_PATH):
            CSIService.generate_all()
        with open(TEMPORAL_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_top_roads() -> List[Dict[str, Any]]:
        if not os.path.exists(TOP_ROADS_PATH):
            CSIService.generate_all()
        with open(TOP_ROADS_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_heatmap_layer() -> List[Dict[str, Any]]:
        """Returns a lightweight layer for heatmap rendering."""
        all_csi = CSIService.get_all_csi()
        return [{
            "lat": d["latitude"],
            "lng": d["longitude"],
            "weight": d["csi_score"] / 100.0,
            "csi_score": d["csi_score"],
            "csi_level": d["csi_level"],
            "csi_color": d["csi_color"],
            "road_name": d["road_name"],
            "hotspot_id": d["hotspot_id"],
        } for d in all_csi]

    @staticmethod
    def get_priority_layer() -> List[Dict[str, Any]]:
        """Returns a lightweight layer for priority marker rendering."""
        all_csi = CSIService.get_all_csi()
        return [{
            "lat": d["latitude"],
            "lng": d["longitude"],
            "priority_level": d["priority_level"],
            "priority_score": d["priority_score"],
            "csi_score": d["csi_score"],
            "csi_color": d["csi_color"],
            "road_name": d["road_name"],
            "hotspot_id": d["hotspot_id"],
            "expected_capacity_recovery": d["expected_capacity_recovery"],
        } for d in all_csi]
