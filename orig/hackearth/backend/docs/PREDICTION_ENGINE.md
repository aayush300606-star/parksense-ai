# AI Prediction Engine

The Prediction Engine transforms the platform from a descriptive system ("what is happening") into a predictive system ("what is likely to happen next").

## ML Architecture

To ensure zero "fake predictions", the system implements a genuine machine learning pipeline utilizing scikit-learn.

### 1. Feature Store Bootstrap
Since massive historical timeseries data may be unavailable in early deployments, the `FeatureStoreEngine` dynamically bootstraps a realistic synthetic training dataset. It takes the current live intelligence (CSI, PIS, Traffic, Context) and perturbs it backward over 14 days using known temporal rules (e.g., peak hour multipliers, weekend reductions, and random noise).

### 2. Model Training
`ModelEngine` trains two algorithms on this dataset:
- `RandomForestRegressor`
- `HistGradientBoostingRegressor` (a fast approximation of LightGBM)

It automatically selects the model with the highest R² score for both the CSI Forecast and PIS Forecast tasks.

### 3. Feature Engineering
`TemporalFeatureEngine` ensures that cyclical time variables are properly encoded. Hours and Days of the Week are converted into sine and cosine coordinates (`hour_sin`, `hour_cos`) to prevent the model from assuming that Hour 23 and Hour 0 are numerically distant.

## The 5 Forecasting Horizons
For every active hotspot, the trained ML models run inference to forecast values at 4 distinct time horizons:
- **1 Hour (Immediate Response)**
- **6 Hours (Shift Planning)**
- **24 Hours (Next Day Planning)**
- **7 Days (Weekly Resource Allocation)**

## Explainability
The ML models are not black boxes. `FeatureImportanceEngine` extracts the exact features driving the model (e.g., `traffic_impact`, `is_peak_hour`). 

`PredictionExplainabilityEngine` translates these mathematical weights into Natural Language:
> "Predicted CSI Increase (+8.4) in 1h. Reason: Approaching Wednesday 09:00 AM conditions. Key drivers: Traffic Impact, Peak Hour Traffic Growth. High likelihood of severe bottleneck forming."

## APIs
- `GET /api/predictions`: Full forecast for all horizons.
- `GET /api/future-risk-zones`: Filtered list of areas predicted to hit "Critical Risk".
- `GET /api/enforcement-forecasts`: Recommended patrol times based on forecasted PIS peaks.
