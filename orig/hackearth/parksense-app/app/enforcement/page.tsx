"use client";

import { useState, useEffect } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { AlertCircle, ArrowRight, ShieldCheck, Route, FileCheck, Navigation } from "lucide-react";

export default function EnforcementPage() {
  const [priorities, setPriorities] = useState<any[]>([]);

  useEffect(() => {
    fetch('/data/enforcement.json')
      .then(res => res.json())
      .then(data => setPriorities(data));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Smart Enforcement Engine</h1>
          <p className="text-slate-400">AI-prioritized action zones and automated patrol routing.</p>
        </div>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg flex items-center gap-2 font-medium transition-colors">
          <Route className="w-4 h-4" />
          Dispatch Patrol
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GlassCard className="lg:col-span-2">
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-rose-400" />
            Top 10 Critical Action Zones
          </h3>
          
          <div className="space-y-4">
            {priorities.slice(0, 10).map((p, i) => (
              <div key={i} className="flex flex-col sm:flex-row gap-4 items-center p-4 bg-slate-800/50 border border-slate-700 rounded-xl hover:bg-slate-800 transition-colors">
                <div className="flex items-center justify-center w-12 h-12 rounded-full bg-slate-900 border border-slate-700 flex-shrink-0 text-xl font-black text-slate-300">
                  #{p.rank}
                </div>
                
                <div className="flex-1 w-full">
                  <h4 className="text-lg font-bold text-white mb-1">{p.location_name}</h4>
                  <div className="flex flex-wrap gap-2 mb-2">
                    <span className="px-2 py-0.5 text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded">Priority: {p.priority_score.toFixed(1)}</span>
                    <span className="px-2 py-0.5 text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30 rounded">ETA: {p.eta_mins} mins</span>
                  </div>
                  <div className="w-full bg-slate-900 rounded-full h-1.5">
                    <div className="bg-gradient-to-r from-amber-500 to-rose-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, p.priority_score)}%` }}></div>
                  </div>
                </div>
                
                <div className="flex-shrink-0 w-full sm:w-auto mt-2 sm:mt-0">
                  <button className="w-full sm:w-auto px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg flex items-center justify-center gap-2 text-sm font-medium transition-colors border border-slate-600">
                    <Navigation className="w-4 h-4" />
                    {p.action}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <div className="space-y-6">
          <GlassCard glowColor="emerald">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" /> System Status
            </h3>
            <ul className="space-y-4">
              <li className="flex justify-between items-center pb-3 border-b border-slate-700">
                <span className="text-slate-400 text-sm">Active Patrols</span>
                <span className="font-bold text-white">12 Teams</span>
              </li>
              <li className="flex justify-between items-center pb-3 border-b border-slate-700">
                <span className="text-slate-400 text-sm">Auto-Challans Issued</span>
                <span className="font-bold text-white">1,402 Today</span>
              </li>
              <li className="flex justify-between items-center pb-3 border-b border-slate-700">
                <span className="text-slate-400 text-sm">Avg Response Time</span>
                <span className="font-bold text-emerald-400">14.2 mins</span>
              </li>
            </ul>
          </GlassCard>

          <GlassCard glowColor="violet">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-violet-400" /> Automated Workflow
            </h3>
            <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-slate-900 bg-blue-500 text-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_10px_rgba(59,130,246,0.5)] z-10">
                  1
                </div>
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-3 rounded bg-slate-800/50 border border-slate-700">
                  <h4 className="font-bold text-white text-sm">AI Detection</h4>
                  <p className="text-xs text-slate-400 mt-1">Hotspot identified</p>
                </div>
              </div>
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-slate-900 bg-amber-500 text-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_10px_rgba(245,158,11,0.5)] z-10">
                  2
                </div>
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-3 rounded bg-slate-800/50 border border-slate-700">
                  <h4 className="font-bold text-white text-sm">CSI Calculation</h4>
                  <p className="text-xs text-slate-400 mt-1">Severity analyzed</p>
                </div>
              </div>
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-slate-900 bg-emerald-500 text-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_10px_rgba(16,185,129,0.5)] z-10">
                  3
                </div>
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-3 rounded bg-slate-800/50 border border-slate-700">
                  <h4 className="font-bold text-white text-sm">Patrol Dispatch</h4>
                  <p className="text-xs text-slate-400 mt-1">Officers deployed</p>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
