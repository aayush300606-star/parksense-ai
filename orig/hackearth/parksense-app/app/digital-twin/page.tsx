"use client";

import { useState, useEffect } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Play, RotateCcw, FastForward, Activity } from "lucide-react";

export default function DigitalTwinPage() {
  const [simulationData, setSimulationData] = useState<any[]>([]);
  const [selectedZone, setSelectedZone] = useState<any>(null);
  const [scenario, setScenario] = useState<"current" | "reduction_50" | "reduction_100">("current");
  const [isSimulating, setIsSimulating] = useState(false);

  useEffect(() => {
    fetch('/data/simulation.json')
      .then(res => res.json())
      .then(data => {
        setSimulationData(data);
        if (data.length > 0) setSelectedZone(data[0]);
      });
  }, []);

  const runSimulation = (targetScenario: "current" | "reduction_50" | "reduction_100") => {
    setIsSimulating(true);
    setScenario(targetScenario);
    setTimeout(() => setIsSimulating(false), 1500); // Mock simulation delay
  };

  if (!selectedZone) return null;

  const currentMetrics = selectedZone.scenarios[scenario];
  const baselineMetrics = selectedZone.scenarios.current;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Digital Twin Simulation</h1>
          <p className="text-slate-400">Simulate traffic impact by dynamically removing illegal parking.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls & Scenarios */}
        <div className="lg:col-span-4 space-y-6">
          <GlassCard>
            <h3 className="font-semibold text-white mb-4">Select Hotspot Zone</h3>
            <select 
              className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              onChange={(e) => {
                const zone = simulationData.find(z => z.id.toString() === e.target.value);
                if (zone) setSelectedZone(zone);
                setScenario("current");
              }}
            >
              {simulationData.map(zone => (
                <option key={zone.id} value={zone.id}>{zone.location_name}</option>
              ))}
            </select>
          </GlassCard>

          <GlassCard>
            <h3 className="font-semibold text-white mb-4">Run Scenario</h3>
            <div className="space-y-3">
              <button 
                onClick={() => runSimulation("current")}
                className={`w-full p-3 rounded-lg flex items-center justify-between transition-colors border ${scenario === 'current' ? 'bg-slate-700 border-slate-500' : 'bg-slate-800 border-slate-700 hover:bg-slate-750'}`}
              >
                <div className="flex items-center gap-3 text-white">
                  <Activity className="w-4 h-4 text-rose-400" />
                  <span>Current State (Baseline)</span>
                </div>
                {scenario === 'current' && !isSimulating && <div className="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></div>}
              </button>

              <button 
                onClick={() => runSimulation("reduction_50")}
                className={`w-full p-3 rounded-lg flex items-center justify-between transition-colors border ${scenario === 'reduction_50' ? 'bg-slate-700 border-slate-500' : 'bg-slate-800 border-slate-700 hover:bg-slate-750'}`}
              >
                <div className="flex items-center gap-3 text-white">
                  <Play className="w-4 h-4 text-amber-400" />
                  <span>50% Parking Removed</span>
                </div>
                {scenario === 'reduction_50' && !isSimulating && <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></div>}
              </button>

              <button 
                onClick={() => runSimulation("reduction_100")}
                className={`w-full p-3 rounded-lg flex items-center justify-between transition-colors border ${scenario === 'reduction_100' ? 'bg-slate-700 border-slate-500' : 'bg-slate-800 border-slate-700 hover:bg-slate-750'}`}
              >
                <div className="flex items-center gap-3 text-white">
                  <FastForward className="w-4 h-4 text-emerald-400" />
                  <span>100% Parking Removed</span>
                </div>
                {scenario === 'reduction_100' && !isSimulating && <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>}
              </button>
            </div>
            
            <div className="mt-6 p-4 rounded-lg bg-blue-900/20 border border-blue-500/30">
              <p className="text-xs text-blue-200">
                This digital twin uses the Greenshields macroscopic traffic flow model to estimate queue reduction and speed improvements upon removing lane blockages.
              </p>
            </div>
          </GlassCard>
        </div>

        {/* Visualizer & Metrics */}
        <div className="lg:col-span-8 space-y-6">
          {/* Animated Map Area Mockup */}
          <GlassCard className="h-64 flex flex-col items-center justify-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
            
            {isSimulating ? (
              <div className="flex flex-col items-center justify-center z-10">
                <RotateCcw className="w-10 h-10 text-blue-400 animate-spin mb-4" />
                <span className="text-lg font-bold text-white tracking-widest uppercase">Simulating Traffic Flow...</span>
              </div>
            ) : (
              <div className="z-10 w-full px-8">
                <div className="flex justify-between items-center mb-6">
                  <span className="px-3 py-1 bg-slate-800 rounded-full border border-slate-700 text-xs font-semibold text-slate-300">
                    {selectedZone.location_name}
                  </span>
                  <span className={`px-3 py-1 rounded-full border text-xs font-bold uppercase tracking-wider ${
                    scenario === 'current' ? 'bg-rose-500/20 border-rose-500/50 text-rose-400' :
                    scenario === 'reduction_50' ? 'bg-amber-500/20 border-amber-500/50 text-amber-400' :
                    'bg-emerald-500/20 border-emerald-500/50 text-emerald-400'
                  }`}>
                    {scenario.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
                
                {/* Visual lane mockup */}
                <div className="relative h-20 bg-slate-800 rounded-lg border border-slate-700 overflow-hidden flex items-center">
                  <div className="absolute top-1/2 w-full border-t-2 border-dashed border-slate-600"></div>
                  
                  {/* Cars */}
                  <div className={`absolute transition-all duration-1000 ease-in-out ${
                    scenario === 'current' ? 'left-[10%] w-[60%]' : 
                    scenario === 'reduction_50' ? 'left-[20%] w-[30%]' : 
                    'left-[50%] w-[10%]'
                  } flex gap-2 h-8`}>
                    {[1,2,3,4,5].map(i => (
                      <div key={i} className="w-8 h-full bg-slate-300 rounded shadow-[0_2px_10px_rgba(255,255,255,0.2)]" />
                    ))}
                  </div>

                  {/* Blockage */}
                  {scenario !== 'reduction_100' && (
                    <div className={`absolute bottom-1 right-10 h-6 bg-rose-500/50 border border-rose-500 rounded transition-all duration-500 ${
                      scenario === 'current' ? 'w-48' : 'w-24'
                    }`}>
                      <div className="w-full h-full flex items-center justify-center text-[8px] text-rose-200 font-bold uppercase">
                        Illegal Parking
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </GlassCard>

          {/* Metrics Comparison */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <GlassCard glowColor="blue">
              <div className="text-sm text-slate-400 mb-2">Average Speed</div>
              <div className="text-4xl font-bold text-white mb-2">
                {isSimulating ? "..." : currentMetrics?.speed_kmh.toFixed(1)} <span className="text-lg text-slate-500">km/h</span>
              </div>
              {!isSimulating && scenario !== 'current' && (
                <div className="text-sm font-semibold text-emerald-400">
                  +{((currentMetrics.speed_kmh - baselineMetrics.speed_kmh) / baselineMetrics.speed_kmh * 100).toFixed(0)}% Improvement
                </div>
              )}
            </GlassCard>

            <GlassCard glowColor="rose">
              <div className="text-sm text-slate-400 mb-2">Queue Length</div>
              <div className="text-4xl font-bold text-white mb-2">
                {isSimulating ? "..." : currentMetrics?.queue_length_m.toFixed(0)} <span className="text-lg text-slate-500">m</span>
              </div>
              {!isSimulating && scenario !== 'current' && (
                <div className="text-sm font-semibold text-emerald-400">
                  -{((baselineMetrics.queue_length_m - currentMetrics.queue_length_m) / baselineMetrics.queue_length_m * 100).toFixed(0)}% Reduction
                </div>
              )}
            </GlassCard>

            <GlassCard glowColor="emerald">
              <div className="text-sm text-slate-400 mb-2">Travel Time</div>
              <div className="text-4xl font-bold text-white mb-2">
                {isSimulating ? "..." : currentMetrics?.travel_time_mins.toFixed(1)} <span className="text-lg text-slate-500">min</span>
              </div>
              {!isSimulating && scenario !== 'current' && (
                <div className="text-sm font-semibold text-emerald-400">
                  Saved {(baselineMetrics.travel_time_mins - currentMetrics.travel_time_mins).toFixed(1)} mins
                </div>
              )}
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  );
}
