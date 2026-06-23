import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.context_intelligence import ContextIntelligence
from ..services.road_service import ROAD_JSON_PATH
from ..services.road_impact_service import ROAD_IMPACT_JSON_PATH
from ..ai.violation_density import DENSITY_JSON_PATH

from ..ai.geospatial_index import GeospatialIndex
from ..ai.junction_intelligence_engine import JunctionIntelligenceEngine
from ..ai.junction_importance_engine import JunctionImportanceEngine
from ..ai.junction_influence_engine import JunctionInfluenceEngine
from ..ai.poi_intelligence_engine import POIIntelligenceEngine
from ..ai.critical_infrastructure_engine import CriticalInfrastructureEngine
from ..ai.emergency_access_engine import EmergencyAccessEngine
from ..ai.poi_density_engine import POIDensityEngine
from ..ai.context_importance_engine import ContextImportanceEngine
from ..ai.context_explainability_engine import ContextExplainabilityEngine

CONTEXT_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'context_intelligence.json')
JUNCTION_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'junction_intelligence.json')
POI_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'poi_intelligence.json')
CRITICAL_INFRA_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'critical_infrastructure.json')
EMERGENCY_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'emergency_access.json')


class ContextIntelligenceService:
    """
    Orchestrator for the Context Intelligence Engine.
    
    Pipeline:
        Hotspot Data + Road Intelligence + Road Impact
            → Geospatial KDTree Index
            → Junction Intelligence Engine
            → Junction Importance Engine
            → Junction Influence Engine
            → POI Intelligence Engine (multi-radius)
            → Critical Infrastructure Engine
            → Emergency Access Engine
            → POI Density Engine (with normalization)
            → Context Importance Engine
            → Context Explainability Engine
            → Structured JSON Outputs (5 files)
    """

    @staticmethod
    def generate_all():
        """
        Executes the full context intelligence pipeline.
        """
        # Load dependencies
        if not os.path.exists(DENSITY_JSON_PATH):
            print("Hotspot density data missing. Run preprocessing first.")
            return []
        if not os.path.exists(ROAD_JSON_PATH):
            print("Road Intelligence data missing. Run Road Intelligence first.")
            return []
        if not os.path.exists(ROAD_IMPACT_JSON_PATH):
            print("Road Impact data missing. Run Effective Width Engine first.")
            return []

        with open(DENSITY_JSON_PATH, 'r') as f:
            hotspots = json.load(f)
        with open(ROAD_JSON_PATH, 'r') as f:
            roads = {r['hotspot_id']: r for r in json.load(f)}
        with open(ROAD_IMPACT_JSON_PATH, 'r') as f:
            impacts = {imp['hotspot_id']: imp for imp in json.load(f)}

        # === STAGE 0: Build KDTree Geospatial Index ===
        print(f"  Building KDTree index for {len(hotspots)} hotspots...")
        geo_index = GeospatialIndex(hotspots)

        context_objects = []
        all_density_data = []  # Collect for batch normalization
        junction_intelligence_data = []
        poi_intelligence_data = []
        critical_infra_data = []
        emergency_data = []

        for hotspot in hotspots:
            hid = hotspot['hotspot_id']
            lat = hotspot['latitude']
            lon = hotspot['longitude']
            location_name = hotspot.get('location_name', '')

            road = roads.get(hid, {})
            impact = impacts.get(hid, {})

            road_name = road.get('road_name', 'Unknown Road')
            road_hierarchy = road.get('road_hierarchy', 'Residential')
            road_priority = road.get('road_priority_score', 40)
            capacity_loss = impact.get('capacity_loss_percentage', 0.0)

            # === STAGE 1: Nearby hotspot discovery via KDTree ===
            nearby_1000m = geo_index.query_radius(lat, lon, 1000.0)
            # Exclude self
            nearby_1000m = [n for n in nearby_1000m if n['hotspot']['hotspot_id'] != hid]

            # Prepare nearby road names for junction convergence
            nearby_with_roads = []
            for n in nearby_1000m:
                n_hid = n['hotspot']['hotspot_id']
                n_road = roads.get(n_hid, {})
                nearby_with_roads.append({
                    "road_name": n_road.get('road_name', ''),
                    "distance_m": n['distance_m']
                })

            # Prepare nearby locations for POI discovery
            nearby_locations = []
            for n in nearby_1000m:
                nearby_locations.append({
                    "location_name": n['hotspot'].get('location_name', ''),
                    "distance_m": n['distance_m']
                })

            # === STAGE 2: Junction Intelligence ===
            junction_data = JunctionIntelligenceEngine.detect_junction(
                hotspot_id=hid,
                latitude=lat,
                longitude=lon,
                location_name=location_name,
                road_hierarchy=road_hierarchy,
                nearby_hotspots=nearby_with_roads
            )

            # === STAGE 3: Junction Importance ===
            importance_data = JunctionImportanceEngine.calculate_importance(
                junction_type=junction_data['junction_type'],
                road_hierarchy=road_hierarchy,
                road_count_connected=junction_data['road_count_connected'],
                signalized=junction_data['signalized']
            )

            # === STAGE 4: Junction Influence ===
            influence_data = JunctionInfluenceEngine.calculate_influence(
                junction_distance_m=junction_data['junction_distance_m']
            )

            # === STAGE 5: POI Intelligence (multi-radius) ===
            poi_data = POIIntelligenceEngine.discover_pois(
                hotspot_id=hid,
                latitude=lat,
                longitude=lon,
                location_name=location_name,
                nearby_hotspot_locations=nearby_locations
            )

            # === STAGE 6: Critical Infrastructure ===
            crit_data = CriticalInfrastructureEngine.calculate_critical_infrastructure(
                all_pois=poi_data['all_pois']
            )

            # === STAGE 7: Emergency Access ===
            emerg_data = EmergencyAccessEngine.calculate_emergency_impact(
                all_pois=poi_data['all_pois'],
                road_hierarchy=road_hierarchy,
                capacity_loss_percentage=capacity_loss
            )

            # === STAGE 8: POI Density (raw — normalized after loop) ===
            density_data = POIDensityEngine.calculate_density(
                poi_count_300m=poi_data['poi_count_300m'],
                poi_count_500m=poi_data['poi_count_500m'],
                poi_count_1000m=poi_data['poi_count_1000m']
            )
            density_data['hotspot_id'] = hid
            all_density_data.append(density_data)

            # Store intermediate results for JSON outputs
            junction_record = {
                "hotspot_id": hid,
                "road_name": road_name,
                **junction_data,
                **importance_data,
                **influence_data
            }
            junction_intelligence_data.append(junction_record)

            poi_record = {
                "hotspot_id": hid,
                "road_name": road_name,
                "poi_count_300m": poi_data['poi_count_300m'],
                "poi_count_500m": poi_data['poi_count_500m'],
                "poi_count_1000m": poi_data['poi_count_1000m'],
                "total_unique_pois": poi_data['total_unique_pois'],
                "pois": poi_data['all_pois'],
                "source": poi_data['source']
            }
            poi_intelligence_data.append(poi_record)

            crit_record = {
                "hotspot_id": hid,
                "road_name": road_name,
                **{k: v for k, v in crit_data.items() if k != 'critical_pois'},
                "critical_poi_types": [p['poi_type'] for p in crit_data.get('critical_pois', [])]
            }
            critical_infra_data.append(crit_record)

            emerg_record = {
                "hotspot_id": hid,
                "road_name": road_name,
                **{k: v for k, v in emerg_data.items() if k != 'emergency_pois_affected'},
                "emergency_poi_types": [p['poi_type'] for p in emerg_data.get('emergency_pois_affected', [])]
            }
            emergency_data.append(emerg_record)

        # === STAGE 8b: Normalize POI Density across all hotspots ===
        POIDensityEngine.normalize_density_scores(all_density_data)
        density_map = {d['hotspot_id']: d for d in all_density_data}

        # === STAGE 9 & 10: Context Importance + Explainability ===
        for i, hotspot in enumerate(hotspots):
            hid = hotspot['hotspot_id']
            junction = junction_intelligence_data[i]
            density = density_map.get(hid, {})
            crit = critical_infra_data[i]
            emerg = emergency_data[i]
            road = roads.get(hid, {})
            poi_rec = poi_intelligence_data[i]

            # Context Importance
            ctx_data = ContextImportanceEngine.calculate_context_importance(
                junction_importance_score=junction.get('junction_importance_score', 0),
                junction_influence_score=junction.get('junction_influence_score', 0),
                poi_density_score=density.get('poi_density_score', 0),
                critical_infrastructure_score=crit.get('critical_infrastructure_score', 0),
                emergency_impact_score=emerg.get('emergency_impact_score', 0)
            )

            # Explainability
            explanation = ContextExplainabilityEngine.generate_explanation(
                road_name=road.get('road_name', 'Unknown Road'),
                context_importance_score=ctx_data['context_importance_score'],
                context_importance_level=ctx_data['context_importance_level'],
                junction_type=junction.get('junction_type', 'Unknown'),
                junction_distance_m=junction.get('junction_distance_m', 0),
                junction_importance_level=junction.get('junction_importance_level', 'Unknown'),
                junction_influence_level=junction.get('junction_influence_level', 'Unknown'),
                poi_count_300m=density.get('poi_count_300m', 0),
                poi_count_500m=density.get('poi_count_500m', 0),
                poi_count_1000m=density.get('poi_count_1000m', 0),
                poi_density_level=density.get('poi_density_level', 'Low'),
                critical_infrastructure_score=crit.get('critical_infrastructure_score', 0),
                critical_infrastructure_level=crit.get('critical_infrastructure_level', 'Minimal'),
                critical_pois=poi_intelligence_data[i].get('pois', []),
                emergency_impact_score=emerg.get('emergency_impact_score', 0),
                emergency_priority=emerg.get('emergency_priority', 'P5-Informational'),
                emergency_route_impact=emerg.get('emergency_route_impact', False)
            )

            # Compute average confidence
            avg_confidence = junction.get('junction_confidence', 0.70)

            # Build standardized object
            ctx_obj = ContextIntelligence(
                hotspot_id=hid,
                road_name=road.get('road_name', 'Unknown Road'),
                junction_id=junction.get('junction_id', ''),
                junction_distance_m=junction.get('junction_distance_m', 0),
                junction_type=junction.get('junction_type', 'Unknown'),
                junction_signalized=junction.get('signalized', False),
                junction_road_count=junction.get('road_count_connected', 2),
                junction_score=junction.get('junction_score', 0),
                junction_importance_score=junction.get('junction_importance_score', 0),
                junction_importance_level=junction.get('junction_importance_level', 'Local Junction'),
                junction_influence_score=junction.get('junction_influence_score', 0),
                junction_influence_level=junction.get('junction_influence_level', 'None'),
                poi_count_300m=density.get('poi_count_300m', 0),
                poi_count_500m=density.get('poi_count_500m', 0),
                poi_count_1000m=density.get('poi_count_1000m', 0),
                poi_density_score=density.get('poi_density_score', 0),
                poi_density_level=density.get('poi_density_level', 'Low'),
                critical_infrastructure_score=crit.get('critical_infrastructure_score', 0),
                critical_infrastructure_level=crit.get('critical_infrastructure_level', 'Minimal'),
                critical_poi_count=crit.get('critical_poi_count', 0),
                emergency_impact_score=emerg.get('emergency_impact_score', 0),
                emergency_priority=emerg.get('emergency_priority', 'P5-Informational'),
                emergency_route_impact=emerg.get('emergency_route_impact', False),
                context_importance_score=ctx_data['context_importance_score'],
                context_importance_level=ctx_data['context_importance_level'],
                context_explainability=explanation,
                source=junction.get('source', 'Deterministic Geospatial Analysis'),
                confidence=avg_confidence,
                generated_at=datetime.now()
            )
            context_objects.append(ctx_obj)

        # === Save all JSON outputs ===
        os.makedirs(os.path.dirname(CONTEXT_JSON_PATH), exist_ok=True)

        json_data = [obj.dict() for obj in context_objects]
        with open(CONTEXT_JSON_PATH, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)

        with open(JUNCTION_JSON_PATH, 'w') as f:
            json.dump(junction_intelligence_data, f, indent=2, default=str)

        with open(POI_JSON_PATH, 'w') as f:
            json.dump(poi_intelligence_data, f, indent=2, default=str)

        with open(CRITICAL_INFRA_JSON_PATH, 'w') as f:
            json.dump(critical_infra_data, f, indent=2, default=str)

        with open(EMERGENCY_JSON_PATH, 'w') as f:
            json.dump(emergency_data, f, indent=2, default=str)

        print(f"Context Intelligence generated for {len(context_objects)} hotspots.")
        return context_objects

    @staticmethod
    def get_all_context() -> List[Dict[str, Any]]:
        if not os.path.exists(CONTEXT_JSON_PATH):
            ContextIntelligenceService.generate_all()
        with open(CONTEXT_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_junction_intelligence() -> List[Dict[str, Any]]:
        if not os.path.exists(JUNCTION_JSON_PATH):
            ContextIntelligenceService.generate_all()
        with open(JUNCTION_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_poi_intelligence() -> List[Dict[str, Any]]:
        if not os.path.exists(POI_JSON_PATH):
            ContextIntelligenceService.generate_all()
        with open(POI_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_emergency_impact() -> List[Dict[str, Any]]:
        if not os.path.exists(EMERGENCY_JSON_PATH):
            ContextIntelligenceService.generate_all()
        with open(EMERGENCY_JSON_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_context_summary() -> Dict[str, Any]:
        """Returns aggregate statistics across all hotspots."""
        all_ctx = ContextIntelligenceService.get_all_context()
        if not all_ctx:
            return {}

        levels = {}
        priorities = {}
        total_critical_pois = 0
        total_emergency_routes = 0

        for ctx in all_ctx:
            lvl = ctx.get('context_importance_level', 'Unknown')
            levels[lvl] = levels.get(lvl, 0) + 1

            pri = ctx.get('emergency_priority', 'Unknown')
            priorities[pri] = priorities.get(pri, 0) + 1

            total_critical_pois += ctx.get('critical_poi_count', 0)
            if ctx.get('emergency_route_impact', False):
                total_emergency_routes += 1

        avg_score = sum(c['context_importance_score'] for c in all_ctx) / len(all_ctx)

        return {
            "total_hotspots": len(all_ctx),
            "average_context_importance_score": round(avg_score, 2),
            "context_level_distribution": levels,
            "emergency_priority_distribution": priorities,
            "total_critical_infrastructure_pois": total_critical_pois,
            "hotspots_blocking_emergency_routes": total_emergency_routes,
        }
