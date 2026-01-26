#!/usr/bin/env python3
"""
Run Script for Minimal Executive Dashboard
Integrates all components: minimal dashboard, backend API manager, client management, and neubyte.tech
"""

import streamlit as st
import sys
import os

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all components
from minimal_dashboard import AutoConfigManager
from backend_api_manager import BackendAPIManager, api_manager
from client_manager import ClientManager, render_client_manager_ui
from neubyte_integration import NeubyteIntegration, neubyte_integration

# Page configuration
st.set_page_config(
    page_title="🚀 Minimal Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize session state components
def initialize_components():
    """Initialize all dashboard components"""
    if 'auto_config' not in st.session_state:
        st.session_state.auto_config = AutoConfigManager()
    
    if 'client_manager' not in st.session_state:
        st.session_state.client_manager = ClientManager()
    
    if 'api_manager' not in st.session_state:
        st.session_state.api_manager = api_manager
    
    if 'neubyte_integration' not in st.session_state:
        st.session_state.neubyte_integration = neubyte_integration
    
    if 'current_client' not in st.session_state:
        st.session_state.current_client = None
    
    if 'dashboard_data' not in st.session_state:
        st.session_state.dashboard_data = None

# Main application
def main():
    """Main dashboard application"""
    initialize_components()
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 0.5rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-connected { background-color: #10b981; }
        .status-disconnected { background-color: #ef4444; }
        .status-warning { background-color: #f59e0b; }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Minimal Executive Dashboard</h1>
        <p>Maximum Analysis with Minimal Input • Auto-Configured • Real-Time Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚡ Quick Setup")
        
        # API Status
        st.subheader("🔌 API Status")
        
        # Backend API Status
        backend_status = st.session_state.api_manager.get_health_status()
        backend_connected = backend_status.get('primary_endpoint') is not None
        
        st.markdown(f"""
        <div>
            <span class="status-indicator {'status-connected' if backend_connected else 'status-disconnected'}"></span>
            Backend API: {'Connected' if backend_connected else 'Disconnected'}
        </div>
        """, unsafe_allow_html=True)
        
        if backend_connected:
            st.success(f"✅ {backend_status['primary_endpoint']}")
        else:
            st.error("❌ No backend API detected")
        
        # Neubyte.tech Status
        neubyte_status = st.session_state.neubyte_integration.get_connection_status()
        neubyte_connected = neubyte_status.get('connected', False)
        
        st.markdown(f"""
        <div>
            <span class="status-indicator {'status-connected' if neubyte_connected else 'status-disconnected'}"></span>
            Neubyte.tech: {'Connected' if neubyte_connected else 'Disconnected'}
        </div>
        """, unsafe_allow_html=True)
        
        if neubyte_connected:
            st.success(f"✅ Latency: {neubyte_status.get('latency', 0):.0f}ms")
        else:
            st.warning("⚠️ Not configured")
        
        # Client Selection
        st.subheader("🏢 Client Management")
        clients = st.session_state.client_manager.list_clients()
        
        if clients:
            client_options = ["Select Client..."] + clients
            selected_client = st.selectbox("Choose Client", client_options)
            
            if selected_client != "Select Client...":
                st.session_state.current_client = selected_client
                client_data = st.session_state.client_manager.get_client(selected_client)
                
                st.success(f"✅ {selected_client}")
                st.write(f"Industry: {client_data.get('industry', 'General')}")
                
                # Configure neubyte if API key exists
                api_key = client_data.get('api_key')
                if api_key and not neubyte_connected:
                    if st.button("🔗 Connect Neubyte.tech", key="connect_neubyte"):
                        if st.session_state.neubyte_integration.configure(api_key):
                            st.success("✅ Neubyte.tech connected!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to connect to Neubyte.tech")
        else:
            st.info("No clients configured")
            if st.button("➕ Add First Client", key="add_first_client"):
                st.session_state.show_client_manager = True
        
        # Data Source Selection
        st.subheader("📊 Data Source")
        
        data_sources = []
        if backend_connected:
            data_sources.append("Backend API")
        if neubyte_connected:
            data_sources.append("Neubyte.tech")
        data_sources.append("Auto-Generated")
        
        data_source = st.selectbox("Select Data Source", data_sources)
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Refreshing data..."):
                # Clear cache and refresh
                st.session_state.api_manager.clear_cache()
                st.session_state.neubyte_integration.clear_cache()
                st.session_state.dashboard_data = None
                st.rerun()
        
        if st.button("🏢 Manage Clients"):
            st.session_state.show_client_manager = True
        
        if st.button("🔧 System Status"):
            st.session_state.show_system_status = True
    
    # Main content area
    if st.session_state.get('show_client_manager', False):
        render_client_manager_ui(st.session_state.client_manager)
        
        if st.button("🔙 Back to Dashboard"):
            st.session_state.show_client_manager = False
            st.rerun()
    
    elif st.session_state.get('show_system_status', False):
        st.header("🔧 System Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Backend API Status")
            backend_status = st.session_state.api_manager.get_health_status()
            st.json(backend_status)
        
        with col2:
            st.subheader("Neubyte.tech Status")
            neubyte_status = st.session_state.neubyte_integration.get_connection_status()
            st.json(neubyte_status)
        
        if st.button("🔙 Back to Dashboard"):
            st.session_state.show_system_status = False
            st.rerun()
    
    else:
        # Main dashboard
        st.header("📈 Executive Dashboard")
        
        # Get data based on selected source
        if st.session_state.dashboard_data is None:
            with st.spinner("🚀 Auto-configuring and loading data..."):
                if data_source == "Backend API" and backend_connected:
                    st.session_state.dashboard_data = st.session_state.api_manager.get_comprehensive_data(
                        st.session_state.current_client
                    )
                elif data_source == "Neubyte.tech" and neubyte_connected:
                    st.session_state.dashboard_data = st.session_state.neubyte_integration.get_business_metrics()
                else:
                    # Auto-generated fallback
                    st.session_state.dashboard_data = st.session_state.api_manager._generate_fallback_data()
        
        data = st.session_state.dashboard_data
        
        if data:
            # Executive Summary
            st.subheader("🎯 Executive Summary")
            
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
            
            # KPIs
            st.subheader("📊 Key Performance Indicators")
            
            kpis = data.get('kpis', [])
            if kpis:
                cols = st.columns(min(len(kpis), 4))
                for i, kpi in enumerate(kpis[:4]):
                    with cols[i]:
                        value = kpi.get('value', 0)
                        change = kpi.get('change', 0)
                        unit = kpi.get('unit', '')
                        
                        if unit == 'USD':
                            formatted_value = f"${value:,.0f}"
                        elif unit == '%':
                            formatted_value = f"{value:.1f}%"
                        elif unit == 'count':
                            formatted_value = f"{value:,.0f}"
                        else:
                            formatted_value = str(value)
                        
                        st.metric(
                            kpi.get('name', 'KPI'),
                            formatted_value,
                            f"{change:+.1f}%" if change else None
                        )
            
            # Insights
            insights = data.get('insights', [])
            if insights:
                st.subheader("🧠 Insights")
                
                for insight in insights[:3]:
                    priority = insight.get('priority', 'medium')
                    priority_color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
                    
                    with st.expander(f"{priority_color} {insight.get('title', 'Insight')}"):
                        st.write(insight.get('description', 'No description'))
                        st.write(f"**Priority:** {priority.title()}")
                        if insight.get('data_source'):
                            st.write(f"**Source:** {insight['data_source']}")
            
            # Recommendations
            recommendations = data.get('recommendations', [])
            if recommendations:
                st.subheader("💡 Recommendations")
                
                for rec in recommendations[:2]:
                    confidence = rec.get('confidence', 'medium')
                    conf_color = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(confidence, '⚪')
                    
                    with st.expander(f"{conf_color} {rec.get('title', 'Recommendation')}"):
                        st.write(rec.get('description', 'No description'))
                        st.write(f"**Confidence:** {confidence.title()}")
                        if rec.get('expected_impact'):
                            st.write(f"**Expected Impact:** {rec['expected_impact']}")
            
            # Data source info
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Data Source", data_source)
            
            with col2:
                st.metric("🏢 Client", st.session_state.current_client or "Default")
            
            with col3:
                last_updated = data.get('last_updated', 'Unknown')
                st.metric("🕐 Last Updated", last_updated[:10] if last_updated != 'Unknown' else 'Unknown')
        
        else:
            st.error("❌ Failed to load dashboard data")
            if st.button("🔄 Retry"):
                st.session_state.dashboard_data = None
                st.rerun()

if __name__ == "__main__":
    main()
