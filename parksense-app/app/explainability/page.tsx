"use client";

import { useState, useEffect } from "react";
import { Brain, FileCode, CheckCircle2, AlertCircle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from "recharts";
import { API_BASE_URL } from "@/lib/api";

export default function ExplainabilityPage() {
  const [shapData, setShapData] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/predictions/shap`)
      .then(res => res.json())
      .then(data => setShapData(data));
  }, []);

  if (!shapData) return <div className="py-24 text-center text-slate-500 font-medium">Loading Explainability Models...</div>;

  // Grab the first local explanation for demo purposes
  const firstZoneId = Object.keys(shapData.local_explanations)[0];
  const localExp = shapData.local_explanations[firstZoneId];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-1">Explainable AI (XAI)</h1>
          <p className="text-slate-500 text-sm mt-1">SHAP-powered transparency into why the AI flags a zone as critical.</p>
        </div>
        <div className="px-4 py-2 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-lg flex items-center gap-2 font-bold text-sm shadow-sm">
          <CheckCircle2 className="w-4 h-4" />
          Model Audited
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="saas-card p-6">
          <h3 className="text-lg font-bold text-slate-900 mb-2 flex items-center gap-2">
            <Brain className="w-5 h-5 text-blue-600" /> Global Feature Importance
          </h3>
          <p className="text-sm text-slate-500 mb-6">What features drive congestion across the entire city?</p>
          
          <div className="h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={shapData.global_importance} layout="vertical" margin={{ left: 30 }}>
                <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="feature" type="category" stroke="#64748b" fontSize={12} width={120} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{fill: '#f1f5f9'}} 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
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
        </div>

        <div className="saas-card p-6 border-t-4 border-t-rose-600">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <FileCode className="w-5 h-5 text-rose-600" /> Local Explanation (SHAP Waterfall)
            </h3>
            <span className="px-3 py-1 text-xs font-bold bg-slate-100 rounded-md border border-slate-200 text-slate-700">Zone ID: {firstZoneId}</span>
          </div>
          <p className="text-sm text-slate-500 mb-6">Why is this specific hotspot flagged as high risk?</p>
          
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={localExp} layout="vertical" margin={{ left: 30 }}>
                <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="feature" type="category" stroke="#64748b" fontSize={12} width={120} tickLine={false} axisLine={false} />
                <ReferenceLine x={0} stroke="#cbd5e1" />
                <Tooltip 
                  cursor={{fill: '#f1f5f9'}} 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  formatter={(value: any) => [Number(value).toFixed(3), 'Impact on Prediction']}
                />
                <Bar dataKey="shap_value" radius={[0, 4, 4, 0]}>
                  {localExp.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.shap_value > 0 ? '#e11d48' : '#10b981'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="mt-6 p-4 rounded-xl bg-amber-50 border border-amber-100">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-amber-900 text-sm">Natural Language Explanation</h4>
                <p className="text-sm text-amber-800/80 mt-1.5 leading-relaxed">
                  This zone is flagged primarily due to <span className="font-bold text-amber-900">high Violation Density</span> which significantly increases the risk score. The <span className="font-bold text-amber-900">Time of Day</span> also contributes positively to the risk, while <span className="font-bold text-emerald-700">Road Narrowing</span> slightly reduces the severity impact for this specific location.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
