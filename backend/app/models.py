from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class KPIId(str, Enum):
    REVENUE = "revenue"
    REVENUE_GROWTH = "revenue-growth"
    PROFIT_MARGIN = "profit-margin"
    EXPENSE_RATIO = "expense-ratio"
    CUSTOMER_HEALTH = "customer-health"
    CHURN_RATE = "churn-rate"
    CLV = "clv"
    CAC = "cac"
    LTV_CAC_RATIO = "ltv-cac-ratio"
    MRR = "mrr"
    ARR = "arr"
    NPS = "nps"
    CSAT = "csat"
    OPERATIONAL_EFFICIENCY = "operational-efficiency"
    EMPLOYEE_SATISFACTION = "employee-satisfaction"
    MARKET_SHARE = "market-share"

class HealthStatus(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"

class TrendDirection(str, Enum):
    UP = "up"
    DOWN = "down"
    STABLE = "stable"

class KPICategory(str, Enum):
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    CUSTOMER = "customer"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ActionType(str, Enum):
    INCREASE = "increase"
    REDUCE = "reduce"
    INVESTIGATE = "investigate"
    PRIORITIZE = "prioritize"
    MAINTAIN = "maintain"

class Timeframe(str, Enum):
    IMMEDIATE = "immediate"
    SHORT_TERM = "short-term"
    LONG_TERM = "long-term"

class Effort(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Severity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class HistoricalValue(BaseModel):
    period: str = Field(..., description="Time period (e.g., '2024-08')")
    value: float = Field(..., description="KPI value for the period")

class KPIData(BaseModel):
    id: KPIId = Field(..., description="Unique KPI identifier")
    current_value: float = Field(..., description="Current KPI value")
    previous_value: float = Field(..., description="Previous period value")
    target_value: float = Field(..., description="Target or goal value")
    trend: TrendDirection = Field(..., description="Current trend direction")
    health_status: HealthStatus = Field(..., description="Current health status")
    last_updated: str = Field(..., description="Last update timestamp")
    historical_values: List[HistoricalValue] = Field(default_factory=list, description="Historical values")

class Insight(BaseModel):
    id: str = Field(..., description="Unique insight identifier")
    kpi_id: KPIId = Field(..., description="Related KPI")
    title: str = Field(..., description="Insight title")
    observation: str = Field(..., description="What: factual metric behavior")
    business_impact: str = Field(..., description="So What: why leadership should care")
    action: str = Field(..., description="Now What: decision or follow-up")
    priority: Priority = Field(..., description="Insight priority level")
    generated_at: str = Field(..., description="Generation timestamp")
    is_auto_generated: bool = Field(default=True, description="Auto-generated flag")

class RiskIndicator(BaseModel):
    id: str = Field(..., description="Unique risk identifier")
    kpi_id: KPIId = Field(..., description="Related KPI")
    status: HealthStatus = Field(..., description="Risk status")
    title: str = Field(..., description="Risk title")
    explanation: str = Field(..., description="Detailed risk explanation")
    threshold_logic: str = Field(..., description="Threshold logic description")
    consecutive_periods: int = Field(..., description="Number of consecutive periods")
    severity: Severity = Field(..., description="Risk severity level")

class Recommendation(BaseModel):
    id: str = Field(..., description="Unique recommendation identifier")
    insight_id: str = Field(..., description="Related insight")
    kpi_id: KPIId = Field(..., description="Related KPI")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed recommendation")
    action_type: ActionType = Field(..., description="Type of action needed")
    expected_impact: str = Field(..., description="Expected business impact")
    timeframe: Timeframe = Field(..., description="Implementation timeframe")
    effort: Effort = Field(..., description="Implementation effort")
    confidence: Confidence = Field(..., description="Confidence level")

class BusinessRisk(BaseModel):
    title: str = Field(..., description="Risk title")
    description: str = Field(..., description="Risk description")
    kpi_id: KPIId = Field(..., description="Related KPI")

class BusinessOpportunity(BaseModel):
    title: str = Field(..., description="Opportunity title")
    description: str = Field(..., description="Opportunity description")
    kpi_id: KPIId = Field(..., description="Related KPI")

class ExecutiveSummary(BaseModel):
    id: str = Field(..., description="Unique summary identifier")
    period: str = Field(..., description="Reporting period")
    overall_health: HealthStatus = Field(..., description="Overall business health")
    key_highlights: List[str] = Field(..., description="Key highlights")
    top_risks: List[BusinessRisk] = Field(..., description="Top identified risks")
    top_opportunities: List[BusinessOpportunity] = Field(..., description="Top opportunities")
    narrative: str = Field(..., description="Executive narrative")
    generated_at: str = Field(..., description="Generation timestamp")

class HealthFactor(BaseModel):
    category: str = Field(..., description="Factor category")
    score: float = Field(..., description="Factor score (0-100)")
    weight: float = Field(..., description="Factor weight in overall score")

class BusinessHealthScore(BaseModel):
    overall: float = Field(..., description="Overall health score (0-100)")
    financial: float = Field(..., description="Financial health score")
    operational: float = Field(..., description="Operational health score")
    customer: float = Field(..., description="Customer health score")
    status: HealthStatus = Field(..., description="Overall health status")
    factors: List[HealthFactor] = Field(..., description="Contributing factors")

class DashboardData(BaseModel):
    kpis: List[KPIData] = Field(..., description="All KPI data")
    insights: List[Insight] = Field(..., description="Business insights")
    risks: List[RiskIndicator] = Field(..., description="Risk indicators")
    recommendations: List[Recommendation] = Field(..., description="Recommendations")
    executive_summary: ExecutiveSummary = Field(..., description="Executive summary")
    business_health_score: BusinessHealthScore = Field(..., description="Business health score")
    last_updated: str = Field(..., description="Last update timestamp")

# Data generation models
class CustomerData(BaseModel):
    customer_id: str
    acquisition_date: str
    total_revenue: float
    order_count: int
    last_order_date: str
    segment: str
    region: str
    satisfaction_score: Optional[float] = None
    churn_probability: Optional[float] = None

class SalesTransaction(BaseModel):
    transaction_id: str
    customer_id: str
    date: str
    amount: float
    product_category: str
    region: str
    margin: float

class ExpenseData(BaseModel):
    expense_id: str
    category: str
    amount: float
    date: str
    description: str
    department: str
    is_fixed: bool

class MarketingSpend(BaseModel):
    campaign_id: str
    channel: str
    amount: float
    date: str
    leads_generated: int
    conversion_rate: float

# Analysis result models
class CustomerSegment(BaseModel):
    segment_name: str
    customer_count: int
    avg_revenue: float
    avg_order_value: float
    churn_rate: float
    characteristics: Dict[str, Any]

class RevenueTrend(BaseModel):
    period: str
    revenue: float
    growth_rate: float
    new_customers: int
    expansion_revenue: float
    churn_revenue: float

class ExpenseBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float
    trend: str
    budget_variance: float

# API Response wrapper
class APIResponse(BaseModel):
    data: Any
    success: bool
    message: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
