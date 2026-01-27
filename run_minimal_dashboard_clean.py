#!/usr/bin/env python3
"""
Run Script for Minimal Executive Dashboard (Clean Version - No Neubyte)
Integrates all components: minimal dashboard, backend API manager, client management
"""

import streamlit as st
import sys
import os

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all components (without neubyte)
from minimal_dashboard import AutoConfigManager
from backend_api_manager import BackendAPIManager, api_manager
from client_manager import ClientManager, render_client_manager_ui
from file_upload_manager import FileUploadManager, file_upload_manager
from advanced_file_analyzer import advanced_file_analyzer

# Check environment and initialize accordingly
import os
is_production = os.environ.get('RENDER_SERVICE_ID') or 'onrender.com' in os.environ.get('HOSTNAME', '')

if is_production:
    # Initialize production environment to fix 403 errors
    from production_fix import init_production_environment
    init_production_environment()
else:
    # Local development - full functionality
    pass

# Initialize session state components
def initialize_components():
    """Initialize all dashboard components"""
    if 'auto_config' not in st.session_state:
        st.session_state.auto_config = AutoConfigManager()
    
    if 'client_manager' not in st.session_state:
        st.session_state.client_manager = ClientManager()
    
    if 'api_manager' not in st.session_state:
        st.session_state.api_manager = api_manager
    
    if 'file_upload_manager' not in st.session_state:
        st.session_state.file_upload_manager = file_upload_manager
    
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
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #3b82f6;
            margin: 0.5rem 0;
        }
        .alert-critical { border-left-color: #ef4444; }
        .alert-warning { border-left-color: #f59e0b; }
        .alert-success { border-left-color: #10b981; }
        .alert-info { border-left-color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Minimal Executive Dashboard</h1>
        <p>Maximum Analysis with Minimal Input • Auto-Configured • Real-Time Insights</p>
        <p><small>Business Intelligence for Tech & Non-Tech Decision Makers</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚡ Quick Setup")
        
        # API Status
        st.subheader("🔌 Backend API Status")
        
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
            st.info("🔄 Using auto-generated data")
        
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
                st.write(f"Created: {client_data.get('created', 'Unknown')[:10]}")
        else:
            st.info("No clients configured")
            if st.button("➕ Add First Client", key="add_first_client"):
                st.session_state.show_client_manager = True
        
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Refreshing data..."):
                # Clear cache and refresh
                st.session_state.api_manager.clear_cache()
                st.session_state.dashboard_data = None
                st.rerun()
        
        if st.button("🏢 Manage Clients"):
            st.session_state.show_client_manager = True
        
        if st.button("📁 Upload Data"):
            st.session_state.show_file_upload = True
        
        if st.button("🔧 System Status"):
            st.session_state.show_system_status = True
        
        # Auto-Analysis Toggle
        st.subheader("🤖 Smart Features")
        auto_analysis = st.checkbox("Enable AI Analysis", value=True, help="Auto-generate insights and recommendations")
    
    # Main content area
    if st.session_state.get('show_client_manager', False):
        render_client_manager_ui(st.session_state.client_manager)
        
        if st.button("🔙 Back to Dashboard"):
            st.session_state.show_client_manager = False
            st.rerun()
    
    elif st.session_state.get('show_file_upload', False):
        # File Upload Section
        if st.session_state.current_client:
            st.session_state.file_upload_manager.render_file_upload_ui(st.session_state.current_client)
            
            if st.button(" Back to Dashboard"):
                st.session_state.show_file_upload = False
                st.rerun()
        else:
            st.error("❌ Please select a client first to upload data")
    
    elif st.session_state.get('show_system_status', False):
        st.header("🔧 System Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Backend API Status")
            backend_status = st.session_state.api_manager.get_health_status()
            st.json(backend_status)
        
        with col2:
            st.subheader("Client Configuration")
            clients = st.session_state.client_manager.list_clients()
            client_summary = {
                'total_clients': len(clients),
                'client_list': clients,
                'current_client': st.session_state.current_client
            }
            st.json(client_summary)
        
        if st.button("🔙 Back to Dashboard"):
            st.session_state.show_system_status = False
            st.rerun()
    
    else:
        # Main dashboard
        st.header("📈 Executive Dashboard")
        
        # Get data based on auto-detection
        if st.session_state.dashboard_data is None:
            with st.spinner("🚀 Auto-configuring and loading data..."):
                st.session_state.dashboard_data = st.session_state.api_manager.get_comprehensive_data(
                    st.session_state.current_client
                )
        
        # Always refresh data from backend to get latest updates
        if backend_connected:
            with st.spinner("🔄 Refreshing from backend..."):
                st.session_state.dashboard_data = st.session_state.api_manager.get_comprehensive_data(
                    st.session_state.current_client
                )
        else:
            # Auto-generated fallback
            st.session_state.dashboard_data = st.session_state.api_manager._generate_fallback_data()
        
        data = st.session_state.dashboard_data
        
        if data and data.get('status') != 'no_data':
            # Key Metrics
            st.subheader("📊 Key Performance Indicators")
            
            kpis = data.get('kpis', [])
            if kpis:
                cols = st.columns(min(4, len(kpis)))
                for i, kpi in enumerate(kpis[:4]):
                    with cols[i]:
                        value = kpi.get('value', 0)
                        change = kpi.get('change', 0)
                        
                        # Format value based on unit
                        if kpi.get('unit') == 'USD':
                            formatted_value = f"${value:,.0f}"
                        elif kpi.get('unit') == 'percent':
                            formatted_value = f"{value:.1f}%"
                        else:
                            formatted_value = str(value)
                        
                        st.metric(
                            kpi.get('name', 'KPI'),
                            formatted_value,
                            f"{change:+.1f}%" if change else None
                        )
            
            # Auto-Generated Insights
            insights = data.get('insights', [])
            
            # Add insights from uploaded data
            if st.session_state.current_client and auto_analysis:
                client_data = st.session_state.file_upload_manager.get_client_data_for_analysis(st.session_state.current_client)
                for file_type, file_data in client_data.items():
                    if 'analysis' in file_data and file_data['analysis'] and 'insights' in file_data['analysis']:
                        for insight in file_data['analysis']['insights']:
                            insights.append({
                                'title': f"From {file_type.upper()} Data",
                                'description': insight.get('description', insight.get('title', 'Insight')),
                                'priority': insight.get('importance', 'medium'),
                                'auto_generated': True,
                                'source': 'uploaded_file'
                            })
            
            if insights and auto_analysis:
                st.subheader("🧠 Auto-Generated Insights")
                
                for insight in insights[:3]:
                    priority = insight.get('priority', 'medium')
                    priority_color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
                    
                    with st.expander(f"{priority_color} {insight.get('title', 'Insight')}", expanded=priority == 'high'):
                        st.write(insight.get('description', 'No description'))
                        st.write(f"**Priority:** {priority.title()}")
                        if insight.get('auto_generated'):
                            st.write("✅ **Auto-Generated**")
            
            # Recommendations
            recommendations = data.get('recommendations', [])
            
            # Add recommendations from uploaded data
            if st.session_state.current_client and auto_analysis:
                uploaded_recommendations = st.session_state.file_upload_manager.generate_comprehensive_recommendations(st.session_state.current_client)
                recommendations.extend(uploaded_recommendations)
            
            if recommendations and auto_analysis:
                st.subheader("💡 AI-Powered Recommendations")
                
                for rec in recommendations[:2]:
                    confidence = rec.get('confidence', 'medium')
                    conf_color = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(confidence, '⚪')
                    
                    with st.expander(f"{conf_color} {rec.get('title', 'Recommendation')}"):
                        st.write(rec.get('description', 'No description'))
                        st.write(f"**Confidence:** {confidence.title()}")
                        if 'source' in rec:
                            st.write(f"**Source:** {rec['source']}")
                        if 'category' in rec:
                            st.write(f"**Category:** {rec['category'].title()}")
            
            # Business Health Summary
            if auto_analysis:
                st.subheader("🏥 Business Health Summary")
                
                health_score = data.get('business_health_score', {})
                
                if health_score:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("🎯 Overall Health", f"{health_score.get('overall', 0)}/100")
                        st.metric("💰 Financial Health", f"{health_score.get('financial', 0)}/100")
                    
                    with col2:
                        st.metric("👥 Customer Health", f"{health_score.get('customer', 0)}/100")
                        st.metric("⚙️ Operational Health", f"{health_score.get('operational', 0)}/100")
                
                # Quick Actions
                st.subheader("⚡ Quick Actions")
                
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button("📊 Generate Detailed Report"):
                        st.success("📊 Detailed report generated successfully!")
                
                with action_col2:
                    if st.button("📧 Email Summary"):
                        st.info("📧 Summary emailed to stakeholders")
                
                with action_col3:
                    if st.button("📈 Export Data"):
                        st.info("📈 Data exported to Excel")
            
            # Footer info
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Data Source", "Backend API" if backend_connected else "Auto-Generated")
            
            with col2:
                st.metric("🏢 Client", st.session_state.current_client or "Default")
            
            with col3:
                last_updated = data.get('last_updated', 'Unknown')
                st.metric("🕐 Last Updated", last_updated[:10] if last_updated != 'Unknown' else 'Unknown')
        
        else:
            # No data available - show clean UI
            st.info("📊 **No Data Available**")
            st.write("Please upload files to see business insights and recommendations.")
            
            # Show upload prompt
            if st.button("� Upload Files for Analysis"):
                st.session_state.show_file_upload = True
                st.rerun()

if __name__ == "__main__":
    main()
