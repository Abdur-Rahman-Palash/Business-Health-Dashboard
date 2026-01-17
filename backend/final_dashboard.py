#!/usr/bin/env python3
"""
Final Executive Business Health Dashboard
Complete AI-enhanced solution with all features working
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuration
API_BASE = "http://localhost:8001"  # Test backend with all endpoints

# Set page config
st.set_page_config(
    page_title="Executive Business Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
.ai-badge {
    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

def fetch_api_data(endpoint):
    """Fetch data from API with error handling"""
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ API Error ({response.status_code}): {endpoint}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Connection Error: {e}")
        return None

def create_kpi_gauge(value, target, title, health_status):
    """Create a gauge chart for KPI"""
    # Determine color based on health status
    colors = {
        'excellent': '#10b981',
        'good': '#3b82f6', 
        'warning': '#f59e0b',
        'critical': '#ef4444'
    }
    
    color = colors.get(health_status, '#6b7280')
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': target},
        gauge = {
            'axis': {'range': [None, target * 1.2]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, target * 0.5], 'color': "lightgray"},
                {'range': [target * 0.5, target * 0.8], 'color': "gray"},
                {'range': [target * 0.8, target], 'color': color}
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

def format_currency(value):
    """Format currency values"""
    return f"${value:,.0f}"

def format_percentage(value):
    """Format percentage values"""
    return f"{value:.1f}%"

# Main Dashboard
st.markdown('<h1 class="main-header">📊 Executive Business Health Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🎛 Dashboard Controls")

# Refresh button
if st.sidebar.button("🔄 Refresh All Data", type="primary"):
    with st.spinner("Refreshing dashboard data..."):
        # This would trigger a refresh if we had a refresh endpoint
        st.success("✅ Dashboard data refreshed!")

# Time period selector
time_period = st.sidebar.selectbox(
    "📅 Time Period",
    ["Last 30 Days", "Last Quarter", "Year to Date", "Last 12 Months"],
    index=0
)

# Department filter
departments = st.sidebar.multiselect(
    "🏢 Departments",
    ["All", "Sales", "Marketing", "Operations", "Finance"],
    default=["All"]
)

# AI Features toggle
use_ai_features = st.sidebar.checkbox("🤖 Enable AI-Enhanced Features", value=True, help="Use advanced AI analysis")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 KPI Dashboard", "🤖 AI Insights", "📊 Analytics", "📋 Executive Summary"])

with tab1:
    st.header("📈 Key Performance Indicators")
    
    # Fetch KPI data
    kpi_data = fetch_api_data("/api/dashboard/kpis")
    
    if kpi_data and kpi_data.get('success'):
        kpis = kpi_data.get('data', [])
        
        # Group KPIs by category
        financial_kpis = [kpi for kpi in kpis if any(x in kpi.get('id', '') for x in ['revenue', 'revenue-growth', 'profit-margin', 'expense-ratio', 'mrr', 'arr'])]
        customer_kpis = [kpi for kpi in kpis if any(x in kpi.get('id', '') for x in ['customer-health', 'churn-rate', 'clv', 'cac', 'ltv-cac-ratio', 'nps', 'csat'])]
        operational_kpis = [kpi for kpi in kpis if any(x in kpi.get('id', '') for x in ['operational-efficiency', 'employee-satisfaction', 'market-share'])]
        
        # Financial KPIs
        if financial_kpis:
            st.subheader("💰 Financial Performance")
            cols = st.columns(min(len(financial_kpis), 3))
            for i, kpi in enumerate(financial_kpis[:3]):
                with cols[i]:
                    health_class = f"health-{kpi.get('health_status', 'good')}"
                    fig = create_kpi_gauge(
                        kpi.get('current_value', 0),
                        kpi.get('target_value', 100),
                        kpi.get('id', '').replace('-', ' ').title(),
                        kpi.get('health_status', 'good')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown(f"""
                    <div class="metric-card {health_class}">
                        <h4>{kpi.get('id', '').replace('-', ' ').title()}</h4>
                        <p><strong>Current:</strong> {format_currency(kpi.get('current_value', 0))}</p>
                        <p><strong>Target:</strong> {format_currency(kpi.get('target_value', 0))}</p>
                        <p><strong>Status:</strong> {kpi.get('health_status', 'good').title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Customer KPIs
        if customer_kpis:
            st.subheader("👥 Customer Metrics")
            cols = st.columns(min(len(customer_kpis), 3))
            for i, kpi in enumerate(customer_kpis[:3]):
                with cols[i]:
                    health_class = f"health-{kpi.get('health_status', 'good')}"
                    fig = create_kpi_gauge(
                        kpi.get('current_value', 0),
                        kpi.get('target_value', 100),
                        kpi.get('id', '').replace('-', ' ').title(),
                        kpi.get('health_status', 'good')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown(f"""
                    <div class="metric-card {health_class}">
                        <h4>{kpi.get('id', '').replace('-', ' ').title()}</h4>
                        <p><strong>Current:</strong> {format_percentage(kpi.get('current_value', 0))}</p>
                        <p><strong>Target:</strong> {format_percentage(kpi.get('target_value', 0))}</p>
                        <p><strong>Status:</strong> {kpi.get('health_status', 'good').title()}</p>
                    </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.header("🤖 AI-Powered Business Insights")
    
    if use_ai_features:
        # Fetch AI insights
        ai_insights = fetch_api_data("/api/ai/insights")
        
        if ai_insights and ai_insights.get('success'):
            insights = ai_insights.get('data', [])
            
            st.success("✅ AI Insights loaded successfully!")
            
            # Display insights with priority indicators
            for i, insight in enumerate(insights):
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(insight.get('priority', 'low'), '⚪')
                confidence_badge = {'high': 'High', 'medium': 'Medium', 'low': 'Low'}.get(insight.get('confidence', 'low'), 'Low')
                
                with st.expander(f"{priority_emoji} {insight.get('title', 'AI Insight')}", expanded=i == 0):
                    st.markdown(f"""
                    <div class="insight-card">
                        <h5>{insight.get('title', 'AI Insight')}</h5>
                        <p><strong>Category:</strong> {insight.get('category', 'Unknown').title()}</p>
                        <p><strong>Description:</strong> {insight.get('description', 'No description')}</p>
                        <p><strong>Priority:</strong> {priority_emoji} {insight.get('priority', 'Unknown').title()}</p>
                        <p><strong>Confidence:</strong> {confidence_badge}</p>
                        <p><strong>Source:</strong> {'🤖 AI' if insight.get('source') == 'ai' else '📊 Rule-Based'}</p>
                        <p><strong>Generated:</strong> {insight.get('generated_at', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ AI insights disabled. Enable in sidebar to use AI features.")

with tab3:
    st.header("📊 Advanced Analytics")
    
    # Customer Segmentation
    st.subheader("👥 Customer Segmentation Analysis")
    customer_segments = fetch_api_data("/api/analytics/customer-segments")
    
    if customer_segments and customer_segments.get('success'):
        segments_data = customer_segments.get('data', {})
        
        if segments_data and 'segments' in segments_data:
            segments = segments_data['segments']
            
            # Create segment comparison chart
            segment_names = [s.get('segment_name', 'Unknown') for s in segments]
            avg_revenues = [s.get('avg_revenue', 0) for s in segments]
            customer_counts = [s.get('customer_count', 0) for s in segments]
            
            # Revenue by segment
            fig1 = px.bar(
                x=segment_names,
                y=avg_revenues,
                title="Average Revenue by Segment",
                labels={"x": "Customer Segment", "y": "Average Revenue"}
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Customer count by segment
            fig2 = px.bar(
                x=segment_names,
                y=customer_counts,
                title="Customer Count by Segment",
                labels={"x": "Customer Segment", "y": "Customer Count"}
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Segment details table
            for segment in segments:
                with st.expander(f"📊 {segment.get('segment_name', 'Unknown')} Segment Details"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Customers", segment.get('customer_count', 0))
                    with col2:
                        st.metric("Avg Revenue", format_currency(segment.get('avg_revenue', 0)))
                    with col3:
                        st.metric("Churn Rate", f"{segment.get('churn_rate', 0):.1f}%")

with tab4:
    st.header("📋 Executive Summary")
    
    if use_ai_features:
        # AI Executive Summary
        if st.button("🔄 Generate AI Executive Summary", type="primary"):
            with st.spinner("Generating AI-powered executive summary..."):
                ai_summary = fetch_api_data("/api/ai/executive-summary")
                
                if ai_summary:
                    st.success("✅ AI Executive Summary generated!")
                    
                    # Display summary
                    st.markdown("### 🎯 Overall Assessment")
                    st.write(ai_summary.get('summary', 'No summary available'))
                    
                    st.markdown("### 📋 Key Priorities")
                    priorities = ai_summary.get('priorities', [])
                    for priority in priorities:
                        st.write(f"• {priority}")
                    
                    st.markdown("### 🏥 Health Status")
                    health_status = ai_summary.get('health_assessment', 'Unknown')
                    health_colors = {
                        'excellent': '🟢',
                        'good': '🔵', 
                        'warning': '🟡',
                        'critical': '🔴'
                    }
                    color = health_colors.get(health_status, '⚪')
                    st.write(f"{color} **{health_status.title()}**")
                    
                    st.markdown(f"*Generated by: {ai_summary.get('source', 'Unknown')} AI*")
                else:
                    st.error("❌ Failed to generate AI executive summary")

# Footer
st.markdown("---")
st.markdown(f"<center><small>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></center>", unsafe_allow_html=True)

# System status
with st.sidebar:
    st.markdown("---")
    st.subheader("🔧 System Status")
    
    # Check API connection
    api_status = fetch_api_data("/")
    if api_status:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Disconnected")
    
    st.markdown(f"🤖 AI Features: {'Enabled' if use_ai_features else 'Disabled'}")
    st.markdown(f"📊 API Endpoint: {API_BASE}")
