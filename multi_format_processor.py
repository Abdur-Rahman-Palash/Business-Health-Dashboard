#!/usr/bin/env python3
"""
Multi-Format Data Processor - Support CSV, PDF, TXT, JSON, XML, Excel
Complete solution without file upload - text-based input for all formats
"""

import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime
import io
import base64

def multi_format_processor():
    """Complete multi-format data processor without file upload"""
    
    st.header("📊 Multi-Format Data Processor")
    st.write("Process CSV, PDF, TXT, JSON, XML, Excel data without file upload")
    st.success("✅ All Formats Supported - No Upload Required!")
    
    # Format selection
    format_type = st.selectbox(
        "Select Data Format:",
        ["📊 CSV Data", "📄 PDF Text", "📝 TXT Text", "🔧 JSON Data", "📋 XML Data", "📈 Excel Data"]
    )
    
    if format_type == "📊 CSV Data":
        process_csv_format()
    elif format_type == "📄 PDF Text":
        process_pdf_format()
    elif format_type == "📝 TXT Text":
        process_txt_format()
    elif format_type == "🔧 JSON Data":
        process_json_format()
    elif format_type == "📋 XML Data":
        process_xml_format()
    elif format_type == "📈 Excel Data":
        process_excel_format()

def process_csv_format():
    """Process CSV format data"""
    st.subheader("📊 CSV Data Processor")
    
    # CSV input options
    input_method = st.radio("Input Method:", ["📝 Manual Entry", "📋 Paste CSV Data", "🔧 Template Based"])
    
    if input_method == "📝 Manual Entry":
        manual_csv_entry()
    elif input_method == "📋 Paste CSV Data":
        paste_csv_data()
    elif input_method == "🔧 Template Based":
        template_csv_entry()

def manual_csv_entry():
    """Manual CSV data entry"""
    st.write("**Enter CSV Data Manually:**")
    
    # Define columns
    headers = st.text_input("Headers (comma-separated):", 
                           value="Name,Category,Amount,Date,Status",
                           help="e.g., Name,Category,Amount,Date,Status")
    
    num_rows = st.number_input("Number of rows:", min_value=1, max_value=20, value=5)
    
    data_rows = []
    for i in range(num_rows):
        with st.expander(f"Row {i+1}"):
            cols = st.columns(len(headers.split(',')))
            row_data = []
            
            for j, header in enumerate(headers.split(',')):
                if j < len(cols):
                    header_clean = header.strip()
                    if 'Amount' in header_clean or 'Price' in header_clean or 'Value' in header_clean:
                        value = cols[j].number_input(f"{header_clean} {i+1}:", value=0.0, key=f"csv_row_{i}_col_{j}")
                    elif 'Date' in header_clean:
                        value = cols[j].date_input(f"{header_clean} {i+1}:", key=f"csv_row_{i}_col_{j}")
                    elif 'Status' in header_clean:
                        value = cols[j].selectbox(f"{header_clean} {i+1}:", ["Active", "Inactive", "Pending", "Completed"], key=f"csv_row_{i}_col_{j}")
                    else:
                        value = cols[j].text_input(f"{header_clean} {i+1}:", key=f"csv_row_{i}_col_{j}")
                    row_data.append(value)
            
            data_rows.append(row_data)
    
    if st.button("📊 Generate CSV"):
        try:
            df = pd.DataFrame(data_rows, columns=[h.strip() for h in headers.split(',')])
            st.session_state.processed_data = df
            st.success(f"✅ CSV generated with {len(df)} rows!")
            st.dataframe(df)
            
            # Statistics
            st.subheader("📈 CSV Statistics")
            st.write(df.describe())
            
            # Download
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"generated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def paste_csv_data():
    """Paste CSV data directly"""
    st.write("**Paste your CSV data:**")
    
    csv_text = st.text_area(
        "Paste CSV data here:",
        height=200,
        placeholder="Name,Category,Amount,Date,Status\nProduct A,Sales,1500.00,2024-01-15,Active\nService B,Service,800.00,2024-01-16,Pending"
    )
    
    if st.button("📊 Process CSV Data"):
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(csv_text))
            st.session_state.processed_data = df
            st.success(f"✅ CSV processed with {len(df)} rows!")
            st.dataframe(df)
            
            # Statistics
            st.subheader("📈 Data Statistics")
            st.write(df.describe())
            
            # Download
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Processed CSV",
                data=csv_data,
                file_name=f"processed_csv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error processing CSV: {str(e)}")

def template_csv_entry():
    """Template-based CSV entry"""
    st.write("**Use predefined templates:**")
    
    template_type = st.selectbox("Choose Template:", 
                                ["📈 Sales Data", "💰 Financial Data", "👥 Employee Data"])
    
    if template_type == "📈 Sales Data":
        sales_template()
    elif template_type == "💰 Financial Data":
        financial_template()
    elif template_type == "👥 Employee Data":
        employee_template()

