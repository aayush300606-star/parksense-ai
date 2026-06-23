"use client";

import { useState } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Camera, MapPin, Upload, AlertCircle, CheckCircle2, LocateFixed } from "lucide-react";

export default function ReportsPage() {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [severity, setSeverity] = useState<"Pending" | "Critical" | "High" | "Medium" | "Low">("Pending");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setAnalyzing(true);
    
    // Simulate AI image analysis and categorization
    setTimeout(() => {
      setAnalyzing(false);
      setSeverity("High");
      setIsSubmitted(true);
    }, 2000);
  };

  const recentReports = [
    { id: "REP-9238", loc: "MG Road Junction", type: "Double Parking", status: "Action Taken", time: "10 mins ago" },
    { id: "REP-9237", loc: "Indiranagar 100ft", type: "Footpath Blocked", status: "Patrol Dispatched", time: "25 mins ago" },
    { id: "REP-9236", loc: "Koramangala 4th Blk", type: "No Parking Zone", status: "Verified", time: "1 hr ago" },
  ];

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Citizen Reporting Module</h1>
        <p className="text-slate-400">Crowdsourced violation detection with AI-automated severity categorization.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Submission Form */}
        <GlassCard>
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <Camera className="w-5 h-5 text-blue-400" /> New Violation Report
          </h3>

          {!isSubmitted ? (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Upload Photo Evidence</label>
                <div className="w-full h-32 border-2 border-dashed border-slate-600 rounded-lg flex flex-col items-center justify-center bg-slate-800/50 hover:bg-slate-800 transition-colors cursor-pointer group">
                  <Upload className="w-8 h-8 text-slate-500 group-hover:text-blue-400 mb-2 transition-colors" />
                  <span className="text-sm text-slate-400">Click to upload or drag and drop</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Location</label>
                <div className="relative">
                  <input type="text" placeholder="e.g. MG Road Junction..." className="w-full bg-slate-800 border border-slate-700 rounded-lg py-2.5 pl-10 pr-4 text-white focus:ring-1 focus:ring-blue-500 focus:outline-none" required />
                  <MapPin className="w-4 h-4 text-slate-500 absolute left-3 top-3.5" />
                  <button type="button" className="absolute right-2 top-2 p-1.5 bg-slate-700 hover:bg-slate-600 rounded text-slate-300">
                    <LocateFixed className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Description (Optional)</label>
                <textarea rows={3} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:ring-1 focus:ring-blue-500 focus:outline-none" placeholder="Add any additional details..."></textarea>
              </div>

              <button 
                type="submit" 
                disabled={analyzing}
                className="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold transition-colors flex items-center justify-center gap-2 disabled:opacity-70"
              >
                {analyzing ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    AI Analyzing Evidence...
                  </>
                ) : "Submit Report"}
              </button>
            </form>
          ) : (
            <div className="py-8 flex flex-col items-center justify-center text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/30">
                <CheckCircle2 className="w-8 h-8 text-emerald-400" />
              </div>
              <div>
                <h4 className="text-xl font-bold text-white mb-1">Report Verified</h4>
                <p className="text-slate-400 text-sm">Thank you for keeping the city moving.</p>
              </div>
              
              <div className="w-full bg-slate-800 rounded-lg p-4 mt-4 border border-slate-700 text-left">
                <div className="text-xs text-slate-400 uppercase font-bold tracking-wider mb-2">AI Auto-Categorization</div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-slate-300">Violation Type:</span>
                  <span className="font-semibold text-white">Obstructive Parking</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-slate-300">Vehicle Type:</span>
                  <span className="font-semibold text-white">SUV</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-300">Severity Assessment:</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                    severity === 'High' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-slate-700 text-white'
                  }`}>
                    {severity} Impact
                  </span>
                </div>
              </div>

              <button 
                onClick={() => { setIsSubmitted(false); setSeverity("Pending"); }}
                className="text-blue-400 text-sm font-medium hover:text-blue-300 mt-4"
              >
                Submit another report
              </button>
            </div>
          )}
        </GlassCard>

        {/* Live Feed */}
        <GlassCard glowColor="violet">
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-violet-400" /> Live Community Feed
          </h3>

          <div className="space-y-4">
            {recentReports.map((report, i) => (
              <div key={i} className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-white text-sm">{report.loc}</h4>
                  <span className="text-xs text-slate-400">{report.time}</span>
                </div>
                <p className="text-slate-300 text-sm mb-3">{report.type}</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs font-mono text-slate-500">{report.id}</span>
                  <span className={`text-xs font-bold px-2 py-1 rounded-md ${
                    report.status === 'Action Taken' ? 'bg-emerald-500/20 text-emerald-400' :
                    report.status === 'Patrol Dispatched' ? 'bg-amber-500/20 text-amber-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>
                    {report.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
