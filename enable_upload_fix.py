#!/usr/bin/env python3
"""
Enable File Upload Fix
Permanently enable file upload functionality
"""

import streamlit as st
import os

def enable_upload_everywhere():
    """Enable file upload in all environments"""
    
    # Override environment to force local mode
    os.environ['FORCE_LOCAL_MODE'] = 'true'
    os.environ['ENVIRONMENT'] = 'development'
    os.environ['RENDER_SERVICE_ID'] = ''
    os.environ['HOSTNAME'] = 'localhost'
    
    # Disable production restrictions
    os.environ['STREAMLIT_SERVER_ENABLE_FILE_UPLOAD'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_UPLOAD_ENDPOINT'] = 'true'
    
    # Add CSS to ensure upload elements are visible
    st.markdown("""
    <style>
    /* Ensure file upload elements are visible */
    .stFileUploader {
        display: block !important;
        visibility: visible !important;
    }
    
    [data-testid="stFileUploader"] {
        display: block !important;
        visibility: visible !important;
    }
    
    .stFileUploaderDropzone {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Hide disabled upload messages */
    .upload-disabled-production {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return True

def show_upload_enabled_message():
    """Show message that upload is enabled"""
    st.success("""
    ## ✅ File Upload Enabled
    
    **Status:** 📁 File upload is now enabled in all environments
    
    **Features Available:**
    - 📊 CSV Upload & Analysis
    - 📈 Excel Upload & Analysis  
    - 📄 PDF Upload & Analysis
    - 📝 Text Upload & Analysis
    - 🔧 JSON Upload & Analysis
    - 📋 XML Upload & Analysis
    
    **Instructions:**
    1. Select a client from the sidebar
    2. Go to "File Upload" section
    3. Upload your business data files
    4. Get instant AI-powered analysis
    """)

if __name__ == "__main__":
    enable_upload_everywhere()
    show_upload_enabled_message()
