"use client";

import { useEffect, useState } from "react";
import { ShieldAlert, Crosshair, Users, Target, CheckCircle2, ChevronRight, Activity } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

export default function EnforcementCommand() {
  const [plans, setPlans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedIntelligence, setExpandedIntelligence] = useState<number | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/enforcement-plan`)
      .then(res => res.json())
      .then(data => {
        setPlans(Array.isArray(data) ? data : (data?.results ? data.results : []));
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setPlans([]);
        setLoading(false);
      });
  }, []);

  const handleDispatch = async (hotspot_id: number) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/enforcement-plan/${hotspot_id}/dispatch`, { method: 'POST' });
      if (res.ok) {
        setPlans(plans.map(p => p.hotspot_id === hotspot_id ? { ...p, status: 'Dispatched' } : p));
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="py-24 text-center text-slate-500 font-medium">Loading Enforcement Strategies...</div>;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Smart Enforcement Plan</h1>
          <p className="text-slate-500 text-sm mt-1">Prioritized interventions based on highest ROI and congestion reduction.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-medium text-slate-500 mb-1">Total Recommended Actions</div>
            <div className="text-3xl font-bold text-slate-900">{plans.length}</div>
          </div>
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
            <ShieldAlert className="w-6 h-6 text-blue-600" />
          </div>
        </div>
        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-medium text-slate-500 mb-1">High ROI Targets</div>
            <div className="text-3xl font-bold text-slate-900">{plans.filter(p => p.roi_score > 60).length}</div>
          </div>
          <div className="w-12 h-12 bg-rose-50 rounded-xl flex items-center justify-center">
            <Crosshair className="w-6 h-6 text-rose-600" />
          </div>
        </div>
        <div className="saas-card p-5 flex items-center justify-between hover:-translate-y-0.5 transition-transform">
          <div>
            <div className="text-sm font-medium text-slate-500 mb-1">Teams Required</div>
            <div className="text-3xl font-bold text-slate-900">5</div>
          </div>
          <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center">
            <Users className="w-6 h-6 text-emerald-600" />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {plans.map((plan, i) => (
          <div key={i} className="saas-card p-6 hover:border-slate-300 transition-colors">
            <div className="flex flex-col xl:flex-row gap-6 items-start">
              <div className="flex-1 w-full">
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 mb-6">
                  <div>
                    <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-bold mb-3 border ${plan.status === 'Dispatched' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-blue-50 text-blue-700 border-blue-100'}`}>
                      <Target className="w-3.5 h-3.5" /> {plan.status === 'Dispatched' ? 'DISPATCHED' : `PRIORITY ${i + 1}`}
                    </div>
                    <h3 className="text-xl font-bold text-slate-900">Hotspot Zone #{plan.hotspot_id}</h3>
                    <p className="text-slate-600 text-sm mt-1">{plan.recommended_action}</p>
                  </div>
                  <div className="sm:text-right flex sm:flex-col items-center sm:items-end gap-3 sm:gap-0">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider sm:mb-1">Projected ROI Score</div>
                    <div className="flex items-baseline gap-1">
                      <div className={`text-3xl font-bold ${plan.roi_score > 70 ? 'text-rose-600' : plan.roi_score > 40 ? 'text-amber-600' : 'text-blue-600'}`}>
                        {Number(plan.roi_score || 0).toFixed(1)}
                      </div>
                      <div className="text-sm font-medium text-slate-400">/ 100</div>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-0 border border-slate-200 rounded-xl overflow-hidden divide-y sm:divide-y-0 sm:divide-x divide-slate-200 bg-slate-50">
                  <div className="p-4 bg-white">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Assigned Team</div>
                    <div className="text-sm font-bold text-slate-900">{plan.recommended_team}</div>
                  </div>
                  <div className="p-4 bg-white">
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Optimal Time</div>
                    <div className="text-sm font-bold text-slate-900">{plan.recommended_time}</div>
                  </div>
                  <div className="p-4 bg-emerald-50/50">
                    <div className="text-xs font-semibold text-emerald-700 uppercase tracking-wider mb-1">Expected Benefit</div>
                    <div className="text-sm font-bold text-emerald-700">Maximized Flow Rate</div>
                  </div>
                </div>
              </div>
              
              <div className="w-full xl:w-64 flex flex-col gap-3 shrink-0 mt-4 xl:mt-0">
                <button 
                  onClick={() => handleDispatch(plan.hotspot_id)}
                  disabled={plan.status === 'Dispatched'}
                  className={`w-full px-6 py-3 font-semibold rounded-lg shadow-sm transition-all flex items-center justify-center gap-2 ${plan.status === 'Dispatched' ? 'bg-emerald-100 text-emerald-700 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 text-white active:scale-[0.98]'}`}>
                  <CheckCircle2 className="w-5 h-5" /> {plan.status === 'Dispatched' ? 'Dispatched' : 'Approve & Dispatch'}
                </button>
                <button 
                  onClick={() => setExpandedIntelligence(expandedIntelligence === i ? null : i)}
                  className="w-full px-6 py-3 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-semibold rounded-lg shadow-sm transition-all active:scale-[0.98] flex items-center justify-center gap-2">
                  {expandedIntelligence === i ? 'Hide Intelligence' : 'View Intelligence'} <ChevronRight className={`w-4 h-4 text-slate-400 transition-transform ${expandedIntelligence === i ? 'rotate-90' : ''}`} />
                </button>
              </div>
            </div>

            {/* Explainability Expansion Layer */}
            {expandedIntelligence === i && (
              <div className="mt-6 border-t border-slate-100 pt-6 animate-in slide-in-from-top-2 fade-in duration-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Activity className="w-4 h-4 text-blue-600" /> Operational Intelligence
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50 p-5 rounded-xl border border-slate-100">
                  <div>
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Resource Allocation Engine</div>
                    <p className="text-sm text-slate-700">{plan.assignment_reasoning}</p>
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Time Window Engine</div>
                    <p className="text-sm text-slate-700">{plan.timing_reasoning}</p>
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Scenario Selection Engine</div>
                    <p className="text-sm text-slate-700">{plan.scenario_reasoning}</p>
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Compliance Confidence Score</div>
                    <p className="text-sm text-emerald-700 font-bold bg-emerald-100 px-2 py-0.5 rounded w-max inline-block">{plan.confidence_score}%</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
