#!/usr/bin/env python3
"""
Simple backend for Executive Dashboard
Provides mock data for testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

app = FastAPI(title="Simple Dashboard Backend", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Executive Dashboard Backend API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "dashboard": "/api/dashboard/complete",
            "ai_insights": "/api/ai/insights",
            "ai_summary": "/api/ai/executive-summary",
            "analytics": {
                "customer_segments": "/api/analytics/customer-segments",
                "revenue_trends": "/api/analytics/revenue-trends",
                "expense_breakdown": "/api/analytics/expense-breakdown"
            }
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Simple Dashboard Backend"
    }

@app.post("/api/dashboard/refresh")
async def refresh_dashboard():
    """Refresh dashboard data"""
    dashboard_data = await get_complete_dashboard()
    return {
        "success": True,
        "message": "Dashboard data refreshed successfully",
        "data": dashboard_data
    }

@app.get("/api/dashboard/complete")
async def get_complete_dashboard():
    """Get complete dashboard data with mock values"""
    
    # Mock KPIs data
    kpis = [
        {
            "id": "revenue",
            "name": "Monthly Revenue",
            "current_value": 125000,
            "target_value": 150000,
            "previous_value": 118000,
            "unit": "currency",
            "category": "financial",
            "health_status": "good",
            "trend_direction": "up",
            "historical_values": [
                {"date": "2024-01", "value": 100000},
                {"date": "2024-02", "value": 108000},
                {"date": "2024-03", "value": 115000},
                {"date": "2024-04", "value": 118000},
                {"date": "2024-05", "value": 125000}
            ]
        },
        {
            "id": "profit-margin",
            "name": "Profit Margin",
            "current_value": 18.5,
            "target_value": 20.0,
            "previous_value": 17.2,
            "unit": "percentage",
            "category": "financial",
            "health_status": "good",
            "trend_direction": "up",
            "historical_values": [
                {"date": "2024-01", "value": 15.2},
                {"date": "2024-02", "value": 16.1},
                {"date": "2024-03", "value": 16.8},
                {"date": "2024-04", "value": 17.2},
                {"date": "2024-05", "value": 18.5}
            ]
        },
        {
            "id": "customer-count",
            "name": "Total Customers",
            "current_value": 1250,
            "target_value": 1500,
            "previous_value": 1180,
            "unit": "count",
            "category": "customer",
            "health_status": "good",
            "trend_direction": "up",
            "historical_values": [
                {"date": "2024-01", "value": 980},
                {"date": "2024-02", "value": 1040},
                {"date": "2024-03", "value": 1110},
                {"date": "2024-04", "value": 1180},
                {"date": "2024-05", "value": 1250}
            ]
        },
        {
            "id": "churn-rate",
            "name": "Customer Churn Rate",
            "current_value": 3.2,
            "target_value": 2.5,
            "previous_value": 3.8,
            "unit": "percentage",
            "category": "customer",
            "health_status": "warning",
            "trend_direction": "down",
            "historical_values": [
                {"date": "2024-01", "value": 4.5},
                {"date": "2024-02", "value": 4.2},
                {"date": "2024-03", "value": 3.9},
                {"date": "2024-04", "value": 3.8},
                {"date": "2024-05", "value": 3.2}
            ]
        }
    ]
    
    # Mock health scores
    health_scores = {
        "overall": 78,
        "financial": 82,
        "customer": 75,
        "operational": 77,
        "status": "good"
    }
    
    # Mock insights
    insights = [
        {
            "id": "insight-1",
            "title": "Revenue Growth Trending Positive",
            "category": "financial",
            "priority": "high",
            "observation": "Monthly revenue has increased by 5.9% compared to last month",
            "business_impact": "Positive trajectory indicates effective sales strategies",
            "action": "Continue current sales initiatives and explore scaling opportunities",
            "confidence": "high",
            "source": "automated",
            "generated_at": datetime.now().isoformat()
        },
        {
            "id": "insight-2",
            "title": "Customer Acquisition Improving",
            "category": "customer",
            "priority": "medium",
            "observation": "Customer base grew by 70 new customers this month",
            "business_impact": "Expanding customer base increases future revenue potential",
            "action": "Focus on customer onboarding to ensure retention",
            "confidence": "medium",
            "source": "automated",
            "generated_at": datetime.now().isoformat()
        }
    ]
    
    # Mock AI insights
    ai_insights = [
        {
            "id": "ai-insight-1",
            "title": "AI-Generated Revenue Forecast",
            "category": "financial",
            "priority": "high",
            "description": "Based on current trends, revenue is projected to reach $135,000 next month",
            "confidence": "high",
            "source": "AI Analysis",
            "generated_at": datetime.now().isoformat()
        }
    ]
    
    # Mock business analysis
    business_analysis = {
        "executive_summary": {
            "narrative": "The business is showing positive growth across key metrics. Revenue and customer acquisition are trending upward, while churn rate is improving. Overall business health is strong.",
            "key_highlights": [
                "Revenue increased by 5.9% month-over-month",
                "Customer base grew by 5.9%",
                "Churn rate decreased by 0.6 percentage points",
                "Profit margin improved to 18.5%"
            ]
        },
        "risks": [
            {
                "id": "risk-1",
                "title": "Churn Rate Above Target",
                "severity": "medium",
                "explanation": "Current churn rate of 3.2% exceeds the target of 2.5%",
                "threshold_logic": "churn_rate > 2.5",
                "consecutive_periods": 2
            }
        ],
        "recommendations": [
            {
                "id": "rec-1",
                "title": "Focus on Customer Retention",
                "description": "Implement customer success programs to reduce churn",
                "expected_impact": "Reduce churn rate by 0.5% over next quarter",
                "timeframe": "3 months",
                "effort": "medium",
                "confidence": "high"
            }
        ]
    }
    
    return {
        "kpis": kpis,
        "health_scores": health_scores,
        "insights": insights,
        "ai_insights": ai_insights,
        "business_analysis": business_analysis,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/ai/insights")
async def get_ai_insights():
    """Get AI-powered insights"""
    dashboard_data = await get_complete_dashboard()
    return {
        "data": dashboard_data["ai_insights"]
    }

@app.get("/api/ai/executive-summary")
async def get_ai_executive_summary():
    """Get AI-generated executive summary"""
    return {
        "summary": "Business performance is strong with positive growth trends across key metrics. Revenue and customer acquisition are increasing, while operational efficiency remains stable.",
        "priorities": [
            "Maintain current revenue growth trajectory",
            "Focus on reducing customer churn",
            "Explore opportunities for profit margin improvement",
            "Scale successful customer acquisition strategies"
        ],
        "health_assessment": "good",
        "source": "AI Executive Analysis"
    }

@app.get("/api/analytics/customer-segments")
async def get_customer_segments():
    """Get customer segmentation analysis"""
    return {
        "data": {
            "segments": [
                {
                    "segment_name": "Enterprise",
                    "customer_count": 125,
                    "avg_revenue": 50000,
                    "avg_order_value": 5000,
                    "churn_rate": 0.05,
                    "characteristics": {"size": "large", "industry": "technology"}
                },
                {
                    "segment_name": "Mid-Market",
                    "customer_count": 312,
                    "avg_revenue": 15000,
                    "avg_order_value": 1500,
                    "churn_rate": 0.08,
                    "characteristics": {"size": "medium", "industry": "varied"}
                },
                {
                    "segment_name": "Small Business",
                    "customer_count": 500,
                    "avg_revenue": 3000,
                    "avg_order_value": 300,
                    "churn_rate": 0.12,
                    "characteristics": {"size": "small", "industry": "retail"}
                },
                {
                    "segment_name": "Startup",
                    "customer_count": 313,
                    "avg_revenue": 500,
                    "avg_order_value": 50,
                    "churn_rate": 0.20,
                    "characteristics": {"size": "small", "industry": "technology"}
                }
            ]
        }
    }

@app.get("/api/analytics/revenue-trends")
async def get_revenue_trends():
    """Get revenue trend analysis"""
    return {
        "data": {
            "monthly_trends": [
                {"month_str": "Jan", "revenue": 100000, "revenue_growth": 0.0},
                {"month_str": "Feb", "revenue": 108000, "revenue_growth": 8.0},
                {"month_str": "Mar", "revenue": 115000, "revenue_growth": 6.5},
                {"month_str": "Apr", "revenue": 118000, "revenue_growth": 2.6},
                {"month_str": "May", "revenue": 125000, "revenue_growth": 5.9}
            ]
        }
    }

@app.get("/api/analytics/expense-breakdown")
async def get_expense_breakdown():
    """Get expense breakdown analysis"""
    return {
        "data": {
            "category_breakdown": [
                {"category": "Salaries", "total_amount": 45000, "percentage": 36.0},
                {"category": "Marketing", "total_amount": 25000, "percentage": 20.0},
                {"category": "Operations", "total_amount": 20000, "percentage": 16.0},
                {"category": "Technology", "total_amount": 15000, "percentage": 12.0},
                {"category": "Office", "total_amount": 10000, "percentage": 8.0},
                {"category": "Other", "total_amount": 10000, "percentage": 8.0}
            ],
            "budget_analysis": [
                {"category": "Salaries", "variance_percentage": 2.0},
                {"category": "Marketing", "variance_percentage": -5.0},
                {"category": "Operations", "variance_percentage": 1.5},
                {"category": "Technology", "variance_percentage": 8.0},
                {"category": "Office", "variance_percentage": -3.0},
                {"category": "Other", "variance_percentage": 0.0}
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Simple Dashboard Backend...")
    print("📍 API Documentation: http://localhost:8001/docs")
    print("🔗 Health Check: http://localhost:8001/health")
    print("⚡ Dashboard API: http://localhost:8001/api/dashboard/complete")
    print("\n" + "="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
