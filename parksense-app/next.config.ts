import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Expose the NEXT_PUBLIC_API_URL env variable to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000',
  },
};

export default nextConfig;
