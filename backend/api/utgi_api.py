from fastapi import APIRouter
from typing import Dict, Any, List

from ..ai.network_csi_engine import NetworkCSIEngine
from ..ai.network_risk_engine import NetworkRiskEngine
from ..ai.corridor_intelligence_engine import CorridorIntelligenceEngine
from ..ai.network_explainability_engine import NetworkExplainabilityEngine
from ..ai.congestion_propagation_engine import CongestionPropagationEngine

router = APIRouter(prefix="/api/utgi", tags=["Urban Traffic Graph Intelligence"])

@router.get("/network-csi")
def get_network_csi():
    """Returns the upgraded Network CSI for all nodes."""
    return NetworkCSIEngine.upgrade_csi()
    
@router.get("/vulnerability-map")
def get_vulnerability_map():
    """Returns GNN and Centrality risk scores for graph visualization."""
    return NetworkRiskEngine.calculate_vulnerability()
    
@router.get("/corridors")
def get_corridors():
    """Returns structurally identified vulnerable corridors."""
    return CorridorIntelligenceEngine.identify_corridors()
    
@router.get("/propagation/{hotspot_id}")
def get_propagation(hotspot_id: int):
    """Returns the primary/secondary/tertiary ripple zones for a given epicenter."""
    return CongestionPropagationEngine.model_spillover(hotspot_id)
    
@router.get("/explain/{hotspot_id}")
def get_explanation(hotspot_id: int):
    """Returns the plain-English explanation for the node's network risk."""
    return NetworkExplainabilityEngine.explain_node(hotspot_id)
