"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Map, 
  TrendingUp, 
  ShieldAlert, 
  Activity, 
  Cpu, 
  MessageSquare, 
  Camera,
  Network,
  Share2
} from "lucide-react";

const navItems = [
  { name: "Executive", href: "/", icon: LayoutDashboard },
  { name: "Heatmaps", href: "/heatmap", icon: Map },
  { name: "AI Predictions", href: "/predictions", icon: TrendingUp },
  { name: "Smart Enforcement", href: "/enforcement", icon: ShieldAlert },
  { name: "Digital Twin", href: "/digital-twin", icon: Activity },
  { name: "Network Intelligence", href: "/network", icon: Network },
  { name: "Root Cause / DNA", href: "/root-cause", icon: Share2 },
  { name: "Explainable AI", href: "/explainability", icon: Cpu },
  { name: "GenAI Analyst", href: "/assistant", icon: MessageSquare },
  { name: "Citizen Reports", href: "/reports", icon: Camera },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 h-screen fixed left-0 top-0 bg-white border-r border-slate-200 z-50 flex flex-col shadow-sm">
      <div className="p-6 flex items-center gap-3 border-b border-slate-100">
        <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-sm">
          P
        </div>
        <div>
          <h1 className="font-bold text-xl tracking-tight text-slate-900">ParkSense <span className="text-blue-600">AI</span></h1>
          <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider">Congestion Intelligence</p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4 px-3">Command Modules</div>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive 
                  ? "bg-blue-50 text-blue-700 border border-blue-100 shadow-sm" 
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50 border border-transparent"
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? "text-blue-600" : "text-slate-400"}`} />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 m-4 rounded-xl bg-slate-50 border border-slate-200">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider">System Active</span>
        </div>
        <p className="text-[11px] text-slate-500 font-medium leading-tight">MapMyIndia API Connected<br/>AI Engine Online</p>
      </div>
    </div>
  );
}
