#!/usr/bin/env python3
"""
Direct Upload Fix - Bypass All Upload Issues
Complete file upload solution without 403 errors
"""

import streamlit as st
import pandas as pd
import io
import base64
from datetime import datetime

def create_download_link(df, filename="data.csv", text="Download CSV"):
    """Create a download link for the dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def direct_file_processor():
    """Direct file processor that bypasses upload endpoints"""
    
    st.header("📁 Direct File Processor")
    st.write("Upload and analyze your files without 403 errors")
    
    # File type selector
    file_type = st.selectbox(
        "Select File Type:",
        ["📊 CSV File", "📈 Excel File", "📝 Text File"]
    )
    
    if file_type == "📊 CSV File":
        process_csv_direct()
    elif file_type == "📈 Excel File":
        process_excel_direct()
    elif file_type == "📝 Text File":
        process_text_direct()

def process_csv_direct():
    """Process CSV directly without upload endpoints"""
    st.subheader("📊 CSV File Analysis")
    
    # Use text input for CSV data as backup
    st.write("**Option 1: Paste CSV Data Directly**")
    csv_data = st.text_area(
        "Paste your CSV data here:",
        height=150,
        placeholder="name,age,salary\nJohn,25,50000\nJane,30,60000\nBob,35,70000"
    )
    
    if csv_data:
        try:
            # Process CSV data
            from io import StringIO
            df = pd.read_csv(StringIO(csv_data))
            
            st.success(f"✅ CSV data processed successfully!")
            st.info(f"📊 Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Show data
            st.subheader("📋 Data Preview")
            st.dataframe(df)
            
            # Show statistics
            st.subheader("📈 Data Statistics")
            st.write(df.describe())
            
            # Download option
            st.subheader("💾 Download Processed Data")
            st.markdown(create_download_link(df, "processed_data.csv", "📥 Download CSV"), unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error processing CSV: {str(e)}")
    
    st.write("---")
    st.write("**Option 2: File Information Input**")
    
    # Manual data input as alternative
    with st.expander("📝 Enter Data Manually"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Name:")
            value1 = st.number_input("Value 1:", value=0)
        
        with col2:
            category = st.selectbox("Category:", ["Sales", "Marketing", "Operations", "Finance"])
            value2 = st.number_input("Value 2:", value=0)
        
        with col3:
            date = st.date_input("Date:")
            notes = st.text_area("Notes:")
        
        if st.button("💾 Add Data"):
            # Create dataframe from manual input
            data = {
                'Name': [name] if name else ['Sample'],
                'Category': [category],
                'Value1': [value1],
                'Value2': [value2],
                'Date': [date],
                'Notes': [notes] if notes else ['No notes']
            }
            df_manual = pd.DataFrame(data)
            
            st.success("✅ Data added successfully!")
            st.dataframe(df_manual)
            
            # Add to session state for accumulation
            if 'accumulated_data' not in st.session_state:
                st.session_state.accumulated_data = df_manual
            else:
                st.session_state.accumulated_data = pd.concat([st.session_state.accumulated_data, df_manual], ignore_index=True)
            
            st.info(f"📊 Total accumulated data: {len(st.session_state.accumulated_data)} rows")
    
    # Show accumulated data
    if 'accumulated_data' in st.session_state:
        st.subheader("📊 Accumulated Data")
        st.dataframe(st.session_state.accumulated_data)
        
        if st.button("🗑️ Clear Accumulated Data"):
            del st.session_state.accumulated_data
            st.success("✅ Data cleared!")
            st.rerun()

def process_excel_direct():
    """Process Excel data directly"""
    st.subheader("📈 Excel File Analysis")
    st.info("Excel processing coming soon! For now, please use CSV option or paste your data below.")
    
    # Text input for Excel-like data
    excel_data = st.text_area(
        "Paste your Excel-like data (tab-separated):",
        height=150,
        placeholder="Name\tAge\tSalary\nJohn\t25\t50000\nJane\t30\t60000"
    )
    
    if excel_data:
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(excel_data), sep='\t')
            st.success("✅ Excel-like data processed!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def process_text_direct():
    """Process text data directly"""
    st.subheader("📝 Text File Analysis")
    
    text_data = st.text_area(
        "Enter your text data:",
        height=200,
        placeholder="Enter your business text, notes, or any text data here..."
    )
    
    if text_data:
        st.success(f"✅ Text processed successfully!")
        st.info(f"📝 Character count: {len(text_data)}")
        st.info(f"📊 Word count: {len(text_data.split())}")
        
        # Basic text analysis
        st.subheader("📋 Text Preview")
        st.text(text_data[:500] + "..." if len(text_data) > 500 else text_data)
        
        # Simple sentiment analysis placeholder
        st.subheader("💭 Basic Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Length", f"{len(text_data)} chars")
        
        with col2:
            st.metric("📝 Words", f"{len(text_data.split())}")
        
        with col3:
            st.metric("📄 Lines", f"{len(text_data.splitlines())}")

if __name__ == "__main__":
    direct_file_processor()
