"use client";

import { useState, useEffect } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Brain, FileCode, CheckCircle2, AlertCircle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from "recharts";

export default function ExplainabilityPage() {
  const [shapData, setShapData] = useState<any>(null);

  useEffect(() => {
    fetch('/data/shap_values.json')
      .then(res => res.json())
      .then(data => setShapData(data));
  }, []);

  if (!shapData) return null;

  // Grab the first local explanation for demo purposes
  const firstZoneId = Object.keys(shapData.local_explanations)[0];
  const localExp = shapData.local_explanations[firstZoneId];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Explainable AI (XAI)</h1>
          <p className="text-slate-400">SHAP-powered transparency into why the AI flags a zone as critical.</p>
        </div>
        <div className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-lg flex items-center gap-2 font-medium">
          <CheckCircle2 className="w-5 h-5" />
          Model Audited
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard glowColor="blue">
          <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
            <Brain className="w-5 h-5 text-blue-400" /> Global Feature Importance
          </h3>
          <p className="text-sm text-slate-400 mb-6">What features drive congestion across the entire city?</p>
          
          <div className="h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={shapData.global_importance} layout="vertical" margin={{ left: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" fontSize={12} />
                <YAxis dataKey="feature" type="category" stroke="#e2e8f0" fontSize={12} width={120} />
                <Tooltip 
                  cursor={{fill: '#334155', opacity: 0.4}} 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }}
                  formatter={(value: any) => [Number(value).toFixed(3), 'Mean |SHAP|']}
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {shapData.global_importance.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill="#3b82f6" />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard glowColor="rose">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <FileCode className="w-5 h-5 text-rose-400" /> Local Explanation (SHAP Waterfall)
            </h3>
            <span className="px-2 py-1 text-xs font-bold bg-slate-800 rounded border border-slate-700 text-slate-300">Zone ID: {firstZoneId}</span>
          </div>
          <p className="text-sm text-slate-400 mb-6">Why is this specific hotspot flagged as high risk?</p>
          
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={localExp} layout="vertical" margin={{ left: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" fontSize={12} />
                <YAxis dataKey="feature" type="category" stroke="#e2e8f0" fontSize={12} width={120} />
                <ReferenceLine x={0} stroke="#cbd5e1" />
                <Tooltip 
                  cursor={{fill: '#334155', opacity: 0.4}} 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }}
                  formatter={(value: any) => [Number(value).toFixed(3), 'Impact on Prediction']}
                />
                <Bar dataKey="shap_value">
                  {localExp.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.shap_value > 0 ? '#ef4444' : '#10b981'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="mt-4 p-4 rounded-lg bg-slate-800/80 border border-slate-700">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-white text-sm">Natural Language Explanation</h4>
                <p className="text-sm text-slate-300 mt-1">
                  This zone is flagged primarily due to <span className="font-bold text-rose-400">high Violation Density</span> which significantly increases the risk score. The <span className="font-bold text-rose-400">Time of Day</span> also contributes positively to the risk, while <span className="font-bold text-emerald-400">Road Narrowing</span> slightly reduces the severity impact for this specific location.
                </p>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
