# Parking Impact Score (PIS™) Engine

While **CSI™ (Congestion Severity Index)** measures the mathematical severity of a bottleneck, **PIS™ (Parking Impact Score)** translates that congestion into tangible socio-economic and environmental impacts.

## Overview

The PIS Engine is composed of 11 distinct micro-engines that convert traffic delays and capacity losses into real-world metrics. It answers:
- How many commuters are affected?
- How much fuel is wasted?
- How much CO₂ is generated?
- What is the economic burden (lost productivity + wasted fuel) in INR?
- What are the quantitative benefits of enforcement?

## The 7 Core Impact Models

### 1. Affected Vehicle Estimation
`affected_vehicle_engine.py`
Calculates the number of vehicles passing through the bottleneck.
- **Inputs:** `road_hierarchy` (baseline capacity), `csi_score` (impact factor), `capacity_loss`.
- **Output:** `vehicles_impacted_per_day`

### 2. Commuter Impact Model
`commuter_impact_engine.py`
Translates vehicle counts into human impact using Indian modal share estimates.
- **Assumptions:** Bike (1.2), Car (1.5), Auto (2.5), Bus (30.0).
- **Output:** `daily_commuters_affected`

### 3. Delay Impact Model
`delay_impact_engine.py`
Aggregates the delay experienced by all vehicles.
- **Output:** `daily_delay_hours`, `annual_delay_hours`

### 4. Fuel Waste Model
`fuel_waste_engine.py`
Estimates fuel wasted due to idling and slow traffic.
- **Assumptions:** Baseline idling consumption rates (e.g., Car: 1.2 L/hr, Bus: 4.0 L/hr).
- **Output:** `fuel_wasted_per_day_liters`

### 5. Environmental Impact Model
`environmental_impact_engine.py`
Calculates carbon footprint.
- **Assumptions:** 2.35 kg CO₂ per liter of fuel.
- **Output:** `co2_emissions_kg_per_day`

### 6. Economic Impact Model
`economic_impact_engine.py`
Monetizes the cost of congestion.
- **Assumptions:** Value of Time (VoT) = ₹120/hr, Fuel Cost = ₹100/liter.
- **Output:** `economic_burden_inr_per_day`

### 7. Capacity Recovery Simulator
`capacity_recovery_engine.py`
Projects the exact benefits if illegal parking is enforced.
- **Output:** `capacity_recovered_pct`, `expected_delay_reduction_hours`

## PIS Calculation & Classification

The `pis_engine.py` aggregates these scores into a unified 0-100 metric:
- **Base CSI:** 20%
- **Economic Burden:** 25%
- **Commuter Toll:** 20%
- **Environmental Impact:** 15%
- **Delay:** 10%
- **Enforcement Recovery:** 10%

The output is then classified by `pis_classification_engine.py` into 5 bands:
1. **Critical (P1)** (80-100)
2. **High (P2)** (60-80)
3. **Moderate (P3)** (40-60)
4. **Low (P4)** (20-40)
5. **Minimal (P5)** (0-20)

## Explainability

Every PIS score guarantees deterministic explainability via the `pis_explainability_engine.py`. This text narrative is consumed by municipal dashboards and LLM Agents.

**Example output:**
> PIS = 94/100 (Critical Impact). Reason: 12.3k commuters affected daily, suffering 840 hours of collective delay. Economic burden is roughly ₹1.2 Lakhs/day due to lost productivity and wasted fuel. 145 liters of fuel wasted daily, generating 340kg of CO₂ emissions. Expected enforcement benefit is critical.
