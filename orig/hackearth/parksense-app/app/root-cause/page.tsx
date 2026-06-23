"use client";

import { useEffect, useState } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Share2, Search, Brain, CheckCircle } from "lucide-react";
import { KPICard } from "@/components/dashboard/KPICard";

export default function RootCauseDashboard() {
  const [dnaData, setDnaData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/rei/generate-dna', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        setDnaData(data || []);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-full text-white">Decoding Hotspot DNA...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Root Cause & Enforcement Intelligence (REI™)</h1>
          <p className="text-slate-400">Deterministic behavioral DNA and prescriptive enforcement strategies.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard title="DNA Signatures" value={dnaData.length} icon={Share2} color="emerald" />
        <KPICard title="High Predictability" value={dnaData.filter(d => d.predictability === 'High').length} icon={Search} color="blue" />
        <KPICard title="Structural Fixes" value={dnaData.length} icon={Brain} color="violet" />
        <KPICard title="Enforcement Matches" value={dnaData.length} icon={CheckCircle} color="amber" />
      </div>

      <div className="grid grid-cols-1 gap-6">
        <GlassCard>
          <h3 className="text-lg font-semibold text-white mb-4">Hotspot Behavioral DNA Registry</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-slate-800/80 text-slate-400">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Hotspot ID</th>
                  <th className="px-4 py-3">DNA Signature</th>
                  <th className="px-4 py-3">Primary Root Cause</th>
                  <th className="px-4 py-3">Predictability</th>
                  <th className="px-4 py-3">Immediate Enforcement</th>
                  <th className="px-4 py-3 rounded-tr-lg">Long-Term Infrastructure</th>
                </tr>
              </thead>
              <tbody>
                {dnaData.map((dna, i) => (
                  <tr key={i} className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                    <td className="px-4 py-3 font-medium text-blue-400">#{dna.hotspot_id}</td>
                    <td className="px-4 py-3 font-mono text-xs text-emerald-400">{dna.dna_signature}</td>
                    <td className="px-4 py-3 text-slate-200">{dna.primary_cause}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs ${dna.predictability === 'High' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                        {dna.predictability}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-rose-400">{dna.recommended_immediate_action}</td>
                    <td className="px-4 py-3 text-blue-300">{dna.recommended_infrastructure_fix}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
