#!/usr/bin/env python3
"""
Test script to update backend data dynamically
"""

import requests
import json
import time
from datetime import datetime

def update_backend_data():
    """Update backend with test data"""
    
    # Test data to send
    test_data = {
        'status': 'success',
        'message': 'Test data updated',
        'data': {
            'business_health_score': {
                'overall': 85,
                'financial': 88,
                'customer': 82,
                'operational': 86,
                'status': 'good'
            },
            'kpis': [
                {
                    "id": "revenue",
                    "name": "Total Revenue",
                    "value": 950000,
                    "change": 12.5,
                    "trend": "up",
                    "category": "financial",
                    "unit": "USD",
                    "target": 1000000,
                    "status": "good"
                },
                {
                    "id": "customers",
                    "name": "Active Customers",
                    "value": 1050,
                    "change": 8.3,
                    "trend": "up",
                    "category": "customer",
                    "unit": "count",
                    "target": 1000,
                    "status": "good"
                }
            ],
            'insights': [
                {
                    "title": "Revenue Growth Detected",
                    "description": "Revenue increased by 12.5% - excellent performance",
                    "priority": "high",
                    "auto_generated": True
                }
            ],
            'recommendations': [
                {
                    "title": "Maintain Growth Strategy",
                    "description": "Current strategies are working well - continue focus on customer acquisition",
                    "confidence": "high",
                    "auto_generated": True
                }
            ],
            'last_updated': datetime.now().isoformat()
        }
    }
    
    try:
        # Try to update backend (if it supports POST)
        response = requests.post(
            "http://localhost:8081/api/dashboard/update",
            json=test_data,
            timeout=5
        )
        print(f"Backend update response: {response.status_code}")
        
    except requests.exceptions.RequestException:
        print("Backend doesn't support update endpoint - this is expected")
    
    return test_data

def test_frontend_update():
    """Test if frontend gets updated data"""
    
    print("🔄 Testing backend-frontend data flow...")
    
    # Get current backend data
    try:
        response = requests.get("http://localhost:8081/api/dashboard/complete", timeout=5)
        backend_data = response.json()
        print(f"✅ Backend data: {backend_data.get('status', 'unknown')}")
        
        if backend_data.get('status') == 'success':
            kpis = backend_data.get('data', {}).get('kpis', [])
            print(f"✅ KPIs found: {len(kpis)}")
            
            for kpi in kpis:
                print(f"   - {kpi.get('name', 'Unknown')}: {kpi.get('value', 0)}")
        else:
            print("ℹ️  No data in backend - upload files to see updates")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection error: {e}")
    
    print("\n📊 Frontend should show:")
    print("   - Backend API: Connected")
    print("   - Data Source: Backend API")
    print("   - Real-time updates when backend data changes")

if __name__ == "__main__":
    test_frontend_update()
