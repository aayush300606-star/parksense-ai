"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Map, Filter, Layers, Clock } from "lucide-react";

// Dynamic import for Leaflet (no SSR)
const MapComponent = dynamic(() => import("@/components/maps/MapComponent"), { 
  ssr: false,
  loading: () => <div className="w-full h-full flex items-center justify-center bg-slate-900 rounded-xl border border-slate-800 text-blue-400">Loading Intelligence Map...</div>
});

export default function HeatmapPage() {
  const [hotspots, setHotspots] = useState([]);
  const [viewMode, setViewMode] = useState<"clusters" | "heatmap">("clusters");
  
  useEffect(() => {
    fetch('/data/hotspots.json')
      .then(res => res.json())
      .then(data => setHotspots(data));
  }, []);

  return (
    <div className="flex flex-col h-[calc(100vh-3rem)] space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Geospatial Intelligence</h1>
          <p className="text-slate-400">Interactive heatmap of parking violations and congestion impact.</p>
        </div>
        
        <div className="flex gap-3">
          <button 
            onClick={() => setViewMode("clusters")}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-all ${viewMode === 'clusters' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
          >
            <Map className="w-4 h-4" />
            Cluster View
          </button>
          <button 
            onClick={() => setViewMode("heatmap")}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-all ${viewMode === 'heatmap' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
          >
            <Layers className="w-4 h-4" />
            Density Heatmap
          </button>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Filters */}
        <div className="lg:col-span-1 space-y-6">
          <GlassCard>
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <Filter className="w-4 h-4 text-blue-400" /> Filters
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-2 block">Time Window</label>
                <div className="flex bg-slate-800 rounded-lg p-1">
                  <button className="flex-1 px-2 py-1.5 text-xs font-medium bg-blue-600/20 text-blue-400 rounded-md">Today</button>
                  <button className="flex-1 px-2 py-1.5 text-xs font-medium text-slate-400 hover:text-white">Week</button>
                  <button className="flex-1 px-2 py-1.5 text-xs font-medium text-slate-400 hover:text-white">Month</button>
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-2 block">Severity Level</label>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 text-sm text-slate-300">
                    <input type="checkbox" defaultChecked className="rounded bg-slate-800 border-slate-600 text-rose-500 focus:ring-rose-500" />
                    Critical (CSI &gt; 75)
                  </label>
                  <label className="flex items-center gap-2 text-sm text-slate-300">
                    <input type="checkbox" defaultChecked className="rounded bg-slate-800 border-slate-600 text-amber-500 focus:ring-amber-500" />
                    High (CSI 50-75)
                  </label>
                  <label className="flex items-center gap-2 text-sm text-slate-300">
                    <input type="checkbox" defaultChecked className="rounded bg-slate-800 border-slate-600 text-blue-500 focus:ring-blue-500" />
                    Medium (CSI 25-50)
                  </label>
                </div>
              </div>
            </div>
          </GlassCard>

          <GlassCard>
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <Clock className="w-4 h-4 text-emerald-400" /> Live Status
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-2 border-b border-slate-700/50">
                <span className="text-sm text-slate-400">Total Hotspots</span>
                <span className="text-sm font-bold text-white">{hotspots.length}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b border-slate-700/50">
                <span className="text-sm text-slate-400">Traffic Condition</span>
                <span className="text-sm font-bold text-rose-400">Heavy</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b border-slate-700/50">
                <span className="text-sm text-slate-400">Data Stream</span>
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span className="text-xs font-bold text-emerald-400">Connected</span>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Map Area */}
        <div className="lg:col-span-3 h-[600px] lg:h-full relative">
          <MapComponent hotspots={hotspots} viewMode={viewMode} />
        </div>
      </div>
    </div>
  );
}
