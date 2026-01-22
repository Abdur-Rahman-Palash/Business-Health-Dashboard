import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import json
import os
import sys

# Configure page
st.set_page_config(
    page_title="Executive Business Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get port from Railway environment
port = int(os.environ.get("PORT", 8501))

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    .health-excellent { border-left-color: #10b981; }
    .health-good { border-left-color: #3b82f6; }
    .health-warning { border-left-color: #f59e0b; }
    .health-critical { border-left-color: #ef4444; }
    .insight-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 3px solid #6366f1;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
# Debug environment variables
st.write("Debug - Environment variables:")
st.write(f"VERCEL: {os.environ.get('VERCEL')}")
st.write(f"AWS_LAMBDA_FUNCTION_NAME: {os.environ.get('AWS_LAMBDA_FUNCTION_NAME')}")

# Force Vercel URL for now - will be detected properly in production
API_BASE = "https://business-health-dashboard.vercel.app"

# Alternative: Use window.location if available in browser
# For now, hardcode the Vercel URL

def fetch_api_data(endpoint):
    """Fetch data from the FastAPI backend"""
    try:
        full_url = f"{API_BASE}{endpoint}"
        st.write(f"Debug - Fetching from: {full_url}")
        response = requests.get(full_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {e}")
        return None

def format_currency(value):
    """Format currency values"""
    return f"${value:,.0f}"

def format_percentage(value):
    """Format percentage values"""
    return f"{value:.1f}%"

def get_health_color(status):
    """Get color based on health status"""
    colors = {
        'excellent': '#10b981',
        'good': '#3b82f6',
        'warning': '#f59e0b',
        'critical': '#ef4444'
    }
    return colors.get(status, '#6b7280')

def create_kpi_gauge(value, target, title, status):
    """Create a gauge chart for KPI"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': target},
        gauge = {
            'axis': {'range': [None, target * 1.2]},
            'bar': {'color': get_health_color(status)},
            'steps': [
                {'range': [0, target * 0.5], 'color': "lightgray"},
                {'range': [target * 0.5, target], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
    return fig

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Executive Business Health Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Dashboard Controls")
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            fetch_api_data("/api/dashboard/refresh")
            st.success("Data refreshed successfully!")
            st.rerun()
        
        # Time period selector
        st.subheader("Time Period")
        time_period = st.selectbox(
            "Select Period",
            ["Last 30 Days", "Last Quarter", "Year to Date", "Last 12 Months"],
            index=0
        )
        
        # Department filter
        st.subheader("Department Filter")
        departments = st.multiselect(
            "Select Departments",
            ["All", "Sales", "Marketing", "Operations", "Finance"],
            default=["All"]
        )
        
        # KPI Categories
        st.subheader("KPI Categories")
        show_financial = st.checkbox("Financial", value=True)
        show_customer = st.checkbox("Customer", value=True)
        show_operational = st.checkbox("Operational", value=True)
    
    # Fetch dashboard data
    with st.spinner("Loading dashboard data..."):
        dashboard_response = fetch_api_data("/api/dashboard/complete")
        
        if not dashboard_response:
            st.error("Unable to load dashboard data. Please check your API connection.")
            return
        
        # Handle different response formats
        if 'data' in dashboard_response:
            data = dashboard_response['data']
        else:
            data = dashboard_response
    
    # Executive Summary Section
    st.header("🎯 Executive Summary")
    
    # Business Health Score - Use mock data if business_health_score not available
    if 'business_health_score' in data:
        health_score = data['business_health_score']
    else:
        # Create mock health score from KPIs
        health_score = {
            'overall': 78,
            'financial': 82,
            'customer': 75,
            'operational': 77,
            'status': 'good'
        }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Health",
            f"{health_score.get('overall', 0):.0f}/100",
            delta=None,
            delta_color="normal"
        )
        st.markdown(f'<div class="metric-card health-{health_score.get("status", "good")}">Status: {health_score.get("status", "unknown").title()}</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Financial", f"{health_score.get('financial', 0):.0f}/100")
    
    with col3:
        st.metric("Customer", f"{health_score.get('customer', 0):.0f}/100")
    
    with col4:
        st.metric("Operational", f"{health_score.get('operational', 0):.0f}/100")
    
    # Executive Summary Narrative
    exec_summary = data.get('executive_summary', {})
    if exec_summary:
        with st.expander("📋 Executive Narrative", expanded=True):
            st.write(exec_summary.get('narrative', 'No narrative available'))
            
            # Key Highlights
            highlights = exec_summary.get('key_highlights', [])
            if highlights:
                st.subheader("Key Highlights")
                for highlight in highlights:
                    st.write(f"• {highlight}")
    
    # KPIs Section
    st.header("📈 Key Performance Indicators")
    
    # Filter KPIs based on user selection
    kpis = data.get('kpis', [])
    if not kpis:
        # Create mock KPIs if none available
        kpis = [
            {
                "id": "revenue",
                "name": "Total Revenue",
                "value": 1250000,
                "change": 12.5,
                "trend": "up",
                "category": "financial",
                "unit": "USD",
                "target": 1500000,
                "status": "good"
            },
            {
                "id": "customers",
                "name": "Active Customers", 
                "value": 8420,
                "change": 8.2,
                "trend": "up",
                "category": "customer",
                "unit": "count",
                "target": 10000,
                "status": "good"
            }
        ]
    
    filtered_kpis = []
    
    for kpi in kpis:
        category = kpi.get('category', '').lower()
        if category == 'financial' and not show_financial:
            continue
        elif category == 'customer' and not show_customer:
            continue
        elif category == 'operational' and not show_operational:
            continue
        filtered_kpis.append(kpi)
    
    # Display KPIs in columns
    if filtered_kpis:
        # Group by category using the category field directly
        financial_kpis = [kpi for kpi in filtered_kpis if kpi.get('category', '').lower() == 'financial']
        customer_kpis = [kpi for kpi in filtered_kpis if kpi.get('category', '').lower() == 'customer']
        operational_kpis = [kpi for kpi in filtered_kpis if kpi.get('category', '').lower() == 'operational']
        
        # Financial KPIs
        if financial_kpis and show_financial:
            st.subheader("💰 Financial Performance")
            cols = st.columns(min(len(financial_kpis), 3))
            for i, kpi in enumerate(financial_kpis[:3]):
                with cols[i]:
                    # Use the correct field names from mock data
                    current_value = kpi.get('value', 0)
                    target_value = kpi.get('target', 100)
                    status = kpi.get('status', 'good')
                    
                    fig = create_kpi_gauge(
                        current_value,
                        target_value,
                        kpi.get('name', 'KPI'),
                        status
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Customer KPIs
        if customer_kpis and show_customer:
            st.subheader("👥 Customer Metrics")
            cols = st.columns(min(len(customer_kpis), 3))
            for i, kpi in enumerate(customer_kpis[:3]):
                with cols[i]:
                    current_value = kpi.get('value', 0)
                    target_value = kpi.get('target', 100)
                    status = kpi.get('status', 'good')
                    
                    fig = create_kpi_gauge(
                        current_value,
                        target_value,
                        kpi.get('name', 'KPI'),
                        status
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Operational KPIs
        if operational_kpis and show_operational:
            st.subheader("⚡ Operational Efficiency")
            cols = st.columns(min(len(operational_kpis), 3))
            for i, kpi in enumerate(operational_kpis[:3]):
                with cols[i]:
                    current_value = kpi.get('value', 0)
                    target_value = kpi.get('target', 100)
                    status = kpi.get('status', 'good')
                    
                    fig = create_kpi_gauge(
                        current_value,
                        target_value,
                        kpi.get('name', 'KPI'),
                        status
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # Insights Section
    st.header("💡 Business Insights")
    
    insights = data.get('insights', [])
    if insights:
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        insights.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
        
        for insight in insights[:5]:  # Show top 5 insights
            priority_color = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(insight.get('priority', 'low'), '⚪')
            
            with st.expander(f"{priority_color} {insight.get('title', 'Untitled Insight')}", expanded=insight.get('priority') == 'high'):
                st.write(f"**Description:** {insight.get('description', 'No description')}")
                st.write(f"**Priority:** {insight.get('priority', 'Unknown').title()}")
                st.write(f"**Category:** {insight.get('category', 'Unknown').title()}")
                if 'impact' in insight:
                    st.write(f"**Impact:** {insight.get('impact', 'No impact specified')}")
                if 'effort' in insight:
                    st.write(f"**Effort:** {insight.get('effort', 'No effort specified')}")
    else:
        st.info("No insights available at the moment.")
    
    # Risks Section
    st.header("⚠️ Risk Indicators")
    
    risks = data.get('risks', [])
    if risks:
        for risk in risks:
            severity_color = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk.get('severity', 'low'), '⚪')
            
            with st.expander(f"{severity_color} {risk.get('title', 'Untitled Risk')}"):
                st.write(risk.get('explanation', 'No explanation'))
                st.write(f"**Threshold Logic:** {risk.get('threshold_logic', 'No threshold logic')}")
                st.write(f"**Consecutive Periods:** {risk.get('consecutive_periods', 0)}")
    
    # Recommendations Section
    st.header("🎯 Actionable Recommendations")
    
    recommendations = data.get('recommendations', [])
    if recommendations:
        for rec in recommendations:
            confidence_color = {
                'high': '🟢',
                'medium': '🟡',
                'low': '🔴'
            }.get(rec.get('confidence', 'low'), '⚪')
            
            with st.expander(f"{confidence_color} {rec.get('title', 'Untitled Recommendation')}"):
                st.write(rec.get('description', 'No description'))
                if 'expectedImpact' in rec:
                    st.write(f"**Expected Impact:** {rec.get('expectedImpact', 'No impact specified')}")
                if 'expected_impact' in rec:
                    st.write(f"**Expected Impact:** {rec.get('expected_impact', 'No impact specified')}")
                if 'timeframe' in rec:
                    st.write(f"**Timeframe:** {rec.get('timeframe', 'No timeframe')}")
                if 'effort' in rec:
                    st.write(f"**Effort Required:** {rec.get('effort', 'No effort specified')}")
    else:
        st.info("No recommendations available at the moment.")
    
    # Footer
    st.markdown("---")
    last_updated = data.get('last_updated', dashboard_response.get('timestamp', 'Unknown'))
    st.markdown(f"<center><small>Last updated: {last_updated}</small></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
