# ParkSense AI: API Reference

The platform exposes several unified JSON endpoints for the frontend.

## Descriptive Endpoints
- `GET /api/hotspots`: Returns standard 100 DBSCAN hotspots.
- `GET /api/roads`: Returns 100 `RoadIntelligence` objects containing hierarchy and width.
- `GET /api/road-impacts`: Returns 100 `RoadImpact` objects detailing lane blockage.
- `GET /api/traffic-intelligence`: Returns average speed reductions and delays.
- `GET /api/context-intelligence`: Returns KDTree mapping of critical infrastructure.
- `GET /api/csi`: Returns the final `AdaptiveCSI` scores (0-100).
- `GET /api/pis`: Returns the `ParkingImpactScore` (Economic/Environmental impacts).

## Predictive & Prescriptive Endpoints
- `GET /api/predictions`: Returns Random Forest time-series forecasts (1h, 6h, 24h, 7d).
- `GET /api/digital-twin`: Returns 400 physics-based simulation scenarios.

## Operational Endpoints
- `GET /api/enforcement-plan`: Returns the Traveling Salesperson optimized daily patrol routes.

## AI Copilot Endpoints
- `POST /api/copilot/query`: Accepts `{"query": "..."}` and returns a RAG knowledge object.
- `GET /api/copilot/daily-brief`: Returns narrative city-wide executive summary.

## Demo Endpoints
- `GET /api/demo/presentation`: 1-Click wrapper that finds the worst hotspot in the city, looks up its simulations and enforcement plans, and generates a unified RAG narrative.
