#!/usr/bin/env python3
"""
Vercel Serverless API for Executive Dashboard
Optimized for < 250MB function size limit
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import sys

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

try:
    from app.services.language_detector import language_detector, Language
    from app.services.bilingual_decision_engine import bilingual_decision_engine
except ImportError:
    # Fallback for deployment
    language_detector = None
    bilingual_decision_engine = None

# Request models
class KPIData(BaseModel):
    revenue: Optional[float] = None
    revenue_growth: Optional[float] = None
    total_customers: Optional[int] = None
    new_customers: Optional[int] = None
    churned_customers: Optional[int] = None
    profit: Optional[float] = None
    expenses: Optional[float] = None

class CompanyInfo(BaseModel):
    name: str
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

# Helper functions
def detect_language_simple(company_name: str, email: str = "") -> str:
    """Simple language detection without heavy dependencies"""
    company_lower = company_name.lower()
    email_lower = email.lower()
    
    # Bangladesh indicators
    bangla_indicators = [
        'bangladesh', 'bengal', 'dhaka', 'chittagong', 'khulna',
        'rajshahi', 'sylhet', 'barisal', 'rangpur', 'mymensingh',
        '.com.bd', '.bd', 'bangladeshi', 'bengali',
        'লিমিটেড', 'প্রাইভেট', 'গ্রুপ', 'ইন্ডাস্ট্রিজ'
    ]
    
    # Check for Bangla indicators
    for indicator in bangla_indicators:
        if indicator in company_lower or indicator in email_lower:
            return 'bn'
    
    # Check for Bangla characters
    if any('\u0980' <= char <= '\u09FF' for char in company_name):
        return 'bn'
    
    return 'en'

def generate_simple_recommendations(kpi_data: Dict, language: str) -> List[Dict]:
    """Generate simple recommendations without heavy ML dependencies"""
    recommendations = []
    
    # Revenue analysis
    revenue_growth = kpi_data.get('revenue_growth', 0)
    if revenue_growth < -10:
        if language == 'bn':
            recommendations.append({
                'title': 'সতর্কতা: আয় হ্রাস পেয়েছে',
                'description': f'আপনার আয় {abs(revenue_growth):.1f}% কমেছে। তাৎক্ষণিক ব্যবস্থা প্রয়োজন।',
                'action': 'আক্রমনাত্মক বিক্রয় কৌশল বাস্তবায়ন করুন',
                'priority': 'high',
                'impact': 0.9
            })
        else:
            recommendations.append({
                'title': 'Critical: Revenue Decline Detected',
                'description': f'Your revenue has decreased by {abs(revenue_growth):.1f}%. Immediate action required.',
                'action': 'Implement aggressive sales strategy',
                'priority': 'high',
                'impact': 0.9
            })
    
    # Customer analysis
    churn_rate = kpi_data.get('churn_rate', 0)
    if churn_rate > 0.15:
        if language == 'bn':
            recommendations.append({
                'title': 'গ্রাহক ক্ষয়ক্ষতি বেশি',
                'description': f'গ্রাহক ক্ষয়ক্ষতির হার {churn_rate*100:.1f}%, যা খুব বেশি।',
                'action': 'গ্রাহক সেবা উন্নত করুন এবং প্রতিক্রিয়া ব্যবস্থা চালু করুন',
                'priority': 'high',
                'impact': 0.8
            })
        else:
            recommendations.append({
                'title': 'High Customer Churn Rate',
                'description': f'Customer churn rate is {churn_rate*100:.1f}%, which is above average.',
                'action': 'Improve customer service and implement feedback system',
                'priority': 'high',
                'impact': 0.8
            })
    
    # Cost analysis
    cost_ratio = kpi_data.get('expenses', 0) / max(kpi_data.get('revenue', 1), 1)
    if cost_ratio > 0.85:
        if language == 'bn':
            recommendations.append({
                'title': 'উচ্চ পরিচালন ব্যয়',
                'description': f'পরিচালন ব্যয় আয়ের {cost_ratio*100:.1f}%, যা খুব বেশি।',
                'action': 'খরচ অপ্টিমাইজ করুন এবং দক্ষতা বাড়ান',
                'priority': 'medium',
                'impact': 0.7
            })
        else:
            recommendations.append({
                'title': 'High Operating Costs',
                'description': f'Operating costs are {cost_ratio*100:.1f}% of revenue, which is high.',
                'action': 'Optimize costs and improve efficiency',
                'priority': 'medium',
                'impact': 0.7
            })
    
    return recommendations

def calculate_health_score(kpi_data: Dict) -> Dict:
    """Simple health score calculation"""
    scores = {}
    
    # Revenue health
    revenue_growth = kpi_data.get('revenue_growth', 0)
    if revenue_growth > 10:
        scores['revenue'] = 90
    elif revenue_growth > 0:
        scores['revenue'] = 70
    elif revenue_growth > -10:
        scores['revenue'] = 50
    else:
        scores['revenue'] = 30
    
    # Customer health
    churn_rate = kpi_data.get('churn_rate', 0)
    if churn_rate < 0.05:
        scores['customers'] = 90
    elif churn_rate < 0.10:
        scores['customers'] = 70
    elif churn_rate < 0.15:
        scores['customers'] = 50
    else:
        scores['customers'] = 30
    
    # Profit health
    profit_margin = (kpi_data.get('profit', 0) / max(kpi_data.get('revenue', 1), 1)) * 100
    if profit_margin > 20:
        scores['profit'] = 90
    elif profit_margin > 10:
        scores['profit'] = 70
    elif profit_margin > 5:
        scores['profit'] = 50
    else:
        scores['profit'] = 30
    
    # Overall score
    overall_score = sum(scores.values()) / len(scores)
    
    return {
        'overall_score': round(overall_score, 1),
        'category_scores': scores,
        'status': 'excellent' if overall_score >= 80 else 'good' if overall_score >= 60 else 'warning' if overall_score >= 40 else 'critical'
    }

# API Endpoints
def handler(request):
    """Main handler for Vercel serverless functions"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    try:
        # Parse request
        if request.method == 'POST':
            data = json.loads(request.body)
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Route handling
        path = request.path.split('/')
        
        if 'detect-language' in path:
            return handle_language_detection(data)
        elif 'analyze' in path:
            return handle_analysis(data)
        elif 'recommendations' in path:
            return handle_recommendations(data)
        elif 'health-score' in path:
            return handle_health_score(data)
        else:
            return handle_dashboard(data)
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_language_detection(data):
    """Handle language detection"""
    try:
        company_info = data.get('company', {})
        company_name = company_info.get('name', '')
        email = company_info.get('email', '')
        
        if language_detector:
            # Use full detector if available
            from app.services.language_detector import CompanyInfo
            detected = language_detector.detect_company_origin(
                company_name, email, 
                company_info.get('website', ''),
                company_info.get('address', ''),
                company_info.get('phone', '')
            )
            language = detected.language.value
            confidence = detected.confidence
        else:
            # Use simple detection
            language = detect_language_simple(company_name, email)
            confidence = 0.8
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'language': language,
                'confidence': confidence,
                'is_bangladeshi': language == 'bn'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_analysis(data):
    """Handle business analysis"""
    try:
        kpi_data = data.get('kpi_data', {})
        company_info = data.get('company', {})
        
        # Detect language
        company_name = company_info.get('name', '')
        email = company_info.get('email', '')
        
        if language_detector:
            detected = language_detector.detect_company_origin(
                company_name, email,
                company_info.get('website', ''),
                company_info.get('address', ''),
                company_info.get('phone', '')
            )
            language = detected.language.value
        else:
            language = detect_language_simple(company_name, email)
        
        # Generate recommendations
        if bilingual_decision_engine:
            from app.services.bilingual_decision_engine import Language as Lang
            lang_enum = Lang.BANGLA if language == 'bn' else Lang.ENGLISH
            recommendations = bilingual_decision_engine.generate_recommendations(kpi_data, lang_enum)
            formatted_recs = [
                bilingual_decision_engine.format_recommendation_for_display(rec, lang_enum)
                for rec in recommendations
            ]
        else:
            formatted_recs = generate_simple_recommendations(kpi_data, language)
        
        # Calculate health score
        health_score = calculate_health_score(kpi_data)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'language': language,
                'kpi_data': kpi_data,
                'health_score': health_score,
                'recommendations': formatted_recs[:5],  # Top 5 recommendations
                'company_info': company_info
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_recommendations(data):
    """Handle recommendations only"""
    try:
        kpi_data = data.get('kpi_data', {})
        language = data.get('language', 'en')
        
        if bilingual_decision_engine:
            from app.services.bilingual_decision_engine import Language as Lang
            lang_enum = Lang.BANGLA if language == 'bn' else Lang.ENGLISH
            recommendations = bilingual_decision_engine.generate_recommendations(kpi_data, lang_enum)
            formatted_recs = [
                bilingual_decision_engine.format_recommendation_for_display(rec, lang_enum)
                for rec in recommendations
            ]
        else:
            formatted_recs = generate_simple_recommendations(kpi_data, language)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'recommendations': formatted_recs
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_health_score(data):
    """Handle health score calculation"""
    try:
        kpi_data = data.get('kpi_data', {})
        health_score = calculate_health_score(kpi_data)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(health_score)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def handle_dashboard(data):
    """Handle complete dashboard data"""
    try:
        return handle_analysis(data)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# Export for Vercel
def lambda_handler(request):
    return handler(request)

# Also support direct handler
def main_handler(request):
    return handler(request)
