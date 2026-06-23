# Context Intelligence Engine

This module is the **location-awareness layer** of ParkSense AI. It transforms raw hotspot coordinates into rich contextual profiles that explain *why* illegal parking at a specific location matters more than at another.

## 1. Architecture

```
Hotspot Data + Road Intelligence + Road Impact
    ↓
Geospatial KDTree Index (scipy.spatial)
    ↓
┌─────────────────────────────────────┐
│        Junction Intelligence        │
│  Detection → Importance → Influence │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│          POI Intelligence           │
│  Discovery → Critical Infra →      │
│  Emergency Access → Density         │
└─────────────────────────────────────┘
    ↓
Context Importance Engine (weighted aggregation)
    ↓
Context Explainability Engine
    ↓
5 Structured JSON APIs
```

## 2. Geospatial Index (`geospatial_index.py`)

Built on `scipy.spatial.KDTree` for O(log n) spatial queries.

**Projection**: Equirectangular flat-earth approximation centered on the dataset centroid. Converts WGS84 lat/lon to local meters for accurate Euclidean distance queries within ~100km of centroid (more than sufficient for a single city).

**Operations**:
- `query_radius(lat, lon, radius_m)` — All hotspots within radius
- `query_nearest(lat, lon, k)` — K-nearest hotspots
- `haversine_distance()` — Precise great-circle distance

This index is reused by future modules: Digital Twin, Prediction Engine, Routing.

## 3. Junction Intelligence

### 3.1 Junction Detection (`junction_intelligence_engine.py`)

**Strategy 1: MapMyIndia Nearby Search API**
When `MAPMYINDIA_API_KEY` is set, queries the Mappls API for nearby junctions, intersections, and signals within 500m.

**Strategy 2: Deterministic Geospatial Analysis**
When API is unavailable, uses three analysis phases:

1. **Keyword Extraction**: Parses location names for junction indicators (`circle`, `signal`, `cross`, `junction`, `flyover`, `underpass`, `chowk`, `gate`, `square`)
2. **Road Pattern Analysis**: Detects Bengaluru-style "Nth Cross Road" / "Nth Main Road" patterns indicating T-junctions
3. **Convergence Analysis**: Uses KDTree to find nearby hotspots with different road names, indicating road convergence at junctions

**Junction Types**: Traffic Circle, Signal Junction, Cross Junction, T-Junction, Flyover Junction, Underpass Junction, Uncontrolled Junction

### 3.2 Junction Importance (`junction_importance_engine.py`)

Classifies junction importance (0-100):

| Junction Type        | Base Score | × Hierarchy Multiplier |
|---------------------|-----------|----------------------|
| Traffic Circle       | 85        | Expressway: 1.20     |
| Signal Junction      | 75        | Major Arterial: 1.10 |
| Flyover Junction     | 70        | Collector: 0.90      |
| Cross Junction       | 50        | Residential: 0.65    |
| T-Junction           | 40        | Service: 0.50        |
| Uncontrolled         | 25        |                      |

Additional bonuses for connected road count and signalization.

### 3.3 Junction Influence (`junction_influence_engine.py`)

Exponential decay model:
```
Influence Score = 100 × e^(-distance / 80m)
```

| Distance | Level     | Score |
|----------|-----------|-------|
| ≤5m      | Very High | 100   |
| ≤20m     | High      | 80    |
| ≤50m     | Medium    | 60    |
| ≤100m    | Low       | 40    |
| ≤300m    | Minimal   | 20    |
| >300m    | None      | 5     |

## 4. POI Intelligence

### 4.1 POI Discovery (`poi_intelligence_engine.py`)

**Multi-radius analysis**: 300m, 500m, 1000m around each hotspot.

**14 POI categories**: Hospital, School, College, Metro Station, Bus Station, Railway Station, Market, Mall, Government Office, Police Station, Fire Station, Industrial Area, Business District, Religious Place, Park, Transit Hub.

**MapMyIndia API integration**: When API key available, queries Mappls Nearby Search for each category. Falls back to deterministic keyword extraction from the rich Bengaluru location names and nearby hotspot contexts.

### 4.2 Critical Infrastructure (`critical_infrastructure_engine.py`)

Filters POIs to 8 critical types (Hospital, Fire, Police, Metro, Railway, Bus, Government, Transit Hub).

Scoring formula (logarithmic saturation):
```
Score = 100 × (1 - e^(-weighted_sum / 150))
```
Where weighted_sum = Σ(category_weight × proximity_multiplier).

### 4.3 Emergency Access (`emergency_access_engine.py`)

Three-factor composite:
```
Score = Infrastructure_Score × 0.50 + Route_Probability × 0.25 + Capacity_Factor × 0.25
```

**Emergency Priority Classification**:
- P1-Critical (≥80): Immediate enforcement required
- P2-High (≥60): High-priority patrol
- P3-Moderate (≥40): Scheduled enforcement
- P4-Low (≥20): Monitoring
- P5-Informational (<20): Record only

### 4.4 POI Density (`poi_density_engine.py`)

Radius-weighted density:
```
Weighted Density = (count_300m × 3.0) + (count_500m × 2.0) + (count_1000m × 1.0)
```
Min-max normalized across all hotspots to 0-100.

## 5. Context Importance Aggregation

### Formula (`context_importance_engine.py`)

| Component                  | Weight |
|---------------------------|--------|
| Junction Importance        | 0.20   |
| Junction Influence         | 0.20   |
| POI Density                | 0.20   |
| Critical Infrastructure    | 0.25   |
| Emergency Access           | 0.15   |

**Levels**: Very Low (<20), Low (20-40), Moderate (40-60), High (60-80), Critical (80-100)

## 6. API Endpoints

| Method | Endpoint                           | Description                          |
|--------|-------------------------------------|--------------------------------------|
| GET    | `/api/junction-intelligence`        | Junction data for all hotspots       |
| GET    | `/api/poi-intelligence`             | Multi-radius POI data                |
| GET    | `/api/context-intelligence`         | Full context intelligence objects    |
| GET    | `/api/context-intelligence/{id}`    | Per-hotspot context data             |
| GET    | `/api/emergency-impact`             | Emergency access analysis            |
| GET    | `/api/context-summary`              | Aggregate statistics                 |

## 7. Output JSON Files

| File                        | Content                               |
|-----------------------------|---------------------------------------|
| `context_intelligence.json` | Complete context objects (28 fields)   |
| `junction_intelligence.json`| Junction detection + importance data  |
| `poi_intelligence.json`     | Multi-radius POI discovery results    |
| `critical_infrastructure.json` | Critical infrastructure scores     |
| `emergency_access.json`     | Emergency impact analysis             |

## 8. Future CSI Integration

The Context Intelligence object provides the final input layer for the Adaptive Congestion Severity Index (CSI™):

```
CSI = f(
    Traffic Intelligence,      ← Task 4
    Context Intelligence,      ← Task 5 (this module)
    Temporal Intelligence,     ← Future
    Enforcement Intelligence   ← Future
)
```

The `context_importance_score` directly modulates the CSI: a hotspot with Critical context importance will have its congestion severity amplified, while a Very Low context hotspot will have reduced priority even with the same traffic impact.
