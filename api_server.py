#!/usr/bin/env python3
"""
Simple API Server for Local Development
Fixes 403 errors for frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "local-api-server",
        "version": "1.0.0"
    })

@app.route('/api/dashboard/complete', methods=['GET'])
def dashboard_complete():
    """Complete dashboard data endpoint"""
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "kpis": [
                {
                    "name": "Revenue",
                    "value": random.randint(800000, 1200000),
                    "unit": "USD",
                    "change": random.uniform(-10, 15),
                    "target": 1000000,
                    "status": "good" if random.random() > 0.3 else "warning"
                },
                {
                    "name": "Customer Satisfaction",
                    "value": random.uniform(3.5, 4.8),
                    "unit": "rating",
                    "change": random.uniform(-0.2, 0.3),
                    "target": 4.5,
                    "status": "good"
                },
                {
                    "name": "Operational Efficiency",
                    "value": random.uniform(75, 95),
                    "unit": "percent",
                    "change": random.uniform(-5, 8),
                    "target": 85,
                    "status": "good" if random.random() > 0.4 else "warning"
                },
                {
                    "name": "Market Share",
                    "value": random.uniform(15, 35),
                    "unit": "percent",
                    "change": random.uniform(-2, 4),
                    "target": 25,
                    "status": "good" if random.random() > 0.5 else "warning"
                }
            ],
            "insights": [
                {
                    "id": "insight_1",
                    "title": "Revenue Growth Opportunity",
                    "description": "Analysis reveals significant revenue growth potential in Q4",
                    "impact": "high",
                    "confidence": 0.85,
                    "category": "Revenue",
                    "recommendation": "Focus on high-value customer segments",
                    "priority": "high"
                },
                {
                    "id": "insight_2",
                    "title": "Operational Efficiency",
                    "description": "Process improvements can reduce costs by 15%",
                    "impact": "medium",
                    "confidence": 0.78,
                    "category": "Operations",
                    "recommendation": "Implement automation in key processes",
                    "priority": "medium"
                }
            ],
            "recommendations": [
                {
                    "id": "rec_1",
                    "title": "Expand Market Presence",
                    "description": "Increase marketing budget by 20% for targeted campaigns",
                    "impact_score": 8.5,
                    "effort_score": 6.0,
                    "roi_estimate": 2.5,
                    "timeline": "6 months",
                    "category": "Growth",
                    "priority": "high"
                },
                {
                    "id": "rec_2",
                    "title": "Optimize Supply Chain",
                    "description": "Implement just-in-time inventory management",
                    "impact_score": 7.2,
                    "effort_score": 5.5,
                    "roi_estimate": 1.8,
                    "timeline": "4 months",
                    "category": "Efficiency",
                    "priority": "medium"
                }
            ],
            "risks": [
                {
                    "id": "risk_1",
                    "name": "Market Competition",
                    "level": "medium",
                    "probability": 0.6,
                    "impact": 7.0,
                    "mitigation": "Strengthen competitive positioning",
                    "category": "Strategic"
                },
                {
                    "id": "risk_2",
                    "name": "Supply Chain Disruption",
                    "level": "low",
                    "probability": 0.3,
                    "impact": 8.0,
                    "mitigation": "Diversify supplier base",
                    "category": "Operational"
                }
            ],
            "business_health_score": random.uniform(70, 95),
            "executive_summary": {
                "overall_status": "positive" if random.random() > 0.3 else "needs_attention",
                "key_highlights": [
                    "Strong revenue growth in Q3",
                    "Customer satisfaction improving",
                    "Operational efficiency gains achieved"
                ],
                "critical_issues": [
                    "Market share pressure in key segments",
                    "Supply chain vulnerabilities identified"
                ]
            }
        }
    })

@app.route('/api/dashboard/update', methods=['POST'])
def dashboard_update():
    """Update dashboard data endpoint"""
    return jsonify({
        "status": "success",
        "message": "Dashboard data updated successfully",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/_stcore/health', methods=['GET'])
def streamlit_health():
    """Streamlit health check endpoint"""
    return "ok"

if __name__ == '__main__':
    print("🚀 Local API Server starting...")
    print("📍 Available endpoints:")
    print("   - GET  http://localhost:8081/api/health")
    print("   - GET  http://localhost:8081/api/dashboard/complete")
    print("   - POST http://localhost:8081/api/dashboard/update")
    print("   - GET  http://localhost:8081/_stcore/health")
    print("🔧 CORS enabled for all origins")
    print("🌐 Server running on http://localhost:8081")
    print("Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=8081, debug=True)
