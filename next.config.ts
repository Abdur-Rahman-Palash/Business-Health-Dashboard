import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: false,
  images: {
    unoptimized: true
  },
  // For Hostinger static hosting
  distDir: 'out',
  // For proper routing
  skipTrailingSlashRedirect: true,
  reactCompiler: false,
};

export default nextConfig;
