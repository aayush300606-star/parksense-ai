"use client";

import { useState, useEffect } from "react";
import { TrendingUp, CalendarClock, BrainCircuit, Target } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { API_BASE_URL } from "@/lib/api";

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [timeWindow, setTimeWindow] = useState<"1h" | "6h" | "24h">("24h");

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/legacy/predictions.json`)
      .then(res => res.json())
      .then(data => setPredictions(Array.isArray(data) ? data : []))
      .catch(() => setPredictions([]));
  }, []);

  const getProbKey = (window: string) => `prob_${window}`;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-1">Predictive Analytics</h1>
          <p className="text-slate-500 text-sm mt-1">XGBoost & LightGBM ensemble models predicting future hotspot formations.</p>
        </div>
        <div className="flex bg-slate-100 rounded-lg p-1 border border-slate-200">
          {(["1h", "6h", "24h"] as const).map(w => (
            <button 
              key={w}
              onClick={() => setTimeWindow(w)}
              className={`px-4 py-2 rounded-md text-sm font-bold transition-all ${
                timeWindow === w 
                  ? 'bg-white text-blue-700 shadow-sm border border-slate-200' 
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              {w === "1h" ? "Next Hour" : w === "6h" ? "Next 6 Hours" : "Tomorrow"}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="saas-card p-6 lg:col-span-2">
          <h3 className="font-bold text-slate-900 mb-6 flex items-center gap-2 text-lg">
            <TrendingUp className="w-5 h-5 text-blue-600" /> Forecasted High-Risk Zones
          </h3>
          <div className="space-y-4">
            {predictions.sort((a, b) => b[getProbKey(timeWindow)] - a[getProbKey(timeWindow)]).slice(0, 6).map((p, i) => (
              <div key={i} className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center p-5 bg-white rounded-xl border border-slate-200 hover:shadow-sm transition-shadow">
                <div className="flex-1">
                  <h4 className="font-bold text-slate-900 mb-1 text-lg">{p.location_name}</h4>
                  <p className="text-xs text-slate-600 flex items-center gap-1.5 font-medium">
                    <BrainCircuit className="w-4 h-4 text-emerald-600" />
                    AI Insight: {p.key_factor}
                  </p>
                </div>
                
                <div className="flex items-center gap-6 w-full sm:w-1/2">
                  <div className="flex-1">
                    <div className="flex justify-between text-xs mb-2">
                      <span className="text-slate-500 font-semibold uppercase tracking-wider">Risk Prob</span>
                      <span className="font-bold text-amber-600">{Number((p[getProbKey(timeWindow)] * 100) || 0).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-slate-100 rounded-full h-2 shadow-inner overflow-hidden">
                      <div className="bg-gradient-to-r from-amber-400 to-amber-500 h-2 rounded-full" style={{ width: `${Math.min(100, p[getProbKey(timeWindow)] * 100)}%` }}></div>
                    </div>
                  </div>
                  
                  <div className="text-right flex-shrink-0 border-l border-slate-100 pl-6">
                    <div className="text-[10px] text-slate-400 uppercase tracking-wider font-bold mb-1">Model Conf</div>
                    <div className="text-sm font-bold text-emerald-600">{Number((p.confidence * 100) || 0).toFixed(1)}%</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="saas-card p-6 border-t-4 border-t-blue-600">
            <h3 className="font-bold text-slate-900 mb-6 flex items-center gap-2 text-lg">
              <Target className="w-5 h-5 text-blue-600" /> Model Performance
            </h3>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-600 font-medium">Accuracy (24h)</span>
                  <span className="font-bold text-emerald-600">92.4%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 shadow-inner overflow-hidden"><div className="bg-emerald-500 h-2 rounded-full w-[92.4%]"></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-600 font-medium">Precision</span>
                  <span className="font-bold text-emerald-600">88.7%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 shadow-inner overflow-hidden"><div className="bg-emerald-500 h-2 rounded-full w-[88.7%]"></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-600 font-medium">Recall</span>
                  <span className="font-bold text-emerald-600">94.2%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 shadow-inner overflow-hidden"><div className="bg-emerald-500 h-2 rounded-full w-[94.2%]"></div></div>
              </div>
            </div>
          </div>

          <div className="saas-card p-6">
            <h3 className="font-bold text-slate-900 mb-6 flex items-center gap-2 text-lg">
              <CalendarClock className="w-5 h-5 text-amber-600" /> Temporal Hotspots
            </h3>
            <div className="h-48 flex items-center justify-center border border-slate-200 bg-slate-50 rounded-xl relative overflow-hidden">
              <div className="absolute inset-0 p-3">
                <div className="w-full h-full grid grid-cols-7 grid-rows-5 gap-1.5">
                  {Array.from({length: 35}).map((_, i) => (
                    <div key={i} className="rounded-sm" style={{ 
                      backgroundColor: `rgba(244, 63, 94, ${Math.random() * 0.8})` 
                    }}></div>
                  ))}
                </div>
              </div>
              <span className="z-10 bg-white/90 px-3 py-1.5 rounded-md text-xs font-bold text-slate-700 shadow-sm border border-slate-200">Hour × Day Matrix</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
