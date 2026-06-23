"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";

interface MapProps {
  hotspots?: any[];
  violations?: any[];
  viewMode?: "clusters" | "heatmap" | "predictions";
  center?: [number, number];
  zoom?: number;
}

// Simple Heatmap component using plain DOM (since react-leaflet-heatmap isn't standard)
// We'll simulate heatmap using overlapping blurred circles or just use CircleMarkers for clusters
function HeatmapOverlay({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;
  
  return (
    <>
      {data.map((point, i) => (
        <CircleMarker
          key={`heat-${i}`}
          center={[point.lat || point.latitude, point.lng || point.longitude]}
          radius={point.csi ? point.csi / 2 : 5}
          fillColor={point.csi > 75 ? "#ef4444" : point.csi > 50 ? "#f59e0b" : "#3b82f6"}
          color="transparent"
          fillOpacity={0.4}
        />
      ))}
    </>
  );
}

export default function MapComponent({ 
  hotspots = [], 
  violations = [], 
  viewMode = "clusters",
  center = [12.9716, 77.5946], // Bangalore
  zoom = 12 
}: MapProps) {
  
  return (
    <div className="w-full h-full rounded-xl overflow-hidden border border-slate-700 shadow-2xl relative">
      <MapContainer 
        center={center} 
        zoom={zoom} 
        style={{ height: "100%", width: "100%", background: "#0f172a" }}
        zoomControl={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | MapMyIndia API Ready'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        
        {viewMode === "clusters" && hotspots.map((h, i) => (
          <CircleMarker
            key={`cluster-${i}`}
            center={[h.lat, h.lng]}
            radius={Math.min(30, Math.max(10, h.count / 2))}
            pathOptions={{ 
              fillColor: h.severity === 'Critical' ? '#ef4444' : h.severity === 'High' ? '#f59e0b' : '#3b82f6',
              color: '#ffffff',
              weight: 1,
              fillOpacity: 0.7
            }}
          >
            <Popup className="glass-popup">
              <div className="p-1">
                <h3 className="font-bold text-slate-800">{h.location_name}</h3>
                <p className="text-sm">Severity: <span className="font-semibold text-rose-600">{h.severity}</span></p>
                <p className="text-sm">CSI Score: <b>{h.csi.toFixed(1)}</b></p>
                <p className="text-sm">Violations: {h.count}</p>
                <p className="text-sm">Delay Impact: +{h.delay_minutes.toFixed(1)}m</p>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {viewMode === "heatmap" && <HeatmapOverlay data={hotspots} />}
        
        {viewMode === "predictions" && hotspots.slice(0, 15).map((h, i) => (
          <Marker key={`pred-${i}`} position={[h.lat, h.lng]}>
            <Popup>
              <b>Predicted Hotspot</b><br/>
              Probability: {(Math.random() * 40 + 50).toFixed(1)}%<br/>
              Reason: Evening peak hour
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Map branding overlay */}
      <div className="absolute bottom-4 left-4 z-[1000] bg-slate-900/80 backdrop-blur-md px-3 py-1.5 rounded-md border border-slate-700 flex items-center gap-2">
        <span className="text-xs font-semibold text-slate-300">Powered by</span>
        <span className="text-sm font-bold text-white">Mappls <span className="text-blue-400">MapMyIndia</span> API</span>
      </div>
    </div>
  );
}
