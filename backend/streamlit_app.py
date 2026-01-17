import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import json

# Configure page
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
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE = "http://localhost:8001"  # Updated to use test backend

def fetch_api_data(endpoint):
    """Fetch data from the FastAPI backend"""
    try:
        response = requests.get(f"{API_BASE}{endpoint}")
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
        dashboard_data = fetch_api_data("/api/dashboard/complete")
        
        if not dashboard_data:
            st.error("Unable to load dashboard data. Please check your API connection.")
            return
        
        data = dashboard_data.get('data', {})
    
    # Executive Summary Section
    st.header("🎯 Executive Summary")
    
    # Business Health Score
    health_score = data.get('business_health_score', {})
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
    filtered_kpis = []
    
    for kpi in kpis:
        category = kpi.get('id', '').split('-')[0]
        if category in ['revenue', 'profit', 'expense', 'mrr', 'arr'] and not show_financial:
            continue
        elif category in ['customer', 'churn', 'clv', 'cac', 'nps', 'csat'] and not show_customer:
            continue
        elif category in ['operational', 'employee', 'market'] and not show_operational:
            continue
        filtered_kpis.append(kpi)
    
    # Display KPIs in columns
    if filtered_kpis:
        # Group by category
        financial_kpis = [kpi for kpi in filtered_kpis if any(x in kpi.get('id', '') for x in ['revenue', 'profit', 'expense', 'mrr', 'arr'])]
        customer_kpis = [kpi for kpi in filtered_kpis if any(x in kpi.get('id', '') for x in ['customer', 'churn', 'clv', 'cac', 'nps', 'csat'])]
        operational_kpis = [kpi for kpi in filtered_kpis if any(x in kpi.get('id', '') for x in ['operational', 'employee', 'market'])]
        
        # Financial KPIs
        if financial_kpis and show_financial:
            st.subheader("💰 Financial Performance")
            cols = st.columns(min(len(financial_kpis), 3))
            for i, kpi in enumerate(financial_kpis[:3]):
                with cols[i]:
                    fig = create_kpi_gauge(
                        kpi.get('current_value', 0),
                        kpi.get('target_value', 100),
                        kpi.get('id', '').replace('-', ' ').title(),
                        kpi.get('health_status', 'good')
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Customer KPIs
        if customer_kpis and show_customer:
            st.subheader("👥 Customer Metrics")
            cols = st.columns(min(len(customer_kpis), 3))
            for i, kpi in enumerate(customer_kpis[:3]):
                with cols[i]:
                    fig = create_kpi_gauge(
                        kpi.get('current_value', 0),
                        kpi.get('target_value', 100),
                        kpi.get('id', '').replace('-', ' ').title(),
                        kpi.get('health_status', 'good')
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Operational KPIs
        if operational_kpis and show_operational:
            st.subheader("⚡ Operational Efficiency")
            cols = st.columns(min(len(operational_kpis), 3))
            for i, kpi in enumerate(operational_kpis[:3]):
                with cols[i]:
                    fig = create_kpi_gauge(
                        kpi.get('current_value', 0),
                        kpi.get('target_value', 100),
                        kpi.get('id', '').replace('-', ' ').title(),
                        kpi.get('health_status', 'good')
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
                st.write(f"**What:** {insight.get('observation', 'No observation')}")
                st.write(f"**So What:** {insight.get('business_impact', 'No business impact')}")
                st.write(f"**Now What:** {insight.get('action', 'No action recommended')}")
    
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
                st.write(f"**Expected Impact:** {rec.get('expected_impact', 'No impact specified')}")
                st.write(f"**Timeframe:** {rec.get('timeframe', 'No timeframe')}")
                st.write(f"**Effort Required:** {rec.get('effort', 'No effort specified')}")
    
    # AI-Powered Insights Section
    st.header("🤖 AI-Powered Business Insights")
    
    # Add AI insights toggle
    use_ai_insights = st.checkbox("🤖 Enable AI-Enhanced Insights", value=True, help="Use Hugging Face AI for advanced analysis")
    
    if use_ai_insights:
        ai_insights = fetch_api_data("/api/ai/insights")
        if ai_insights:
            st.success("✅ AI Insights loaded successfully!")
            
            for i, insight in enumerate(ai_insights.get('data', [])[:5]):
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(insight.get('priority', 'low'), '⚪')
                
                with st.expander(f"{priority_emoji} {insight.get('title', 'AI Insight')}", expanded=i == 0):
                    st.write(f"**Category:** {insight.get('category', 'Unknown').title()}")
                    st.write(f"**Description:** {insight.get('description', 'No description')}")
                    st.write(f"**Priority:** {insight.get('priority', 'Unknown').title()}")
                    st.write(f"**Confidence:** {insight.get('confidence', 'Unknown').title()}")
                    st.write(f"**Source:** {insight.get('source', 'Unknown')}")
                    st.write(f"**Generated:** {insight.get('generated_at', 'Unknown')}")
    else:
        st.info("ℹ️ AI insights disabled. Toggle the checkbox above to enable.")
    
    # AI Executive Summary
    if use_ai_insights:
        st.subheader("📊 AI Executive Summary")
        
        if st.button("🔄 Generate AI Executive Summary", type="primary"):
            with st.spinner("Generating AI-powered executive summary..."):
                ai_summary = fetch_api_data("/api/ai/executive-summary")
                
                if ai_summary:
                    st.success("✅ AI Executive Summary generated!")
                    
                    # Display the summary
                    st.markdown("### 🎯 Overall Assessment")
                    st.write(ai_summary.get('summary', 'No summary available'))
                    
                    st.markdown("### 📋 Key Priorities")
                    priorities = ai_summary.get('priorities', [])
                    for priority in priorities:
                        st.write(f"• {priority}")
                    
                    st.markdown("### 🏥 Health Status")
                    health_status = ai_summary.get('health_assessment', 'Unknown')
                    health_color = {
                        'excellent': '🟢',
                        'good': '🔵',
                        'warning': '🟡',
                        'critical': '🔴'
                    }.get(health_status, '⚪')
                    
                    st.write(f"{health_color} **{health_status.title()}**")
                    
                    st.markdown(f"*Generated by: {ai_summary.get('source', 'Unknown')} AI*")
                else:
                    st.error("❌ Failed to generate AI executive summary")
    
    # Original Advanced Analytics Section
    st.header("📈 Advanced Analytics")
    
    # Add tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["Customer Segments", "Revenue Trends", "Expense Analysis"])
    
    with tab1:
        st.subheader("Customer Segmentation Analysis")
        customer_segments = fetch_api_data("/api/analytics/customer-segments")
        
        if customer_segments:
            segments_data = customer_segments.get('data', {})
            segments = segments_data.get('segments', [])
            
            if segments:
                # Create segment comparison chart
                segment_names = [s.get('segment_name', 'Unknown') for s in segments]
                avg_revenues = [s.get('avg_revenue', 0) for s in segments]
                customer_counts = [s.get('customer_count', 0) for s in segments]
                
                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('Average Revenue by Segment', 'Customer Count by Segment'),
                    specs=[[{"secondary_y": False}, {"secondary_y": False}]]
                )
                
                fig.add_trace(
                    go.Bar(x=segment_names, y=avg_revenues, name='Avg Revenue'),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=segment_names, y=customer_counts, name='Customer Count'),
                    row=1, col=2
                )
                
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Segment details
                for segment in segments:
                    with st.expander(f"📊 {segment.get('segment_name', 'Unknown')} Segment"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Customers", segment.get('customer_count', 0))
                        with col2:
                            st.metric("Avg Revenue", format_currency(segment.get('avg_revenue', 0)))
                        with col3:
                            st.metric("Churn Rate", format_percentage(segment.get('churn_rate', 0) * 100))
    
    with tab2:
        st.subheader("Revenue Trend Analysis")
        revenue_trends = fetch_api_data("/api/analytics/revenue-trends")
        
        if revenue_trends:
            trends_data = revenue_trends.get('data', {})
            monthly_trends = trends_data.get('monthly_trends', [])
            
            if monthly_trends:
                df_trends = pd.DataFrame(monthly_trends)
                
                # Revenue over time
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_trends['month_str'],
                    y=df_trends['revenue'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color='#3b82f6', width=3)
                ))
                
                fig.update_layout(
                    title='Revenue Trend Over Time',
                    xaxis_title='Month',
                    yaxis_title='Revenue ($)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Growth rate
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=df_trends['month_str'],
                    y=df_trends['revenue_growth'],
                    mode='lines+markers',
                    name='Growth Rate',
                    line=dict(color='#10b981', width=3)
                ))
                
                fig2.update_layout(
                    title='Monthly Growth Rate',
                    xaxis_title='Month',
                    yaxis_title='Growth Rate (%)',
                    height=400
                )
                
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.subheader("Expense Breakdown Analysis")
        expense_breakdown = fetch_api_data("/api/analytics/expense-breakdown")
        
        if expense_breakdown:
            expense_data = expense_breakdown.get('data', {})
            categories = expense_data.get('category_breakdown', [])
            
            if categories:
                df_expenses = pd.DataFrame(categories)
                
                # Expense by category
                fig = go.Figure(data=[
                    go.Pie(
                        labels=df_expenses['category'],
                        values=df_expenses['total_amount'],
                        hole=0.3
                    )
                ])
                
                fig.update_layout(
                    title='Expense Distribution by Category',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Budget variance
                budget_analysis = expense_data.get('budget_analysis', [])
                if budget_analysis:
                    df_budget = pd.DataFrame(budget_analysis)
                    
                    fig2 = go.Figure(data=[
                        go.Bar(
                            x=df_budget['category'],
                            y=df_budget['variance_percentage'],
                            marker_color=['red' if x > 5 else 'green' if x < -5 else 'gray' for x in df_budget['variance_percentage']]
                        )
                    ])
                    
                    fig2.update_layout(
                        title='Budget Variance by Category (%)',
                        xaxis_title='Category',
                        yaxis_title='Variance (%)',
                        height=400
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"<center><small>Last updated: {data.get('last_updated', 'Unknown')}</small></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
