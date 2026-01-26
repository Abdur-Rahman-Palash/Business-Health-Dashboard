from http.server import BaseHTTPRequestHandler
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
