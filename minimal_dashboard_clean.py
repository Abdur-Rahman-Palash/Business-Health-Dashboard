#!/usr/bin/env python3
"""
Minimal Input, Maximum Analysis Executive Dashboard (Clean Version - No Neubyte)
Auto-inserts backend API data with minimal user configuration required
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import os
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="🚀 Minimal Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# Professional styling
st.markdown("""
<style>
    .minimal-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .auto-badge {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .alert-critical { border-left-color: #ef4444; }
    .alert-warning { border-left-color: #f59e0b; }
    .alert-success { border-left-color: #10b981; }
    .alert-info { border-left-color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# Auto-configuration class (Clean Version)
class AutoConfigManagerClean:
    """Manages automatic backend API configuration and insertion (without neubyte)"""
    
    def __init__(self):
        self.api_endpoints = [
            "https://business-health-dashboard.vercel.app",
            "https://executive-dashboard.vercel.app", 
            "http://localhost:8080",
            "http://localhost:3000"
        ]
        self.client_configs = {}
        self.load_saved_configs()
    
    def load_saved_configs(self):
        """Load saved client configurations"""
        if 'client_configs' in st.session_state:
            self.client_configs = st.session_state.client_configs
    
    def save_configs(self):
        """Save configurations to session state"""
        st.session_state.client_configs = self.client_configs
    
    def auto_detect_api(self) -> str:
        """Auto-detect working API endpoint"""
        for endpoint in self.api_endpoints:
            try:
                response = requests.get(f"{endpoint}/api/health", timeout=5)
                if response.status_code == 200:
                    return endpoint
            except:
                continue
        return None  # Return None if no endpoint works
    
    def get_client_data(self, client_id: str = None) -> Dict:
        """Get client-specific data with auto-insertion"""
        api_url = self.auto_detect_api()
        
        if api_url:
            try:
                # Try to get comprehensive dashboard data
                response = requests.get(f"{api_url}/api/dashboard/complete", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data:
                        return data['data']
                    return data
            except:
                pass
        
        # Fallback to generated data
        return self.generate_minimal_data()
    
    def generate_minimal_data(self) -> Dict:
        """Generate minimal but comprehensive business data"""
        np.random.seed(42)
        
        # Core KPIs
        current_revenue = np.random.normal(850000, 100000)
        prev_revenue = current_revenue * np.random.normal(0.95, 0.05)
        revenue_growth = ((current_revenue - prev_revenue) / prev_revenue) * 100
        
        customers = np.random.randint(800, 1200)
        satisfaction = np.random.normal(78, 8)
        churn_rate = np.random.normal(6, 2)
        profit_margin = np.random.normal(22, 5)
        
        # Calculate health scores
        overall_health = min(100, max(0, 75 + revenue_growth/2 - churn_rate*2 + (satisfaction-75)/2))
        financial_health = min(100, max(0, 80 + revenue_growth/2))
        customer_health = min(100, max(0, 75 + (satisfaction-70) - churn_rate*3))
        operational_health = min(100, max(0, 80 - churn_rate*2))
        
        # Determine status
        if overall_health >= 85:
            status = 'excellent'
        elif overall_health >= 70:
            status = 'good'
        elif overall_health >= 55:
            status = 'warning'
        else:
            status = 'critical'
        
        # Auto-generated insights based on metrics
        insights = []
        if revenue_growth < -5:
            insights.append({
                "title": "Significant Revenue Decline",
                "description": f"Revenue decreased by {abs(revenue_growth):.1f}% - immediate action required",
                "priority": "high",
                "auto_generated": True
            })
        elif revenue_growth < 0:
            insights.append({
                "title": "Revenue Decline Detected",
                "description": f"Revenue decreased by {abs(revenue_growth):.1f}% - monitor closely",
                "priority": "medium",
                "auto_generated": True
            })
        
        if churn_rate > 8:
            insights.append({
                "title": "High Customer Churn",
                "description": f"Churn rate of {churn_rate:.1f}% exceeds acceptable threshold",
                "priority": "high",
                "auto_generated": True
            })
        
        if satisfaction < 70:
            insights.append({
                "title": "Low Customer Satisfaction",
                "description": f"Average satisfaction score of {satisfaction:.1f}% needs improvement",
                "priority": "medium",
                "auto_generated": True
            })
        
        # Auto-generated recommendations
        recommendations = []
        if revenue_growth < 0:
            recommendations.append({
                "title": "Revenue Recovery Plan",
                "description": "Implement immediate sales initiatives and review pricing strategy",
                "confidence": "high",
                "expected_impact": "Revenue increase of 10-15% in 2-3 months",
                "auto_generated": True
            })
        
        if churn_rate > 6:
            recommendations.append({
                "title": "Customer Retention Program",
                "description": "Launch comprehensive customer success and retention initiatives",
                "confidence": "medium",
                "expected_impact": "Reduce churn by 2-3% in 3 months",
                "auto_generated": True
            })
        
        if profit_margin < 20:
            recommendations.append({
                "title": "Profit Margin Optimization",
                "description": "Review cost structure and implement efficiency improvements",
                "confidence": "medium",
                "expected_impact": "Improve margins by 2-4%",
                "auto_generated": True
            })
        
        return {
            'business_health_score': {
                'overall': overall_health,
                'financial': financial_health,
                'customer': customer_health,
                'operational': operational_health,
                'status': status
            },
            'kpis': [
                {
                    "id": "revenue",
                    "name": "Total Revenue",
                    "value": current_revenue,
                    "change": revenue_growth,
                    "trend": "up" if revenue_growth > 0 else "down",
                    "category": "financial",
                    "unit": "USD",
                    "target": 1000000,
                    "status": "excellent" if current_revenue > 900000 else "good" if current_revenue > 700000 else "warning"
                },
                {
                    "id": "customers",
                    "name": "Active Customers",
                    "value": customers,
                    "change": 5.2,
                    "trend": "up",
                    "category": "customer",
                    "unit": "count",
                    "target": 1000,
                    "status": "good" if customers > 900 else "warning"
                },
                {
                    "id": "satisfaction",
                    "name": "Customer Satisfaction",
                    "value": satisfaction,
                    "change": 2.1,
                    "trend": "up",
                    "category": "customer",
                    "unit": "%",
                    "target": 85,
                    "status": "excellent" if satisfaction > 80 else "good" if satisfaction > 70 else "warning"
                },
                {
                    "id": "profit_margin",
                    "name": "Profit Margin",
                    "value": profit_margin,
                    "change": -1.5,
                    "trend": "down",
                    "category": "financial",
                    "unit": "%",
                    "target": 25,
                    "status": "good" if profit_margin > 20 else "warning"
                }
            ],
            'insights': insights,
            'recommendations': recommendations,
            'last_updated': datetime.now().isoformat()
        }

# Initialize auto-config manager
if 'auto_config_clean' not in st.session_state:
    st.session_state.auto_config_clean = AutoConfigManagerClean()

auto_config = st.session_state.auto_config_clean

# Header with auto-status
st.markdown("""
<div class="minimal-header">
    <h1>🚀 Minimal Executive Dashboard</h1>
    <p>Maximum Analysis with Minimal Input • Auto-Configured • Real-Time Insights</p>
    <p><small>Perfect for Tech & Non-Tech Business Decision Makers</small></p>
    <p><span class="auto-badge">AUTO-CONFIGURED</span> <span class="auto-badge">MINIMAL INPUT</span> <span class="auto-badge">MAX ANALYSIS</span></p>
</div>
""", unsafe_allow_html=True)

# Minimal sidebar - auto-configured
with st.sidebar:
    st.header("⚡ Quick Config")
    
    # Auto-detect API status
    api_url = auto_config.auto_detect_api()
    if api_url:
        st.success(f"✅ API Auto-Detected")
        st.info(f"📡 {api_url}")
    else:
        st.warning("⚠️ Using Generated Data")
    
    # Client selection with auto-population
    clients = ["Auto-Detect", "Client A", "Client B", "Client C", "Add New..."]
    selected_client = st.selectbox("🏢 Client", clients, index=0)
    
    if selected_client == "Add New...":
        with st.form("add_client"):
            client_name = st.text_input("Client Name", placeholder="Enter client name")
            if st.form_submit_button("Add Client", type="primary"):
                if client_name:
                    st.success(f"✅ {client_name} added!")
                    st.rerun()
    
    # One-click refresh
    if st.button("🔄 Auto-Refresh Data", type="primary"):
        with st.spinner("Auto-configuring and fetching data..."):
            st.session_state.dashboard_data = auto_config.get_client_data()
            st.success("✅ Data auto-refreshed!")
            st.rerun()
    
    # Auto-analysis toggle
    auto_analysis = st.checkbox("🤖 Auto-Analysis", value=True, help="Enable AI-powered automatic analysis")

# Main dashboard area
if 'dashboard_data' not in st.session_state:
    with st.spinner("🚀 Auto-configuring dashboard..."):
        st.session_state.dashboard_data = auto_config.get_client_data()

data = st.session_state.dashboard_data

# Executive Summary - Auto-generated
st.header("🎯 Executive Summary")

health_score = data.get('business_health_score', {})
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Overall Health",
        f"{health_score.get('overall', 0):.0f}/100",
        delta=None
    )
    status = health_score.get('status', 'good')
    st.markdown(f'<div class="metric-card alert-{status}">Status: {status.title()}</div>', unsafe_allow_html=True)

with col2:
    st.metric("Financial", f"{health_score.get('financial', 0):.0f}/100")

with col3:
    st.metric("Customer", f"{health_score.get('customer', 0):.0f}/100")

with col4:
    st.metric("Operational", f"{health_score.get('operational', 0):.0f}/100")

# Auto-generated KPIs
st.header("📈 Auto-Analyzed KPIs")

kpis = data.get('kpis', [])
if kpis:
    # Auto-categorize and display
    financial_kpis = [kpi for kpi in kpis if kpi.get('category') == 'financial']
    customer_kpis = [kpi for kpi in kpis if kpi.get('category') == 'customer']
    
    # Financial KPIs
    if financial_kpis:
        st.subheader("💰 Financial Performance")
        cols = st.columns(min(len(financial_kpis), 2))
        for i, kpi in enumerate(financial_kpis[:2]):
            with cols[i]:
                value = kpi.get('value', 0)
                change = kpi.get('change', 0)
                status = kpi.get('status', 'good')
                
                st.metric(
                    kpi.get('name', 'KPI'),
                    f"${value:,.0f}" if kpi.get('unit') == 'USD' else f"{value:.1f}%",
                    f"{change:+.1f}%" if change else None
                )
                st.markdown(f'<div class="metric-card alert-{status}">Auto-Status: {status.title()}</div>', unsafe_allow_html=True)
    
    # Customer KPIs
    if customer_kpis:
        st.subheader("👥 Customer Metrics")
        cols = st.columns(min(len(customer_kpis), 2))
        for i, kpi in enumerate(customer_kpis[:2]):
            with cols[i]:
                value = kpi.get('value', 0)
                change = kpi.get('change', 0)
                status = kpi.get('status', 'good')
                
                st.metric(
                    kpi.get('name', 'KPI'),
                    f"{value:,.0f}" if kpi.get('unit') == 'count' else f"{value:.1f}%",
                    f"{change:+.1f}%" if change else None
                )
                st.markdown(f'<div class="metric-card alert-{status}">Auto-Status: {status.title()}</div>', unsafe_allow_html=True)

# Auto-Generated Insights
st.header("🤖 Auto-Generated Insights")

insights = data.get('insights', [])
if insights and auto_analysis:
    for insight in insights[:3]:  # Show top 3
        priority = insight.get('priority', 'medium')
        priority_color = {'high': 'critical', 'medium': 'warning', 'low': 'info'}.get(priority, 'info')
        
        with st.expander(f"🔍 {insight.get('title', 'Insight')}", expanded=priority == 'high'):
            st.write(insight.get('description', 'No description'))
            st.markdown(f'<small><span class="auto-badge">AUTO-GENERATED</span> Priority: {priority.title()}</small>', unsafe_allow_html=True)
else:
    if auto_analysis:
        st.info("🤖 No critical insights detected - Business is performing well!")
    else:
        st.info("ℹ️ Enable Auto-Analysis to see insights")

# Auto-Recommendations
st.header("🎯 Auto-Recommendations")

recommendations = data.get('recommendations', [])
if recommendations and auto_analysis:
    for rec in recommendations[:2]:  # Show top 2
        confidence = rec.get('confidence', 'medium')
        conf_color = {'high': 'success', 'medium': 'warning', 'low': 'info'}.get(confidence, 'info')
        
        with st.expander(f"💡 {rec.get('title', 'Recommendation')}"):
            st.write(rec.get('description', 'No description'))
            if rec.get('expected_impact'):
                st.write(f"**Expected Impact:** {rec['expected_impact']}")
            st.markdown(f'<small><span class="auto-badge">AUTO-GENERATED</span> Confidence: {confidence.title()}</small>', unsafe_allow_html=True)
else:
    if auto_analysis:
        st.info("🎯 No specific recommendations - Continue current strategy")
    else:
        st.info("ℹ️ Enable Auto-Analysis to see recommendations")

# Decision Support Section (if auto-analysis enabled)
if auto_analysis:
    st.header("🎯 Quick Decision Support")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔴 Immediate Actions:**")
        high_priority_insights = [i for i in insights if i.get('priority') == 'high']
        if high_priority_insights:
            for insight in high_priority_insights[:2]:
                st.write(f"• {insight.get('title', 'High Priority')}")
        else:
            st.write("✅ None required")
    
    with col2:
        st.markdown("**🟡 Monitor Closely:**")
        medium_priority_insights = [i for i in insights if i.get('priority') == 'medium']
        if medium_priority_insights:
            for insight in medium_priority_insights[:2]:
                st.write(f"• {insight.get('title', 'Monitor')}")
        else:
            st.write("✅ All stable")
    
    with col3:
        st.markdown("**🟢 Growth Opportunities:**")
        if recommendations:
            for rec in recommendations[:2]:
                st.write(f"• {rec.get('title', 'Opportunity')}")
        else:
            st.write("📊 Focus on optimization")

# Footer with auto-status
st.markdown("---")
last_updated = data.get('last_updated', 'Unknown')
st.markdown(f"<center><small>🚀 Minimal Dashboard • Auto-Configured • Last Updated: {last_updated}</small></center>", unsafe_allow_html=True)

# Auto-status sidebar info
with st.sidebar:
    st.markdown("---")
    st.subheader("🔧 Auto-Status")
    st.success("✅ Auto-Config Active")
    st.info(f"📊 {len(kpis)} KPIs Auto-Analyzed")
    st.info(f"🧠 {len(insights)} Insights Generated")
    st.info(f"💡 {len(recommendations)} Recommendations")
    st.markdown(f"🏢 Client: {selected_client}")
    st.markdown(f"🤖 Auto-Analysis: {'ON' if auto_analysis else 'OFF'}")
    st.markdown(f"📡 API: {'Connected' if api_url else 'Generated'}")
