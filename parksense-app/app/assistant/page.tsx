"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2, Sparkles, Zap, ChevronRight, FileText, TrendingUp, ShieldAlert, CheckCircle2 } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

const SUGGESTED_PROMPTS = [
  "Analyze the top 3 critical hotspots and their primary causes.",
  "What is the current Congestion Severity Index?",
  "Explain the Parking Impact Score.",
  "Identify the most vulnerable nodes in the traffic network.",
  "What is the root cause of congestion in Zone 4?",
  "Simulate a 20% reduction in illegal parking at Indiranagar.",
  "What are the predicted hotspots for tomorrow?"
];

const QUICK_ACTIONS = [
  { id: "daily-brief", label: "Daily Brief", icon: FileText, endpoint: "/api/copilot/daily-brief" },
  { id: "top-insights", label: "Top Insights", icon: TrendingUp, endpoint: "/api/copilot/top-insights" },
  { id: "recommendations", label: "Enforcement Recommendations", icon: ShieldAlert, endpoint: "/api/copilot/recommendations" }
];

export default function AnalystWorkspace() {
  const [messages, setMessages] = useState<{ role: string, content: string, followUps?: string[], confidence?: number }[]>([
    { role: 'assistant', content: 'Welcome to the AI Analysis Workspace. I am connected to the SCAC Copilot Orchestrator. How can I assist you today?' }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const executeQuickAction = async (action: any) => {
    setMessages(prev => [...prev, { role: 'user', content: `Execute Quick Action: ${action.label}` }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}${action.endpoint}`);
      if (!res.ok) throw new Error("API Route Failed");
      const data = await res.json();
      
      // Some endpoints return the narrative directly or inside a response/summary key
      const content = data.response || data.summary || data.brief || JSON.stringify(data, null, 2);
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: typeof content === 'string' ? content : JSON.stringify(content, null, 2),
        followUps: data.recommendations || []
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'System Error: Failed to execute quick action. Backend route may be offline.' }]);
    } finally {
      setLoading(false);
    }
  };

  const sendSpecificQuery = async (query: string) => {
    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/copilot/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });
      if (!res.ok) throw new Error("API Route Failed");
      
      const data = await res.json();
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response,
        followUps: data.recommendations || [],
        confidence: data.confidence
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Connection Error: Unable to reach the copilot orchestrator API (`/api/copilot/query`).' }]);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    await sendSpecificQuery(input);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="mb-6 flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            GenAI Analyst <Sparkles className="w-6 h-6 text-blue-600" />
          </h1>
          <p className="text-slate-500 text-sm mt-1">Natural language querying over live platform intelligence.</p>
        </div>
      </div>

      <div className="flex-1 saas-card flex flex-col overflow-hidden bg-white shadow-sm border border-slate-200">
        
        {/* Quick Actions Bar */}
        <div className="bg-slate-50/80 border-b border-slate-200 p-3 flex items-center gap-3 overflow-x-auto scrollbar-hide">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1 shrink-0">
            <Zap className="w-4 h-4 text-amber-500" /> Quick Actions:
          </span>
          {QUICK_ACTIONS.map(action => {
            const Icon = action.icon;
            return (
              <button
                key={action.id}
                onClick={() => executeQuickAction(action)}
                disabled={loading}
                className="shrink-0 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 hover:text-blue-700 hover:border-blue-300 hover:bg-blue-50 transition-colors flex items-center gap-1.5 disabled:opacity-50 shadow-sm"
              >
                <Icon className="w-3.5 h-3.5" />
                {action.label}
              </button>
            )
          })}
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/30">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-4 max-w-[85%] sm:max-w-[75%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm border ${
                  msg.role === 'user' ? 'bg-white text-slate-600 border-slate-200' : 'bg-blue-600 text-white border-blue-700'
                }`}>
                  {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>
                
                <div className="flex flex-col gap-2">
                  <div className={`px-5 py-4 rounded-2xl text-sm leading-relaxed shadow-sm whitespace-pre-wrap ${
                    msg.role === 'user' 
                      ? 'bg-blue-600 text-white rounded-tr-none' 
                      : 'bg-white border border-slate-200 text-slate-700 rounded-tl-none'
                  }`}>
                    {msg.content}
                  </div>
                  
                  {/* Confidence Badge */}
                  {msg.confidence !== undefined && (
                    <div className="flex items-center gap-1.5 ml-2 mt-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                      <span className="text-xs font-medium text-slate-500">
                        AI Confidence: {Number((msg.confidence * 100) || 0).toFixed(0)}%
                      </span>
                    </div>
                  )}

                  {/* Dynamic Suggested Questions (Follow-ups) */}
                  {msg.followUps && msg.followUps.length > 0 && (
                    <div className="mt-2 space-y-2">
                      <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider ml-2">Suggested Follow-ups:</div>
                      <div className="flex flex-wrap gap-2">
                        {msg.followUps.map((followUp, fIdx) => (
                          <button
                            key={fIdx}
                            onClick={() => sendSpecificQuery(followUp)}
                            disabled={loading}
                            className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-600 hover:text-blue-600 hover:border-blue-200 hover:bg-blue-50 transition-colors text-left disabled:opacity-50"
                          >
                            {followUp}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="flex gap-4 max-w-[80%] flex-row">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-sm">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="px-5 py-4 rounded-2xl rounded-tl-none text-sm bg-white border border-slate-200 text-slate-500 flex items-center gap-3 shadow-sm font-medium">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                  Orchestrating intelligence pipelines...
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area & Static Prompts */}
        <div className="border-t border-slate-200 bg-white">
          <div className="p-4 border-b border-slate-50 bg-slate-50/50">
            <div className="flex flex-wrap gap-2 justify-center max-w-4xl mx-auto">
              {SUGGESTED_PROMPTS.map((prompt, idx) => (
                <button
                  key={idx}
                  onClick={() => sendSpecificQuery(prompt)}
                  disabled={loading}
                  className="px-3 py-1.5 bg-white border border-slate-200 rounded-full text-[11px] font-medium text-slate-500 hover:text-slate-900 hover:border-slate-300 hover:bg-slate-100 transition-colors truncate max-w-[200px] disabled:opacity-50"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>

          <div className="p-4 sm:p-5">
            <div className="relative flex items-center max-w-4xl mx-auto">
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Ask about hotspots, root causes, or enforcement..."
                className="flex-1 bg-slate-50 border border-slate-300 rounded-xl py-3.5 pl-5 pr-14 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all shadow-sm placeholder-slate-400"
                disabled={loading}
              />
              <button 
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white rounded-lg transition-all shadow-sm active:scale-95"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
            <div className="mt-3 text-[10px] text-slate-400 text-center font-medium uppercase tracking-widest">
              Powered by ParkSense Copilot Orchestrator
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
