#!/usr/bin/env python3
"""
Executive Business Health Dashboard - FastAPI Backend
Provides comprehensive business analytics and AI-powered insights
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .services.data_generator import BusinessDataGenerator
from .services.kpi_calculator import KPICalculator
from .services.health_scorer import HealthScorer
from .services.insight_engine import InsightEngine
from .services.ai_insight_engine import AIInsightEngine
from .services.business_analyzer import BusinessAnalyzer
from .models import *

# Initialize FastAPI app
app = FastAPI(
    title="Executive Business Health Dashboard API",
    description="Comprehensive business analytics and AI-powered insights",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_generator = BusinessDataGenerator()
kpi_calculator = KPICalculator()
health_scorer = HealthScorer()
insight_engine = InsightEngine()
ai_insight_engine = AIInsightEngine()
business_analyzer = BusinessAnalyzer()

# Health check endpoint
@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Executive Business Health Dashboard"
    }

# Complete dashboard data endpoint
@app.get("/api/dashboard/complete", response_model=CompleteDashboardResponse)
async def get_complete_dashboard():
    """Get complete dashboard data including KPIs, health scores, and insights"""
    try:
        # Generate comprehensive business data
        raw_data = data_generator.generate_comprehensive_business_data()
        
        # Calculate KPIs
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        
        # Calculate health scores
        health_scores = health_scorer.calculate_overall_health(kpis)
        
        # Generate insights
        insights = insight_engine.generate_insights(kpis, raw_data)
        
        # Generate AI-powered insights
        ai_insights = ai_insight_engine.generate_insights_with_ai(kpis, raw_data)
        
        # Business analysis
        business_analysis = business_analyzer.analyze_business_performance(raw_data, kpis)
        
        return CompleteDashboardResponse(
            kpis=kpis,
            health_scores=health_scores,
            insights=insights,
            ai_insights=ai_insights,
            business_analysis=business_analysis,
            last_updated=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# KPIs endpoint
@app.get("/api/kpis", response_model=List[KPIData])
async def get_kpis():
    """Get all KPIs"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        return kpis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health scores endpoint
@app.get("/api/health-scores", response_model=Dict[str, Any])
async def get_health_scores():
    """Get health scores for all KPIs"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        health_scores = health_scorer.calculate_overall_health(kpis)
        return health_scores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Insights endpoint
@app.get("/api/insights", response_model=List[Insight])
async def get_insights():
    """Get business insights"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        insights = insight_engine.generate_insights(kpis, raw_data)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI-powered insights endpoint
@app.get("/api/ai/insights", response_model=List[Insight])
async def get_ai_insights():
    """Get AI-powered business insights"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        ai_insights = ai_insight_engine.generate_insights_with_ai(kpis, raw_data)
        return ai_insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI executive summary endpoint
@app.get("/api/ai/executive-summary", response_model=ExecutiveSummary)
async def get_ai_executive_summary():
    """Get AI-generated executive summary"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        ai_insights = ai_insight_engine.generate_insights_with_ai(kpis, raw_data)
        ai_summary = ai_insight_engine.generate_executive_summary_with_ai(ai_insights, kpis)
        return ai_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Business analysis endpoint
@app.get("/api/business-analysis", response_model=Dict[str, Any])
async def get_business_analysis():
    """Get comprehensive business analysis"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        kpis = kpi_calculator.calculate_all_kpis(raw_data)
        business_analysis = business_analyzer.analyze_business_performance(raw_data, kpis)
        return business_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Customer segmentation endpoint
@app.get("/api/customer-segmentation", response_model=Dict[str, Any])
async def get_customer_segmentation():
    """Get customer segmentation analysis"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        segmentation = business_analyzer.analyze_customer_segments(raw_data['customers'])
        return segmentation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Trend analysis endpoint
@app.get("/api/trend-analysis", response_model=Dict[str, Any])
async def get_trend_analysis():
    """Get trend analysis"""
    try:
        raw_data = data_generator.generate_comprehensive_business_data()
        trends = business_analyzer.analyze_trends(raw_data['sales'])
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Set Hugging Face token for AI features (load from environment)
    hf_token = os.getenv('HF_TOKEN')
    if hf_token:
        os.environ['HF_TOKEN'] = hf_token
    
    print("🚀 Starting Executive Business Health Dashboard Backend...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("🤖 AI Insights: http://localhost:8000/api/ai/insights")
    print("📊 AI Executive Summary: http://localhost:8000/api/ai/executive-summary")
    print("⚡ Dashboard API: http://localhost:8000/api/dashboard/complete")
    print("\n" + "="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
