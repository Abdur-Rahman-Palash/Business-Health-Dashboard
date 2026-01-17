#!/bin/bash
# Vercel Deployment Script for Executive Dashboard

echo "🚀 Starting Vercel Deployment..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "🔐 Checking Vercel authentication..."
vercel whoami

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment Complete!"
echo ""
echo "🌐 Your Executive Dashboard is now live at:"
echo "https://executive-dashboard.vercel.app"
echo ""
echo "📋 Post-Deployment Actions:"
echo "1. 🎯 Visit your live dashboard at the URL above"
echo "2. 📊 Monitor performance at vercel.com/dashboard"
echo "3. 🔄 Update: Push new code to trigger redeployment"
echo "4. 🔧 Configure: Add custom domain in Vercel dashboard"
echo "5. 📈 Analytics: Set up Vercel Analytics for usage tracking"
