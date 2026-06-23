# Smart Enforcement Planner (SEP™)

The Smart Enforcement Planner (SEP™) acts as the operational command center. It ingests the descriptive, predictive, and prescriptive intelligence from upstream modules to construct a mathematically optimal daily patrol schedule.

## Architecture

### 1. Enforcement Priority Engine
Ranks hotspots (0-100) by fusing:
- Current CSI Score
- Current PIS Score
- Prediction Risk (1h Forecast Probability)
- Context Multipliers (Emergency Routes, Hospitals)

### 2. Time Window Engine
Uses the `peak_hour` predicted by the Temporal Engine to schedule enforcement **before** the peak hits. For example, if peak congestion is 17:00, the intervention window is set to 16:00 - 18:00 to maximize preventative impact.

### 3. Scenario Selection Engine
Interfaces with the Digital Twin to select the intervention strategy (e.g., 75% Removal vs 100% Removal) that yields the best ROI. 

### 4. Resource Allocation Engine
Simulates a constrained environment (e.g., 5 total available patrol teams). Assigns the absolute highest priority hotspots to these teams until their capacity (e.g., 5 interventions per shift) is reached.

### 5. Patrol Optimization Engine
Groups assigned hotspots by team and optimizes their patrol sequence using a geographic Nearest-Neighbor Traveling Salesperson (TSP) heuristic to minimize driving time between interventions.

### 6. Explainability Engine
Generates human-readable operational reasoning for police dispatchers.
*Example: "Priority #1. Reason: CSI=92, PIS=95. Critical Emergency Route. Action: 100% Illegal Parking Removal. Expected Capacity Recovery = 48%."*

## Output Files
- `enforcement_plan.json`: The ranked and assigned orders for all targeted hotspots.
- `daily_plan.json`: The compiled daily schedule grouped by Patrol Team.
- `weekly_strategy.json`: Macro-level trends and resource shift recommendations.

## APIs
- `GET /api/enforcement-plan`
- `GET /api/daily-plan`
- `GET /api/weekly-plan`
