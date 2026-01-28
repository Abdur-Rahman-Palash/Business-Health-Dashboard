import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable static export for Vercel deployment
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // For static hosting
  distDir: 'out',
  // For proper routing
  skipTrailingSlashRedirect: true,
  reactCompiler: false,
};

export default nextConfig;
