"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, Car, Clock, MapPin, TrendingUp, ShieldCheck } from "lucide-react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area, Cell
} from "recharts";
import dynamic from 'next/dynamic';

const CityMap = dynamic(() => import('@/components/maps/CityMap'), { ssr: false });
import { API_BASE_URL } from '@/lib/api';

export default function ExecutiveDashboard() {
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/legacy/hotspots.json`)
      .then(res => res.json())
      .then(data => {
        setHotspots(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading data:", err);
        setLoading(false);
      });
  }, []);

  const totalViolations = hotspots.reduce((acc, h) => acc + h.count, 0);
  const criticalZones = hotspots.filter(h => h.severity === 'Critical').length;
  const avgDelay = hotspots?.length ? Number(hotspots.reduce((acc, h) => acc + (h.delay_minutes || 0), 0) / hotspots.length).toFixed(1) : 0;
  
  // Mock trend data for charts
  const trendData = [
    { time: '08:00', violations: 120 },
    { time: '10:00', violations: 250 },
    { time: '12:00', violations: 180 },
    { time: '14:00', violations: 190 },
    { time: '16:00', violations: 300 },
    { time: '18:00', violations: 410 },
    { time: '20:00', violations: 280 }
  ];

  const csiDistribution = [
    { name: 'Critical', value: criticalZones, fill: '#e11d48' },
    { name: 'High', value: hotspots.filter(h => h.severity === 'High').length, fill: '#ea580c' },
    { name: 'Medium', value: hotspots.filter(h => h.severity === 'Medium').length, fill: '#d97706' },
    { name: 'Low', value: hotspots.filter(h => h.severity === 'Low').length, fill: '#2563eb' }
  ];

  if (loading) return <div className="py-24 text-center text-slate-500 font-medium">Loading Intelligence...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Executive Dashboard</h1>
          <p className="text-slate-500 text-sm mt-1">Real-time congestion intelligence and hotspot tracking.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Avg CSI</div>
            <div className="text-3xl font-bold text-slate-900">72.4</div>
          </div>
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-blue-600" />
          </div>
        </div>
        
        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Total Violations</div>
            <div className="text-3xl font-bold text-slate-900">{totalViolations}</div>
          </div>
          <div className="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center">
            <Car className="w-6 h-6 text-amber-600" />
          </div>
        </div>

        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Critical Zones</div>
            <div className="text-3xl font-bold text-rose-600">{criticalZones}</div>
          </div>
          <div className="w-12 h-12 bg-rose-50 rounded-xl flex items-center justify-center">
            <AlertTriangle className="w-6 h-6 text-rose-600" />
          </div>
        </div>

        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Avg Delay</div>
            <div className="text-3xl font-bold text-slate-900">{avgDelay}m</div>
          </div>
          <div className="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center">
            <Clock className="w-6 h-6 text-slate-600" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 saas-card overflow-hidden flex flex-col h-[500px]">
          <div className="bg-slate-50/50 border-b border-slate-200 px-6 py-4 flex items-center gap-2">
            <MapPin className="w-4 h-4 text-slate-400" />
            <h3 className="font-bold text-slate-900 text-lg">Live Congestion Map</h3>
          </div>
          <div className="flex-1 bg-slate-100 relative">
            <CityMap hotspots={hotspots} />
          </div>
        </div>

        <div className="space-y-6 flex flex-col">
          <div className="saas-card p-6 flex-1">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">Congestion Trend</h3>
            <div className="h-[150px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Area type="monotone" dataKey="violations" stroke="#2563eb" strokeWidth={3} fillOpacity={1} fill="url(#colorPv)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="saas-card p-6 flex-1">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">Severity Distribution</h3>
            <div className="h-[150px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={csiDistribution} layout="vertical" margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={12} width={60} tickLine={false} axisLine={false} />
                  <Tooltip cursor={{fill: '#f1f5f9'}} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20}>
                    {csiDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      <div className="saas-card p-6">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-6">Effective Road Width Loss (%)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
          {hotspots.slice(0, 6).map((h, i) => (
            <div key={i}>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-700 font-semibold">{h.location_name}</span>
                <span className={`${h.width_loss_percent > 60 ? 'text-rose-600' : 'text-amber-600'} font-bold`}>{Number(h?.width_loss_percent ?? 0).toFixed(1)}% Blocked</span>
              </div>
              <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden flex shadow-inner">
                <div className={`h-full ${h.width_loss_percent > 60 ? 'bg-gradient-to-r from-rose-500 to-rose-400' : 'bg-gradient-to-r from-amber-500 to-amber-400'}`} style={{ width: `${h.width_loss_percent}%` }}></div>
                <div className="bg-slate-200 h-full flex-1"></div>
              </div>
              <div className="flex justify-between text-[11px] font-semibold uppercase tracking-wider text-slate-400 mt-2">
                <span>Occupied by Illegal Parking</span>
                <span>Effective Usable Width</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
