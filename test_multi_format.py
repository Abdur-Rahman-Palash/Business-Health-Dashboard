#!/usr/bin/env python3
"""
Test Multi-Format Processor Directly
"""

import streamlit as st
from multi_format_processor import multi_format_processor

def main():
    st.header("🧪 Test Multi-Format Processor")
    st.write("Testing the multi-format processor directly")
    
    # Call the multi-format processor
    multi_format_processor()

if __name__ == "__main__":
    main()
