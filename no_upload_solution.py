#!/usr/bin/env python3
"""
No Upload Solution - Complete Data Input Without File Upload
100% working solution without any file upload functionality
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
import io

def manual_data_input():
    """Complete manual data input solution - no file upload"""
    
    st.header("📊 Business Data Input System")
    st.write("Enter your business data manually - no file upload required")
    st.success("✅ 100% Working - No 403 Errors!")
    
    # Data input method selection
    method = st.selectbox(
        "Choose Data Input Method:",
        ["📝 Quick CSV Data Entry", "📋 Manual Form Entry", "📊 Batch Data Entry", "📈 Financial Data Entry"]
    )
    
    if method == "📝 Quick CSV Data Entry":
        quick_csv_entry()
    elif method == "📋 Manual Form Entry":
        manual_form_entry()
    elif method == "📊 Batch Data Entry":
        batch_data_entry()
    elif method == "📈 Financial Data Entry":
        financial_data_entry()

def quick_csv_entry():
    """Quick CSV-like data entry"""
    st.subheader("📝 Quick CSV Data Entry")
    
    st.write("**Enter your data in CSV format (comma-separated):**")
    
    # Column headers
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        headers = st.text_input("Column Headers (comma-separated):", 
                               value="Name,Category,Amount,Date", 
                               help="e.g., Name,Category,Amount,Date")
    
    # Data rows
    st.write("**Enter your data rows:**")
    
    num_rows = st.number_input("Number of rows to add:", min_value=1, max_value=20, value=3)
    
    data_rows = []
    for i in range(num_rows):
        with st.expander(f"Row {i+1}"):
            cols = st.columns(len(headers.split(',')))
            row_data = []
            
            for j, header in enumerate(headers.split(',')):
                if j < len(cols):
                    if 'Amount' in header or 'Price' in header or 'Value' in header:
                        value = cols[j].number_input(f"{header} {i+1}:", value=0.0, key=f"row_{i}_col_{j}")
                    elif 'Date' in header:
                        value = cols[j].date_input(f"{header} {i+1}:", key=f"row_{i}_col_{j}")
                    else:
                        value = cols[j].text_input(f"{header} {i+1}:", key=f"row_{i}_col_{j}")
                    row_data.append(value)
            
            data_rows.append(row_data)
    
    if st.button("📊 Create DataFrame"):
        try:
            # Create DataFrame
            df = pd.DataFrame(data_rows, columns=headers.split(','))
            
            # Store in session state
            st.session_state.current_data = df
            
            st.success(f"✅ DataFrame created with {len(df)} rows and {len(df.columns)} columns!")
            st.dataframe(df)
            
            # Show statistics
            st.subheader("📈 Data Statistics")
            st.write(df.describe())
            
            # Download option
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"business_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error creating DataFrame: {str(e)}")

def manual_form_entry():
    """Manual form-based data entry"""
    st.subheader("📋 Manual Form Entry")
    
    with st.form("manual_entry_form"):
        st.write("**Enter Business Record:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Business Name/Item:")
            category = st.selectbox("Category:", ["Sales", "Marketing", "Operations", "Finance", "HR", "Other"])
            amount = st.number_input("Amount ($):", value=0.0, min_value=0.0)
        
        with col2:
            date = st.date_input("Date:", value=datetime.now().date())
            status = st.selectbox("Status:", ["Completed", "Pending", "In Progress", "Cancelled"])
            notes = st.text_area("Notes:")
        
        submitted = st.form_submit_button("💾 Add Record")
        
        if submitted:
            # Create record
            record = {
                'Name': [name] if name else ['Unnamed'],
                'Category': [category],
                'Amount': [amount],
                'Date': [date],
                'Status': [status],
                'Notes': [notes] if notes else ['No notes']
            }
            
            df_new = pd.DataFrame(record)
            
            # Add to session state
            if 'manual_records' not in st.session_state:
                st.session_state.manual_records = df_new
            else:
                st.session_state.manual_records = pd.concat([st.session_state.manual_records, df_new], ignore_index=True)
            
            st.success("✅ Record added successfully!")
            st.rerun()
    
    # Show accumulated records
    if 'manual_records' in st.session_state:
        st.subheader("📊 All Records")
        st.dataframe(st.session_state.manual_records)
        
        # Summary statistics
        total_amount = st.session_state.manual_records['Amount'].sum()
        st.metric("💰 Total Amount", f"${total_amount:,.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download Records"):
                csv = st.session_state.manual_records.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"manual_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🗑️ Clear All Records"):
                del st.session_state.manual_records
                st.success("✅ Records cleared!")
                st.rerun()

def batch_data_entry():
    """Batch data entry for multiple records"""
    st.subheader("📊 Batch Data Entry")
    
    st.write("Enter multiple records at once:")
    
    # Template data
    template_data = """Name,Category,Amount,Date,Status
