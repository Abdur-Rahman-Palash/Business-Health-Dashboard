import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable static export for Vercel serverless functions
  // output: 'export',
  trailingSlash: false,
  images: {
    unoptimized: true
  },
  // For proper routing
  skipTrailingSlashRedirect: true,
  reactCompiler: false,
};

export default nextConfig;
