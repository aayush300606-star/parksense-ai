"use client";

import { LucideIcon } from "lucide-react";
import { GlassCard } from "./GlassCard";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface KPICardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  color?: "blue" | "emerald" | "violet" | "rose" | "amber";
}

export function KPICard({ title, value, icon: Icon, trend, color = "blue" }: KPICardProps) {
  const colorClasses = {
    blue: "text-blue-400 bg-blue-400/10",
    emerald: "text-emerald-400 bg-emerald-400/10",
    violet: "text-violet-400 bg-violet-400/10",
    rose: "text-rose-400 bg-rose-400/10",
    amber: "text-amber-400 bg-amber-400/10",
  };

  return (
    <GlassCard glowColor={color} className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400">{title}</span>
        <div className={cn("p-2 rounded-lg", colorClasses[color])}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      
      <div className="flex items-end justify-between">
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-3xl font-bold text-white tracking-tight"
        >
          {value}
        </motion.div>
        
        {trend && (
          <div className={cn(
            "flex items-center text-xs font-semibold px-2 py-1 rounded-full",
            trend.isPositive ? "text-emerald-400 bg-emerald-400/10" : "text-rose-400 bg-rose-400/10"
          )}>
            {trend.isPositive ? "+" : "-"}{Math.abs(trend.value)}%
          </div>
        )}
      </div>
    </GlassCard>
  );
}
