"use client";

import { useState } from "react";
import { GlassCard } from "@/components/dashboard/GlassCard";
import { Send, Bot, User, Sparkles } from "lucide-react";

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am the ParkSense GenAI Analyst. I can help you understand congestion patterns, prioritize enforcement zones, or explain AI predictions. What would you like to know?" }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const predefinedResponses: Record<string, string> = {
    "Which area should police prioritize today?": "Based on current CSI scores and predictive models, I recommend dispatching patrols to **Connaught Place** and **Karol Bagh**. These zones show a 92% probability of severe congestion forming within the next hour due to illegal parking spillovers from nearby commercial activities.",
    "Show top congestion-causing hotspots.": "The top 3 congestion hotspots currently are:\n\n1. **Chandni Chowk** (Effective width loss: 42%, Delay: +14m)\n2. **Lajpat Nagar Market** (Effective width loss: 38%, Delay: +11m)\n3. **ITO Intersection** (Effective width loss: 31%, Delay: +8m)\n\nWould you like me to run a digital twin simulation on any of these to see the impact of enforcement?",
    "What happens if parking is removed from this zone?": "According to our Digital Twin simulation, if we achieve a 100% reduction in illegal parking at this zone, the average traffic speed will increase from **14.2 km/h** to **38.5 km/h**. The queue length will reduce by **82%**, saving commuters an average of **12.4 minutes** of travel time.",
    "Which area experiences maximum delays?": "Currently, **Chandni Chowk** is experiencing the maximum delay of **+14.5 minutes** compared to the baseline. This is primarily driven by double-parking violations narrowing the effective road width to just 1 lane."
  };

  const handleSend = () => {
    if (!input.trim()) return;
    
    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setInput("");
    setIsTyping(true);

    // Mock AI response
    setTimeout(() => {
      let response = "I'm analyzing the real-time telemetry and AI models... Based on the data, this appears to be a critical enforcement priority. Please check the Smart Enforcement dashboard for automated patrol routes.";
      
      // Match exact predefined questions if clicked
      if (predefinedResponses[userMsg]) {
        response = predefinedResponses[userMsg];
      }
      
      setMessages(prev => [...prev, { role: "assistant", content: response }]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3rem)]">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white mb-1 flex items-center gap-3">
          <Sparkles className="w-8 h-8 text-blue-400" />
          GenAI Traffic Analyst
        </h1>
        <p className="text-slate-400">Conversational interface for complex traffic intelligence queries.</p>
      </div>

      <div className="flex-1 flex gap-6 overflow-hidden">
        {/* Chat Area */}
        <GlassCard className="flex-1 flex flex-col p-0 overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-4 max-w-[80%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg ${
                  msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-800 border border-slate-600 text-blue-400'
                }`}>
                  {msg.role === 'user' ? <User className="w-5 h-5 text-white" /> : <Bot className="w-6 h-6" />}
                </div>
                <div className={`p-4 rounded-2xl ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-tr-none' 
                    : 'bg-slate-800/80 border border-slate-700 text-slate-200 rounded-tl-none'
                }`}>
                  {msg.content.split('\n').map((line, j) => (
                    <p key={j} className={j > 0 ? "mt-2" : ""}>
                      {/* Very basic markdown bold parsing for demo */}
                      {line.split('**').map((part, k) => k % 2 === 1 ? <strong key={k} className="text-white">{part}</strong> : part)}
                    </p>
                  ))}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex gap-4 max-w-[80%]">
                <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-600 text-blue-400 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-6 h-6" />
                </div>
                <div className="p-4 rounded-2xl bg-slate-800/80 border border-slate-700 rounded-tl-none flex gap-1 items-center">
                  <div className="w-2 h-2 rounded-full bg-slate-500 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            )}
          </div>
          
          <div className="p-4 bg-slate-900 border-t border-slate-700">
            <div className="relative">
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask the AI Analyst..."
                className="w-full bg-slate-800 border border-slate-600 rounded-full py-3 pl-6 pr-12 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
              <button 
                onClick={handleSend}
                className="absolute right-2 top-1.5 p-2 rounded-full bg-blue-600 hover:bg-blue-500 text-white transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </GlassCard>

        {/* Suggested Prompts */}
        <div className="w-80 hidden lg:flex flex-col gap-4">
          <GlassCard glowColor="violet" className="flex-1">
            <h3 className="font-semibold text-white mb-4">Suggested Queries</h3>
            <div className="space-y-3">
              {Object.keys(predefinedResponses).map((q, i) => (
                <button 
                  key={i}
                  onClick={() => {
                    setInput(q);
                    setTimeout(() => {
                      document.querySelector('button .lucide-send')?.parentElement?.click();
                    }, 100);
                  }}
                  className="w-full text-left p-3 text-sm text-slate-300 hover:text-white bg-slate-800/50 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
