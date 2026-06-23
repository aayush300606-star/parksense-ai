# ParkSense AI: System Architecture

The ParkSense platform has evolved from a basic analytics dashboard into a complete **Smart City Operating System**, heavily augmented by Artificial Intelligence. 

## High-Level Data Flow

1. **Raw Ingestion**: Unstructured, noisy JSON/CSV police challan data.
2. **Spatial Clustering**: DBSCAN aggregates tickets into distinct geographic hotspots.
3. **Descriptive AI (What is happening?)**:
   - `RoadIntelligenceEngine`: Detects road hierarchy, type, and capacity.
   - `ContextIntelligenceEngine`: Detects proximity to critical infrastructure (hospitals, fire stations).
   - `AdaptiveCSIEngine`: Calculates the Congestion Severity Index (0-100).
   - `ParkingImpactEngine`: Calculates the real-world economic loss (PIS).
4. **Predictive AI (What will happen?)**:
   - `PredictionEngine`: Uses ensemble tree models to forecast 1h, 6h, 24h, and 7d bottleneck risks.
5. **Prescriptive AI (What if?)**:
   - `DigitalTwinEngine`: Simulates the physical physics of the road to test interventions before applying them.
6. **Operational AI (What should we do?)**:
   - `SmartEnforcementPlanner`: Allocates constrained police resources using Traveling Salesperson optimization to generate daily patrol routes.
7. **Executive AI (SCAC™)**:
   - `SmartCityAICopilot`: A 0-hallucination RAG reasoning layer that allows city officials to query the platform in natural language.

## Technology Stack
- **Backend**: FastAPI (Python 3.10+)
- **ML/Data**: Pandas, NumPy, Scikit-Learn, SciPy
- **Geospatial**: KDTree, Haversine, DBSCAN
- **API integrations**: MapMyIndia (Mappls)

## Directory Structure
- `/backend/ai/`: Contains the 20+ specialized intelligence engines.
- `/backend/api/`: REST endpoints for the frontend.
- `/backend/services/`: Service orchestrators that chain engines together.
- `/backend/models/`: Pydantic data schemas.
- `/backend/data/processed/`: The JSON "Database".
