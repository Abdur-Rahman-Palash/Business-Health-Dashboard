#!/usr/bin/env python3
"""
Update backend with test data
"""

import requests
import json

# Test data to update backend
test_data = {
    "status": "success",
    "data": {
        "kpis": [
            {
                "id": "revenue",
                "name": "Total Revenue",
                "value": 1000000,
                "change": 15.5,
                "trend": "up",
                "category": "financial",
                "unit": "USD"
            }
        ],
        "business_health_score": {
            "overall": 90,
            "financial": 92,
            "customer": 88,
            "operational": 89,
            "status": "excellent"
        },
        "insights": [
            {
                "title": "Revenue Growth",
                "description": "Revenue increased by 15.5%",
                "priority": "high"
            }
        ],
        "recommendations": [
            {
                "title": "Maintain Growth",
                "description": "Current strategies working well",
                "confidence": "high"
            }
        ]
    }
}

try:
    response = requests.post(
        "http://localhost:8081/api/dashboard/update",
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    print(f"✅ Backend updated: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
