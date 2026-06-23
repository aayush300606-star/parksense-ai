# KPI Methodology & Calculation Report

This report defines the core Key Performance Indicators (KPIs) exposed to the executive dashboard, using procurement-grade terminology suitable for government deployment.

## 1. Congestion Severity Index (CSI™)
**Definition:** A universal metric (0-100) indicating the physical severity and contextual danger of a parking-induced bottleneck.
**Methodology:** Combines physical width loss, traffic speed reduction, and spatial proximity to critical infrastructure (hospitals, fire stations).
**Confidence:** 0.95 (Based on deterministic spatial formulas).

## 2. Parking Impact Score (PIS™)
**Definition:** The tangible economic and environmental damage caused by the bottleneck, localized to the specific road segment.
**Methodology:** 
- *Economic Loss:* (Average Commuter Delay Hours) × (Average Regional Hourly Wage).
- *Environmental Loss:* (Idling Fuel Consumption Rate) × (Fuel Cost).
**Confidence:** 0.85 (Relies on regional wage proxy variables).

## 3. Capacity Recovery Expectation
**Definition:** The exact percentage of road bandwidth restored if a specific enforcement action is taken.
**Methodology:** Digital Twin simulation subtracts the physical dimensions of the illegally parked vehicles from the road and recalculates the traffic flow capacity (Vehicles Per Hour).

## 4. Expected Congestion Reduction (ROI)
**Definition:** The operational benefit returned to the city per enforcement action dispatched.
**Methodology:** Ratio of the simulated CSI reduction against the manpower/equipment cost of the intervention.
