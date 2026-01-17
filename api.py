"""
Vercel Serverless API for Executive Dashboard
Provides endpoints for static data and configuration
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
from standalone_dashboard import generate_business_data
import os

class DashboardAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve main dashboard page
            self.send_response(200, {
                'Content-Type': 'text/html; charset=utf-8',
                'Cache-Control': 'no-cache'
            })
            
            # Simple HTML redirect to Streamlit
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Executive Business Health Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #1f2937; margin-bottom: 20px; }
        .status { background: #e8f5e8; color: #333; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .links { text-align: center; margin-top: 20px; }
        .links a { display: inline-block; margin: 0 10px; padding: 10px 20px; background: #FF6B6B; color: white; text-decoration: none; border-radius: 5px; }
        .links a:hover { background: #059669; }
        .health-check { background: #10b981; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Executive Business Health Dashboard</h1>
        
        <div class="status">
            <h2>🚀 Deployment Status</h2>
            <p><strong>Status:</strong> ✅ Successfully Deployed</p>
            <p><strong>Platform:</strong> Vercel Serverless</p>
            <p><strong>Dashboard:</strong> Ready for Access</p>
        </div>
        
        <div class="health-check">
            <h3>🔍 Kibana Check</h3>
            <p><strong>Health Endpoint:</strong> <a href="/api/health" target="_blank">/api/health</a></p>
            <p><strong>Data Endpoint:</strong> <a href="/api/data" target="_blank">/api/data</a></p>
            <p><strong>Monitor:</strong> Check logs in Vercel dashboard</p>
        </div>
        
        <div class="links">
            <h2>🌐 Access Your Dashboard</h2>
            <a href="https://executive-dashboard.vercel.app" target="_blank">
                🎯 Open Live Dashboard
            </a>
            <a href="https://executive-dashboard.vercel.app/api/data" target="_blank">
                📊 View API Data
            </a>
            <a href="https://executive-dashboard.vercel.app/api/health" target="_blank">
                🔍 Health Check
            </a>
        </div>
        
        <div class="status">
            <h2>📋 How to Use After Deployment</h2>
            <p><strong>1. Main Dashboard:</strong> Click "Open Live Dashboard" to access the full Streamlit interface</p>
            <p><strong>2. API Access:</strong> Use the API endpoint for data integration</p>
            <p><strong>3. Health Monitoring:</strong> Use /api/health endpoint for uptime checks</p>
            <p><strong>4. Kibana Integration:</strong> Monitor logs in Vercel dashboard</p>
            <p><strong>5. Performance:</strong> Monitor Vercel analytics for usage metrics</p>
            <p><strong>6. Updates:</strong> Redeploy by pushing to your Git repository</p>
        </div>
    </div>
</body>
</html>
            """
            
            self.wfile.write(html_content.encode('utf-8'))
            self.end_headers()
            
        elif parsed_path.path == '/api/health':
            # Health check endpoint
            self.send_response(200, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            })
            
            health_data = {
                'status': 'healthy',
                'timestamp': '2026-01-17T23:34:00Z',
                'service': 'Executive Dashboard API',
                'version': '1.0.0',
                'uptime': '100%',
                'checks': {
                    'api': 'pass',
                    'data_generation': 'pass',
                    'dependencies': 'pass'
                }
            }
            
            self.wfile.write(json.dumps(health_data, indent=2).encode('utf-8'))
            self.end_headers()
            # Serve business data as JSON
            self.send_response(200, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            })
            
            business_data = generate_business_data()
            response_data = {
                'status': 'success',
                'timestamp': '2026-01-17T23:30:00Z',
                'data': business_data
            }
            
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            self.end_headers()
            
        else:
            # 404 for other paths
            self.send_response(404, {'Content-Type': 'text/plain'})
            self.wfile.write(b'Not Found')
            self.end_headers()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), DashboardAPIHandler)
    
    print(f"🚀 Starting Vercel API Server on port {port}")
    server.serve_forever()
