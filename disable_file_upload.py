#!/usr/bin/env python3
"""
Disable Streamlit File Upload Endpoints
Fix 403 Forbidden errors on Render.com
"""

import streamlit as st
import os
import sys

def disable_problematic_features():
    """Disable features that cause 403 errors"""
    
    # Set environment variables to disable problematic upload features
    os.environ['STREAMLIT_SERVER_ENABLE_FILE_UPLOAD'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_UPLOAD_ENDPOINT'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_WIDGET_STATE'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_CACHING'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION'] = 'false'
    
    # Disable analytics
    os.environ['STREAMLIT_SERVER_GATHER_USAGE_STATS'] = 'false'
    
    # Set security settings
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    
    return True

def create_custom_file_uploader(label, key, help_text=None, file_types=None):
    """Create custom file uploader that doesn't use Streamlit's upload endpoint"""
    
    st.markdown(f"""
    <div style="border: 2px dashed #cbd5e0; border-radius: 8px; padding: 20px; background-color: #f7fafc; margin: 10px 0;">
        <h4>{label}</h4>
        <p style="color: #718096; font-size: 14px;">{help_text or 'Choose a file to upload'}</p>
        <p style="color: #e53e3e; font-weight: bold;">⚠️ File upload temporarily disabled for deployment stability</p>
        <p style="color: #4a5568;">Please use the local development environment for file uploads.</p>
    </div>
    """, unsafe_allow_html=True)
    
    return None

def show_upload_disabled_message():
    """Show message about upload being disabled"""
    st.warning("""
    ## 📁 File Upload Feature
    
    **Status:** ⚠️ Temporarily Disabled for Deployment Stability
    
    **Reason:** Streamlit file upload endpoints are causing 403 Forbidden errors on Render.com deployment.
    
    **Solution:** 
    - ✅ Use **Local Development** for file uploads: `npm run dev` + `python simple_api_server.py`
    - ✅ All other features work perfectly on deployed version
    - 🔄 Working on permanent fix for production uploads
    
    **Available Features:**
    - ✅ Dashboard Analytics
    - ✅ KPI Monitoring  
    - ✅ Business Insights
    - ✅ Decision Making Tools
    - ✅ Client Management
    - ❌ File Upload (Local Only)
    
    **For File Upload Testing:**
    1. Run locally: `npm run dev` (port 3002)
    2. Start API server: `python simple_api_server.py` (port 8081)
    3. Access: http://localhost:3002
    4. Upload files work perfectly locally
    """)

def init_production_mode():
    """Initialize production mode with disabled uploads"""
    disable_problematic_features()
    
    # Add custom CSS to hide upload elements
    st.markdown("""
    <style>
    /* Hide problematic upload elements */
    .stFileUploader {
        display: none !important;
    }
    
    /* Hide upload progress indicators */
    .stProgress {
        display: none !important;
    }
    
    /* Hide file upload related elements */
    [data-testid="stFileUploader"] {
        display: none !important;
    }
    
    /* Custom styling for disabled upload area */
    .upload-disabled {
        border: 2px dashed #e53e3e;
        border-radius: 8px;
        padding: 20px;
        background-color: #fff5f5;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Test the disable functionality
    init_production_mode()
    show_upload_disabled_message()
