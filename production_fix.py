#!/usr/bin/env python3
"""
Production Fix for Render.com 403 Errors
Completely disable problematic features
"""

import streamlit as st
import os

def disable_all_uploads():
    """Disable all upload functionality"""
    
    # Set environment variables to disable ALL upload features
    os.environ['STREAMLIT_SERVER_ENABLE_FILE_UPLOAD'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_UPLOAD_ENDPOINT'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_WIDGET_STATE'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_CACHING'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_WEBRTC'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_PROFILING'] = 'false'
    
    # Disable analytics
    os.environ['STREAMLIT_SERVER_GATHER_USAGE_STATS'] = 'false'
    
    # Set security settings
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    
    # Disable session management
    os.environ['STREAMLIT_SERVER_ENABLE_SESSION_STATE'] = 'false'
    
    return True

def show_production_message():
    """Show production deployment message"""
    st.error("""
    ## 🚫 File Upload Disabled in Production
    
    **Error:** 403 Forbidden on file upload endpoints
    
    **Status:** File upload temporarily disabled for deployment stability
    
    **Why:** Streamlit's built-in file upload endpoints are blocked on Render.com for security reasons.
    
    **✅ Working Features:**
    - Dashboard Analytics
    - KPI Monitoring
    - Business Insights  
    - Decision Making Tools
    - Client Management
    
    **📁 File Upload:** Local Development Only
    
    **For Full Functionality:**
    1. **Local Development:** Run `npm run dev` + `python simple_api_server.py`
    2. **URL:** http://localhost:3002
    3. **File Upload:** Works perfectly locally
    
    **Production Alternative:**
    - Use API endpoints for data integration
    - Manual data input through forms
    - Database integration for persistent storage
    """)

def override_file_uploader():
    """Override file uploader with disabled version"""
    
    # Add CSS to hide all upload elements
    st.markdown("""
    <style>
    /* Hide ALL file upload elements */
    .stFileUploader {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide upload related elements */
    [data-testid="stFileUploader"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide upload buttons */
    [data-testid="stFileUploaderDropzone"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide upload instructions */
    .stFileUploaderDropzoneInstructions {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide upload container */
    .stFileUploaderContainer {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Custom disabled message */
    .upload-disabled-production {
        border: 2px solid #e53e3e;
        border-radius: 8px;
        padding: 30px;
        background-color: #fff5f5;
        text-align: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Show disabled message
    st.markdown("""
    <div class="upload-disabled-production">
        <h3>📁 File Upload</h3>
        <p><strong>Status:</strong> ⚠️ Disabled in Production</p>
        <p><strong>Reason:</strong> 403 Forbidden errors on Render.com</p>
        <p><strong>Solution:</strong> Use local development for file uploads</p>
        <p><strong>Local URL:</strong> <code>http://localhost:3002</code></p>
    </div>
    """, unsafe_allow_html=True)

def init_production_environment():
    """Initialize production environment"""
    disable_all_uploads()
    override_file_uploader()
    return True

if __name__ == "__main__":
    init_production_environment()
    show_production_message()
