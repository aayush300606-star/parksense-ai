# AI Data Foundation Pipeline

This document explains the real, data-driven ML architecture that replaces the previous mocked script.

## 1. Preprocessing (`backend/ai/preprocessing.py`)
- **How it works**: Loads the 109MB `jan to may police violation_anonymized791b166.csv` dataset using Pandas.
- **Cleaning**: Drops duplicates, drops missing coordinates, filters out completely invalid lat/longs that fall outside the Bangalore geographical bounds.
- **Features**: Converts timestamps to actual `datetime` objects. Extracts new contextual features: `hour`, `day`, `weekday`, `month`, `is_weekend`, `peak_hour`, and `time_slot` (Morning/Afternoon/Evening/Night). 
- **Output**: `backend/data/processed/cleaned_dataset.csv`.

## 2. DBSCAN Hotspot Detection (`backend/ai/hotspot_detection.py`)
- **How it works**: Scikit-learn's DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups closely packed violation coordinates into spatial clusters.
- **Real Metrics**: 
  - Instead of euclidean distance on raw degrees, it uses the **Haversine metric** to calculate accurate great-circle distances in kilometers.
  - Generates a **cluster_radius** by finding the max distance from the center to any edge violation.
  - Generates a **cluster_area** ($A = \pi r^2$) representing the physical footprint of the hotspot.
- **Output**: `backend/data/processed/hotspots.json`.

## 3. Violation Density Engine (`backend/ai/violation_density.py`)
- **How it works**: Density is calculated purely as:
  $$ \text{Violation Density} = \frac{\text{Number of Violations}}{\text{Cluster Area}} $$
- **Normalization**: It takes these raw densities and applies Min-Max Scaling so that the scores map smoothly to a 0-100 scale (`violation_density_score`).
- **Output**: `backend/data/processed/hotspots_with_density.json`.

## 4. Backend APIs & Future Usage
- **FastAPI Core**: A standard `Hotspot` Pydantic model is exposed over `/api/hotspots` providing structured intelligence objects.
- **Legacy Compatibility**: A startup hook in `main.py` executes the entire pipeline and automatically writes the output to `parksense-app/public/data/hotspots.json` using mathematically derived legacy fields (e.g., mapping density score directly to CSI), ensuring the existing Next.js frontend works completely unchanged.

## What Files Are Generated
1. `backend/data/processed/cleaned_dataset.csv`: The sanitized, chronologically sorted dataset with temporal features.
2. `backend/data/processed/hotspots.json`: Raw DB-SCAN clusters.
3. `backend/data/processed/hotspots_with_density.json`: Final clusters with calculated physical density.
4. `parksense-app/public/data/hotspots.json`: The legacy payload generated for UI compatibility.
