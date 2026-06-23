# ParkSense AI: Demo Guide

This project is built to never fail during a live presentation.

## Offline Demo Mode
All ML models and engines have been pre-run, and their outputs are cached in `backend/data/demo_cache/`.
If you do not have a MapMyIndia API key or internet access, the system will seamlessly load the pre-calculated deterministic fallback values.

## Executing the Demo
1. **Start the backend:** `uvicorn backend.main:app --reload`
2. **Start the frontend:** `npm run dev` in the `parksense-app` folder.

## The "Golden Path" Walkthrough
1. **Show the Map:** Point out the thousands of raw tickets, now clustered into beautiful hotspots.
2. **Show the CSI:** Click on a specific point (e.g. "Konanakunte Main Road") and explain that the score is `67.6` because it blocks an emergency route.
3. **Show the Future:** Go to the Prediction tab and show how we know it will get worse tomorrow.
4. **Show the Digital Twin:** Show how towing 100% of vehicles returns exactly 62 hours of life to commuters.
5. **Show the Copilot:** Trigger the Presentation Mode endpoint to prove that the AI can explain everything in plain English.
