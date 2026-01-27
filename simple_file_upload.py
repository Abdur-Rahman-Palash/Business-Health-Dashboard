#!/usr/bin/env python3
"""
Simple File Upload - Direct Working Solution
No complex logic, just basic Streamlit upload
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

def simple_csv_upload():
    """Simple CSV upload that works"""
    st.subheader("📊 Upload CSV File")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        key="simple_csv_upload"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Show success
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            st.info(f"📊 Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Show data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head())
            
            # Show basic stats
            st.subheader("📈 Basic Statistics")
            st.write(df.describe())
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
            return False
    
    return False

def simple_excel_upload():
    """Simple Excel upload that works"""
    st.subheader("📈 Upload Excel File")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        key="simple_excel_upload"
    )
    
    if uploaded_file is not None:
        try:
            # Read Excel
            df = pd.read_excel(uploaded_file)
            
            # Show success
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            st.info(f"📊 Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Show data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head())
            
            # Show basic stats
            st.subheader("📈 Basic Statistics")
            st.write(df.describe())
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error reading Excel: {str(e)}")
            return False
    
    return False

def simple_text_upload():
    """Simple text upload that works"""
    st.subheader("📝 Upload Text File")
    
    uploaded_file = st.file_uploader(
        "Choose a text file",
        type=['txt'],
        key="simple_text_upload"
    )
    
    if uploaded_file is not None:
        try:
            # Read text
            content = uploaded_file.read().decode('utf-8')
            
            # Show success
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            st.info(f"📝 Content length: {len(content)} characters")
            
            # Show content preview
            st.subheader("📋 Content Preview")
            st.text_area("File Content", content[:1000] + "..." if len(content) > 1000 else content, height=200)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error reading text: {str(e)}")
            return False
    
    return False

def show_simple_upload_interface():
    """Show simple upload interface"""
    st.header("📁 Simple File Upload")
    st.write("Upload your files for instant analysis")
    
    # Upload options
    option = st.selectbox(
        "Choose file type to upload:",
        ["📊 CSV File", "📈 Excel File", "📝 Text File", "📄 PDF File"]
    )
    
    if option == "📊 CSV File":
        simple_csv_upload()
    elif option == "📈 Excel File":
        simple_excel_upload()
    elif option == "📝 Text File":
        simple_text_upload()
    elif option == "📄 PDF File":
        st.subheader("📄 Upload PDF File")
        st.info("PDF upload coming soon! For now, please use CSV, Excel, or Text files.")

if __name__ == "__main__":
    show_simple_upload_interface()
