# Trust & Reliability Center

Government deployment requires total transparency. Black-box AI models are unacceptable when determining police deployment routes and city budgets.

## 1. Zero Black-Box Guarantee
Every engine in the ParkSense platform is fundamentally deterministic or mathematically explainable.
- Our clustering uses **DBSCAN** (a mathematically rigid density algorithm, not a neural net approximation).
- Our CSI score is a **weighted mathematical formula**, not an opaque prediction.
- Our Digital Twin is a **physics-based simulation**, calculating literal road width and capacity recovery.

## 2. Explainable Predictions (SHAP)
Where we do use opaque Machine Learning (such as the Random Forest Prediction Engine), we wrap the output in **SHapley Additive exPlanations (SHAP)** approximations. The platform doesn't just say "High Risk Tomorrow." It exposes the top features driving that risk (e.g., *Proximity to Peak Hour*, *Historical Trend*).

## 3. The Score Audit Engine
We built `score_audit_engine.py` to automatically unpack and justify every single score in the system. Any auditor can query the API to see the exact formula, inputs, and weights that generated a specific CSI or PIS score for a specific road.

## 4. RAG-Enforced Copilot
The Smart City AI Copilot (SCAC™) does not use the LLM to "think" about traffic. It uses the LLM purely as a **translation layer**. The LLM reads the verified JSON calculations from the backend and translates them into English. If the JSON says CSI is 80, the Copilot can only say 80.
