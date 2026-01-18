"""
Vercel Serverless Function - Streamlit Proxy
This acts as a bridge between Vercel and Streamlit
"""

import http.client
import json
import os
from urllib.parse import urlparse

def handler(request):
    """Vercel serverless function handler"""
    
    # Get Streamlit URL from environment
    streamlit_url = os.environ.get('STREAMLIT_URL', 'https://your-streamlit-app.railway.app')
    
    try:
        # Parse the request
        method = request.method
        path = request.path
        headers = dict(request.headers)
        body = request.body if hasattr(request, 'body') else b''
        
        # Create connection to Streamlit
        parsed_url = urlparse(streamlit_url)
        conn = http.client.HTTPSConnection(parsed_url.netloc)
        
        # Forward request to Streamlit
        conn.request(method, path, body, headers)
        response = conn.getresponse()
        
        # Read response
        response_body = response.read()
        response_headers = dict(response.getheaders())
        
        return {
            'statusCode': response.status,
            'headers': response_headers,
            'body': response_body
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
