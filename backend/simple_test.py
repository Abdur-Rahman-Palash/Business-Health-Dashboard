import streamlit as st
import requests

st.title("🧪 Simple Streamlit Test")

st.write("Testing basic Streamlit functionality...")

# Test API connection
try:
    response = requests.get("http://localhost:8001/api/dashboard/kpis", timeout=5)
    if response.status_code == 200:
        st.success("✅ API Connection: SUCCESS")
        st.json(response.json())
    else:
        st.error(f"❌ API Connection: {response.status_code}")
except Exception as e:
    st.error(f"❌ API Error: {e}")

st.write("If you see this page, Streamlit is working!")
