from fastapi import APIRouter
from typing import Dict, Any, List

from ..ai.hotspot_dna_engine import HotspotDNAEngine
from ..ai.root_cause_engine import RootCauseEngine
from ..ai.intervention_recommendation_engine import InterventionRecommendationEngine
from ..ai.root_cause_explainability_engine import RootCauseExplainabilityEngine

router = APIRouter(prefix="/api/rei", tags=["Root Cause & Enforcement Intelligence"])

@router.post("/generate-dna")
def generate_dna():
    """Generates the Hotspot DNA for the entire city dataset."""
    import json
    import os
    # We load the 100 hotspots from the base JSON
    hotspots_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'hotspots_with_density.json')
    if not os.path.exists(hotspots_path):
        return {"error": "Hotspots data missing"}
    with open(hotspots_path, 'r') as f:
        hotspots = json.load(f)
    ids = [h['hotspot_id'] for h in hotspots]
    return HotspotDNAEngine.generate_all_dna(ids)

@router.get("/dna/{hotspot_id}")
def get_dna(hotspot_id: int):
    """Returns the unique behavioral DNA signature for a hotspot."""
    return HotspotDNAEngine.get_dna(hotspot_id)
    
@router.get("/root-cause/{hotspot_id}")
def get_root_cause(hotspot_id: int):
    """Returns the primary and secondary cause of congestion."""
    return RootCauseEngine.analyze_root_cause(hotspot_id)
    
@router.get("/recommendation/{hotspot_id}")
def get_recommendation(hotspot_id: int):
    """Returns the immediate and long-term enforcement strategies."""
    return InterventionRecommendationEngine.recommend(hotspot_id)
    
@router.get("/explain/{hotspot_id}")
def get_explanation(hotspot_id: int):
    """Returns a deterministic, plain-English explanation of why the hotspot exists and how to fix it."""
    return RootCauseExplainabilityEngine.explain_root_cause(hotspot_id)
