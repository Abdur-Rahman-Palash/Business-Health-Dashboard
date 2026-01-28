#!/usr/bin/env python3
"""
Quick Test Script for Bilingual Dashboard
Tests language detection and bilingual recommendations
"""

import sys
import os
import pandas as pd

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.language_detector import language_detector, Language
from backend.app.services.bilingual_decision_engine import bilingual_decision_engine

def test_language_detection():
    """Test language detection with sample companies"""
    
    print("🔍 Testing Language Detection")
    print("=" * 50)
    
    # Test companies
    test_companies = [
        {
            'name': 'ABC Garments Ltd',
            'email': 'info@abcgarments.com.bd',
            'website': 'www.abcgarments.com.bd',
            'address': 'Dhaka, Bangladesh',
            'phone': '+8801712345678'
        },
        {
            'name': 'Global Tech Solutions Inc',
            'email': 'info@globaltech.com',
            'website': 'www.globaltech.com',
            'address': 'New York, USA',
            'phone': '+12125551234'
        },
        {
            'name': 'বাংলা টেক্সটাইল লিমিটেড',
            'email': 'info@banglatextile.com.bd',
            'website': 'www.banglatextile.com.bd',
            'address': 'Dhaka, Bangladesh',
            'phone': '+8801712345679'
        }
    ]
    
    for i, company in enumerate(test_companies, 1):
        print(f"\n📋 Test {i}: {company['name']}")
        
        company_info = language_detector.detect_company_origin(
            company['name'],
            company['email'],
            company['website'],
            company['address'],
            company['phone']
        )
        
        print(f"   🌍 Country: {company_info.country}")
        print(f"   🗣️ Language: {company_info.language.value}")
        print(f"   🇧🇩 Bangladeshi: {company_info.is_bangladeshi}")
        print(f"   📊 Confidence: {company_info.confidence:.1%}")

def test_bilingual_recommendations():
    """Test bilingual recommendations"""
    
    print("\n\n🎯 Testing Bilingual Recommendations")
    print("=" * 50)
    
    # Sample KPI data
    kpi_data = {
        'revenue': 45000000,
        'revenue_growth': -15.5,
        'total_customers': 150,
        'new_customers': 12,
        'churned_customers': 3,
        'churn_rate': 0.02,
        'profit': 7000000,
        'profit_margin': 0.155,
        'cost_ratio': 0.845,
        'market_share': 0.12,
        'customer_satisfaction': 85
    }
    
    # Test Bangla recommendations
    print("\n🇧🇩 Bangla Recommendations:")
    bangla_recs = bilingual_decision_engine.generate_recommendations(
        kpi_data, Language.BANGLA
    )
    
    for i, rec in enumerate(bangla_recs[:3], 1):
        formatted_rec = bilingual_decision_engine.format_recommendation_for_display(rec, Language.BANGLA)
        print(f"\n   {i}. {formatted_rec['title']}")
        print(f"      {formatted_rec['description']}")
        print(f"      🎯 Priority: {formatted_rec['priority']}")
        print(f"      📈 Impact: {formatted_rec['impact_score']:.2f}")
        print(f"      🚀 Action: {formatted_rec['action']}")
    
    # Test English recommendations
    print("\n🌍 English Recommendations:")
    english_recs = bilingual_decision_engine.generate_recommendations(
        kpi_data, Language.ENGLISH
    )
    
    for i, rec in enumerate(english_recs[:3], 1):
        formatted_rec = bilingual_decision_engine.format_recommendation_for_display(rec, Language.ENGLISH)
        print(f"\n   {i}. {formatted_rec['title']}")
        print(f"      {formatted_rec['description']}")
        print(f"      🎯 Priority: {formatted_rec['priority']}")
        print(f"      📈 Impact: {formatted_rec['impact_score']:.2f}")
        print(f"      🚀 Action: {formatted_rec['action']}")

def test_with_sample_data():
    """Test with sample CSV data"""
    
    print("\n\n📊 Testing with Sample Data")
    print("=" * 50)
    
    # Load sample data
    try:
        df = pd.read_csv('backend/test_bilingual_data.csv')
        print(f"✅ Loaded {len(df)} companies from test data")
        
        # Detect languages for all companies
        companies = language_detector.detect_from_dataframe(df)
        
        bangla_count = sum(1 for c in companies if c.language == Language.BANGLA)
        english_count = sum(1 for c in companies if c.language == Language.ENGLISH)
        
        print(f"\n📈 Language Detection Results:")
        print(f"   🇧🇩 Bangladeshi companies: {bangla_count}")
        print(f"   🌍 International companies: {english_count}")
        
        print(f"\n🏢 Company Breakdown:")
        for company in companies:
            flag = "🇧🇩" if company.language == Language.BANGLA else "🌍"
            print(f"   {flag} {company.name} ({company.country})")
        
    except FileNotFoundError:
        print("❌ Sample data file not found. Please ensure 'backend/test_bilingual_data.csv' exists.")
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")

def main():
    """Main test function"""
    
    print("🧪 Bilingual Dashboard Test Suite")
    print("=" * 60)
    
    # Run all tests
    test_language_detection()
    test_bilingual_recommendations()
    test_with_sample_data()
    
    print("\n\n✅ All tests completed!")
    print("\n🚀 To run the bilingual dashboard:")
    print("   cd backend")
    print("   streamlit run bilingual_streamlit_dashboard.py")
    print("\n📤 Test with the sample data file: backend/test_bilingual_data.csv")

if __name__ == "__main__":
    main()
