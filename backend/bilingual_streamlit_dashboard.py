#!/usr/bin/env python3
"""
Bilingual Executive Dashboard - Streamlit Version
Automatically detects company origin and displays results in appropriate language
"""

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

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.language_detector import language_detector, Language
from app.services.bilingual_decision_engine import bilingual_decision_engine, Priority
from app.services.kpi_calculator import KPICalculator
from app.services.health_scorer import HealthScorer

# Configure page
st.set_page_config(
    page_title="Executive Business Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for bilingual support
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
    
    .recommendation-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #8b5cf6;
    }
    
    .priority-high { border-left-color: #ef4444; }
    .priority-medium { border-left-color: #f59e0b; }
    .priority-low { border-left-color: #10b981; }
    
    .bangla-font {
        font-family: 'Hind Siliguri', 'SolaimanLipi', Arial, sans-serif;
        line-height: 1.6;
    }
    
    .language-indicator {
        background: #e0f2fe;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
kpi_calculator = KPICalculator()
health_scorer = HealthScorer()

# Bilingual text dictionary
BILINGUAL_TEXT = {
    'title': {
        'en': 'Executive Business Health Dashboard',
        'bn': 'এক্সিকিউটিভ বিজনেস হেলথ ড্যাশবোর্ড'
    },
    'upload_data': {
        'en': '📤 Upload Your Business Data',
        'bn': '📤 আপনার ব্যবসায়িক ডেটা আপলোড করুন'
    },
    'company_detected': {
        'en': '🌍 Company Detected',
        'bn': '🌍 কোম্পানি সনাক্ত হয়েছে'
    },
    'kpi_summary': {
        'en': '📊 KPI Summary',
        'bn': '📊 কেপিআই সারাংশ'
    },
    'recommendations': {
        'en': '🎯 Actionable Recommendations',
        'bn': '🎯 কার্যকর সুপারিশ'
    },
    'health_score': {
        'en': 'Business Health Score',
        'bn': 'ব্যবসায়িক স্বাস্থ্য স্কোর'
    },
    'revenue': {
        'en': 'Revenue',
        'bn': 'আয়'
    },
    'customers': {
        'en': 'Customers',
        'bn': 'গ্রাহক'
    },
    'profit': {
        'en': 'Profit',
        'bn': 'মুনাফা'
    },
    'growth': {
        'en': 'Growth',
        'bn': 'প্রবৃদ্ধি'
    },
    'churn_rate': {
        'en': 'Churn Rate',
        'bn': 'ক্ষয়ক্ষতি হার'
    },
    'satisfaction': {
        'en': 'Customer Satisfaction',
        'bn': 'গ্রাহক সন্তুষ্টি'
    },
    'efficiency': {
        'en': 'Operational Efficiency',
        'bn': 'অপারেশনাল দক্ষতা'
    },
    'market_share': {
        'en': 'Market Share',
        'bn': 'বাজার অংশ'
    },
    'priority': {
        'en': 'Priority',
        'bn': 'অগ্রাধিকার'
    },
    'impact': {
        'en': 'Impact Score',
        'bn': 'প্রভাব স্কোর'
    },
    'implementation': {
        'en': 'Implementation Time',
        'bn': 'বাস্তবায়ন সময়'
    },
    'resources': {
        'en': 'Resources Needed',
        'bn': 'প্রয়োজনীয় সম্পদ'
    },
    'no_data': {
        'en': 'No data uploaded yet. Please upload your business data to see insights.',
        'bn': 'এখনও কোন ডেটা আপলোড করা হয়নি। অন্তর্দৃষ্টি দেখতে আপনার ব্যবসায়িক ডেটা আপলোড করুন।'
    }
}

def get_text(key: str, language: Language) -> str:
    """Get text in specified language"""
    return BILINGUAL_TEXT.get(key, {}).get(language.value, key)

def format_currency(amount: float, language: Language) -> str:
    """Format currency based on language"""
    if language == Language.BANGLA:
        return f"৳{amount:,.2f}"
    else:
        return f"${amount:,.2f}"

def format_percentage(value: float, language: Language) -> str:
    """Format percentage based on language"""
    return f"{value:.1f}%"

def detect_company_language(uploaded_file) -> tuple:
    """Detect company origin and determine language"""
    try:
        # Read uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Detect company information
        companies = language_detector.detect_from_dataframe(df)
        
        if companies:
            # Use the first detected company
            company_info = companies[0]
            return company_info, df
        
        # Fallback: default to English
        fallback_info = type('CompanyInfo', (), {
            'name': 'Unknown Company',
            'country': 'International',
            'is_bangladeshi': False,
            'language': Language.ENGLISH,
            'confidence': 0.5
        })()
        return fallback_info, df
        
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None, None

def display_kpi_metrics(kpi_data: dict, language: Language):
    """Display KPI metrics in appropriate language"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        revenue = kpi_data.get('revenue', 0)
        revenue_growth = kpi_data.get('revenue_growth', 0)
        st.metric(
            label=get_text('revenue', language),
            value=format_currency(revenue, language),
            delta=f"{format_percentage(revenue_growth, language)} vs last month"
        )
    
    with col2:
        customers = kpi_data.get('total_customers', 0)
        new_customers = kpi_data.get('new_customers', 0)
        st.metric(
            label=get_text('customers', language),
            value=f"{customers:,}",
            delta=f"+{new_customers} new"
        )
    
    with col3:
        profit = kpi_data.get('profit', 0)
        profit_margin = kpi_data.get('profit_margin', 0)
        st.metric(
            label=get_text('profit', language),
            value=format_currency(profit, language),
            delta=f"{format_percentage(profit_margin, language)} margin"
        )
    
    with col4:
        churn_rate = kpi_data.get('churn_rate', 0) * 100
        satisfaction = kpi_data.get('customer_satisfaction', 0)
        st.metric(
            label=get_text('churn_rate', language),
            value=f"{churn_rate:.1f}%",
            delta=f"{satisfaction}/100 satisfaction"
        )

def display_health_score(health_data: dict, language: Language):
    """Display business health score"""
    
    overall_score = health_data.get('overall_score', 0)
    category_scores = health_data.get('category_scores', {})
    
    # Determine health status
    if overall_score >= 80:
        health_status = "excellent"
        status_color = "#10b981"
    elif overall_score >= 60:
        health_status = "good"
        status_color = "#3b82f6"
    elif overall_score >= 40:
        health_status = "warning"
        status_color = "#f59e0b"
    else:
        health_status = "critical"
        status_color = "#ef4444"
    
    # Display overall score
    st.markdown(f"""
    <div class="metric-card health-{health_status}">
        <h3>{get_text('health_score', language)}</h3>
        <h1 style="color: {status_color}; font-size: 3rem; margin: 0;">{overall_score}/100</h1>
        <p style="margin: 0; color: #6b7280;">{health_status.title()} Health Status</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display category scores
    if category_scores:
        categories = list(category_scores.keys())
        scores = list(category_scores.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=[get_text(cat.replace('_', ''), language) for cat in categories],
                y=scores,
                marker_color=['#10b981' if score >= 70 else '#f59e0b' if score >= 50 else '#ef4444' for score in scores]
            )
        ])
        
        fig.update_layout(
            title="Category Breakdown",
            xaxis_title="Categories",
            yaxis_title="Score",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_recommendations(recommendations: list, language: Language):
    """Display actionable recommendations"""
    
    if not recommendations:
        return
    
    for i, rec in enumerate(recommendations[:5]):  # Show top 5
        formatted_rec = bilingual_decision_engine.format_recommendation_for_display(rec, language)
        
        priority_class = f"priority-{formatted_rec['priority']}"
        
        st.markdown(f"""
        <div class="recommendation-card {priority_class}">
            <h4>{formatted_rec['title']}</h4>
            <p>{formatted_rec['description']}</p>
            <br>
            <strong>🎯 {get_text('priority', language)}:</strong> {formatted_rec['priority'].title()}<br>
            <strong>📈 {get_text('impact', language)}:</strong> {formatted_rec['impact_score']:.2f}<br>
            <strong>⏱️ {get_text('implementation', language)}:</strong> {formatted_rec['implementation_time']}<br>
            <strong>💼 {get_text('resources', language)}:</strong> {', '.join(formatted_rec['resources_needed'])}
            <br><br>
            <strong>🚀 Action:</strong> {formatted_rec['action']}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    
    # Initialize session state
    if 'company_info' not in st.session_state:
        st.session_state.company_info = None
    if 'kpi_data' not in st.session_state:
        st.session_state.kpi_data = None
    if 'health_data' not in st.session_state:
        st.session_state.health_data = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    
    # Main title
    st.markdown('<h1 class="main-header">📊 Executive Business Health Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for file upload
    with st.sidebar:
        st.markdown("### 📤 Upload Business Data")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your business data (CSV or Excel)"
        )
        
        if uploaded_file is not None:
            with st.spinner("🔍 Analyzing your data..."):
                company_info, df = detect_company_language(uploaded_file)
                
                if company_info and df is not None:
                    st.session_state.company_info = company_info
                    
                    # Calculate KPIs
                    kpi_data = kpi_calculator.calculate_kpis(df)
                    st.session_state.kpi_data = kpi_data
                    
                    # Calculate health score
                    health_data = health_scorer.calculate_health_score(kpi_data)
                    st.session_state.health_data = health_data
                    
                    # Generate recommendations
                    recommendations = bilingual_decision_engine.generate_recommendations(
                        kpi_data, 
                        company_info.language,
                        company_info.industry if hasattr(company_info, 'industry') else 'general'
                    )
                    st.session_state.recommendations = recommendations
                    
                    st.success(f"✅ Data analyzed successfully!")
                else:
                    st.error("❌ Failed to analyze data. Please check your file format.")
    
    # Main content area
    if st.session_state.company_info is None:
        # Welcome message
        st.markdown(f"""
        <div style="text-align: center; padding: 3rem; background: #f8fafc; border-radius: 0.5rem; margin: 2rem 0;">
            <h2 style="color: #1f2937; margin-bottom: 1rem;">Welcome to Executive Dashboard</h2>
            <p style="color: #6b7280; font-size: 1.1rem; line-height: 1.6;">
                Upload your business data to get instant AI-powered insights and recommendations.<br>
                Our system automatically detects your company's origin and provides results in your preferred language.<br>
                <strong>Bangladeshi companies get results in Bangla, international companies in English.</strong>
            </p>
            <div style="margin-top: 2rem;">
                <span style="background: #e0f2fe; padding: 0.5rem 1rem; border-radius: 0.25rem; margin: 0.25rem;">🇧🇩 Bangla Support</span>
                <span style="background: #e0f2fe; padding: 0.5rem 1rem; border-radius: 0.25rem; margin: 0.25rem;">🌍 Global Coverage</span>
                <span style="background: #e0f2fe; padding: 0.5rem 1rem; border-radius: 0.25rem; margin: 0.25rem;">🤖 AI Insights</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data format
        st.markdown("### 📋 Sample Data Format")
        sample_data = {
            'company_name': ['ABC Garments Ltd', 'Tech Solutions BD'],
            'revenue': [45000000, 8500000],
            'expenses': [38000000, 6200000],
            'customers': [150, 85],
            'new_customers': [12, 8],
            'churned_customers': [3, 1],
            'date': ['2024-01-01', '2024-01-01']
        }
        st.dataframe(pd.DataFrame(sample_data))
        
    else:
        # Display company information
        company_info = st.session_state.company_info
        language = company_info.language
        
        # Language indicator
        language_flag = "🇧🇩" if language == Language.BANGLA else "🌍"
        language_text = "Bangla" if language == Language.BANGLA else "English"
        
        st.markdown(f"""
        <div class="language-indicator">
            {language_flag} Displaying results in {language_text} for {company_info.name} ({company_info.country})
            <br>
            <small>Detection confidence: {company_info.confidence:.1%}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # KPI Summary
        st.markdown(f"### {get_text('kpi_summary', language)}")
        if st.session_state.kpi_data:
            display_kpi_metrics(st.session_state.kpi_data, language)
        
        # Health Score
        st.markdown(f"### {get_text('health_score', language)}")
        if st.session_state.health_data:
            display_health_score(st.session_state.health_data, language)
        
        # Recommendations
        st.markdown(f"### {get_text('recommendations', language)}")
        if st.session_state.recommendations:
            display_recommendations(st.session_state.recommendations, language)
        
        # Detailed analysis section
        with st.expander("📈 Detailed Analysis"):
            if st.session_state.kpi_data:
                # Revenue trend chart
                kpi_data = st.session_state.kpi_data
                
                # Sample trend data (in real implementation, this would come from historical data)
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                revenue_trend = [kpi_data.get('revenue', 0) * (1 + np.random.normal(0, 0.1)) for _ in months]
                
                fig = go.Figure(data=[
                    go.Scatter(
                        x=months,
                        y=revenue_trend,
                        mode='lines+markers',
                        name=get_text('revenue', language),
                        line=dict(color='#3b82f6', width=3)
                    )
                ])
                
                fig.update_layout(
                    title=f"{get_text('revenue', language)} Trend",
                    xaxis_title="Month",
                    yaxis_title=f"{get_text('revenue', language)} ({'৳' if language == Language.BANGLA else '$'})",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Customer segments
                if 'customer_segments' in kpi_data:
                    segments = kpi_data['customer_segments']
                    
                    fig = px.pie(
                        values=list(segments.values()),
                        names=list(segments.keys()),
                        title="Customer Segments"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # Export options
        st.markdown("### 📤 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"📄 Export Report ({language_text})"):
                # Generate report
                report_data = {
                    'company_info': {
                        'name': company_info.name,
                        'country': company_info.country,
                        'language': language_text
                    },
                    'kpi_data': st.session_state.kpi_data,
                    'health_score': st.session_state.health_data,
                    'recommendations': [
                        bilingual_decision_engine.format_recommendation_for_display(rec, language)
                        for rec in st.session_state.recommendations
                    ]
                }
                
                st.download_button(
                    label=f"Download {language_text} Report",
                    data=json.dumps(report_data, indent=2, ensure_ascii=False),
                    file_name=f"executive_dashboard_report_{language.value}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Reset Analysis"):
                # Clear session state
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    main()
