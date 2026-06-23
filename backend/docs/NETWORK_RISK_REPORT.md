# Network Risk & Vulnerability Report

**Objective:** Identify the absolute most fragile points of failure in the city's infrastructure.

## The Network Fragility Score
We created a composite metric to fuse our Deep Learning output with strict graph mathematics.

### The Equation
`Fragility = (GNN_Risk * 0.5) + (Normalized_Betweenness * 0.3) + (Ripple_Score * 0.2)`

### Why this works:
- **GNN Risk:** Captures the complex ML prediction of cascade failure.
- **Betweenness Centrality:** Ensures that structurally critical bridges and arterial highways are heavily penalized if they become congested.
- **Ripple Score:** Accounts for the sheer volume of adjacent roads that will be destroyed by the spillover.

### Output Classifications
- **Critical (> 80):** Total network cascade failure imminent. Immediate towing required.
- **High (60 - 80):** Severe regional delay expected.
- **Moderate (< 60):** Localized delay.

**Conclusion:** This engine tells the Smart Enforcement Planner precisely which hotspots will trigger a city-wide gridlock if ignored.
