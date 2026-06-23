# The Upgraded Network CSI™ Report

**Objective:** Evolve the Adaptive Congestion Severity Index from a localized metric to a city-wide metric.

## The Limitation of Base CSI
The original CSI™ was calculated using:
`Density + Width Loss + Delay + POI Proximity`
This perfectly describes how bad *that specific road* is. However, it fails to capture network context.

## The Network CSI™ Upgrade
We shifted the paradigm from *"How bad is this road?"* to *"How bad is this road for the ENTIRE CITY?"*

### The New Formula
`Network_CSI = (Base_CSI * 0.8) + (Network_Fragility_Score * 0.2)`

By injecting the GNN-driven Network Fragility Score into the core metric, the platform now automatically elevates the priority of structurally critical hotspots, even if their isolated violation density is slightly lower than a suburban hotspot.

**Conclusion:** Network CSI™ is the ultimate, unified prioritization metric for smart city traffic enforcement.
