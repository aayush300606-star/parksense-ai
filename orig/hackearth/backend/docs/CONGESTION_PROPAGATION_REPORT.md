# Congestion Propagation & Ripple Effect Report

**Objective:** Map exactly how far a traffic jam will spread.

## The Propagation Engine
When a hotspot reaches critical mass, the traffic queue spills backward into previous intersections. We model this using bounded **Breadth-First Search (BFS)** and Shortest-Path algorithms across the NetworkX graph.

### The 3 Zones of Impact
For any given epicenter, the engine calculates:
1. **Primary Impact Zone (< 1.0 km):** Direct gridlock. Emergency vehicles cannot pass.
2. **Secondary Impact Zone (1.0 - 2.5 km):** Heavy slowdowns. Intersection blocking occurs.
3. **Tertiary Impact Zone (2.5 - 5.0 km):** Rerouting behavior begins. Alternate corridors experience unnatural volume spikes.

### The Ripple Effect Score
We quantify this damage into a single integer. A hotspot that spills into 5 major arteries will have a massive Ripple Score compared to a hotspot that spills into a dead-end residential street.

**Conclusion:** Planners can now triage parking enforcement based on "Blast Radius" rather than just isolated severity.
