#!/usr/bin/env python3
"""
Executive Business Health Dashboard - Streamlit Runner
Convenience script to start Streamlit analytics dashboard
"""

import streamlit.web.cli as stcli
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("📊 Starting Executive Business Health Dashboard - Streamlit Analytics...")
    print("🌐 Dashboard will be available at: http://localhost:8501")
    print("🔗 Make sure FastAPI backend is running at http://localhost:8000")
    print("\n" + "="*60)
    
    sys.argv = [
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    
    stcli.main()
