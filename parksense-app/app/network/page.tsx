"use client";

import { useEffect, useState } from "react";
import { Network, Activity, AlertTriangle, Route } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

export default function NetworkIntelligenceDashboard() {
  const [networkData, setNetworkData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/utgi/vulnerability-map`)
      .then(res => res.json())
      .then(data => {
        setNetworkData(Array.isArray(data) ? data : (data?.results ? data.results : []));
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setNetworkData([]);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="py-24 text-center text-slate-500 font-medium">Loading Network Intelligence...</div>;

  const avgRisk = networkData.length ? networkData.reduce((acc, n) => acc + (n.network_fragility_score || 0), 0) / networkData.length : 0;
  const criticalNodes = networkData.filter(n => (n.network_fragility_score || 0) > 75).length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Network Intelligence</h1>
          <p className="text-slate-500 text-sm mt-1">Graph neural network vulnerability mapping and ripple effect analysis.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <div className="saas-card p-5 hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center gap-2 mb-3">
            <div className="p-2 bg-blue-50 rounded-lg">
              <Network className="w-4 h-4 text-blue-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Nodes Analyzed</h3>
          </div>
          <div className="text-3xl font-bold text-slate-900">{networkData.length}</div>
        </div>
        
        <div className="saas-card p-5 hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center gap-2 mb-3">
            <div className="p-2 bg-amber-50 rounded-lg">
              <Activity className="w-4 h-4 text-amber-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Network Risk</h3>
          </div>
          <div className="flex items-baseline gap-1">
            <div className="text-3xl font-bold text-slate-900">{Number(avgRisk || 0).toFixed(1)}</div>
            <div className="text-sm font-medium text-slate-400">/ 100</div>
          </div>
        </div>
        
        <div className="saas-card p-5 hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center gap-2 mb-3">
            <div className="p-2 bg-rose-50 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-rose-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Critical Vulnerabilities</h3>
          </div>
          <div className="text-3xl font-bold text-slate-900">{criticalNodes}</div>
        </div>
        
        <div className="saas-card p-5 border-l-4 border-l-blue-600 hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center gap-2 mb-3">
            <div className="p-2 bg-blue-50 rounded-lg">
              <Route className="w-4 h-4 text-blue-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Highest Ripple Impact</h3>
          </div>
          <div className="text-xl font-bold text-slate-900">
            Node #{[...networkData].sort((a,b) => (b.network_fragility_score || 0) - (a.network_fragility_score || 0))[0]?.hotspot_id || "..."}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {/* Left Col - List */}
        <div className="saas-card overflow-hidden flex flex-col h-[500px]">
          <div className="bg-slate-50/50 border-b border-slate-200 px-6 py-4 flex items-center gap-2">
            <Network className="w-4 h-4 text-slate-400" />
            <h3 className="font-bold text-slate-900 text-lg">Critical Vulnerability List</h3>
          </div>
          <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
            {[...networkData].sort((a,b) => (b.network_fragility_score || 0) - (a.network_fragility_score || 0)).slice(0, 10).map((node, i) => (
              <div key={i} className="p-4 flex justify-between items-center hover:bg-slate-50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500 border border-slate-200">
                    {i + 1}
                  </div>
                  <div>
                    <div className="text-sm font-bold text-slate-900">Hotspot #{node.hotspot_id}</div>
                    <div className="text-xs font-medium text-slate-500 mt-0.5">{node.risk_level} Risk Level</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-lg font-bold ${node.network_fragility_score > 75 ? 'text-rose-600' : 'text-amber-600'}`}>
                    {Number(node.network_fragility_score || 0).toFixed(1)}
                  </div>
                  <div className="text-[10px] uppercase tracking-wider font-semibold text-slate-400">Fragility Score</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Col - Progress Bars */}
        <div className="saas-card overflow-hidden flex flex-col h-[500px]">
          <div className="bg-slate-50/50 border-b border-slate-200 px-6 py-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-slate-400" />
            <h3 className="font-bold text-slate-900 text-lg">Congestion Propagation Risk</h3>
          </div>
          <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-white">
            {[...networkData].sort((a,b) => (b.network_fragility_score || 0) - (a.network_fragility_score || 0)).slice(0, 7).map((node, i) => (
              <div key={i} className="group">
                <div className="flex justify-between items-end mb-2">
                  <div>
                    <span className="text-sm font-bold text-slate-700 group-hover:text-blue-600 transition-colors">Node #{node.hotspot_id}</span>
                  </div>
                  <span className={`text-sm font-bold ${node.network_fragility_score > 75 ? 'text-rose-600' : 'text-slate-900'}`}>
                    {Number(node.network_fragility_score || 0).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden shadow-inner relative">
                  <div 
                    className={`h-full rounded-full transition-all duration-1000 ${node.network_fragility_score > 75 ? 'bg-gradient-to-r from-rose-500 to-rose-400' : node.network_fragility_score > 50 ? 'bg-gradient-to-r from-amber-500 to-amber-400' : 'bg-gradient-to-r from-blue-500 to-blue-400'}`} 
                    style={{ width: `${node.network_fragility_score}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
