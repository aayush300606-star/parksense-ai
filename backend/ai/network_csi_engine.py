import os
import json
from typing import List, Dict, Any
from .network_risk_engine import NetworkRiskEngine
from ..services.csi_service import CSIService

NETWORK_CSI_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'network_csi.json')

class NetworkCSIEngine:
    """
    Upgrades the existing localized Adaptive CSI to include Network Propagation Risk.
    This shifts the metric from "How bad is this road?" to "How bad is this road for the ENTIRE CITY?"
    """

    @staticmethod
    def upgrade_csi() -> List[Dict[str, Any]]:
        base_csi_list = CSIService.get_all_csi()
        network_risks = NetworkRiskEngine.calculate_vulnerability()
        
        risk_map = {r['hotspot_id']: r for r in network_risks}
        
        upgraded_csi = []
        
        for csi in base_csi_list:
            hid = csi['hotspot_id']
            net_risk = risk_map.get(hid, {})
            
            base_score = csi['csi_score']
            fragility = net_risk.get('network_fragility_score', 0)
            
            # The new UTGI Score equation
            # 80% Localized Impact, 20% City-Wide Ripple Impact
            network_csi_score = (base_score * 0.8) + (fragility * 0.2)
            
            upgraded_csi.append({
                "hotspot_id": hid,
                "location_name": csi.get('road_name', 'Unknown'),
                "base_csi": base_score,
                "network_fragility": fragility,
                "network_csi": network_csi_score,
                "ripple_effect_score": net_risk.get('ripple_score', 0),
                "is_critical_network_node": fragility > 80
            })
            
        os.makedirs(os.path.dirname(NETWORK_CSI_PATH), exist_ok=True)
        with open(NETWORK_CSI_PATH, 'w') as f:
            json.dump(upgraded_csi, f, indent=2)
            
        return upgraded_csi
