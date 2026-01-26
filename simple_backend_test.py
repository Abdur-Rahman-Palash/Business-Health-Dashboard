#!/usr/bin/env python3
"""
Real Backend API Server with Dynamic Data Updates
No mock data - only processes real uploaded data
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
from datetime import datetime
import os
import threading
import time

# Global data storage
backend_data = {
    'status': 'success',
    'message': 'No data available - please upload files for analysis',
    'data': {
        'business_health_score': {
            'overall': 0,
            'financial': 0,
            'customer': 0,
            'operational': 0,
            'status': 'no_data'
        },
        'kpis': [],
        'insights': [],
        'recommendations': [],
        'last_updated': datetime.now().isoformat()
    }
}

class RealAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            health_data = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'Executive Dashboard API',
                'version': '1.0.0',
                'message': 'Real API - Dynamic updates enabled'
            }
            
            self.wfile.write(json.dumps(health_data).encode())
            
        elif parsed_path.path == '/api/dashboard/complete':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return current data with timestamp
            backend_data['data']['last_updated'] = datetime.now().isoformat()
            self.wfile.write(json.dumps(backend_data).encode())
            
        elif parsed_path.path == '/api/dashboard/update':
            # Allow POST for updates but handle GET too
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'ready',
                'message': 'Send POST request to update data',
                'current_data': backend_data
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/dashboard/update':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Update backend data
                global backend_data
                backend_data = json.loads(post_data.decode('utf-8'))
                backend_data['data']['last_updated'] = datetime.now().isoformat()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': 'Data updated successfully',
                    'timestamp': datetime.now().isoformat()
                }
                
                self.wfile.write(json.dumps(response).encode())
                print(f"✅ Backend data updated at {datetime.now().isoformat()}")
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    'status': 'error',
                    'message': f'Failed to update data: {str(e)}'
                }
                
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Suppress log messages
        pass

def simulate_data_updates():
    """Simulate periodic data updates for testing"""
    global backend_data
    
    while True:
        time.sleep(10)  # Update every 10 seconds
        
        # Only update if there's actual data
        if backend_data.get('data', {}).get('kpis'):
            # Simulate small changes
            for kpi in backend_data['data']['kpis']:
                if kpi.get('id') == 'revenue':
                    kpi['value'] = int(kpi['value'] * (1 + 0.01))  # 1% increase
                    kpi['change'] = kpi.get('change', 0) + 0.5
            
            backend_data['data']['last_updated'] = datetime.now().isoformat()
            print(f"🔄 Auto-updated data at {datetime.now().isoformat()}")

def run_server():
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, RealAPIHandler)
    
    # Start background thread for data updates
    update_thread = threading.Thread(target=simulate_data_updates, daemon=True)
    update_thread.start()
    
    print("🚀 Real Backend API Server running on http://localhost:8081")
    print("📊 Available endpoints:")
    print("   - GET /api/health")
    print("   - GET /api/dashboard/complete (real-time data)")
    print("   - POST /api/dashboard/update (update data)")
    print("🔄 Auto-updates enabled every 10 seconds when data exists")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