Product A,Sales,1500.00,2024-01-15,Completed
Product B,Marketing,800.00,2024-01-16,Pending
Service C,Operations,2200.00,2024-01-17,In Progress"""
    
    batch_data = st.text_area(
        "Paste your data (CSV format):",
        value=template_data,
        height=200,
        help="Enter data in CSV format with headers"
    )
    
    if st.button("📊 Process Batch Data"):
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(batch_data))
            
            st.success(f"✅ Processed {len(df)} records!")
            st.dataframe(df)
            
            # Store in session state
            st.session_state.batch_data = df
            
            # Statistics
            st.subheader("📈 Batch Statistics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Records", len(df))
            with col2:
                if 'Amount' in df.columns:
                    st.metric("💰 Total Amount", f"${df['Amount'].sum():,.2f}")
            with col3:
                if 'Category' in df.columns:
                    st.metric("📋 Categories", df['Category'].nunique())
            
            # Category breakdown
            if 'Category' in df.columns:
                st.subheader("📋 Category Breakdown")
                category_counts = df['Category'].value_counts()
                st.bar_chart(category_counts)
            
            # Download
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Processed Data",
                data=csv,
                file_name=f"batch_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error processing batch data: {str(e)}")

def financial_data_entry():
    """Specialized financial data entry"""
    st.subheader("📈 Financial Data Entry")
    
    with st.form("financial_form"):
        st.write("**Enter Financial Data:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            revenue = st.number_input("Revenue ($):", value=0.0, min_value=0.0)
            expenses = st.number_input("Expenses ($):", value=0.0, min_value=0.0)
            profit = revenue - expenses
        
        with col2:
            period = st.selectbox("Period:", ["Monthly", "Quarterly", "Yearly"])
            department = st.selectbox("Department:", ["Sales", "Marketing", "Operations", "Finance", "All"])
            date = st.date_input("Period Date:", value=datetime.now().date())
        
        # Calculate metrics
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        st.metric("💰 Profit", f"${profit:,.2f}")
        st.metric("📊 Profit Margin", f"{profit_margin:.1f}%")
        
        notes = st.text_area("Financial Notes:")
        
        submitted = st.form_submit_button("💾 Add Financial Record")
        
        if submitted:
            record = {
                'Revenue': [revenue],
                'Expenses': [expenses],
                'Profit': [profit],
                'Profit Margin %': [profit_margin],
                'Period': [period],
                'Department': [department],
                'Date': [date],
                'Notes': [notes] if notes else ['No notes']
            }
            
            df_new = pd.DataFrame(record)
            
            if 'financial_records' not in st.session_state:
                st.session_state.financial_records = df_new
            else:
                st.session_state.financial_records = pd.concat([st.session_state.financial_records, df_new], ignore_index=True)
            
            st.success("✅ Financial record added!")
            st.rerun()
    
    # Show financial records
    if 'financial_records' in st.session_state:
        st.subheader("📊 Financial Records")
        st.dataframe(st.session_state.financial_records)
        
        # Financial summary
        total_revenue = st.session_state.financial_records['Revenue'].sum()
        total_expenses = st.session_state.financial_records['Expenses'].sum()
        total_profit = st.session_state.financial_records['Profit'].sum()
        avg_margin = st.session_state.financial_records['Profit Margin %'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
        with col2:
            st.metric("💸 Total Expenses", f"${total_expenses:,.2f}")
        with col3:
            st.metric("📈 Total Profit", f"${total_profit:,.2f}")
        with col4:
            st.metric("📊 Avg Margin", f"{avg_margin:.1f}%")
        
        # Download
        if st.button("📥 Download Financial Data"):
            csv = st.session_state.financial_records.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"financial_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    manual_data_input()
