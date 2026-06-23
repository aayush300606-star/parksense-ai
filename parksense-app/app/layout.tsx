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
    <html lang="en">
      <body className={`${inter.className} bg-slate-50 text-slate-900 antialiased selection:bg-blue-200 min-h-screen flex`}>
        <Sidebar />
        <main className="flex-1 ml-64 p-8 min-h-screen max-w-7xl">
          {children}
        </main>
      </body>
    </html>
  );
}
