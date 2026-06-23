# Digital Twin Simulation Engine

The Digital Twin Simulation Engine elevates the platform into a pure decision-support layer. It mathematically calculates the Return on Investment (ROI) of parking enforcement before a single officer is deployed.

## Core Simulation Logic

We enforce the strict rule of "No Fake Simulations". Every metric produced by the Digital Twin is directly calculated via physical transport engineering approximations.

### 1. Capacity Recovery
When the user executes a scenario (e.g., 75% Removal), the engine calculates the exact width (in meters) of the road that is reclaimed from illegally parked cars, and computes the new `capacity_loss_percentage`.

### 2. Traffic Flow Recovery
Using a modified BPR (Bureau of Public Roads) function heuristic, the engine maps the recovered capacity back into increased traffic speed (km/h) and reduced delay.

### 3. CSI™ & PIS™ Recalculation
With the new speed and capacity numbers:
- `CSIRecalculationEngine` calculates the new lowered CSI score.
- `PISRecalculationEngine` calculates the new lowered economic burden, fuel waste, delay hours, and CO₂ emissions.

## Standard Scenarios
The `MultiScenarioEngine` simultaneously tests four standard scenarios on every hotspot:
- **Scenario A:** 100% Illegal Parking Removal
- **Scenario B:** 75% Removal (High Enforcement)
- **Scenario C:** 50% Removal (Moderate Enforcement)
- **Scenario D:** 25% Removal (Low Enforcement)

## Benefit Scoring & ROI
`BenefitAnalysisEngine` aggregates the improvements across CSI, Delay, and Speed into a normalized `benefit_score` (0-100).
`EnforcementROIEngine` compares this benefit score against the effort required (the removal percentage) to classify the ROI as Excellent, Good, Moderate, or Poor.

For example, if 50% enforcement yields 90% of the maximum possible benefit, the system ranks Scenario C as the best ROI.

## APIs
- `GET /api/digital-twin`: Returns pre-calculated A/B/C/D scenarios for all hotspots.
- `GET /api/best-scenarios`: Returns the recommended intervention scenario for each hotspot.
- `POST /api/simulate`: Runs a real-time custom simulation for a single hotspot (e.g., passing a custom `removal_pct`).
