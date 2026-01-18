#!/usr/bin/env python3
"""
Executive Business Health Dashboard - Backend Runner
Convenience script to start the FastAPI backend server
"""

import uvicorn
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Executive Business Health Dashboard Backend...")
    print("📍 API Documentation will be available at: http://localhost:8001/docs")
    print("🔗 Health Check: http://localhost:8001/api/health")
    print("⚡ Dashboard API: http://localhost:8001/api/dashboard/complete")
    print("\n" + "="*60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
