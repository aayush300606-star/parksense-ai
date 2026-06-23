"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { Map, Filter, Layers, Clock } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

// Dynamic import for Leaflet (no SSR)
const MapComponent = dynamic(() => import("@/components/maps/MapComponent"), { 
  ssr: false,
  loading: () => <div className="w-full h-full flex items-center justify-center bg-slate-50 rounded-xl border border-slate-200 text-blue-600 font-medium">Loading Intelligence Map...</div>
});

export default function HeatmapPage() {
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [viewMode, setViewMode] = useState<"clusters" | "heatmap">("clusters");
  
  const [timeWindow, setTimeWindow] = useState("today");
  const [severity, setSeverity] = useState({
    critical: true,
    high: true,
    medium: true,
    low: false
  });
  
  useEffect(() => {
    const activeSeverities = [];
    if (severity.critical) activeSeverities.push("Critical");
    if (severity.high) activeSeverities.push("High");
    if (severity.medium) activeSeverities.push("Medium");
    if (severity.low) activeSeverities.push("Low");
    const sevString = activeSeverities.join(",");

    fetch(`${API_BASE_URL}/api/legacy/hotspots.json?timeWindow=${timeWindow}&severity=${sevString}`)
      .then(res => res.json())
      .then(data => setHotspots(Array.isArray(data) ? data : []))
      .catch(err => {
          console.error("Failed to fetch dynamically filtered hotspots:", err);
          setHotspots([]);
      });
  }, [timeWindow, severity]);

  const averageCsi = hotspots.length > 0 ? (hotspots.reduce((acc, h) => acc + (h.csi || 0), 0) / hotspots.length) : 0;
  const trafficCondition = averageCsi > 75 ? "Critical" : averageCsi > 50 ? "Heavy" : averageCsi > 25 ? "Moderate" : "Light";
  const trafficColor = averageCsi > 75 ? "text-rose-600" : averageCsi > 50 ? "text-amber-500" : averageCsi > 25 ? "text-blue-500" : "text-emerald-500";

  return (
    <div className="flex flex-col h-[calc(100vh-3rem)] space-y-6">
      <div className="flex justify-between items-end mb-2">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-1">Geospatial Intelligence</h1>
          <p className="text-slate-500 text-sm">Interactive heatmap of parking violations and congestion impact.</p>
        </div>
        
        <div className="flex gap-2">
          <button 
            onClick={() => setViewMode("clusters")}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-all ${viewMode === 'clusters' ? 'bg-blue-600 text-white shadow-sm' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'}`}
          >
            <Map className="w-4 h-4" />
            Cluster View
          </button>
          <button 
            onClick={() => setViewMode("heatmap")}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-all ${viewMode === 'heatmap' ? 'bg-blue-600 text-white shadow-sm' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'}`}
          >
            <Layers className="w-4 h-4" />
            Density Heatmap
          </button>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Filters */}
        <div className="lg:col-span-1 space-y-6">
          <div className="saas-card p-6">
            <h3 className="font-bold text-slate-900 mb-6 flex items-center gap-2 text-lg">
              <Filter className="w-5 h-5 text-blue-600" /> Filters
            </h3>
            
            <div className="space-y-6">
              <div>
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 block">Time Window</label>
                <div className="flex bg-slate-100 rounded-lg p-1 border border-slate-200">
                  <button onClick={() => setTimeWindow('today')} className={`flex-1 px-2 py-1.5 text-xs rounded-md transition-all ${timeWindow === 'today' ? 'font-bold bg-white text-blue-700 shadow-sm' : 'font-medium text-slate-500 hover:text-slate-900'}`}>Today</button>
                  <button onClick={() => setTimeWindow('week')} className={`flex-1 px-2 py-1.5 text-xs rounded-md transition-all ${timeWindow === 'week' ? 'font-bold bg-white text-blue-700 shadow-sm' : 'font-medium text-slate-500 hover:text-slate-900'}`}>Week</button>
                  <button onClick={() => setTimeWindow('month')} className={`flex-1 px-2 py-1.5 text-xs rounded-md transition-all ${timeWindow === 'month' ? 'font-bold bg-white text-blue-700 shadow-sm' : 'font-medium text-slate-500 hover:text-slate-900'}`}>Month</button>
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 block">Severity Level</label>
                <div className="space-y-3">
                  <label className="flex items-center gap-3 text-sm text-slate-700 font-medium cursor-pointer">
                    <input type="checkbox" checked={severity.critical} onChange={(e) => setSeverity({...severity, critical: e.target.checked})} className="rounded bg-white border-slate-300 text-rose-600 focus:ring-rose-500 w-4 h-4" />
                    Critical (CSI &gt; 75)
                  </label>
                  <label className="flex items-center gap-3 text-sm text-slate-700 font-medium cursor-pointer">
                    <input type="checkbox" checked={severity.high} onChange={(e) => setSeverity({...severity, high: e.target.checked})} className="rounded bg-white border-slate-300 text-amber-500 focus:ring-amber-500 w-4 h-4" />
                    High (CSI 50-75)
                  </label>
                  <label className="flex items-center gap-3 text-sm text-slate-700 font-medium cursor-pointer">
                    <input type="checkbox" checked={severity.medium} onChange={(e) => setSeverity({...severity, medium: e.target.checked})} className="rounded bg-white border-slate-300 text-blue-500 focus:ring-blue-500 w-4 h-4" />
                    Medium (CSI 25-50)
                  </label>
                  <label className="flex items-center gap-3 text-sm text-slate-700 font-medium cursor-pointer">
                    <input type="checkbox" checked={severity.low} onChange={(e) => setSeverity({...severity, low: e.target.checked})} className="rounded bg-white border-slate-300 text-emerald-500 focus:ring-emerald-500 w-4 h-4" />
                    Low (CSI &lt; 25)
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div className="saas-card p-6">
            <h3 className="font-bold text-slate-900 mb-6 flex items-center gap-2 text-lg">
              <Clock className="w-5 h-5 text-emerald-600" /> Live Status
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                <span className="text-sm font-medium text-slate-500">Filtered Hotspots</span>
                <span className="text-sm font-bold text-slate-900">{hotspots.length}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                <span className="text-sm font-medium text-slate-500">Average CSI</span>
                <span className={`text-sm font-bold ${trafficColor}`}>{Number(averageCsi || 0).toFixed(1)}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                <span className="text-sm font-medium text-slate-500">Network Condition</span>
                <span className={`text-sm font-bold ${trafficColor}`}>{trafficCondition}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-slate-500">Data Stream</span>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">Connected</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Map Area */}
        <div className="lg:col-span-3 h-[600px] lg:h-full relative saas-card overflow-hidden">
          <MapComponent hotspots={hotspots} viewMode={viewMode} />
        </div>
      </div>
    </div>
  );
}
