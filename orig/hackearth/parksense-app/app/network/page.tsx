"use client";

import { useEffect, useState } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Network, Activity, AlertTriangle, Route } from "lucide-react";
import { KPICard } from "@/components/dashboard/KPICard";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

export default function NetworkIntelligenceDashboard() {
  const [networkData, setNetworkData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In demo, we fetch the generated json
    fetch('http://127.0.0.1:8000/api/utgi/vulnerability-map')
      .then(res => res.json())
      .then(data => {
        setNetworkData(data || []);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-full text-white">Loading UTGI Core...</div>;

  const avgRisk = networkData.length ? networkData.reduce((acc, n) => acc + (n.network_fragility_score || 0), 0) / networkData.length : 0;
  const criticalNodes = networkData.filter(n => (n.network_fragility_score || 0) > 75).length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Urban Traffic Graph Intelligence (UTGI™)</h1>
          <p className="text-slate-400">GNN-powered network vulnerability and congestion propagation mapping.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard title="Graph Nodes Analyzed" value={networkData.length} icon={Network} color="blue" />
        <KPICard title="Avg Network Risk" value={avgRisk.toFixed(1)} icon={Activity} color="amber" />
        <KPICard title="Critical Vulnerabilities" value={criticalNodes} icon={AlertTriangle} color="rose" />
        <KPICard title="Fragile Corridors" value={Math.floor(criticalNodes / 3) || 1} icon={Route} color="violet" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard>
          <h3 className="text-lg font-semibold text-white mb-4">Top Vulnerable Junctions</h3>
          <div className="space-y-3">
            {[...networkData].sort((a,b) => (b.network_fragility_score || 0) - (a.network_fragility_score || 0)).slice(0, 8).map((node, i) => (
              <div key={i} className="p-3 rounded-lg bg-slate-800/50 border border-slate-700 flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium text-slate-200">Hotspot #{node.hotspot_id}</div>
                  <div className="text-xs text-slate-400">{node.risk_level} Risk Level</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-bold text-rose-400">{(node.network_fragility_score || 0).toFixed(1)}</div>
                  <div className="text-xs text-slate-500">Fragility Score</div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard>
          <h3 className="text-lg font-semibold text-white mb-4">Congestion Propagation (Ripple Effect)</h3>
          <div className="h-[400px]">
             <ResponsiveContainer width="100%" height="100%">
               <BarChart data={[...networkData].sort((a,b) => (b.network_fragility_score || 0) - (a.network_fragility_score || 0)).slice(0, 10)} layout="vertical">
                 <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                 <XAxis type="number" stroke="#94a3b8" fontSize={12} domain={[0, 100]} />
                 <YAxis dataKey="hotspot_id" type="category" stroke="#94a3b8" fontSize={12} width={50} />
                 <Tooltip cursor={{fill: '#334155', opacity: 0.4}} contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                 <Bar dataKey="network_fragility_score" radius={[0, 4, 4, 0]}>
                   {networkData.map((entry, index) => (
                     <Cell key={`cell-${index}`} fill={(entry.network_fragility_score || 0) > 75 ? '#ef4444' : (entry.network_fragility_score || 0) > 50 ? '#f59e0b' : '#3b82f6'} />
                   ))}
                 </Bar>
               </BarChart>
             </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
