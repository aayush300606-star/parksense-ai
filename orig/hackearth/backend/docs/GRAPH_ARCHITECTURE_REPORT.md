# Road Network Graph Architecture Report

**Objective:** Transform independent, disparate traffic hotspots into a contiguous mathematical network.

## Graph Construction (NetworkX)
The ParkSense Urban Traffic Graph Intelligence Engine (UTGI™) utilizes **NetworkX** to build a dynamic `DiGraph` (Directed Graph) representing the city's physical geometry.

### 1. Nodes
- **Definition:** Nodes represent intersections, critical Points of Interest (POIs), and known congestion hotspots.
- **Node Features:**
  - `base_density`: The volume of illegal parking violations.
  - `lat/lng`: Geospatial coordinates.
  - `type`: "hotspot", "junction", "transit_hub".

### 2. Edges
- **Definition:** Edges represent the physical road segments connecting nodes.
- **Edge Features:**
  - `distance_km`: Calculated via Haversine formula.
  - `capacity`: Maximum vehicles per hour (VPH).
  - `lanes`: Total lane count.
  - `weight`: Used for shortest-path routing algorithms.

## Feature Extraction (Graph Theory)
Before any Machine Learning is applied, the engine calculates strict mathematical topologies:
1. **Degree Centrality:** Identifies primary hubs (e.g., a massive 6-way roundabout).
2. **Betweenness Centrality:** Identifies critical bridges. A road may have low traffic but high betweenness if it is the *only* path connecting two major city sectors.
3. **PageRank:** Identifies structural importance based on connectivity flow.

**Conclusion:** The platform no longer just understands "a road". It understands the road's structural role within the city.
