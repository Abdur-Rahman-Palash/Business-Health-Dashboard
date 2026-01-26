#!/usr/bin/env python3
"""
Deploy Streamlit Dashboard to Vercel as Serverless Function
"""

import os
import json

def create_vercel_streamlit_config():
    """Create Vercel configuration for Streamlit"""
    
    config = {
        "version": 2,
        "builds": [
            {
                "src": "api/streamlit-proxy.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/api/streamlit-proxy.py"
            }
        ],
        "env": {
            "STREAMLIT_SERVER_PORT": "8501",
            "STREAMLIT_SERVER_ADDRESS": "0.0.0.0"
        }
    }
    
    with open('vercel-streamlit.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ vercel-streamlit.json created")

def create_streamlit_proxy():
    """Create Streamlit proxy for Vercel"""
    
    proxy_code = '''from http.server import BaseHTTPRequestHandler
import json
import subprocess
import threading
import time
import os
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Start Streamlit if not running
        if not hasattr(self, 'streamlit_started'):
            self.start_streamlit()
            self.streamlit_started = True
        
        # Proxy to Streamlit
        self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def start_streamlit(self):
        """Start Streamlit in background"""
        def run_streamlit():
            os.system("streamlit run run_minimal_dashboard_clean.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true")
        
        thread = threading.Thread(target=run_streamlit, daemon=True)
        thread.start()
        time.sleep(5)  # Wait for Streamlit to start
    
    def proxy_request(self):
        """Proxy request to Streamlit"""
        try:
            import requests
            response = requests.get(f"http://localhost:8501{self.path}", timeout=10)
            
            self.send_response(response.status_code)
            for header, value in response.headers.items():
                if header.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(header, value)
            self.end_headers()
            
            self.wfile.write(response.content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
'''
    
    # Create api directory if not exists
    os.makedirs('api', exist_ok=True)
    
    with open('api/streamlit-proxy.py', 'w') as f:
        f.write(proxy_code)
    
    print("✅ api/streamlit-proxy.py created")

def create_package_json():
    """Create package.json for Vercel"""
    
    package = {
        "name": "streamlit-executive-dashboard",
        "version": "1.0.0",
        "scripts": {
            "build": "echo 'Build complete'",
            "start": "python api/streamlit-proxy.py"
        },
        "dependencies": {
            "requests": "^2.31.0"
        }
    }
    
    with open('package-streamlit.json', 'w') as f:
        json.dump(package, f, indent=2)
    
    print("✅ package-streamlit.json created")

def main():
    print("🚀 Streamlit Dashboard Vercel Deployment")
    print("=" * 50)
    
    # Create configurations
    create_vercel_streamlit_config()
    create_streamlit_proxy()
    create_package_json()
    
    print("\n📋 Next Steps:")
    print("1. Copy vercel-streamlit.json to vercel.json")
    print("2. Copy package-streamlit.json to package.json")
    print("3. Deploy: vercel --prod")
    print("4. Your Streamlit dashboard will be available at your Vercel URL")
    
    print("\n⚠️  Important Notes:")
    print("- Streamlit on Vercel has limitations")
    print("- Better to use Railway for full Streamlit functionality")
    print("- Vercel is best for Next.js frontend")

if __name__ == "__main__":
    main()
