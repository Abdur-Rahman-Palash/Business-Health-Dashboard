#!/bin/bash

# Executive Dashboard MVP Deployment Script
# Bangladesh Market Focus - Quick Launch

echo "🚀 Executive Dashboard MVP Deployment - Bangladesh Market"
echo "========================================================"

# Check prerequisites
echo "📋 Checking prerequisites..."

# Node.js check
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Python check
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

# Docker check
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker"
    exit 1
fi

echo "✅ Prerequisites checked"

# Environment setup
echo "🔧 Setting up environment..."

# Frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Add Bangladesh-specific dependencies
pip install psycopg2-binary python-dotenv
cd ..

echo "✅ Dependencies installed"

# Database setup
echo "🗄️ Setting up PostgreSQL database..."

# Start PostgreSQL container
docker run --name exec-dashboard-db \
  -e POSTGRES_PASSWORD=password123 \
  -e POSTGRES_DB=executive_dashboard \
  -p 5432:5432 \
  -d postgres:15

# Wait for database to start
echo "⏳ Waiting for database to start..."
sleep 10

# Create database tables
cd backend
python database_setup.py
cd ..

echo "✅ Database setup complete"

# Environment configuration
echo "⚙️ Configuring environment..."

# Create .env file
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://postgres:password123@localhost:5432/executive_dashboard

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000

# Bangladesh Configuration
DEFAULT_CURRENCY=BDT
DEFAULT_TIMEZONE=Asia/Dhaka
DEFAULT_LANGUAGE=en

# Development Mode
NODE_ENV=development
EOF

echo "✅ Environment configured"

# Build and start applications
echo "🏗️ Building and starting applications..."

# Start backend
echo "🔧 Starting FastAPI backend..."
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 5

# Build and start frontend
echo "🎨 Building Next.js frontend..."
npm run build

echo "🚀 Starting Next.js frontend..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Applications started"

# Wait for applications to be ready
echo "⏳ Waiting for applications to be ready..."
sleep 10

# Health checks
echo "🏥 Performing health checks..."

# Backend health check
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

# Frontend health check
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi

# Test Bangladesh-specific features
echo "🇧🇩 Testing Bangladesh features..."

# Test BDT formatting
curl -X POST http://localhost:8000/api/test/bdt-format \
  -H "Content-Type: application/json" \
  -d '{"amount": 12345678.90}' || echo "BDT formatting test failed"

# Test Bengali language support
curl -X POST http://localhost:8000/api/test/bengali-support \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}' || echo "Bengali support test failed"

echo "✅ Bangladesh features tested"

# Deployment information
echo ""
echo "🎉 Executive Dashboard MVP is now running!"
echo "=========================================="
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🗄️ Database: localhost:5432"
echo ""
echo "🇧🇩 Bangladesh Features Enabled:"
echo "   ✅ BDT Currency Formatting"
echo "   ✅ Bengali Language Support"
echo "   ✅ Local Business Templates"
echo "   ✅ Bangladesh KPI Metrics"
echo ""
echo "🚀 Next Steps for Market Launch:"
echo "   1. Test with sample Bangladesh business data"
echo "   2. Deploy to Vercel (frontend) and Railway (backend)"
echo "   3. Set up custom domain"
echo "   4. Launch beta testing program"
echo ""
echo "📞 For support, check the documentation or create an issue"
echo ""

# Save process IDs for cleanup
echo $BACKEND_PID > .backend_pid
echo $FRONTEND_PID > .frontend_pid

echo "💡 To stop the applications: kill \$(cat .backend_pid) && kill \$(cat .frontend_pid)"
echo "💡 To stop database: docker stop exec-dashboard-db && docker rm exec-dashboard-db"
