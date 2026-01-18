#!/bin/bash

# Executive Dashboard - Hostinger Deployment Script
# This script prepares and packages the dashboard for Hostinger deployment

echo "🚀 Executive Dashboard - Hostinger Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Clean previous build
echo -e "${BLUE}🧹 Cleaning previous build...${NC}"
rm -rf out
rm -rf .next

# Step 2: Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
npm install

# Step 3: Build for production
echo -e "${BLUE}🏗️ Building for production...${NC}"
npm run export

# Step 4: Check if build was successful
if [ ! -d "out" ]; then
    echo -e "${RED}❌ Build failed! 'out' directory not found.${NC}"
    exit 1
fi

if [ ! -f "out/index.html" ]; then
    echo -e "${RED}❌ Build failed! 'index.html' not found in 'out' directory.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful!${NC}"

# Step 5: Create deployment package
echo -e "${BLUE}📦 Creating deployment package...${NC}"
cd out
zip -r ../executive-dashboard-hostinger.zip .
cd ..

echo -e "${GREEN}✅ Package created: executive-dashboard-hostinger.zip${NC}"

# Step 6: Show deployment instructions
echo -e "${YELLOW}📋 Deployment Instructions:${NC}"
echo "1. Upload 'executive-dashboard-hostinger.zip' to Hostinger"
echo "2. Extract the zip file in 'public_html' directory"
echo "3. Make sure '.htaccess' file is in the root"
echo "4. Visit your domain to test"
echo ""

echo -e "${BLUE}📁 Files in 'out' directory:${NC}"
ls -la out/

echo -e "${GREEN}🎉 Ready for Hostinger deployment!${NC}"
echo ""
echo -e "${YELLOW}📝 Important Notes:${NC}"
echo "- All routing is handled by .htaccess"
echo "- Page reload will work perfectly"
echo "- Static files are served directly"
echo "- Security headers are enabled"
echo "- Gzip compression is active"
echo "- Cache is optimized for performance"
