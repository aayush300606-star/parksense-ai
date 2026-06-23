import os
import json
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .api import hotspots, road, road_impact, traffic_intelligence, context_intelligence, csi_intelligence, pis_intelligence, prediction_intelligence, digital_twin_intelligence, smart_enforcement_intelligence, copilot_api, demo_mode, utgi_api, rei_api

# Setup Structured Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("parksense_core")

app = FastAPI(
    title="ParkSense AI Data Foundation & Smart City Operating System",
    description="The executive intelligence layer for predicting, simulating, and resolving parking-induced congestion.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Hardened Security Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled system error on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal platform error occurred.", "code": "SC_500"}
    )

app.include_router(hotspots.router)
app.include_router(road.router)
app.include_router(road_impact.router)
app.include_router(traffic_intelligence.router)
app.include_router(context_intelligence.router)
app.include_router(csi_intelligence.router)
app.include_router(pis_intelligence.router)
app.include_router(prediction_intelligence.router)
app.include_router(digital_twin_intelligence.router)
app.include_router(smart_enforcement_intelligence.router)
app.include_router(copilot_api.router)
app.include_router(demo_mode.router)
app.include_router(utgi_api.router)
app.include_router(rei_api.router)

@app.on_event("startup")
async def startup_event():
    """
    On startup, we ensure the pipeline has run and we update the legacy frontend's JSON file 
    so that the existing Next.js app stays perfectly functional without any frontend code changes.
    """
    from .ai.preprocessing import preprocess_data
    from .ai.hotspot_detection import detect_hotspots
    from .ai.violation_density import calculate_violation_density
    from .services.hotspot_service import HotspotService
    from .services.road_service import RoadService
    from .services.road_impact_service import RoadImpactService
    from .services.traffic_intelligence_service import TrafficIntelligenceService
    from .services.context_intelligence_service import ContextIntelligenceService
    from .services.csi_service import CSIService
    from .services.pis_service import PISService
    from .services.prediction_service import PredictionService
    from .services.digital_twin_service import DigitalTwinService
    from .services.smart_enforcement_service import SmartEnforcementService

    print("--- Initializing AI Data Foundation ---")
    
    # Run Pipeline
    try:
        df = preprocess_data()
        detected_hotspots = detect_hotspots(df)
        calculate_violation_density(detected_hotspots)
        
        # Overwrite legacy hotspots.json in the Next.js public directory
        legacy_data = HotspotService.generate_frontend_compatible_hotspots()
        legacy_path = os.path.join(os.path.dirname(__file__), '..', 'parksense-app', 'public', 'data', 'hotspots.json')
        
        if os.path.exists(os.path.dirname(legacy_path)):
            with open(legacy_path, 'w') as f:
                json.dump(legacy_data, f, indent=2)
            print(f"Legacy frontend compatibility file updated at {legacy_path}")
            
        print("--- Initializing Road Intelligence Layer ---")
        RoadService.generate_all()
        
        print("--- Initializing Effective Road Width Engine ---")
        RoadImpactService.generate_all()
        
        print("--- Initializing Traffic Intelligence Engine ---")
        TrafficIntelligenceService.generate_all()
        
        print("--- Initializing Context Intelligence Engine ---")
        ContextIntelligenceService.generate_all()
        
        print("--- Initializing CSI™ + PIS™ Engine ---")
        CSIService.generate_all()
        
        print("--- Initializing PIS Impact Engine ---")
        PISService.generate_all()
        
        print("--- Initializing AI Prediction Engine ---")
        PredictionService.generate_all()
        
        print("--- Initializing Digital Twin Simulation Engine ---")
        DigitalTwinService.generate_all()
        
        print("--- Initializing Smart Enforcement Planner (SEP) ---")
        SmartEnforcementService.generate_all()
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Pipeline initialization failed (maybe dataset is missing?): {e}")

@app.get("/")
def read_root():
    return {"status": "AI Data Foundation is running."}
