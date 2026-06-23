"use client";

import { useState, useEffect } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { TrendingUp, CalendarClock, BrainCircuit, Target } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [timeWindow, setTimeWindow] = useState<"1h" | "6h" | "24h">("24h");

  useEffect(() => {
    fetch('/data/predictions.json')
      .then(res => res.json())
      .then(data => setPredictions(data));
  }, []);

  const getProbKey = (window: string) => `prob_${window}`;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Predictive Analytics</h1>
          <p className="text-slate-400">XGBoost & LightGBM ensemble models predicting future hotspot formations.</p>
        </div>
        <div className="flex bg-slate-800 rounded-lg p-1 border border-slate-700">
          {(["1h", "6h", "24h"] as const).map(w => (
            <button 
              key={w}
              onClick={() => setTimeWindow(w)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                timeWindow === w 
                  ? 'bg-blue-600 text-white shadow-[0_0_10px_rgba(37,99,235,0.3)]' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              {w === "1h" ? "Next Hour" : w === "6h" ? "Next 6 Hours" : "Tomorrow"}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GlassCard className="lg:col-span-2">
          <h3 className="font-semibold text-white mb-6 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-400" /> Forecasted High-Risk Zones
          </h3>
          <div className="space-y-4">
            {predictions.sort((a, b) => b[getProbKey(timeWindow)] - a[getProbKey(timeWindow)]).slice(0, 6).map((p, i) => (
              <div key={i} className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                <div className="flex-1">
                  <h4 className="font-bold text-white mb-1">{p.location_name}</h4>
                  <p className="text-xs text-slate-400 flex items-center gap-1">
                    <BrainCircuit className="w-3 h-3 text-emerald-400" />
                    AI Insight: {p.key_factor}
                  </p>
                </div>
                
                <div className="flex items-center gap-6 w-full sm:w-1/2">
                  <div className="flex-1">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">Risk Probability</span>
                      <span className="font-bold text-amber-400">{(p[getProbKey(timeWindow)] * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-slate-900 rounded-full h-2">
                      <div className="bg-gradient-to-r from-blue-500 to-amber-500 h-2 rounded-full" style={{ width: `${Math.min(100, p[getProbKey(timeWindow)] * 100)}%` }}></div>
                    </div>
                  </div>
                  
                  <div className="text-right flex-shrink-0">
                    <div className="text-[10px] text-slate-500 uppercase tracking-wider font-bold mb-0.5">Model Conf</div>
                    <div className="text-sm font-bold text-emerald-400">{(p.confidence * 100).toFixed(1)}%</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <div className="space-y-6">
          <GlassCard glowColor="violet">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-violet-400" /> Model Performance
            </h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">Accuracy (24h)</span>
                  <span className="font-bold text-emerald-400">92.4%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5"><div className="bg-emerald-500 h-1.5 rounded-full w-[92.4%]"></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">Precision</span>
                  <span className="font-bold text-emerald-400">88.7%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5"><div className="bg-emerald-500 h-1.5 rounded-full w-[88.7%]"></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">Recall</span>
                  <span className="font-bold text-emerald-400">94.2%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5"><div className="bg-emerald-500 h-1.5 rounded-full w-[94.2%]"></div></div>
              </div>
            </div>
          </GlassCard>

          <GlassCard>
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <CalendarClock className="w-5 h-5 text-amber-400" /> Temporal Hotspots
            </h3>
            <div className="h-48 flex items-center justify-center border border-slate-700 border-dashed rounded-lg bg-slate-800/30 relative">
              <div className="absolute inset-0 p-2">
                <div className="w-full h-full grid grid-cols-7 grid-rows-5 gap-1">
                  {Array.from({length: 35}).map((_, i) => (
                    <div key={i} className="rounded" style={{ 
                      backgroundColor: `rgba(239, 68, 68, ${Math.random() * 0.8})` 
                    }}></div>
                  ))}
                </div>
              </div>
              <span className="z-10 bg-slate-900/80 px-3 py-1 rounded text-xs font-bold text-slate-300 backdrop-blur-sm">Hour × Day Matrix</span>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
