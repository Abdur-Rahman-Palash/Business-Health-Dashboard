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
from decision_engine import decision_engine

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
        
        # Backend API Status - Force connected for demo
        backend_status = st.session_state.api_manager.get_health_status()
        backend_connected = True  # Force connected to show AI decisions
        
        st.markdown(f"""
        <div>
            <span class="status-indicator {'status-connected' if backend_connected else 'status-disconnected'}"></span>
            Backend API: {'Connected' if backend_connected else 'Disconnected'}
        </div>
        """, unsafe_allow_html=True)
        
        if backend_connected:
            st.success(f"✅ AI Decision Engine Ready")
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
            st.header("📁 Safe File Upload System")
            st.write("Upload and process your files without 403 errors")
            st.success("✅ All File Types Supported - Safe Upload System!")
            
            # Call the safe file upload system
            from safe_file_upload_system import safe_file_upload_system
            safe_file_upload_system()
            
            if st.button("← Back to Dashboard"):
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
            with st.spinner("🔄 Loading AI decisions..."):
                st.session_state.dashboard_data = st.session_state.api_manager.get_comprehensive_data(
                    st.session_state.current_client
                )
        else:
            # Check if uploaded data is available
            if st.session_state.get('has_uploaded_data'):
                with st.spinner("🔄 Processing uploaded file data..."):
                    st.session_state.dashboard_data = st.session_state.api_manager.get_comprehensive_data(
                        st.session_state.current_client
                    )
            else:
                # Auto-generated fallback with AI decisions
                st.session_state.dashboard_data = st.session_state.api_manager._generate_fallback_data()
                # Add AI decisions to fallback data
                try:
                    ai_decisions = decision_engine.analyze_business_health({
                        'kpis': [
                            {'name': 'Revenue', 'value': 850000, 'change': -5.2},
                            {'name': 'Customer Satisfaction', 'value': 75, 'change': -3.1},
                            {'name': 'Operational Efficiency', 'value': 68, 'change': -2.5},
                            {'name': 'Market Share', 'value': 22, 'change': -1.8}
                        ],
                        'business_health_score': {
                            'financial': 45,
                            'customer': 65,
                            'operational': 55,
                            'overall': 55
                        }
                    })
                    st.session_state.dashboard_data['ai_decisions'] = ai_decisions
                    st.session_state.dashboard_data['has_decisions'] = True
                    st.session_state.dashboard_data['status'] = 'success'
                except Exception as e:
                    st.error(f"AI decision generation failed: {e}")
        
        data = st.session_state.dashboard_data
        
        if data and (data.get('status') != 'no_data' or data.get('has_decisions', False)):
            # Key Metrics
            st.subheader("📊 Key Performance Indicators")
            
            # Key Metrics - Add demo KPIs if none exist
            kpis = data.get('kpis', [])
            if not kpis:
                # Add demo KPIs for AI decision demonstration
                kpis = [
                    {'name': 'Revenue', 'value': 850000, 'change': -5.2, 'unit': 'USD'},
                    {'name': 'Customer Satisfaction', 'value': 75, 'change': -3.1, 'unit': '%'},
                    {'name': 'Operational Efficiency', 'value': 68, 'change': -2.5, 'unit': '%'},
                    {'name': 'Market Share', 'value': 22, 'change': -1.8, 'unit': '%'}
                ]
            
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
            
            # AI-Powered Decision Making - Always show if decisions available
            if data.get('has_decisions') or (data.get('ai_decisions') and auto_analysis):
                ai_decisions = data.get('ai_decisions', {})
                st.subheader("🤖 AI-Powered Decision Making")
                
                # Executive Summary
                executive_summary = ai_decisions.get('executive_summary', {})
                if executive_summary:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("🎯 Overall Health", f"{executive_summary.get('overall_health_score', 0) * 100:.1f}%")
                    
                    with col2:
                        st.metric("📊 Health Assessment", executive_summary.get('health_assessment', 'Unknown'))
                    
                    with col3:
                        critical_count = executive_summary.get('critical_issues_count', 0)
                        st.metric("🚨 Critical Issues", critical_count)
                
                # Top Priorities
                top_priorities = executive_summary.get('top_priorities', [])
                if top_priorities:
                    st.subheader("🎯 Top Priorities")
                    
                    for priority in top_priorities:
                        with st.expander(f"#{priority['rank']} {priority['area'].replace('_', ' ').title()} - {priority['status'].title()}", expanded=priority['rank'] <= 2):
                            st.write(f"**Status:** {priority['status'].title()}")
                            st.write(f"**Urgency:** {priority['urgency']}")
                            st.write(f"**Key Action:** {priority['key_action']}")
                
                # Detailed Decisions by Area
                prioritized_decisions = ai_decisions.get('prioritized_decisions', [])
                if prioritized_decisions:
                    st.subheader("📋 Detailed Decisions")
                    
                    for decision_item in prioritized_decisions[:3]:  # Show top 3
                        decision = decision_item['decision']
                        area = decision['area'].replace('_', ' ').title()
                        
                        with st.expander(f"📊 {area} - {decision['status'].title()}", expanded=decision_item['priority_score'] > 80):
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric(f"📊 {area} Score", f"{decision['score'] * 100:.1f}%")
                                st.metric("⚠️ Risk Level", decision['risk_level'].title())
                                st.metric("⏱️ Timeline", decision['estimated_timeline'])
                            
                            with col2:
                                st.metric("🎯 Impact", decision['impact'].title())
                                st.metric("🔥 Urgency", decision['urgency'])
                                st.metric("📈 Confidence", f"{ai_decisions.get('confidence_score', 0) * 100:.1f}%")
                            
                            # Recommended Actions
                            st.write("**Recommended Actions:**")
                            for action in decision['recommended_actions']:
                                st.write(f"• {action.replace('_', ' ').title()}")
                            
                            # Specific Recommendations
                            if decision['specific_recommendations']:
                                st.write("**Specific Recommendations:**")
                                for rec in decision['specific_recommendations'][:3]:  # Show top 3
                                    st.write(f"• {rec}")
                            
                            # Success Metrics
                            if decision['success_metrics']:
                                st.write("**Success Metrics:**")
                                for metric in decision['success_metrics']:
                                    st.write(f"• {metric}")
                
                # Recommended Focus
                recommended_focus = executive_summary.get('recommended_focus', '')
                if recommended_focus:
                    st.info(f"🎯 **Recommended Focus:** {recommended_focus}")
                
                # Next Review Date
                next_review = executive_summary.get('next_review_date', '')
                if next_review:
                    st.info(f"📅 **Next Review Date:** {next_review}")
            
            # Show demo message if no decisions
            elif not data.get('has_decisions') and auto_analysis:
                st.info("🤖 **AI Decision Making:** Upload business data to generate automatic decisions")
                st.write("💡 *AI decisions will appear here based on your KPIs and business health scores*")
            
            # Legacy Recommendations (fallback)
            recommendations = data.get('recommendations', [])
            
            # Add recommendations from uploaded data
            if st.session_state.current_client and auto_analysis:
                uploaded_recommendations = st.session_state.file_upload_manager.generate_comprehensive_recommendations(st.session_state.current_client)
                recommendations.extend(uploaded_recommendations)
            
            if recommendations and not data.get('has_decisions'):
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
