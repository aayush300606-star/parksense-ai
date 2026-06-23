# CSI™ + PIS™ Engine Documentation

The Adaptive Congestion Severity Index (CSI™) and Parking Impact Score (PIS™) are the **capstone analytics outputs** of ParkSense AI. They fuse all 5 upstream intelligence layers into two flagship scores.

## 1. Architecture

```
Upstream Intelligence Layers:
┌──────────────────────────────────────────────┐
│  Violation Density  │  Road Intelligence     │
│  Road Impact        │  Traffic Intelligence  │
│  Context Intelligence                        │
└──────────────┬───────────────────────────────┘
               ↓
        Temporal Pattern Engine
        (raw dataset analysis)
               ↓
        CSI Engine (5-signal fusion)
               ↓
        PIS Engine (enforcement priority)
               ↓
        Hotspot Ranking Engine
        (city-wide ordering + percentiles)
               ↓
        CSI Explainability Engine
               ↓
        4 Structured JSON Outputs + 6 APIs
```

## 2. Congestion Severity Index (CSI™)

### Formula

```
CSI = Traffic_Congestion × 0.30
    + Capacity_Loss × 0.25
    + Context_Importance × 0.20
    + Violation_Intensity × 0.15
    + Road_Priority × 0.10
```

### Component Sources

| Component | Source | Range |
|-----------|--------|-------|
| Traffic Congestion | `congestion_impact_score` from BPR model | 73.5 – 84.8 |
| Capacity Loss | `capacity_loss_percentage` from Road Impact | 0 – 100 |
| Context Importance | `context_importance_score` from Context Intelligence | 18.3 – 63.0 |
| Violation Intensity | `violation_density_score` from Density Engine | 0 – 100 |
| Road Priority | `road_priority_score` from Road Hierarchy | 40 – 90 |

### Severity Bands

| Range | Severity |
|-------|----------|
| 80-100 | Critical |
| 60-80 | High |
| 40-60 | Moderate |
| 20-40 | Low |
| 0-20 | Minimal |

### Observed Results

- **CSI Range**: 58.1 – 72.2 (Mean: 62.4, Std Dev: 3.4)
- **Distribution**: 69 High, 31 Moderate
- **#1 Hotspot**: Konanakunte Main Road (CSI 72.2) — Major Arterial with emergency route impact

## 3. Parking Impact Score (PIS™)

### Formula

```
PIS = CSI × 0.45
    + Emergency_Factor × 0.20
    + Violation_Volume × 0.15
    + Temporal_Recurrence × 0.10
    + Critical_Infrastructure × 0.10
```

PIS amplifies CSI with enforcement-relevant factors:
- **Emergency Factor**: Emergency access impact score from Context Intelligence
- **Violation Volume**: Min-max normalized violation count across all hotspots
- **Temporal Recurrence**: Month-over-month consistency from Temporal Pattern Engine
- **Critical Infrastructure**: Nearby hospital/transit/government score

### Priority Classification

| Range | Priority | Action |
|-------|----------|--------|
| ≥85 | P1-Immediate | Deploy enforcement within 24 hours |
| ≥70 | P2-High | Schedule enforcement this week |
| ≥50 | P3-Moderate | Monthly enforcement rotation |
| ≥30 | P4-Low | Monitor and record |
| <30 | P5-Monitor | Passive observation |

### Observed Results

- **PIS Range**: 32.2 – 65.5 (Mean: 36.6)
- **Distribution**: 3 P3-Moderate, 97 P4-Low
- **#1 by PIS**: 5th Main Road / Kempe Gowda Circle (PIS 65.5) — highest enforcement urgency

## 4. Temporal Pattern Engine

Analyzes the raw 298,450-row violation dataset to extract:

- **Hourly distribution**: Violation counts per hour of day
- **Daily distribution**: Weekday vs weekend patterns
- **Monthly coverage**: How many months have violations (Jan-May)
- **Temporal Recurrence Score** (0-100):
  ```
  Recurrence = Month_Coverage × 0.60 + Consistency × 0.40
  ```
  Where consistency uses coefficient of variation (lower CV = more consistent = higher score)

## 5. Hotspot Ranking Engine

- Sorts all hotspots by CSI (primary), PIS (secondary)
- Assigns **rank** (1-100), **percentile** (0-100), and **tier** (Top 10%, Top 25%, etc.)
- Generates **city-wide analytics**: statistics, distributions, annual delay totals

## 6. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/csi` | Full CSI + PIS for all hotspots (ranked) |
| GET | `/api/csi/{id}` | Per-hotspot CSI intelligence |
| GET | `/api/csi-rankings` | Compact rankings (supports `?top=N`) |
| GET | `/api/pis` | Parking Impact Scores + recommendations |
| GET | `/api/city-analytics` | City-wide aggregate dashboard data |
| GET | `/api/temporal-patterns` | Time-of-day/day-of-week analysis |

## 7. JSON Outputs

| File | Content |
|------|---------|
| `csi_intelligence.json` | Full CSI+PIS objects with rankings + explainability |
| `csi_rankings.json` | Compact ranked list with tier classification |
| `csi_city_analytics.json` | Aggregate statistics, distributions, top-5 |
| `temporal_patterns.json` | Hourly/daily distributions, recurrence scores |

## 8. Complete Pipeline

```
Raw Dataset (298,450 violations)
  → Preprocessing
  → DBSCAN Hotspot Detection (100 clusters)
  → Violation Density Engine
  → Road Intelligence Layer
  → Effective Road Width Loss Engine
  → Traffic Intelligence Engine
  → Context Intelligence Engine
  → CSI™ + PIS™ Engine  ← THIS MODULE
  → City-wide Rankings + Analytics
```

## 9. City Impact Summary

| Metric | Value |
|--------|-------|
| Total hotspots analyzed | 100 |
| Average CSI | 62.4/100 |
| Total annual delay | 2,942,737 vehicle-hours |
| Emergency route hotspots | 1 |
| Worst hotspot | Konanakunte Main Road (CSI 72.2) |
