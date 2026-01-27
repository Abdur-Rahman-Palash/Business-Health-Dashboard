#!/usr/bin/env python3
"""
Ultra Simple API Server for Local Development
No dependencies required - uses only standard library
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import random
from datetime import datetime
import threading
import time

class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Handle API requests with no dependencies"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if parsed_path.path == '/api/health':
            response = self.health_response()
        elif parsed_path.path == '/api/dashboard/complete':
            response = self.dashboard_response()
        elif parsed_path.path == '/_stcore/health':
            response = "ok"
            self.wfile.write(response.encode())
            return
        else:
            response = {"error": "Endpoint not found", "path": parsed_path.path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if parsed_path.path == '/api/dashboard/update':
            response = self.update_response()
        else:
            response = {"error": "Endpoint not found", "path": parsed_path.path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def health_response(self):
        """Health check response"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "simple-api-server",
            "version": "1.0.0"
        }
    
    def dashboard_response(self):
        """Dashboard data response"""
        return {
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
        }
    
    def update_response(self):
        """Update response"""
        return {
            "status": "success",
            "message": "Dashboard data updated successfully",
            "timestamp": datetime.now().isoformat()
        }
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server():
    """Run the API server"""
    server = HTTPServer(('localhost', 8081), SimpleAPIHandler)
    print("🚀 Simple API Server running on http://localhost:8081")
    print("📊 Available endpoints:")
    print("   - GET  http://localhost:8081/api/health")
    print("   - GET  http://localhost:8081/api/dashboard/complete")
    print("   - POST http://localhost:8081/api/dashboard/update")
    print("   - GET  http://localhost:8081/_stcore/health")
    print("🔧 CORS enabled for all origins")
    print("📦 No dependencies required")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    run_server()
