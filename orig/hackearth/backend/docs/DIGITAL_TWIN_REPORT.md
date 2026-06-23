# Digital Twin Showcase Guide

The Digital Twin Engine is the prescriptive powerhouse of ParkSense AI. It answers the question: *"What happens if we take action?"*

## The Problem with Traditional Planning
City planners traditionally rely on trial and error. They put up a "No Parking" sign and wait 3 months to see if traffic improves. 

## The Digital Twin Solution
Our physics-based simulation engine allows authorities to test interventions digitally before deploying physical police resources.

### Core Simulation Scenarios
1. **Monitor (Baseline):** What happens if we do nothing? (Usually predicts a worsening CSI as peak hour approaches).
2. **Ticketing/Fining:** Simulates a 30% reduction in vehicle dwell time. Modest capacity recovery.
3. **Clamping/Immobilization:** *Counter-intuitive Insight.* The simulation reveals that clamping vehicles actually **worsens** the CSI during peak hours, because the physical obstruction remains on the road permanently until the owner returns.
4. **Towing (Clearance):** Simulates 100% immediate removal of the obstruction. Maximum capacity recovery.

### Showcase Mode (For Judges)
The UI features a "One Click Simulation" button that runs all 4 scenarios simultaneously for a selected hotspot. It immediately graphs:
- **Before Action:** CSI = 88
- **After Towing:** CSI = 32
- **Capacity Recovered:** 1.5 Lanes (3.8 meters)
- **Commuter Savings:** 62 Delay Hours recovered.

This feature transforms the platform from an analytics dashboard into an **Active Decision Support System.**
