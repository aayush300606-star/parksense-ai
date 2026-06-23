import { cn } from "@/lib/utils";
import React from "react";

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  glowColor?: "blue" | "emerald" | "violet" | "rose" | "amber" | "none";
}

export function GlassCard({ children, className, glowColor = "none", ...props }: GlassCardProps) {
  const glowMap = {
    blue: "shadow-[0_0_15px_rgba(59,130,246,0.15)]",
    emerald: "shadow-[0_0_15px_rgba(16,185,129,0.15)]",
    violet: "shadow-[0_0_15px_rgba(139,92,246,0.15)]",
    rose: "shadow-[0_0_15px_rgba(244,63,94,0.15)]",
    amber: "shadow-[0_0_15px_rgba(245,158,11,0.15)]",
    none: "",
  };

  return (
    <div 
      className={cn(
        "glass-card p-6 relative overflow-hidden", 
        glowMap[glowColor],
        className
      )}
      {...props}
    >
      {/* Subtle top highlight for 3D effect */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
      {children}
    </div>
  );
}
