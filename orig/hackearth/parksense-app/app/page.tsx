"use client";

import { useEffect, useState } from "react";
import { KPICard } from "@/components/dashboard/KPICard";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { AlertTriangle, Car, Clock, MapPin, TrendingUp, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, AreaChart, Area, Cell
} from "recharts";

export default function ExecutiveDashboard() {
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [networkData, setNetworkData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('/data/hotspots.json').then(res => res.json()),
      fetch('http://127.0.0.1:8000/api/utgi/vulnerability-map').then(res => res.json()).catch(() => [])
    ])
    .then(([hotspotData, netData]) => {
      setHotspots(hotspotData);
      setNetworkData(netData || []);
      setLoading(false);
    })
    .catch(err => {
      console.error("Error loading data:", err);
      setLoading(false);
    });
  }, []);

  const totalViolations = hotspots.reduce((acc, h) => acc + h.count, 0);
  const criticalZones = hotspots.filter(h => h.severity === 'Critical').length;
  const avgDelay = hotspots.length ? (hotspots.reduce((acc, h) => acc + h.delay_minutes, 0) / hotspots.length).toFixed(1) : 0;
  
  // Mock trend data for charts
  const trendData = [
    { time: '08:00', violations: 120 },
    { time: '10:00', violations: 250 },
    { time: '12:00', violations: 180 },
    { time: '14:00', violations: 190 },
    { time: '16:00', violations: 300 },
    { time: '18:00', violations: 450 },
    { time: '20:00', violations: 280 },
  ];

  const csiDistribution = [
    { name: 'Critical', value: hotspots.filter(h => h.csi > 75).length, fill: '#ef4444' },
    { name: 'High', value: hotspots.filter(h => h.csi > 50 && h.csi <= 75).length, fill: '#f59e0b' },
    { name: 'Medium', value: hotspots.filter(h => h.csi > 25 && h.csi <= 50).length, fill: '#3b82f6' },
    { name: 'Low', value: hotspots.filter(h => h.csi <= 25).length, fill: '#10b981' },
  ];

  if (loading) return <div className="flex items-center justify-center h-full text-white">Loading Intelligence Core...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Executive Overview</h1>
          <p className="text-slate-400">Real-time parking congestion intelligence for Bangalore City.</p>
        </div>
        <div className="flex gap-2">
          <div className="px-3 py-1.5 rounded-md bg-slate-800 border border-slate-700 text-sm text-slate-300 font-medium">
            Last Updated: Just now
          </div>
          <div className="px-3 py-1.5 rounded-md bg-blue-600/20 border border-blue-500/30 text-sm text-blue-400 font-medium">
            City: Bangalore
          </div>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-8 gap-4">
        <KPICard title="Violations" value={totalViolations.toLocaleString()} icon={Car} color="blue" trend={{value: 12, isPositive: false}} />
        <KPICard title="Critical Hotspots" value={criticalZones} icon={AlertTriangle} color="rose" />
        <KPICard title="Avg Delay" value={`+${avgDelay}m`} icon={Clock} color="amber" />
        <KPICard title="Active Clusters" value={hotspots.length} icon={MapPin} color="violet" />
        <KPICard title="Enforcement Score" value="78/100" icon={ShieldCheck} color="blue" />
        <KPICard title="Avg Network CSI™" value={networkData.length ? (networkData.reduce((acc,n) => acc + (n.network_csi_score||n.fragility_score||0), 0) / networkData.length).toFixed(1) : "0"} icon={TrendingUp} color="rose" />
        <KPICard title="Critical Corridors" value={networkData.filter(n => (n.fragility_score||0) > 75).length > 0 ? 1 : 0} icon={MapPin} color="amber" />
        <KPICard title="Highest Ripple" value={networkData.length ? `${Math.max(...networkData.map(n => n.ripple_effect_multiplier || n.fragility_score/50 || 1)).toFixed(1)}x` : "0x"} icon={AlertTriangle} color="rose" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Chart */}
        <GlassCard className="lg:col-span-2 flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-4">24-Hour Violation Intensity Trend</h3>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorVio" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }}
                  itemStyle={{ color: '#60a5fa' }}
                />
                <Area type="monotone" dataKey="violations" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorVio)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        {/* Top Critical Zones */}
        <GlassCard className="flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center justify-between">
            Top Priority Zones
            <span className="text-xs px-2 py-1 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30">Action Req</span>
          </h3>
          <div className="flex-1 overflow-y-auto pr-2 space-y-3">
            {hotspots.slice(0, 5).map((h, i) => (
              <div key={i} className="p-3 rounded-lg bg-slate-800/50 border border-slate-700 hover:bg-slate-800 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium text-slate-200 text-sm truncate max-w-[150px]" title={h.location_name}>
                    {h.location_name}
                  </h4>
                  <span className="text-xs font-bold text-rose-400">CSI: {h.csi.toFixed(1)}</span>
                </div>
                <div className="flex justify-between text-xs text-slate-400">
                  <span>{h.count} violations</span>
                  <span className="text-amber-400">+{h.delay_minutes.toFixed(1)}m delay</span>
                </div>
                <div className="mt-2 w-full bg-slate-700 rounded-full h-1.5">
                  <div className="bg-rose-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, h.csi)}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Secondary Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard>
          <h3 className="text-lg font-semibold text-white mb-4">Congestion Severity Index (CSI) Distribution</h3>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={csiDistribution} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" fontSize={12} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={12} width={80} />
                <Tooltip cursor={{fill: '#334155', opacity: 0.4}} contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {csiDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        
        <GlassCard>
          <h3 className="text-lg font-semibold text-white mb-4">Effective Road Width Loss (%)</h3>
          <div className="space-y-4">
            {hotspots.slice(0, 4).map((h, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">{h.location_name}</span>
                  <span className="text-amber-400 font-medium">{h.width_loss_percent.toFixed(1)}% Blocked</span>
                </div>
                <div className="w-full h-3 bg-slate-700 rounded-full overflow-hidden flex">
                  <div className="bg-amber-500 h-full" style={{ width: `${h.width_loss_percent}%` }}></div>
                  <div className="bg-slate-600 h-full flex-1"></div>
                </div>
                <div className="flex justify-between text-xs text-slate-500 mt-1">
                  <span>Occupied by Illegal Parking</span>
                  <span>Effective Usable Width</span>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
