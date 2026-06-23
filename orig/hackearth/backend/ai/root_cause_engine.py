from typing import Dict, Any
from .hotspot_segmentation_engine import HotspotSegmentationEngine
from .enforcement_knowledge_base import EnforcementKnowledgeBase
from .cause_congestion_mapper import CauseCongestionMapper

class RootCauseEngine:
    """
    Deterministically assigns the core reason a hotspot exists by evaluating its Archetype.
    """

    @staticmethod
    def analyze_root_cause(hotspot_id: int) -> Dict[str, Any]:
        segment_data = HotspotSegmentationEngine.classify_archetype(hotspot_id)
        archetype = segment_data.get('archetype', 'Mixed-Use')
        
        # Deterministic mapping of Archetype to Root Cause
        if archetype == "Metro-Oriented":
            primary_cause_key = "RC_METRO"
            secondary_cause_key = "RC_RIDE_HAIL"
        elif archetype == "School-Oriented":
            primary_cause_key = "RC_SCHOOL"
            secondary_cause_key = "RC_RIDE_HAIL"
        elif archetype == "Hospital-Oriented":
            primary_cause_key = "RC_HOSPITAL"
            secondary_cause_key = "RC_RIDE_HAIL"
        elif archetype == "Commercial/Retail":
            primary_cause_key = "RC_COMMERCIAL"
            secondary_cause_key = "RC_MARKET"
        elif archetype == "Nightlife/Dining":
            primary_cause_key = "RC_NIGHTLIFE"
            secondary_cause_key = "RC_RIDE_HAIL"
        else:
            primary_cause_key = "RC_RESIDENTIAL"
            secondary_cause_key = "RC_COMMERCIAL"
            
        primary_label = EnforcementKnowledgeBase.get_root_cause_label(primary_cause_key)
        secondary_label = EnforcementKnowledgeBase.get_root_cause_label(secondary_cause_key)
        
        pathway = CauseCongestionMapper.map_pathway(primary_cause_key)
        
        return {
            "hotspot_id": hotspot_id,
            "primary_cause_key": primary_cause_key,
            "primary_cause_label": primary_label,
            "secondary_cause_key": secondary_cause_key,
            "secondary_cause_label": secondary_label,
            "confidence": segment_data.get('archetype_confidence', 0.5),
            "physical_manifestation": pathway
        }
