# Effective Road Width Loss Engine

This module is the flagship innovation of ParkSense AI. It physically quantifies the spatial impact of illegal parking by calculating capacity loss and lane blockages using transportation engineering models.

## 1. Architecture

1. **`vehicle_occupancy_engine.py`**: Maps raw dataset strings (e.g., "PASSENGER AUTO", "SCOOTER") to their standard footprint widths (1.5m, 1.0m respectively).
2. **`occupied_width_engine.py`**: Computes the aggregated lateral impact. To remain deterministic, it relies strictly on summing the total width of all illegally parked vehicles in a hotspot.
3. **`effective_width_engine.py`**: A deterministic calculation: `Road Width - Occupied Width`. Clamped gracefully to 0.
4. **`capacity_loss_engine.py`**: Calculates the precise percentage of capacity lost: `(Occupied Width / Original Road Width) * 100` and assigns intuitive warning levels.
5. **`lane_blockage_engine.py`**: Determines lane utility. Calculates `Blocked Lanes` (by checking how many 3.5m standard lane width chunks are occupied) and outputs a `Lane Utilization` score.
6. **`explainability_engine.py`**: A synthetic intelligence script that translates the metrics into natural language GIS logic for non-technical stakeholders (e.g., "14 SCOOTERS occupying 14m laterally...").

## 2. API Design & Data Pipeline

These engines are unified via the `RoadImpactService`. The service automatically merges the clusters from `hotspot_detection.py` (which now aggregate vehicle types securely) with the geometry calculations from `road_service.py`.

It surfaces output locally to the frontend dashboards via:
- `data/processed/road_impact.json` (Full structural representation)
- `data/processed/capacity_loss.json` (Visuals-only subset)
- `data/processed/lane_blockage.json` (Visuals-only subset)

And via REST APIs on the FastAPI router:
- `/api/road-impact`
- `/api/effective-width`
- `/api/capacity-loss`
- `/api/lane-blockage`

## 3. Strict Determinism Rules Applied
All calculations use the 100% strict datasets parameters. We map vehicle boundaries directly, bypassing the need for mocked outputs, pseudo-randomization, or generic ML placeholder strings.
