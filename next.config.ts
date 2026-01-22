import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Remove output: 'export' to enable API routes on Vercel
  // output: 'export',
  trailingSlash: false,
  images: {
    unoptimized: true
  },
  // For Hostinger static hosting - only use when building for static export
  // distDir: 'out',
  // For proper routing
  skipTrailingSlashRedirect: true,
  reactCompiler: false,
};

export default nextConfig;
