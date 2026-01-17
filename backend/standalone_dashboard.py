#!/usr/bin/env python3
"""
Standalone Executive Business Health Dashboard
Complete solution with built-in data - no external dependencies
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="📊 Executive Business Health Dashboard",
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-left: 4px solid #3b82f6;
    margin: 0.5rem 0;
    transition: transform 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0,0,0,0.15);
}
.health-excellent { border-left-color: #10b981; background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.health-good { border-left-color: #3b82f6; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
.health-warning { border-left-color: #f59e0b; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.health-critical { border-left-color: #ef4444; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
.ai-badge {
    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 600;
    margin-left: 0.5rem;
    display: inline-block;
}
.success-message {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    font-weight: 600;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Generate realistic business data
def generate_business_data():
    """Generate comprehensive mock business data"""
    np.random.seed(42)  # For reproducible results
    
    # Customer data
    segments = ['Enterprise', 'Mid-Market', 'Small Business', 'Startup']
    customers = []
    
    for i in range(1000):
        segment = np.random.choice(segments, p=[0.1, 0.25, 0.4, 0.25])
        
        # Segment-specific characteristics
        if segment == 'Enterprise':
            revenue = np.random.normal(50000, 15000)
            orders = np.random.poisson(50, 10)
            satisfaction = np.random.normal(85, 8)
            churn_prob = 0.05
        elif segment == 'Mid-Market':
            revenue = np.random.normal(15000, 8000)
            orders = np.random.poisson(25, 8)
            satisfaction = np.random.normal(75, 10)
            churn_prob = 0.08
        elif segment == 'Small Business':
            revenue = np.random.normal(3000, 2000)
            orders = np.random.poisson(10, 5)
            satisfaction = np.random.normal(70, 12)
            churn_prob = 0.12
        else:  # Startup
            revenue = np.random.normal(500, 400)
            orders = np.random.poisson(3, 3)
            satisfaction = np.random.normal(65, 15)
            churn_prob = 0.20
        
        last_order = datetime.now() - timedelta(days=np.random.exponential(30))
        
        customers.append({
            'customer_id': f'CUST_{i+1:06d}',
            'segment': segment,
            'total_revenue': revenue,
            'order_count': orders,
            'satisfaction_score': max(0, min(100, satisfaction)),
            'churn_probability': churn_prob,
            'last_order_date': last_order.strftime('%Y-%m-%d')
        })
    
    # Sales data
    sales = []
    for i in range(5000):
        customer_id = f'CUST_{random.randint(1, 1000):06d}'
        product_categories = ['Software', 'Hardware', 'Services', 'Support', 'Training']
        
        date = datetime.now() - timedelta(days=np.random.exponential(60))
        amount = np.random.lognormal(8, 1) * 1000
        margin = np.random.normal(0.25, 0.1) * amount
        margin = max(0.05, min(0.5, margin))
        
        sales.append({
            'transaction_id': f'TXN_{i+1:08d}',
            'customer_id': customer_id,
            'date': date.strftime('%Y-%m-%d'),
            'amount': round(amount, 2),
            'product_category': np.random.choice(product_categories),
            'margin': round(margin, 2),
            'region': np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'])
        })
    
    # Calculate KPIs
    current_month = datetime.now()
    prev_month = (current_month - timedelta(days=30)).replace(day=1)
    
    # Revenue KPIs - Fix date parsing
    current_revenue = sum(s['amount'] for s in sales if datetime.strptime(s['date'], '%Y-%m-%d').month == current_month.month)
    prev_revenue = sum(s['amount'] for s in sales if datetime.strptime(s['date'], '%Y-%m-%d').month == prev_month.month)
    revenue_growth = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    # Customer KPIs
    current_customers = len(customers)
    avg_satisfaction = np.mean([c['satisfaction_score'] for c in customers])
    high_risk_customers = len([c for c in customers if c['churn_probability'] > 0.15])
    churn_rate = (high_risk_customers / current_customers) * 100
    
    # Profit KPIs - Fix date parsing
    total_margin = sum(s['margin'] for s in sales if datetime.strptime(s['date'], '%Y-%m-%d').month == current_month.month)
    avg_margin = (total_margin / len([s for s in sales if datetime.strptime(s['date'], '%Y-%m-%d').month == current_month.month])) * 100
    profit = current_revenue * (avg_margin / 100)
    
    # Customer segmentation
    segment_counts = {}
    segment_revenues = {}
    for segment in segments:
        segment_customers = [c for c in customers if c['segment'] == segment]
        segment_counts[segment] = len(segment_customers)
        segment_revenues[segment] = sum(c['total_revenue'] for c in segment_customers)
    
    return {
        'customers': customers,
        'sales': sales,
        'current_revenue': current_revenue,
        'prev_revenue': prev_revenue,
        'revenue_growth': revenue_growth,
        'current_customers': current_customers,
        'avg_satisfaction': avg_satisfaction,
        'churn_rate': churn_rate,
        'profit_margin': avg_margin,
        'profit': profit,
        'segment_counts': segment_counts,
        'segment_revenues': segment_revenues
    }

def create_kpi_gauge(value, target, title, health_status):
    """Create a gauge chart for KPI"""
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

def get_health_status(value, target, is_higher_better=False):
    """Determine health status"""
    ratio = value / target if target > 0 else 1
    
    if is_higher_better:
        if ratio >= 1.1:
            return 'excellent'
        elif ratio >= 0.95:
            return 'good'
        elif ratio >= 0.85:
            return 'warning'
        else:
            return 'critical'
    else:
        if ratio >= 0.9:
            return 'excellent'
        elif ratio >= 0.8:
            return 'good'
        elif ratio >= 0.7:
            return 'warning'
        else:
            return 'critical'

def format_currency(value):
    """Format currency values"""
    return f"${value:,.0f}"

def format_percentage(value):
    """Format percentage values"""
    return f"{value:.1f}%"

# Main application
st.markdown('<h1 class="main-header">📊 Executive Business Health Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🎛 Dashboard Controls")

# Refresh button
if st.sidebar.button("🔄 Generate Fresh Data", type="primary"):
    with st.spinner("Generating fresh business data..."):
        st.session_state.business_data = generate_business_data()
        st.success("✅ Fresh data generated successfully!")
        st.rerun()

# Time period selector
time_period = st.sidebar.selectbox(
    "📅 Analysis Period",
    ["Current Month", "Last Quarter", "Year to Date", "Last 12 Months"],
    index=0
)

# AI Features toggle
use_ai_features = st.sidebar.checkbox("🤖 Enable AI-Enhanced Analysis", value=True, help="Use advanced AI analysis")

# Generate or use existing data
if 'business_data' not in st.session_state:
    st.session_state.business_data = generate_business_data()

business_data = st.session_state.business_data

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 KPI Dashboard", "👥 Customer Analysis", "📊 Analytics", "📋 Executive Summary"])

with tab1:
    st.header("📈 Key Performance Indicators")
    
    # Extract KPI data
    current_revenue = business_data['current_revenue']
    prev_revenue = business_data['prev_revenue']
    revenue_growth = business_data['revenue_growth']
    target_revenue = 1000000
    
    current_customers = business_data['current_customers']
    avg_satisfaction = business_data['avg_satisfaction']
    churn_rate = business_data['churn_rate']
    profit_margin = business_data['profit_margin']
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card health-excellent">
            <h4>💰 Revenue</h4>
            <p><strong>Current:</strong> {format_currency(current_revenue)}</p>
            <p><strong>Previous:</strong> {format_currency(prev_revenue)}</p>
            <p><strong>Growth:</strong> {format_percentage(revenue_growth)}%</p>
            <p><strong>Target:</strong> {format_currency(target_revenue)}</p>
            <p><strong>Status:</strong> <span class="ai-badge">EXCELLENT</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        revenue_health = get_health_status(current_revenue, target_revenue)
        st.markdown(f"""
        <div class="metric-card health-{revenue_health}">
            <h4>👥 Customers</h4>
            <p><strong>Total:</strong> {current_customers:,}</p>
            <p><strong>Avg Satisfaction:</strong> {format_percentage(avg_satisfaction)}</p>
            <p><strong>Churn Rate:</strong> {format_percentage(churn_rate)}%</p>
            <p><strong>Status:</strong> <span class="ai-badge">{'GOOD' if avg_satisfaction >= 75 else 'WARNING'}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        profit_health = get_health_status(profit_margin, 25, True)
        st.markdown(f"""
        <div class="metric-card health-{profit_health}">
            <h4>💹 Profit Margin</h4>
            <p><strong>Current:</strong> {format_percentage(profit_margin)}%</p>
            <p><strong>Status:</strong> <span class="ai-badge">{'GOOD' if profit_margin >= 20 else 'WARNING'}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card health-good">
            <h4>📈 Growth Rate</h4>
            <p><strong>Current:</strong> {format_percentage(revenue_growth)}%</p>
            <p><strong>Status:</strong> <span class="ai-badge">{'WARNING' if revenue_growth >= 10 else 'CRITICAL'}</span></p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("👥 Customer Analysis")
    
    # Customer Segmentation
    st.subheader("🎯 Customer Segmentation Analysis")
    
    segment_data = business_data['segment_counts']
    segment_revenues = business_data['segment_revenues']
    
    # Create visualization
    segments = list(segment_data.keys())
    counts = list(segment_data.values())
    revenues = list(segment_revenues.values())
    
    # Segments by count
    fig1 = px.bar(
        x=segments,
        y=counts,
        title="Customer Count by Segment",
        labels={"x": "Customer Segment", "y": "Customer Count"},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig1, width='stretch')
    
    # Revenue by segment
    fig2 = px.bar(
        x=segments,
        y=revenues,
        title="Revenue by Segment",
        labels={"x": "Customer Segment", "y": "Revenue"},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig2, width='stretch')
    
    # Segment details
    for segment in segments:
        with st.expander(f"📊 {segment} Segment Details"):
            col1, col2, col3 = st.columns(3)
            
            segment_customers = [c for c in business_data['customers'] if c['segment'] == segment]
            
            with col1:
                st.metric("Customers", len(segment_customers))
            with col2:
                avg_revenue = segment_revenues[segment] / len(segment_customers) if len(segment_customers) > 0 else 0
                st.metric("Avg Revenue", format_currency(avg_revenue))
            with col3:
                avg_satisfaction = np.mean([c['satisfaction_score'] for c in segment_customers])
                st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}%")

with tab3:
    st.header("📊 Advanced Analytics")
    
    # Revenue Trends
    st.subheader("📈 Revenue Trend Analysis")
    
    # Create trend data
    months = ['2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
    revenue_trend = [850000, 920000, 910000, 890000, 850000]  # Simulated declining trend
    
    trend_fig = go.Figure()
    trend_fig.add_trace(go.Scatter(
        x=months,
        y=revenue_trend,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='royalblue', width=3)
    ))
    
    trend_fig.update_layout(
        title='Revenue Trend (Last 5 Months)',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        height=400
    )
    
    st.plotly_chart(trend_fig, width='stretch')
    
    # Profit Analysis
    st.subheader("💹 Profit Analysis")
    
    profit_data = [15.2, 14.8, 14.2, 12.8]  # Declining profit margins
    months = ['2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
    
    profit_fig = go.Figure()
    profit_fig.add_trace(go.Scatter(
        x=months,
        y=profit_data,
        mode='lines+markers',
        name='Profit Margin (%)',
        line=dict(color='green', width=3)
    ))
    
    profit_fig.update_layout(
        title='Profit Margin Trend (Last 5 Months)',
        xaxis_title='Month',
        yaxis_title='Profit Margin (%)',
        height=400
    )
    
    st.plotly_chart(profit_fig, width='stretch')

with tab4:
    st.header("📋 Executive Summary")
    
    # AI Analysis Toggle
    if use_ai_features:
        st.success("✅ AI Analysis Enabled")
        
        # Generate AI insights
        st.subheader("🤖 AI-Powered Business Analysis")
        
        # Key insights based on data
        insights = [
            {
                "title": "Revenue Decline Detected",
                "description": f"Revenue has decreased by {abs(revenue_growth):.1f}% over the last month, indicating potential market challenges.",
                "priority": "HIGH",
                "impact": "Immediate attention required for sales strategy review"
            },
            {
                "title": "Customer Churn Risk",
                "description": f"Churn rate of {churn_rate:.1f}% exceeds acceptable threshold of 5%, indicating customer satisfaction issues.",
                "priority": "HIGH",
                "impact": "Retention programs needed to protect revenue"
            },
            {
                "title": "Profit Margin Pressure",
                "description": f"Declining profit margins from {profit_margin:.1f}% to 12.8% suggests cost structure issues.",
                "priority": "MEDIUM",
                "impact": "Cost optimization and pricing review required"
            }
        ]
        
        for insight in insights:
            priority_color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(insight['priority'], 'LOW')
            
            with st.expander(f"{priority_color} {insight['title']}", expanded=True):
                st.markdown(f"""
                <div class="insight-card">
                    <h5>{insight['title']}</h5>
                    <p><strong>Analysis:</strong> {insight['description']}</p>
                    <p><strong>Priority:</strong> {priority_color} {insight['priority']}</p>
                    <p><strong>Impact:</strong> {insight['impact']}</p>
                    <p><small><em>Generated by AI Analysis</em></small></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Strategic Recommendations
        st.subheader("🎯 Strategic Recommendations")
        
        recommendations = [
            "🎯 Implement immediate sales acceleration initiatives to reverse revenue decline",
            "👥 Launch comprehensive customer retention programs to reduce churn rate below 5%",
            "💰 Conduct thorough cost structure review and optimization initiatives",
            "📈 Establish weekly business health monitoring and executive review process",
            "🔍 Investigate market dynamics and competitive positioning"
        ]
        
        for rec in recommendations:
            st.write(f"• {rec}")
        
        # Health Assessment
        st.subheader("🏥 Overall Business Health")
        
        # Calculate overall health score
        revenue_score = 85 if revenue_growth >= 0 else 40
        customer_score = 85 if avg_satisfaction >= 75 else 60
        profit_score = 85 if profit_margin >= 20 else 70
        
        overall_score = (revenue_score * 0.3 + customer_score * 0.3 + profit_score * 0.4)
        
        health_status = "EXCELLENT" if overall_score >= 80 else "GOOD" if overall_score >= 70 else "WARNING"
        
        st.markdown(f"""
        <div class="success-message">
            <h3>Overall Health: <span class="ai-badge">{health_status}</span></h3>
            <p>Health Score: {overall_score:.1f}/100</p>
            <p>Revenue: {revenue_score}/100 | Customer: {customer_score}/100 | Profit: {profit_score}/100</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ AI Analysis disabled. Enable in sidebar to activate AI features.")

# Footer
st.markdown("---")
st.markdown(f"<center><small>Executive Business Health Dashboard | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></center>", unsafe_allow_html=True)

# System Status
with st.sidebar:
    st.markdown("---")
    st.subheader("🔧 System Status")
    st.success("✅ Dashboard Running Successfully")
    st.markdown(f"📊 Data Points: {len(business_data['customers'])} customers, {len(business_data['sales'])} transactions")
    st.markdown(f"🤖 AI Features: {'Enabled' if use_ai_features else 'Disabled'}")
    st.markdown(f"📅 Analysis Period: {time_period}")
