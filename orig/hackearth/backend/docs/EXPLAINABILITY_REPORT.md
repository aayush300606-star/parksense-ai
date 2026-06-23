# Universal Explainability Report

This document outlines how every core metric in the ParkSense AI platform is explained and justified to the end-user.

## Universal Score Engine
The `UniversalScoreEngine` was implemented to ensure that no metric is presented without an explanation.

### Adaptive CSI™
- **Formula:** `w1*(Density) + w2*(Width Loss) + w3*(Delay) + w4*(POI Penalty)`
- **Explainability:** The engine exposes the exact breakdown. If CSI is 90, the user can click "Why?" and see that 40 points came from Width Loss and 30 points came from POI proximity (e.g., blocking a hospital).

### Parking Impact Score (PIS™)
- **Formula:** `(Delay_Hours * Hourly_Wage) + (Idling_Fuel_Waste * Fuel_Cost)`
- **Explainability:** The engine shows the economic parameters used (wage assumptions, fuel cost assumptions) so city planners can trust the Rupee loss figures.

### KPI Metadata Engine
We implemented `kpi_metadata_engine.py` to back the frontend UI. Every single KPI card in the dashboard has a tooltip pulling from this registry, defining:
1. What the metric is.
2. The formula used to calculate it.
3. The data sources powering it.
4. The statistical confidence of the metric.

## Result
City officials do not need a Data Science degree to understand the platform. The AI explains itself in procurement-grade, operational language.
