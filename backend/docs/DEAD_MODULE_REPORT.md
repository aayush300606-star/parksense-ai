# Dead Module Trace Report
**Objective**: Identify "Dead Modules" (code that is fully written and tested but entirely invisible to the end user).

## Dead Module Definition
A module is considered "Dead" if it exists in the codebase and passes unit tests, but cannot be interacted with via the visual dashboard, demo mode, or the AI Copilot.

## Detected Dead Modules
**Category 1: Urban Traffic Graph Intelligence (UTGI™)**
- `gnn_engine.py`
- `road_network_graph_engine.py`
- `network_risk_engine.py`
- `network_csi_engine.py`
- `corridor_intelligence_engine.py`

*Status:* These modules are successfully running inside the `test_e2e_pipeline.py` script and writing their outputs to the `processed/` JSON folder. They are also wired to `backend/api/utgi_api.py`. However, they are Dead because the frontend `parksense-app` has zero pages that pull from `utgi_api.py`.

**Category 2: Root Cause & Enforcement Intelligence (REI™)**
- `hotspot_dna_engine.py`
- `root_cause_engine.py`
- `behavior_analytics_engine.py`
- `hotspot_segmentation_engine.py`
- `enforcement_effectiveness_engine.py`
- `policy_impact_engine.py`

*Status:* These modules are also running perfectly via the E2E script and have routes in `rei_api.py`. They are Dead because there is no `Enforcement Strategy` or `Root Cause` visualization page in the frontend Next.js app.

## Resolution Plan
To resurrect these modules, we must build dedicated Next.js pages (`/network`, `/root-cause`) and inject their outputs into the AI Copilot orchestrator.
