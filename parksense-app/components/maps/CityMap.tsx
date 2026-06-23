"use client";

import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// This fix ensures map markers show properly in Next.js
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from "react-leaflet";

let DefaultIcon = L.icon({
  iconUrl: icon.src,
  shadowUrl: iconShadow.src,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function CityMap({ hotspots = [] }: { hotspots: any[] }) {
  // Center of Bangalore
  const center: [number, number] = [12.9716, 77.5946];

  return (
    <MapContainer 
      center={center} 
      zoom={13} 
      style={{ height: "100%", width: "100%", zIndex: 0 }}
      zoomControl={true}
      className="z-0 outline-none"
    >
      {/* Clean Light Voyager theme for premium SaaS feel */}
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
      />
      
      {hotspots.map((hotspot, idx) => {
        // Just mock some random offset based on ID since we don't have exact lat/lon in this json right now
        // Or if we do, we use it. For demo, we scatter them around Bangalore.
        const lat = 12.9716 + (Math.random() - 0.5) * 0.1;
        const lon = 77.5946 + (Math.random() - 0.5) * 0.1;
        const isCritical = hotspot.csi > 75;

        return (
          <CircleMarker
            key={idx}
            center={[lat, lon]}
            radius={isCritical ? 10 : 7}
            pathOptions={{
              fillColor: isCritical ? "#E11D48" : "#2563EB", // rose-600 vs blue-600
              color: "#ffffff",
              weight: 2,
              fillOpacity: 0.8
            }}
          >
            <Popup>
              <div className="p-4 min-w-[200px]">
                <div className="flex justify-between items-start mb-2 border-b border-slate-100 pb-2">
                  <h4 className="font-bold text-slate-900 text-sm leading-tight">{hotspot.location_name}</h4>
                </div>
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-slate-500">CSI Score</span>
                    <span className={`font-semibold ${isCritical ? 'text-rose-600' : 'text-blue-600'}`}>
                      {hotspot.csi.toFixed(1)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-slate-500">Active Violations</span>
                    <span className="font-medium text-slate-900">{hotspot.count}</span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-slate-500">Delay Impact</span>
                    <span className="font-medium text-amber-600">+{hotspot.delay_minutes.toFixed(1)}m</span>
                  </div>
                </div>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
