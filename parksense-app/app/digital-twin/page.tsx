"use client";

import { useEffect, useState } from "react";
import { Activity, ShieldCheck, ArrowRight, Table, BarChart3, Clock, MapPin, Settings2, Zap, Cpu, Target, ChevronRight, Play, RefreshCw } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

export default function DigitalTwinWorkspace() {
  const [simData, setSimData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [groupedData, setGroupedData] = useState<Record<string, any>>({});
  const [selectedHotspotId, setSelectedHotspotId] = useState<string | null>(null);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>("A");

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/digital-twin`)
      .then(res => res.json())
      .then(data => {
        const arr = Array.isArray(data) ? data : (data?.results ? data.results : []);
        setSimData(arr);
        
        // Group by hotspot_id
        const grouped: Record<string, any> = {};
        arr.forEach((sim: any) => {
          if (!grouped[sim.hotspot_id]) {
            grouped[sim.hotspot_id] = {
              hotspot_id: sim.hotspot_id,
              road_name: sim.road_name,
              scenarios: {},
              scenarioList: []
            };
          }
          grouped[sim.hotspot_id].scenarios[sim.scenario_id] = sim;
          grouped[sim.hotspot_id].scenarioList.push(sim);
        });
        
        setGroupedData(grouped);
        const keys = Object.keys(grouped);
        if (keys.length > 0) {
          setSelectedHotspotId(keys[0]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setSimData([]);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="py-24 text-center text-slate-500 font-medium">Running microscopic traffic simulation...</div>;

  const currentHotspot = selectedHotspotId ? groupedData[selectedHotspotId] : null;
  const currentSim = currentHotspot?.scenarios[selectedScenarioId];
  const baseline = currentSim?.baseline_state;
  const simulated = currentSim?.simulated_state;
  const deltas = currentSim?.deltas;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Digital Twin Simulation</h1>
          <p className="text-slate-500 text-sm mt-1">Compare current city state against simulated infrastructure changes.</p>
        </div>
        
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
          {/* Hotspot Dropdown */}
          <div className="relative w-full sm:w-64">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <MapPin className="w-4 h-4 text-slate-400" />
            </div>
            <select 
              value={selectedHotspotId || ""}
              onChange={(e) => setSelectedHotspotId(e.target.value)}
              className="w-full bg-white border border-slate-300 text-slate-700 text-sm rounded-lg pl-9 pr-8 py-2.5 focus:ring-blue-500 focus:border-blue-500 appearance-none shadow-sm cursor-pointer"
            >
              {Object.values(groupedData).map((h: any) => (
                <option key={h.hotspot_id} value={h.hotspot_id}>#{h.hotspot_id} - {h.road_name}</option>
              ))}
            </select>
          </div>

          {/* Scenario Dropdown */}
          <div className="relative w-full sm:w-56">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <Settings2 className="w-4 h-4 text-slate-400" />
            </div>
            <select 
              value={selectedScenarioId}
              onChange={(e) => setSelectedScenarioId(e.target.value)}
              className="w-full bg-blue-50 border border-blue-200 text-blue-700 text-sm font-medium rounded-lg pl-9 pr-8 py-2.5 focus:ring-blue-500 focus:border-blue-500 appearance-none shadow-sm cursor-pointer"
            >
              <option value="A">100% Parking Removal</option>
              <option value="B">75% Parking Removal</option>
              <option value="C">50% Parking Removal</option>
              <option value="D">25% Parking Removal</option>
            </select>
          </div>
        </div>
      </div>

      {/* Split Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative">
        
        {/* Before: Current State */}
        <div className="saas-card overflow-hidden flex flex-col h-full">
          <div className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center">
            <span className="font-semibold text-slate-900 text-lg">Current City State</span>
            <span className="text-xs font-semibold text-slate-700 bg-slate-100 px-3 py-1 rounded-md border border-slate-200 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span> Live Feed
            </span>
          </div>

          <div className="p-6 flex-1 flex flex-col">
            <div className="w-full h-[200px] bg-slate-50 rounded-xl border border-slate-200 flex flex-col items-center justify-center mb-6 shadow-inner relative overflow-hidden">
               <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#000 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
               <BarChart3 className="w-8 h-8 text-slate-400 mb-2" />
               <span className="text-slate-500 font-medium">Real-time Traffic Flow Model</span>
               <div className="mt-2 text-sm text-slate-400">Current Speed: {Number(baseline?.current_speed_kmh ?? 0).toFixed(1) || 0} km/h</div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-auto">
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <div className="text-sm font-medium text-slate-500 mb-1">Baseline CSI</div>
                <div className="text-3xl font-bold text-slate-900">{Number(baseline?.csi_score ?? 0).toFixed(1) || "..."}</div>
              </div>
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <div className="text-sm font-medium text-slate-500 mb-1">Baseline PIS</div>
                <div className="text-3xl font-bold text-slate-900">{Number(baseline?.pis_score ?? 0).toFixed(1) || "..."}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Center Arrow for larger screens */}
        <div className="hidden lg:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10 w-12 h-12 bg-white border border-slate-200 rounded-full items-center justify-center shadow-md">
          <ArrowRight className="w-5 h-5 text-slate-400" />
        </div>

        {/* After: Simulated State */}
        <div className="saas-card overflow-hidden flex flex-col h-full border-emerald-200 ring-1 ring-emerald-500/10 shadow-[0_4px_20px_-4px_rgba(16,185,129,0.1)]">
          <div className="bg-emerald-50/50 border-b border-emerald-100 px-6 py-4 flex justify-between items-center">
            <span className="font-semibold text-slate-900 text-lg">Simulated Outcome</span>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-100 px-3 py-1 rounded-md border border-emerald-200 flex items-center gap-2">
              <Clock className="w-3.5 h-3.5" /> Projected
            </span>
          </div>

          <div className="p-6 flex-1 flex flex-col">
            <div className="w-full h-[200px] bg-emerald-50/50 rounded-xl border border-emerald-100 flex flex-col items-center justify-center mb-6 relative overflow-hidden shadow-inner">
               <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#10b981 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
               <ShieldCheck className="w-8 h-8 text-emerald-500 mb-2" />
               <span className="text-emerald-700 font-medium">Optimised Flow Model</span>
               <div className="mt-2 text-sm text-emerald-600/70">Projected Speed: {Number(simulated?.current_speed_kmh ?? 0).toFixed(1) || 0} km/h (+{baseline?.current_speed_kmh ? Number(((deltas?.speed_kmh?.improvement / baseline.current_speed_kmh) * 100) || 0).toFixed(0) : 0}%)</div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-auto">
              <div className="bg-white p-5 rounded-xl border border-emerald-100 shadow-sm">
                <div className="text-sm font-medium text-slate-500 mb-1">Projected CSI</div>
                <div className="text-3xl font-bold text-slate-900">{Number(simulated?.csi_score ?? 0).toFixed(1) || "..."}</div>
              </div>
              <div className="bg-emerald-500 p-5 rounded-xl shadow-sm text-white">
                <div className="text-sm font-medium text-emerald-100 mb-1">CSI Reduction</div>
                <div className="text-3xl font-bold">-{Number(deltas?.csi?.improvement ?? 0).toFixed(1) || 0} pts</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <div className="saas-card overflow-hidden mt-8">
        <div className="bg-white border-b border-slate-200 px-6 py-5 flex items-center gap-3">
          <div className="p-2 bg-blue-50 rounded-lg text-blue-600">
            <Table className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900">Simulated ROI Outcomes ({currentHotspot?.road_name})</h3>
            <p className="text-xs text-slate-500 mt-0.5">Detailed breakdown of infrastructure interventions for this hotspot.</p>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Scenario</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Baseline CSI</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Projected CSI</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Speed Impr.</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Benefit Score</th>
                <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">ROI</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-100">
              {currentHotspot?.scenarioList?.map((sim: any, i: number) => (
                <tr key={i} className={`transition-colors ${sim.scenario_id === selectedScenarioId ? 'bg-blue-50' : 'hover:bg-slate-50'}`}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800">
                    {sim.scenario_name}
                    {sim.scenario_id === selectedScenarioId && <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800 uppercase tracking-wider">Active</span>}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{Number(sim.baseline_state?.csi_score ?? 0).toFixed(1)}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                      {Number(sim.simulated_state?.csi_score ?? 0).toFixed(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">+{sim.baseline_state.current_speed_kmh ? Number(((sim.deltas?.speed_kmh?.improvement / sim.baseline_state?.current_speed_kmh) * 100) || 0).toFixed(0) : 0}%</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{Number(sim.benefit_score ?? 0).toFixed(0)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{sim.roi}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
