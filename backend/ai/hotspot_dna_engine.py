import os
import json
from typing import Dict, Any

from .root_cause_engine import RootCauseEngine
from .behavior_analytics_engine import BehaviorAnalyticsEngine
from .intervention_recommendation_engine import InterventionRecommendationEngine

DNA_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'hotspot_dna.json')

class HotspotDNAEngine:
    """
    Generates a unique behavioral signature for every hotspot, fusing the Analytics layer
    with the Prescriptive Intelligence layer.
    """

    @staticmethod
    def generate_all_dna(hotspot_ids: list) -> list:
        dna_database = []
        
        for hid in hotspot_ids:
            behavior = BehaviorAnalyticsEngine.analyze_behavior(hid)
            root_cause = RootCauseEngine.analyze_root_cause(hid)
            intervention = InterventionRecommendationEngine.recommend(hid)
            
            dna = {
                "hotspot_id": hid,
                "dna_signature": f"{root_cause['primary_cause_key']}::{behavior['predictability_level'][:3].upper()}::{intervention['immediate_action'].replace(' ', '')[:6].upper()}::{int(root_cause['confidence']*100)}",
                "primary_cause": root_cause['primary_cause_label'],
                "secondary_cause": root_cause['secondary_cause_label'],
                "root_cause_reasoning": root_cause.get('root_cause_reasoning', ''),
                "confidence_score": root_cause.get('confidence', 0.8) * 100,
                
                "peak_violation_time": f"{behavior['peak_violation_hour']:02d}:00",
                "predictability": behavior['predictability_level'],
                "predictability_reasoning": behavior.get('predictability_reasoning', ''),
                
                "recommended_immediate_action": intervention['immediate_action'],
                "immediate_action_reasoning": intervention.get('immediate_action_reasoning', ''),
                "recommended_infrastructure_fix": intervention['long_term_action'],
                "long_term_action_reasoning": intervention.get('long_term_action_reasoning', '')
            }
            dna_database.append(dna)
            
        os.makedirs(os.path.dirname(DNA_JSON_PATH), exist_ok=True)
        with open(DNA_JSON_PATH, 'w') as f:
            json.dump(dna_database, f, indent=2)
            
        return dna_database
        
    @staticmethod
    def get_dna(hotspot_id: int) -> Dict[str, Any]:
        if not os.path.exists(DNA_JSON_PATH):
            return {"error": "DNA database missing"}
        with open(DNA_JSON_PATH, 'r') as f:
            dna_database = json.load(f)
            
        return next((d for d in dna_database if d['hotspot_id'] == hotspot_id), {"error": "DNA not found"})
