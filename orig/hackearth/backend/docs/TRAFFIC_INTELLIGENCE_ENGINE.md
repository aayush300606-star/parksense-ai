# Traffic Intelligence Engine

This module is the **congestion quantification core** of ParkSense AI. It transforms upstream capacity loss metrics into actionable traffic flow degradation measurements using macroscopic transportation engineering models.

## 1. Architecture

```
Road Intelligence → Road Impact (Width/Capacity/Lane Loss)
    ↓
Base Speed Engine (IRC free-flow speeds)
    ↓
Traffic Speed Engine (BPR-adapted urban model)
    ↓
Travel Time Engine (distance / speed)
    ↓
Delay Estimation Engine (per-vehicle + annualized)
    ↓
Congestion Impact Engine (multi-signal weighted aggregator)
    ↓
Traffic Explainability Engine (human-readable narratives)
    ↓
Structured JSON APIs
```

## 2. Engine Specifications

### 2.1 Base Speed Engine (`base_speed_engine.py`)

Maps road hierarchy to standard free-flow speeds derived from **IRC (Indian Roads Congress)** urban design standards:

| Road Hierarchy   | Free-Flow Speed (km/h) | Baseline V/C Ratio |
|------------------|----------------------:|--------------------:|
| Expressway       | 80                    | 0.30                |
| Major Arterial   | 60                    | 0.45                |
| Minor Arterial   | 50                    | 0.50                |
| Collector        | 40                    | 0.55                |
| Secondary        | 35                    | 0.60                |
| Residential      | 25                    | 0.65                |
| Service          | 20                    | 0.70                |

### 2.2 Traffic Speed Engine (`traffic_speed_engine.py`)

Uses an adapted **Bureau of Public Roads (BPR) function**:

```
Standard BPR:   t = t₀ × [1 + α × (V/C)^β]
Our adaptation: Speed Factor = 1 / [1 + α × (Adjusted V/C)^β]
                Current Speed = Base Speed × Speed Factor
```

**Calibration:**
- **α = 0.15** (sensitivity coefficient, tuned for urban context)
- **β = 4.0** (standard exponential growth factor)
- **Capacity Loss Amplifier = 1.2** (how much 1% capacity loss raises V/C)

The V/C ratio increases as parking eats capacity, causing non-linear speed degradation.

**Severity thresholds:**
- Critical: ≥60% speed reduction
- Severe: ≥40%
- Moderate: ≥25%
- Low: ≥10%
- Minimal: <10%

### 2.3 Travel Time Engine (`travel_time_engine.py`)

```
Normal Time (s) = Road Segment Length (m) / Base Speed (m/s)
Current Time (s) = Road Segment Length (m) / Current Speed (m/s)
```

Road segment length is derived from the DBSCAN cluster diameter (2 × cluster_radius), representing the localized stretch where the parking impact is physically felt.

### 2.4 Delay Estimation Engine (`delay_estimation_engine.py`)

```
Per-Vehicle Delay (s) = Current Time − Normal Time
Daily Vehicle-Hours = (ADT × Congestion Hours Fraction × Delay) / 3600
Annual Vehicle-Hours = Daily × 300 days (chronic hotspot assumption)
```

**Average Daily Traffic (ADT) by hierarchy:**

| Road Hierarchy   | ADT (vehicles/day) |
|------------------|-------------------:|
| Expressway       | 40,000             |
| Major Arterial   | 25,000             |
| Collector        | 8,000              |
| Residential      | 2,000              |
| Service          | 800                |

**Congestion hours fraction:** 6/24 (peak morning + evening hours).

### 2.5 Congestion Impact Engine (`congestion_impact_engine.py`)

Multi-signal weighted aggregator producing a **0-100 Congestion Impact Score**:

| Component             | Weight | Source                      |
|-----------------------|-------:|-----------------------------|
| Speed Reduction %     | 0.30   | Traffic Speed Engine        |
| Capacity Loss %       | 0.25   | Road Impact Service         |
| Lane Blockage Score   | 0.20   | Lane Blockage Engine        |
| Delay Severity Factor | 0.15   | Delay Estimation Engine     |
| Road Priority Factor  | 0.10   | Road Hierarchy Engine       |

**Severity thresholds:**
- Critical: ≥80
- Severe: ≥60
- Moderate: ≥40
- Low: ≥20
- Minimal: <20

### 2.6 Traffic Explainability Engine (`traffic_explainability_engine.py`)

Generates human-readable, multi-sentence impact narratives including:
- Speed reduction causation chain
- Per-vehicle delay quantification
- Annual projected impact
- Actionable enforcement recommendations

## 3. API Endpoints

| Method | Endpoint                              | Description                           |
|--------|---------------------------------------|---------------------------------------|
| GET    | `/api/traffic-intelligence`           | Full traffic intelligence objects     |
| GET    | `/api/speed-analysis`                 | Speed reduction analysis subset       |
| GET    | `/api/delay-analysis`                 | Delay estimation analysis subset      |
| GET    | `/api/congestion-impact`              | Congestion Impact Score subset        |
| GET    | `/api/traffic-intelligence/{id}`      | Per-hotspot traffic intelligence      |

## 4. Output JSON Files

| File                        | Content                               |
|-----------------------------|---------------------------------------|
| `traffic_intelligence.json` | Complete traffic intelligence objects  |
| `speed_analysis.json`       | Speed-focused dashboard subset        |
| `delay_analysis.json`       | Delay-focused dashboard subset        |
| `congestion_impact.json`    | Congestion score dashboard subset     |

## 5. Design Decisions

1. **BPR over Greenshields**: The BPR function handles oversaturated conditions (V/C > 1) more gracefully than Greenshields, which collapses to zero speed at jam density.

2. **Cluster diameter as road_length**: The DBSCAN cluster radius defines the spatial extent of each parking violation zone. The diameter (2r) is the physical stretch over which congestion materializes.

3. **Minimum crawl speed = 3 km/h**: Macroscopic models assume continuous flow. A 3 km/h floor prevents unrealistic zero-speed predictions while still indicating near-gridlock conditions.

4. **300-day annualization**: Chronic parking violation hotspots are assumed to exhibit consistent behavior on weekdays and partial weekends, yielding ~300 effective violation days per year.