def sales_template():
    """Sales data template"""
    st.write("**Sales Data Entry:**")
    
    num_sales = st.number_input("Number of sales records:", min_value=1, max_value=10, value=3)
    
    sales_data = []
    for i in range(num_sales):
        with st.expander(f"Sale {i+1}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                product = col1.text_input(f"Product Name {i+1}:", key=f"sales_product_{i}")
            with col2:
                amount = col2.number_input(f"Amount ${i+1}:", value=0.0, key=f"sales_amount_{i}")
            with col3:
                date = col3.date_input(f"Date {i+1}:", key=f"sales_date_{i}")
            with col4:
                status = col4.selectbox(f"Status {i+1}:", ["Completed", "Pending", "Cancelled"], key=f"sales_status_{i}")
            
            sales_data.append([product, amount, date, status])
    
    if st.button("📊 Generate Sales CSV"):
        df = pd.DataFrame(sales_data, columns=["Product", "Amount", "Date", "Status"])
        st.session_state.processed_data = df
        st.success(f"✅ Sales CSV generated!")
        st.dataframe(df)
        
        # Summary
        total_sales = df["Amount"].sum()
        st.metric("💰 Total Sales", f"${total_sales:,.2f}")
        
        # Download
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sales CSV",
            data=csv_data,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def financial_template():
    """Financial data template"""
    st.write("**Financial Data Entry:**")
    
    num_records = st.number_input("Number of financial records:", min_value=1, max_value=10, value=3)
    
    financial_data = []
    for i in range(num_records):
        with st.expander(f"Financial Record {i+1}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                category = col1.selectbox(f"Category {i+1}:", ["Revenue", "Expenses", "Profit", "Investment"], key=f"fin_category_{i}")
            with col2:
                amount = col2.number_input(f"Amount ${i+1}:", value=0.0, key=f"fin_amount_{i}")
            with col3:
                period = col3.selectbox(f"Period {i+1}:", ["Monthly", "Quarterly", "Yearly"], key=f"fin_period_{i}")
            with col4:
                date = col4.date_input(f"Date {i+1}:", key=f"fin_date_{i}")
            
            financial_data.append([category, amount, period, date])
    
    if st.button("📊 Generate Financial CSV"):
        df = pd.DataFrame(financial_data, columns=["Category", "Amount", "Period", "Date"])
        st.session_state.processed_data = df
        st.success(f"✅ Financial CSV generated!")
        st.dataframe(df)
        
        # Summary
        total_revenue = df[df["Category"] == "Revenue"]["Amount"].sum()
        total_expenses = df[df["Category"] == "Expenses"]["Amount"].sum()
        net_profit = total_revenue - total_expenses
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
        with col2:
            st.metric("💸 Total Expenses", f"${total_expenses:,.2f}")
        with col3:
            st.metric("📈 Net Profit", f"${net_profit:,.2f}")
        
        # Download
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Financial CSV",
            data=csv_data,
            file_name=f"financial_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def employee_template():
    """Employee data template"""
    st.write("**Employee Data Entry:**")
    
    num_employees = st.number_input("Number of employees:", min_value=1, max_value=10, value=3)
    
    employee_data = []
    for i in range(num_employees):
        with st.expander(f"Employee {i+1}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                name = col1.text_input(f"Name {i+1}:", key=f"emp_name_{i}")
            with col2:
                department = col2.selectbox(f"Department {i+1}:", ["Sales", "Marketing", "IT", "HR", "Finance"], key=f"emp_dept_{i}")
            with col3:
                salary = col3.number_input(f"Salary ${i+1}:", value=0.0, key=f"emp_salary_{i}")
            with col4:
                status = col4.selectbox(f"Status {i+1}:", ["Active", "On Leave", "Terminated"], key=f"emp_status_{i}")
            
            employee_data.append([name, department, salary, status])
    
    if st.button("📊 Generate Employee CSV"):
        df = pd.DataFrame(employee_data, columns=["Name", "Department", "Salary", "Status"])
        st.session_state.processed_data = df
        st.success(f"✅ Employee CSV generated!")
        st.dataframe(df)
        
        # Summary
        total_salary = df["Salary"].sum()
        avg_salary = df["Salary"].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Total Salary", f"${total_salary:,.2f}")
        with col2:
            st.metric("📊 Average Salary", f"${avg_salary:,.2f}")
        
        # Department breakdown
        st.subheader("📋 Department Breakdown")
        dept_counts = df["Department"].value_counts()
        st.bar_chart(dept_counts)
        
        # Download
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Employee CSV",
            data=csv_data,
            file_name=f"employee_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def process_pdf_format():
    """Process PDF format (text-based)"""
    st.subheader("📄 PDF Text Processor")
    st.write("Enter PDF content as text (copy-paste from PDF):")
    
    pdf_text = st.text_area(
        "Paste PDF content here:",
        height=300,
        placeholder="Paste text content from your PDF file here..."
    )
    
    if pdf_text:
        st.success(f"✅ PDF text processed! Character count: {len(pdf_text)}")
        
        # Text analysis
        st.subheader("📊 Text Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Characters", len(pdf_text))
        with col2:
            st.metric("📄 Words", len(pdf_text.split()))
        with col3:
            st.metric("📋 Lines", len(pdf_text.splitlines()))
        
        # Extract key information
        st.subheader("🔍 Extracted Information")
        
        # Find numbers (amounts, dates, etc.)
        numbers = re.findall(r'\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?', pdf_text)
        if numbers:
            st.write("**Found Numbers/Amounts:**")
            st.write(numbers[:10])  # Show first 10
        
        # Find dates
        dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', pdf_text)
        if dates:
            st.write("**Found Dates:**")
            st.write(dates[:10])  # Show first 10
        
        # Text preview
        st.subheader("📋 Text Preview")
        st.text_area("PDF Content", pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text, height=200)

def process_txt_format():
    """Process TXT format"""
    st.subheader("📝 TXT Text Processor")
    
    txt_text = st.text_area(
        "Enter your text data:",
        height=250,
        placeholder="Enter your text content here..."
    )
    
    if txt_text:
        st.success(f"✅ Text processed! Character count: {len(txt_text)}")
        
        # Text analysis
        st.subheader("📊 Text Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Characters", len(txt_text))
        with col2:
            st.metric("📄 Words", len(txt_text.split()))
        with col3:
            st.metric("📋 Lines", len(txt_text.splitlines()))
        with col4:
            st.metric("📊 Paragraphs", len(txt_text.split('\n\n')))
        
        # Word frequency
        words = txt_text.lower().split()
        word_freq = {}
        for word in words:
            word = re.sub(r'[^\w]', '', word)
            if word and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        if word_freq:
            st.subheader("🔤 Top Words")
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            for word, count in top_words:
                st.write(f"• {word}: {count}")
        
        # Text preview
        st.subheader("📋 Text Preview")
        st.text_area("Text Content", txt_text[:1000] + "..." if len(txt_text) > 1000 else txt_text, height=200)

def process_json_format():
    """Process JSON format"""
    st.subheader("🔧 JSON Data Processor")
    
    json_input_method = st.radio("Input Method:", ["📝 Manual JSON Builder", "📋 Paste JSON Data"])
    
    if json_input_method == "📝 Manual JSON Builder":
        manual_json_builder()
    elif json_input_method == "📋 Paste JSON Data":
        paste_json_data()

def manual_json_builder():
    """Manual JSON data builder"""
    st.write("**Build JSON data manually:**")
    
    json_type = st.selectbox("JSON Structure Type:", 
                             ["📊 Simple Object", "📋 Array of Objects"])
    
    if json_type == "📊 Simple Object":
        simple_json_builder()
    elif json_type == "📋 Array of Objects":
        array_json_builder()

def simple_json_builder():
    """Build simple JSON object"""
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name:")
        value = st.text_input("Value:")
        category = st.selectbox("Category:", ["Data", "Config", "Settings", "Info"])
        active = st.checkbox("Active:")
    
    with col2:
        description = st.text_area("Description:")
        priority = st.selectbox("Priority:", ["Low", "Medium", "High"])
        tags = st.text_input("Tags (comma-separated):")
    
    if st.button("🔧 Build JSON"):
        json_data = {
            "name": name,
            "value": value,
            "category": category,
            "active": active,
            "description": description,
            "priority": priority,
            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
            "created_at": datetime.now().isoformat()
        }
        
        st.session_state.json_data = json_data
        st.success("✅ JSON object created!")
        
        # Display JSON
        st.subheader("📋 Generated JSON")
        st.json(json_data)
        
        # Download
        json_str = json.dumps(json_data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"simple_json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def array_json_builder():
    """Build array of JSON objects"""
    st.write("**Build array of JSON objects:**")
    
    num_objects = st.number_input("Number of objects:", min_value=1, max_value=5, value=3)
    
    json_array = []
    for i in range(num_objects):
        with st.expander(f"Object {i+1}"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(f"Name {i+1}:", key=f"arr_name_{i}")
                value = st.number_input(f"Value {i+1}:", value=0.0, key=f"arr_value_{i}")
                status = st.selectbox(f"Status {i+1}:", ["Active", "Inactive", "Pending"], key=f"arr_status_{i}")
            
            with col2:
                category = st.selectbox(f"Category {i+1}:", ["A", "B", "C"], key=f"arr_category_{i}")
                priority = st.selectbox(f"Priority {i+1}:", ["Low", "Medium", "High"], key=f"arr_priority_{i}")
                notes = st.text_area(f"Notes {i+1}:", key=f"arr_notes_{i}")
            
            json_array.append({
                "name": name,
                "value": value,
                "status": status,
                "category": category,
                "priority": priority,
                "notes": notes,
                "created_at": datetime.now().isoformat()
            })
    
    if st.button("🔧 Build JSON Array"):
        st.session_state.json_array = json_array
        st.success(f"✅ JSON array created with {len(json_array)} objects!")
        
        # Display JSON
        st.subheader("📋 Generated JSON Array")
        st.json(json_array)
        
        # Download
        json_str = json.dumps(json_array, indent=2)
        st.download_button(
            label="📥 Download JSON Array",
            data=json_str,
            file_name=f"json_array_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def paste_json_data():
    """Paste JSON data directly"""
    st.write("**Paste your JSON data:**")
    
    json_text = st.text_area(
        "Paste JSON data here:",
        height=250,
        placeholder='{"name": "example", "value": 123, "active": true}'
    )
    
    if st.button("🔧 Process JSON"):
        try:
            json_data = json.loads(json_text)
            st.session_state.json_data = json_data
            st.success("✅ JSON processed successfully!")
            
            # Display JSON
            st.subheader("📋 Processed JSON")
            st.json(json_data)
            
            # Download
            json_str = json.dumps(json_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"processed_json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid JSON: {str(e)}")

def process_xml_format():
    """Process XML format"""
    st.subheader("📋 XML Data Processor")
    
    xml_input_method = st.radio("Input Method:", ["📝 Manual XML Builder", "📋 Paste XML Data"])
    
    if xml_input_method == "📝 Manual XML Builder":
        manual_xml_builder()
    elif xml_input_method == "📋 Paste XML Data":
        paste_xml_data()

def manual_xml_builder():
    """Manual XML builder"""
    st.write("**Build XML data manually:**")
    
    root_element = st.text_input("Root Element Name:", value="data")
    element_name = st.text_input("Element Name:", value="item")
    element_value = st.text_input("Element Value:")
    attribute_name = st.text_input("Attribute Name:")
    attribute_value = st.text_input("Attribute Value:")
    
    if st.button("📋 Build XML"):
        # Build XML string
        xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += f'<{root_element}>\n'
        
        if attribute_name and attribute_value:
            xml_content += f'  <{element_name} {attribute_name}="{attribute_value}">{element_value}</{element_name}>\n'
        else:
            xml_content += f'  <{element_name}>{element_value}</{element_name}>\n'
        
        xml_content += f'</{root_element}>'
        
        st.session_state.xml_data = xml_content
        st.success("✅ XML created!")
        
        # Display XML
        st.subheader("📋 Generated XML")
        st.code(xml_content, language='xml')
        
        # Download
        st.download_button(
            label="📥 Download XML",
            data=xml_content,
            file_name=f"generated_xml_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
            mime="application/xml"
        )

def paste_xml_data():
    """Paste XML data directly"""
    st.write("**Paste your XML data:**")
    
    xml_text = st.text_area(
        "Paste XML data here:",
        height=250,
        placeholder='<?xml version="1.0" encoding="UTF-8"?>\n<data>\n  <item>Example</item>\n</data>'
    )
    
    if st.button("📋 Process XML"):
        st.session_state.xml_data = xml_text
        st.success("✅ XML processed!")
        
        # Display XML
        st.subheader("📋 Processed XML")
        st.code(xml_text, language='xml')
        
        # Download
        st.download_button(
            label="📥 Download XML",
            data=xml_text,
            file_name=f"processed_xml_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
            mime="application/xml"
        )

def process_excel_format():
    """Process Excel format (CSV-based)"""
    st.subheader("📈 Excel Data Processor")
    st.write("Process Excel-like data (tab-separated values):")
    
    excel_text = st.text_area(
        "Paste Excel-like data (tab-separated):",
        height=200,
        placeholder="Name\tAge\tSalary\nJohn\t25\t50000\nJane\t30\t60000"
    )
    
    if st.button("📈 Process Excel Data"):
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(excel_text), sep='\t')
            st.session_state.processed_data = df
            st.success(f"✅ Excel-like data processed with {len(df)} rows!")
            st.dataframe(df)
            
            # Statistics
            st.subheader("📈 Data Statistics")
            st.write(df.describe())
            
            # Download as CSV (Excel compatible)
            csv_data = df.to_csv(index=False, sep='\t')
            st.download_button(
                label="📥 Download Excel-Compatible CSV",
                data=csv_data,
                file_name=f"excel_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error processing Excel data: {str(e)}")

if __name__ == "__main__":
    multi_format_processor()
