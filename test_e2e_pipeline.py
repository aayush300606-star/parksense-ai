import os
import sys
import time
import json
import traceback

sys.path.insert(0, '.')

def print_header(title):
    print(f"\n{'='*60}")
    print(f"=== {title:^52} ===")
    print(f"{'='*60}")

async def run_e2e_audit():
    print_header("PARKSENSE FINAL END-TO-END VALIDATION AUDIT")
    start_time = time.time()
    
    audit_results = {}
    
    try:
        from backend.ai.hotspot_detection import detect_hotspots
        from backend.ai.violation_density import calculate_violation_density
        from backend.ai.temporal_pattern_engine import TemporalPatternEngine
        from backend.services.road_service import RoadService
        from backend.services.road_impact_service import RoadImpactService
        from backend.services.traffic_intelligence_service import TrafficIntelligenceService
        from backend.services.context_intelligence_service import ContextIntelligenceService
        from backend.services.csi_service import CSIService
        from backend.services.pis_service import PISService
        from backend.services.prediction_service import PredictionService
        from backend.services.digital_twin_service import DigitalTwinService
        from backend.services.smart_enforcement_service import SmartEnforcementService
        from backend.ai.copilot_orchestrator import CopilotOrchestrator
        
        # UTGI Components
        from backend.ai.road_network_graph_engine import RoadNetworkGraphEngine
        from backend.ai.network_risk_engine import NetworkRiskEngine
        from backend.ai.network_csi_engine import NetworkCSIEngine
        from backend.ai.corridor_intelligence_engine import CorridorIntelligenceEngine
        
        # REI Components
        from backend.ai.hotspot_dna_engine import HotspotDNAEngine
        
        # 1. Hotspot Detection
        print("[1/11] Running Hotspot Detection & Density...")
        raw_hotspots = detect_hotspots()
        hotspots = calculate_violation_density(raw_hotspots)
        TemporalPatternEngine.analyze_temporal_patterns(hotspots)
        audit_results['hotspots'] = {"count": len(hotspots) if hotspots else 0, "status": "PASS"}
        
        # 2. Road Intelligence
        print("[2/11] Running RoadService...")
        roads = RoadService.generate_all()
        audit_results['road_intelligence'] = {"count": len(roads) if roads else 0, "status": "PASS"}
        
        # 3. Effective Width (Road Impact)
        print("[3/11] Running RoadImpactService...")
        widths = RoadImpactService.generate_all()
        audit_results['effective_width'] = {"count": len(widths) if widths else 0, "status": "PASS"}
        
        # 4. Traffic Intelligence
        print("[4/11] Running TrafficIntelligenceService...")
        traffic = TrafficIntelligenceService.generate_all()
        audit_results['traffic'] = {"count": len(traffic) if traffic else 0, "status": "PASS"}
        
        # 5. Context Intelligence
        print("[5/11] Running ContextIntelligenceService...")
        context = ContextIntelligenceService.generate_all()
        audit_results['context'] = {"count": len(context) if context else 0, "status": "PASS"}
        
        # 6. Adaptive CSI
        print("[6/11] Running CSIService...")
        csi = CSIService.generate_all()
        audit_results['csi'] = {"count": len(csi) if csi else 0, "status": "PASS"}
        
        # 7. Parking Impact Score
        print("[7/11] Running PISService...")
        pis = PISService.generate_all()
        audit_results['pis'] = {"count": len(pis) if pis else 0, "status": "PASS"}
        
        # 8. Prediction Engine
        print("[8/11] Running PredictionService...")
        preds = PredictionService.generate_all()
        audit_results['predictions'] = {"count": len(preds) if preds else 0, "status": "PASS"}
        
        # 9. Digital Twin
        print("[9/11] Running DigitalTwinService...")
        twins = DigitalTwinService.generate_all()
        audit_results['digital_twin'] = {"count": len(twins) if twins else 0, "status": "PASS"}
        
        # 10. Smart Enforcement Planner
        print("[10/11] Running SmartEnforcementService...")
        SmartEnforcementService.generate_all()
        plan = SmartEnforcementService.get_enforcement_plan()
        audit_results['smart_enforcement'] = {"interventions": len(plan) if plan else 0, "status": "PASS"}
        
        # 11. UTGI (Urban Traffic Graph Intelligence)
        print("[11/12] Running Urban Traffic Graph Intelligence Engine (UTGI™)...")
        print("  > Building NetworkX Road Graph...")
        RoadNetworkGraphEngine.load_graph()
        print("  > Predicting Network Risk via Graph Neural Networks...")
        network_risks = NetworkRiskEngine.calculate_vulnerability()
        print("  > Upgrading to Network CSI™...")
        NetworkCSIEngine.upgrade_csi()
        print("  > Identifying Critical Corridors...")
        corridors = CorridorIntelligenceEngine.identify_corridors()
        audit_results['utgi_graph'] = {"vulnerable_nodes": len(network_risks), "corridors_detected": len(corridors), "status": "PASS"}
        
        # 12. REI (Root Cause & Enforcement Intelligence Engine)
        print("[12/13] Running Root Cause & Enforcement Intelligence Engine (REI™)...")
        import json
        with open('backend/data/processed/hotspots_with_density.json', 'r') as f:
            hid_list = [h['hotspot_id'] for h in json.load(f)]
        dna_list = HotspotDNAEngine.generate_all_dna(hid_list)
        audit_results['rei'] = {"dna_generated": len(dna_list), "status": "PASS"}
        
        # 13. AI Copilot testing
        print("[13/13] Testing AI Copilot (SCAC™)...")
        scac_query = "What happens if we remove parking from the hotspot?"
        scac_res = CopilotOrchestrator.process_query(scac_query)
        audit_results['ai_copilot'] = {"intent": scac_res['intent'], "sources": scac_res['context_sources'], "status": "PASS"}
        
        print_header("AUDIT SUMMARY: SUCCESS")
        
    except Exception as e:
        print_header("AUDIT SUMMARY: FAILED")
        print(traceback.format_exc())
        audit_results['error'] = str(e)
    
    elapsed = time.time() - start_time
    print(f"\nTotal Execution Time: {elapsed:.2f}s")
    print(json.dumps(audit_results, indent=2))
    
    os.makedirs('backend/data/processed', exist_ok=True)
    with open('backend/data/processed/audit_report.json', 'w') as f:
        json.dump(audit_results, f, indent=2)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_e2e_audit())
