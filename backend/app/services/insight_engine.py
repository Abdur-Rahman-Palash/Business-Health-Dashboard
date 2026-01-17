import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from ..models import (
    Insight, Recommendation, ExecutiveSummary, BusinessRisk, BusinessOpportunity,
    KPIData, BusinessHealthScore, KPIId, Priority, ActionType, Timeframe, 
    Effort, Confidence, HealthStatus
)

class InsightEngine:
    """Generates AI-powered business insights and recommendations"""
    
    def __init__(self):
        self.insight_templates = self._load_insight_templates()
        self.recommendation_templates = self._load_recommendation_templates()
    
    def generate_insights(self, kpis: List[KPIData], data: Dict[str, Any]) -> List[Insight]:
        """Generate actionable business insights from KPI data"""
        insights = []
        
        # Convert KPIs to dictionary for easier access
        kpi_dict = {kpi.id.value: kpi for kpi in kpis}
        
        # Generate insights for each KPI
        for kpi in kpis:
            kpi_insights = self._generate_kpi_insights(kpi, kpi_dict, data)
            insights.extend(kpi_insights)
        
        # Generate cross-KPI insights
        cross_insights = self._generate_cross_kpi_insights(kpis, data)
        insights.extend(cross_insights)
        
        # Sort by priority and return top insights
        insights.sort(key=lambda x: self._priority_score(x.priority), reverse=True)
        
        return insights[:10]  # Return top 10 insights
    
    def generate_recommendations(self, insights: List[Insight], kpis: List[KPIData]) -> List[Recommendation]:
        """Generate actionable recommendations based on insights"""
        recommendations = []
        
        for insight in insights:
            # Generate 1-2 recommendations per high-priority insight
            if insight.priority in [Priority.HIGH, Priority.MEDIUM]:
                recs = self._generate_insight_recommendations(insight, kpis)
                recommendations.extend(recs)
        
        # Remove duplicates and sort by confidence
        unique_recommendations = self._deduplicate_recommendations(recommendations)
        unique_recommendations.sort(key=lambda x: self._confidence_score(x.confidence), reverse=True)
        
        return unique_recommendations[:8]  # Return top 8 recommendations
    
    def create_executive_summary(self, kpis: List[KPIData], insights: List[Insight], 
                               risks: List, health_score: BusinessHealthScore) -> ExecutiveSummary:
        """Create C-level executive summary"""
        
        # Key highlights
        highlights = self._generate_key_highlights(kpis, health_score)
        
        # Top risks
        top_risks = self._extract_top_risks(insights, risks)
        
        # Top opportunities
        top_opportunities = self._extract_top_opportunities(insights, kpis)
        
        # Executive narrative
        narrative = self._generate_executive_narrative(health_score, highlights, top_risks, top_opportunities)
        
        return ExecutiveSummary(
            id=f"exec-summary-{datetime.now().strftime('%Y%m%d')}",
            period=self._get_current_period(),
            overall_health=health_score.status,
            key_highlights=highlights,
            top_risks=top_risks,
            top_opportunities=top_opportunities,
            narrative=narrative,
            generated_at=datetime.now().isoformat()
        )
    
    def _generate_kpi_insights(self, kpi: KPIData, kpi_dict: Dict[str, KPIData], data: Dict[str, Any]) -> List[Insight]:
        """Generate insights for a specific KPI"""
        insights = []
        
        # Performance vs target insights
        if kpi.current_value < kpi.target_value * 0.8:
            insights.append(self._create_underperformance_insight(kpi))
        elif kpi.current_value > kpi.target_value * 1.2:
            insights.append(self._create_overperformance_insight(kpi))
        
        # Trend insights
        if kpi.trend.value == 'down' and kpi.health_status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
            insights.append(self._create_declining_trend_insight(kpi))
        elif kpi.trend.value == 'up' and kpi.health_status in [HealthStatus.GOOD, HealthStatus.EXCELLENT]:
            insights.append(self._create_positive_trend_insight(kpi))
        
        # Specific KPI insights
        if kpi.id == KPIId.REVENUE:
            insights.extend(self._generate_revenue_insights(kpi, data))
        elif kpi.id == KPIId.CHURN_RATE:
            insights.extend(self._generate_churn_insights(kpi, data))
        elif kpi.id == KPIId.PROFIT_MARGIN:
            insights.extend(self._generate_margin_insights(kpi, data))
        
        return insights
    
    def _generate_cross_kpi_insights(self, kpis: List[KPIData], data: Dict[str, Any]) -> List[Insight]:
        """Generate insights that span multiple KPIs"""
        insights = []
        
        kpi_dict = {kpi.id.value: kpi for kpi in kpis}
        
        # Revenue vs Profit Margin correlation
        revenue_kpi = kpi_dict.get('revenue')
        margin_kpi = kpi_dict.get('profit-margin')
        
        if (revenue_kpi and margin_kpi and 
            revenue_kpi.trend.value == 'down' and margin_kpi.trend.value == 'down'):
            insights.append(Insight(
                id=f"insight-revenue-margin-{datetime.now().strftime('%H%M%S')}",
                kpi_id=KPIId.REVENUE,
                title="Revenue and Margin Double Decline",
                observation="Both revenue and profit margin are declining simultaneously",
                business_impact="This indicates serious business model challenges requiring immediate strategic review",
                action="Conduct comprehensive pricing and cost structure analysis within 30 days",
                priority=Priority.HIGH,
                generated_at=datetime.now().isoformat(),
                is_auto_generated=True
            ))
        
        # Customer acquisition vs retention
        cac_kpi = kpi_dict.get('cac')
        churn_kpi = kpi_dict.get('churn-rate')
        
        if (cac_kpi and churn_kpi and 
            cac_kpi.trend.value == 'up' and churn_kpi.trend.value == 'up'):
            insights.append(Insight(
                id=f"insight-cac-churn-{datetime.now().strftime('%H%M%S')}",
                kpi_id=KPIId.CAC,
                title="Leaky Bucket Syndrome",
                observation="Customer acquisition costs are rising while churn rate increases",
                business_impact="This creates a unsustainable growth model that will impact long-term profitability",
                action="Prioritize customer retention programs and review acquisition channels immediately",
                priority=Priority.HIGH,
                generated_at=datetime.now().isoformat(),
                is_auto_generated=True
            ))
        
        return insights
    
    def _create_underperformance_insight(self, kpi: KPIData) -> Insight:
        """Create insight for underperforming KPI"""
        gap_percentage = ((kpi.target_value - kpi.current_value) / kpi.target_value * 100)
        
        return Insight(
            id=f"insight-underperform-{kpi.id.value}-{datetime.now().strftime('%H%M%S')}",
            kpi_id=kpi.id,
            title=f"{kpi.id.value.replace('-', ' ').title()} Below Target",
            observation=f"{kpi.id.value.replace('-', ' ').title()} is {gap_percentage:.1f}% below target",
            business_impact=f"This performance gap could impact overall business objectives and stakeholder confidence",
            action=f"Implement immediate improvement plan to close {gap_percentage:.1f}% performance gap",
            priority=Priority.HIGH if gap_percentage > 30 else Priority.MEDIUM,
            generated_at=datetime.now().isoformat(),
            is_auto_generated=True
        )
    
    def _generate_revenue_insights(self, kpi: KPIData, data: Dict[str, Any]) -> List[Insight]:
        """Generate revenue-specific insights"""
        insights = []
        
        if 'sales' in data:
            sales_df = pd.DataFrame(data['sales'])
            sales_df['date'] = pd.to_datetime(sales_df['date'])
            
            # Analyze revenue concentration
            revenue_by_customer = sales_df.groupby('customer_id')['amount'].sum()
            top_10_percent = revenue_by_customer.nlargest(int(len(revenue_by_customer) * 0.1)).sum()
            total_revenue = revenue_by_customer.sum()
            concentration = (top_10_percent / total_revenue) * 100
            
            if concentration > 70:  # High concentration risk
                insights.append(Insight(
                    id=f"insight-revenue-concentration-{datetime.now().strftime('%H%M%S')}",
                    kpi_id=KPIId.REVENUE,
                    title="High Customer Revenue Concentration",
                    observation=f"Top 10% of customers generate {concentration:.1f}% of revenue",
                    business_impact="High dependency on few customers increases revenue volatility and risk",
                    action="Develop customer diversification strategy and expand middle-market segment",
                    priority=Priority.MEDIUM,
                    generated_at=datetime.now().isoformat(),
                    is_auto_generated=True
                ))
        
        return insights
    
    def _generate_churn_insights(self, kpi: KPIData, data: Dict[str, Any]) -> List[Insight]:
        """Generate churn-specific insights"""
        insights = []
        
        if 'customers' in data:
            customers_df = pd.DataFrame(data['customers'])
            
            # Analyze churn by segment
            high_churn_segments = customers_df.groupby('segment')['churn_probability'].mean()
            worst_segment = high_churn_segments.idxmax()
            worst_rate = high_churn_segments.max()
            
            if worst_rate > 0.15:  # 15% churn threshold
                insights.append(Insight(
                    id=f"insight-segment-churn-{datetime.now().strftime('%H%M%S')}",
                    kpi_id=KPIId.CHURN_RATE,
                    title=f"High Churn in {worst_segment} Segment",
                    observation=f"{worst_segment} segment has {worst_rate:.1%} churn probability",
                    business_impact="Segment-specific churn indicates product-market fit or service delivery issues",
                    action=f"Conduct root cause analysis for {worst_segment} segment and implement targeted retention",
                    priority=Priority.HIGH,
                    generated_at=datetime.now().isoformat(),
                    is_auto_generated=True
                ))
        
        return insights
    
    def _generate_insight_recommendations(self, insight: Insight, kpis: List[KPIData]) -> List[Recommendation]:
        """Generate recommendations for a specific insight"""
        recommendations = []
        
        # Use templates based on insight type and KPI
        if "revenue" in insight.title.lower():
            recommendations.append(self._create_revenue_recommendation(insight))
        elif "churn" in insight.title.lower():
            recommendations.append(self._create_churn_recommendation(insight))
        elif "margin" in insight.title.lower():
            recommendations.append(self._create_margin_recommendation(insight))
        elif "cost" in insight.title.lower() or "expense" in insight.title.lower():
            recommendations.append(self._create_cost_recommendation(insight))
        else:
            recommendations.append(self._create_general_recommendation(insight))
        
        return recommendations
    
    def _create_revenue_recommendation(self, insight: Insight) -> Recommendation:
        """Create revenue-focused recommendation"""
        return Recommendation(
            id=f"rec-revenue-{datetime.now().strftime('%H%M%S')}",
            insight_id=insight.id,
            kpi_id=insight.kpi_id,
            title="Accelerate Revenue Growth Initiative",
            description="Implement comprehensive revenue acceleration program focusing on high-impact opportunities",
            action_type=ActionType.INCREASE,
            expected_impact="10-15% revenue increase within 2 quarters",
            timeframe=Timeframe.SHORT_TERM,
            effort=Effort.HIGH,
            confidence=Confidence.HIGH
        )
    
    def _create_churn_recommendation(self, insight: Insight) -> Recommendation:
        """Create churn reduction recommendation"""
        return Recommendation(
            id=f"rec-churn-{datetime.now().strftime('%H%M%S')}",
            insight_id=insight.id,
            kpi_id=insight.kpi_id,
            title="Customer Retention Excellence Program",
            description="Launch targeted customer success initiatives to reduce churn and improve satisfaction",
            action_type=ActionType.PRIORITIZE,
            expected_impact="20-30% reduction in churn rate within 6 months",
            timeframe=Timeframe.SHORT_TERM,
            effort=Effort.MEDIUM,
            confidence=Confidence.HIGH
        )
    
    def _generate_key_highlights(self, kpis: List[KPIData], health_score: BusinessHealthScore) -> List[str]:
        """Generate key highlights for executive summary"""
        highlights = []
        
        # Overall health status
        highlights.append(f"Overall business health: {health_score.status.value.upper()} ({health_score.overall}/100)")
        
        # Best performing areas
        best_category = max(['financial', 'customer', 'operational'], 
                          key=lambda x: getattr(health_score, x))
        highlights.append(f"Strongest performance: {best_category.title()} ({getattr(health_score, best_category)}/100)")
        
        # Critical issues
        critical_kpis = [kpi for kpi in kpis if kpi.health_status == HealthStatus.CRITICAL]
        if critical_kpis:
            highlights.append(f"Critical attention needed: {len(critical_kpis)} KPIs in critical state")
        
        # Positive trends
        positive_trends = [kpi for kpi in kpis if kpi.trend.value == 'up' and kpi.health_status in [HealthStatus.GOOD, HealthStatus.EXCELLENT]]
        if positive_trends:
            highlights.append(f"Positive momentum: {len(positive_trends)} KPIs showing strong upward trends")
        
        return highlights[:4]  # Return top 4 highlights
    
    def _generate_executive_narrative(self, health_score: BusinessHealthScore, 
                                     highlights: List[str], risks: List, opportunities: List) -> str:
        """Generate executive narrative"""
        
        status_descriptors = {
            HealthStatus.EXCELLENT: "strong performance across all business areas",
            HealthStatus.GOOD: "solid performance with opportunities for improvement",
            HealthStatus.WARNING: "mixed performance requiring focused attention",
            HealthStatus.CRITICAL: "significant challenges demanding immediate action"
        }
        
        narrative = f"""
Business performance shows {status_descriptors.get(health_score.status, 'mixed results')} with an overall health score of {health_score.overall}/100.

Financial health stands at {health_score.financial}/100, customer metrics at {health_score.customer}/100, and operational efficiency at {health_score.operational}/100. 

Key priorities include addressing the {len(risks)} identified risks while capitalizing on {len(opportunities)} growth opportunities. The data suggests that focused interventions in the underperforming areas could yield significant improvements within the next quarter.

Leadership should prioritize the high-impact recommendations while maintaining strong performance in existing strengths. This balanced approach will ensure sustainable growth and long-term business resilience.
        """.strip()
        
        return narrative
    
    def _priority_score(self, priority: Priority) -> int:
        """Convert priority to numeric score for sorting"""
        scores = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
        return scores.get(priority, 0)
    
    def _confidence_score(self, confidence: Confidence) -> int:
        """Convert confidence to numeric score for sorting"""
        scores = {Confidence.HIGH: 3, Confidence.MEDIUM: 2, Confidence.LOW: 1}
        return scores.get(confidence, 0)
    
    def _deduplicate_recommendations(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Remove duplicate recommendations based on title similarity"""
        seen_titles = set()
        unique_recommendations = []
        
        for rec in recommendations:
            title_key = rec.title.lower().replace(" ", "")
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _get_current_period(self) -> str:
        """Get current reporting period"""
        now = datetime.now()
        return f"Q{(now.month-1)//3 + 1} {now.year}"
    
    def _load_insight_templates(self) -> Dict:
        """Load insight templates (could be from database in production)"""
        return {}
    
    def _load_recommendation_templates(self) -> Dict:
        """Load recommendation templates (could be from database in production)"""
        return {}
    
    def _create_overperformance_insight(self, kpi: KPIData) -> Insight:
        """Create insight for overperforming KPI"""
        excess_percentage = ((kpi.current_value - kpi.target_value) / kpi.target_value * 100)
        
        return Insight(
            id=f"insight-overperform-{kpi.id.value}-{datetime.now().strftime('%H%M%S')}",
            kpi_id=kpi.id,
            title=f"{kpi.id.value.replace('-', ' ').title()} Exceeds Target",
            observation=f"{kpi.id.value.replace('-', ' ').title()} is {excess_percentage:.1f}% above target",
            business_impact=f"This exceptional performance creates opportunities for scaling and best practice sharing",
            action=f"Document success factors and consider raising targets to maintain motivation",
            priority=Priority.LOW,
            generated_at=datetime.now().isoformat(),
            is_auto_generated=True
        )
    
    def _create_declining_trend_insight(self, kpi: KPIData) -> Insight:
        """Create insight for declining trend"""
        return Insight(
            id=f"insight-declining-{kpi.id.value}-{datetime.now().strftime('%H%M%S')}",
            kpi_id=kpi.id,
            title=f"Declining {kpi.id.value.replace('-', ' ').title()} Trend",
            observation=f"{kpi.id.value.replace('-', ' ').title()} shows consistent downward trend",
            business_impact=f"Continued decline could impact overall business performance and competitive position",
            action=f"Implement immediate intervention strategy to reverse negative trend",
            priority=Priority.HIGH,
            generated_at=datetime.now().isoformat(),
            is_auto_generated=True
        )
    
    def _create_positive_trend_insight(self, kpi: KPIData) -> Insight:
        """Create insight for positive trend"""
        return Insight(
            id=f"insight-positive-{kpi.id.value}-{datetime.now().strftime('%H%M%S')}",
            kpi_id=kpi.id,
            title=f"Strong {kpi.id.value.replace('-', ' ').title()} Momentum",
            observation=f"{kpi.id.value.replace('-', ' ').title()} demonstrates consistent positive trend",
            business_impact=f"This momentum creates competitive advantage and growth opportunities",
            action=f"Scale successful practices and invest further to accelerate growth",
            priority=Priority.LOW,
            generated_at=datetime.now().isoformat(),
            is_auto_generated=True
        )
    
    def _generate_margin_insights(self, kpi: KPIData, data: Dict[str, Any]) -> List[Insight]:
        """Generate margin-specific insights"""
        insights = []
        
        if 'sales' in data and 'expenses' in data:
            sales_df = pd.DataFrame(data['sales'])
            expenses_df = pd.DataFrame(data['expenses'])
            
            # Analyze margin by product category
            margin_by_category = sales_df.groupby('product_category').apply(
                lambda x: (x['margin'].sum() / x['amount'].sum() * 100) if x['amount'].sum() > 0 else 0
            )
            
            worst_category = margin_by_category.idxmin()
            worst_margin = margin_by_category.min()
            
            if worst_margin < 10:  # Low margin threshold
                insights.append(Insight(
                    id=f"insight-low-margin-{datetime.now().strftime('%H%M%S')}",
                    kpi_id=KPIId.PROFIT_MARGIN,
                    title=f"Low Margin in {worst_category} Category",
                    observation=f"{worst_category} category has only {worst_margin:.1f}% profit margin",
                    business_impact="Low-margin categories drag overall profitability and may indicate pricing issues",
                    action=f"Review pricing strategy and cost structure for {worst_category} products",
                    priority=Priority.MEDIUM,
                    generated_at=datetime.now().isoformat(),
                    is_auto_generated=True
                ))
        
        return insights
    
    def _create_margin_recommendation(self, insight: Insight) -> Recommendation:
        """Create margin improvement recommendation"""
        return Recommendation(
            id=f"rec-margin-{datetime.now().strftime('%H%M%S')}",
            insight_id=insight.id,
            kpi_id=insight.kpi_id,
            title="Profit Margin Optimization Program",
            description="Implement comprehensive margin improvement through pricing optimization and cost management",
            action_type=ActionType.INCREASE,
            expected_impact="3-5% margin improvement within 6 months",
            timeframe=Timeframe.SHORT_TERM,
            effort=Effort.HIGH,
            confidence=Confidence.MEDIUM
        )
    
    def _create_cost_recommendation(self, insight: Insight) -> Recommendation:
        """Create cost optimization recommendation"""
        return Recommendation(
            id=f"rec-cost-{datetime.now().strftime('%H%M%S')}",
            insight_id=insight.id,
            kpi_id=insight.kpi_id,
            title="Strategic Cost Optimization Initiative",
            description="Review and optimize cost structure while maintaining quality and service levels",
            action_type=ActionType.REDUCE,
            expected_impact="5-10% cost reduction within 3 months",
            timeframe=Timeframe.SHORT_TERM,
            effort=Effort.MEDIUM,
            confidence=Confidence.MEDIUM
        )
    
    def _create_general_recommendation(self, insight: Insight) -> Recommendation:
        """Create general improvement recommendation"""
        return Recommendation(
            id=f"rec-general-{datetime.now().strftime('%H%M%S')}",
            insight_id=insight.id,
            kpi_id=insight.kpi_id,
            title="Performance Improvement Initiative",
            description="Implement targeted improvement actions based on insight analysis",
            action_type=ActionType.INVESTIGATE,
            expected_impact="Measurable improvement in key metrics",
            timeframe=Timeframe.SHORT_TERM,
            effort=Effort.MEDIUM,
            confidence=Confidence.MEDIUM
        )
    
    def _extract_top_risks(self, insights: List[Insight], risks: List) -> List[BusinessRisk]:
        """Extract top risks from insights and risk indicators"""
        top_risks = []
        
        # Get high-priority insights that indicate risks
        risk_insights = [insight for insight in insights if insight.priority == Priority.HIGH]
        
        for insight in risk_insights[:3]:  # Top 3 risk insights
            top_risks.append(BusinessRisk(
                title=insight.title,
                description=insight.observation,
                kpi_id=insight.kpi_id
            ))
        
        return top_risks
    
    def _extract_top_opportunities(self, insights: List[Insight], kpis: List[KPIData]) -> List[BusinessOpportunity]:
        """Extract top opportunities from insights and KPIs"""
        opportunities = []
        
        # Get positive insights and overperforming KPIs
        positive_insights = [insight for insight in insights if "momentum" in insight.title.lower() or "exceeds" in insight.title.lower()]
        overperforming_kpis = [kpi for kpi in kpis if kpi.current_value > kpi.target_value * 1.1]
        
        for insight in positive_insights[:2]:  # Top 2 opportunities from insights
            opportunities.append(BusinessOpportunity(
                title=insight.title,
                description=insight.business_impact,
                kpi_id=insight.kpi_id
            ))
        
        for kpi in overperforming_kpis[:1]:  # Top 1 opportunity from KPIs
            opportunities.append(BusinessOpportunity(
                title=f"Scale {kpi.id.value.replace('-', ' ').title()} Success",
                description=f"Exceptional performance in {kpi.id.value.replace('-', ' ').title()} presents scaling opportunity",
                kpi_id=kpi.id
            ))
        
        return opportunities
