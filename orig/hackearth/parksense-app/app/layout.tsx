import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/dashboard/Sidebar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ParkSense AI - Congestion Intelligence",
  description: "AI-Driven Parking Intelligence for Detecting Illegal Parking Hotspots",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-slate-950 text-slate-50 antialiased overflow-x-hidden selection:bg-blue-500/30`}>
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 ml-64 p-6 min-h-screen">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
