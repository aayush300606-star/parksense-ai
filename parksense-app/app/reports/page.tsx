"use client";

import { useState, useEffect } from "react";
import { Camera, MapPin, Upload, AlertCircle, CheckCircle2, LocateFixed } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

export default function ReportsPage() {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [severity, setSeverity] = useState<string>("Pending");
  const [violationType, setViolationType] = useState<string>("");
  
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState<File | null>(null);
  
  const [recentReports, setRecentReports] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/reports/history`)
      .then(res => res.json())
      .then(data => setRecentReports(data))
      .catch(err => console.error("Error fetching reports", err));
  }, [isSubmitted]); // Refetch when a new report is submitted

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!location) return;
    
    setAnalyzing(true);
    
    const formData = new FormData();
    formData.append("location", location);
    formData.append("description", description);
    if (file) {
      formData.append("file", file);
    }
    
    try {
      const res = await fetch(`${API_BASE_URL}/api/reports/submit`, {
          method: "POST",
          body: formData
      });
      const data = await res.json();
      
      if (data.success) {
          setSeverity(data.report.severity);
          setViolationType(data.report.type);
          setIsSubmitted(true);
      }
    } catch (err) {
      console.error("Submission failed", err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-1">Citizen Reporting Module</h1>
        <p className="text-slate-500 text-sm mt-1">Crowdsourced violation detection with AI-automated severity categorization.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Submission Form */}
        <div className="saas-card p-6">
          <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
            <Camera className="w-5 h-5 text-blue-600" /> New Violation Report
          </h3>

          {!isSubmitted ? (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Upload Photo Evidence</label>
                <div className="relative w-full h-32 border-2 border-dashed border-slate-300 rounded-xl flex flex-col items-center justify-center bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer group overflow-hidden">
                  <input 
                    type="file" 
                    accept="image/*" 
                    onChange={(e) => {
                        if (e.target.files && e.target.files.length > 0) {
                            setFile(e.target.files[0]);
                        }
                    }}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" 
                  />
                  {file ? (
                    <div className="text-center p-4">
                      <span className="text-emerald-600 font-bold block mb-1">Evidence Attached</span>
                      <span className="text-xs text-slate-500 truncate max-w-[200px] block">{file.name}</span>
                    </div>
                  ) : (
                    <>
                      <Upload className="w-8 h-8 text-slate-400 group-hover:text-blue-600 mb-2 transition-colors" />
                      <span className="text-sm font-medium text-slate-500">Click to upload or drag and drop</span>
                    </>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Location</label>
                <div className="relative">
                  <input 
                    type="text" 
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g. MG Road Junction..." 
                    className="w-full bg-white border border-slate-300 rounded-xl py-3 pl-10 pr-4 text-slate-900 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all shadow-sm placeholder-slate-400" 
                    required 
                  />
                  <MapPin className="w-4 h-4 text-slate-400 absolute left-4 top-3.5" />
                  <button type="button" className="absolute right-2 top-2 p-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-slate-600 transition-colors">
                    <LocateFixed className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Description (Optional)</label>
                <textarea 
                  rows={3} 
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl p-3 text-slate-900 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all shadow-sm placeholder-slate-400" 
                  placeholder="Add any additional details..."
                ></textarea>
              </div>

              <button 
                type="submit" 
                disabled={analyzing}
                className="w-full py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold transition-all flex items-center justify-center gap-2 disabled:opacity-70 shadow-sm active:scale-[0.98]"
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
            <div className="py-8 flex flex-col items-center justify-center text-center space-y-4 animate-in fade-in zoom-in duration-300">
              <div className="w-16 h-16 rounded-full bg-emerald-50 flex items-center justify-center border border-emerald-100">
                <CheckCircle2 className="w-8 h-8 text-emerald-600" />
              </div>
              <div>
                <h4 className="text-xl font-bold text-slate-900 mb-1">Report Verified</h4>
                <p className="text-slate-500 text-sm">Thank you for keeping the city moving.</p>
              </div>
              
              <div className="w-full bg-slate-50 rounded-xl p-5 mt-4 border border-slate-200 text-left">
                <div className="text-xs text-slate-400 uppercase font-bold tracking-wider mb-4">AI Auto-Categorization</div>
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-600">Violation Type:</span>
                  <span className="font-bold text-slate-900">{violationType || "Obstructive Parking"}</span>
                </div>
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-600">Evidence Status:</span>
                  <span className="font-bold text-emerald-600">Securely Stored</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-slate-600">Severity Assessment:</span>
                  <span className={`px-2.5 py-1 rounded-md text-xs font-bold border ${
                    severity === 'Critical' ? 'bg-rose-50 text-rose-700 border-rose-200' :
                    severity === 'High' ? 'bg-amber-50 text-amber-700 border-amber-200' : 
                    severity === 'Medium' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                    'bg-slate-100 text-slate-700 border-slate-200'
                  }`}>
                    {severity} Impact
                  </span>
                </div>
              </div>

              <button 
                onClick={() => { 
                    setIsSubmitted(false); 
                    setSeverity("Pending"); 
                    setLocation("");
                    setDescription("");
                    setFile(null);
                }}
                className="text-blue-600 text-sm font-bold hover:text-blue-700 mt-4 underline decoration-blue-600/30 underline-offset-4"
              >
                Submit another report
              </button>
            </div>
          )}
        </div>

        {/* Live Feed */}
        <div className="saas-card p-6 flex flex-col max-h-[600px]">
          <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-blue-600" /> Live Community Feed
          </h3>

          <div className="space-y-4 overflow-y-auto pr-2 custom-scrollbar">
            {recentReports.length > 0 ? recentReports.map((report, i) => (
              <div key={i} className="p-5 bg-white rounded-xl border border-slate-200 hover:shadow-sm transition-shadow">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-slate-900 text-sm truncate pr-2 max-w-[70%]">{report.loc}</h4>
                  <span className="text-xs font-medium text-slate-500 flex-shrink-0">{report.time}</span>
                </div>
                <p className="text-slate-600 text-sm mb-4">{report.type}</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs font-mono font-bold text-slate-400 bg-slate-100 px-2 py-1 rounded">{report.id}</span>
                  <span className={`text-xs font-bold px-2.5 py-1 rounded-md border ${
                    report.status === 'Action Taken' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                    report.status === 'Patrol Dispatched' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                    report.status === 'Verified' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                    'bg-slate-100 text-slate-600 border-slate-200'
                  }`}>
                    {report.status}
                  </span>
                </div>
              </div>
            )) : (
                <div className="text-center text-slate-500 text-sm py-12">
                    No recent reports found.
                </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
