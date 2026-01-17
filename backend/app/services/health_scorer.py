import numpy as np
from typing import List, Dict, Any
from ..models import KPIData, BusinessHealthScore, HealthFactor, HealthStatus, KPIId

class HealthScorer:
    """Calculates comprehensive business health scores using weighted metrics"""
    
    def __init__(self):
        # Define weights for different KPI categories
        self.weights = {
            'financial': {
                'revenue': 0.25,
                'revenue-growth': 0.20,
                'profit-margin': 0.25,
                'expense-ratio': 0.15,
                'mrr': 0.10,
                'arr': 0.05
            },
            'customer': {
                'customer-health': 0.25,
                'churn-rate': 0.20,
                'clv': 0.15,
                'cac': 0.10,
                'ltv-cac-ratio': 0.15,
                'nps': 0.10,
                'csat': 0.05
            },
            'operational': {
                'operational-efficiency': 0.30,
                'employee-satisfaction': 0.25,
                'market-share': 0.20,
                # Other operational KPIs would be added here
            }
        }
        
        # Normalize weights to ensure they sum to 1.0 for each category
        for category in self.weights:
            total = sum(self.weights[category].values())
            for kpi in self.weights[category]:
                self.weights[category][kpi] /= total
    
    def calculate_overall_health(self, kpis: List[KPIData], data: Dict[str, Any]) -> BusinessHealthScore:
        """Calculate comprehensive business health score"""
        
        # Convert KPIs to dictionary for easier access
        kpi_dict = {kpi.id.value: kpi for kpi in kpis}
        
        # Calculate category scores
        financial_score = self._calculate_category_score('financial', kpi_dict)
        customer_score = self._calculate_category_score('customer', kpi_dict)
        operational_score = self._calculate_category_score('operational', kpi_dict)
        
        # Calculate overall score with category weights
        category_weights = {
            'financial': 0.4,
            'customer': 0.35,
            'operational': 0.25
        }
        
        overall_score = (
            financial_score * category_weights['financial'] +
            customer_score * category_weights['customer'] +
            operational_score * category_weights['operational']
        )
        
        # Determine health status
        status = self._get_health_status(overall_score)
        
        # Create contributing factors
        factors = self._create_health_factors(kpi_dict, overall_score)
        
        return BusinessHealthScore(
            overall=round(overall_score, 1),
            financial=round(financial_score, 1),
            customer=round(customer_score, 1),
            operational=round(operational_score, 1),
            status=status,
            factors=factors
        )
    
    def _calculate_category_score(self, category: str, kpi_dict: Dict[str, KPIData]) -> float:
        """Calculate score for a specific category"""
        category_kpis = self.weights.get(category, {})
        total_score = 0
        total_weight = 0
        
        for kpi_id, weight in category_kpis.items():
            if kpi_id in kpi_dict:
                kpi = kpi_dict[kpi_id]
                kpi_score = self._normalize_kpi_score(kpi)
                total_score += kpi_score * weight
                total_weight += weight
        
        return total_score if total_weight > 0 else 50  # Default to neutral if no data
    
    def _normalize_kpi_score(self, kpi: KPIData) -> float:
        """Normalize individual KPI to 0-100 scale"""
        
        # Base score from health status
        health_scores = {
            HealthStatus.EXCELLENT: 90,
            HealthStatus.GOOD: 75,
            HealthStatus.WARNING: 50,
            HealthStatus.CRITICAL: 25
        }
        
        base_score = health_scores.get(kpi.health_status, 50)
        
        # Adjust based on performance vs target
        performance_ratio = kpi.current_value / kpi.target_value if kpi.target_value > 0 else 1
        
        # For some KPIs, lower is better (like churn rate, expense ratio)
        lower_is_better = ['churn-rate', 'expense-ratio', 'cac']
        
        if kpi.id.value in lower_is_better:
            performance_ratio = 2 - performance_ratio  # Invert for lower-is-better metrics
            performance_ratio = max(0, min(2, performance_ratio))  # Clamp to reasonable range
        
        # Adjust score based on performance
        if performance_ratio >= 1.0:
            performance_adjustment = min(10, (performance_ratio - 1.0) * 20)
        else:
            performance_adjustment = max(-15, (performance_ratio - 1.0) * 30)
        
        # Adjust based on trend
        trend_adjustment = 0
        if kpi.trend.value == 'up':
            trend_adjustment = 5
        elif kpi.trend.value == 'down':
            trend_adjustment = -5
        
        final_score = base_score + performance_adjustment + trend_adjustment
        return max(0, min(100, final_score))
    
    def _get_health_status(self, score: float) -> HealthStatus:
        """Convert numeric score to health status"""
        if score >= 80:
            return HealthStatus.EXCELLENT
        elif score >= 65:
            return HealthStatus.GOOD
        elif score >= 50:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _create_health_factors(self, kpi_dict: Dict[str, KPIData], overall_score: float) -> List[HealthFactor]:
        """Create detailed health factors for transparency"""
        factors = []
        
        # Key business drivers with their weights in overall score
        key_drivers = [
            ('Revenue Growth', self._get_kpi_score(kpi_dict.get('revenue-growth')), 0.2),
            ('Profitability', self._get_kpi_score(kpi_dict.get('profit-margin')), 0.2),
            ('Cost Efficiency', self._get_kpi_score(kpi_dict.get('expense-ratio')), 0.2),
            ('Customer Satisfaction', self._get_kpi_score(kpi_dict.get('customer-health')), 0.2),
            ('Churn Management', self._get_kpi_score(kpi_dict.get('churn-rate')), 0.1),
            ('Customer Lifetime Value', self._get_kpi_score(kpi_dict.get('clv')), 0.1)
        ]
        
        for name, score, weight in key_drivers:
            factors.append(HealthFactor(
                category=name,
                score=round(score, 1),
                weight=weight
            ))
        
        return factors
    
    def _get_kpi_score(self, kpi: KPIData) -> float:
        """Get normalized score for a single KPI"""
        if not kpi:
            return 50  # Neutral score if KPI not available
        return self._normalize_kpi_score(kpi)
    
    def calculate_health_trend(self, current_score: float, historical_scores: List[float]) -> str:
        """Analyze health score trend over time"""
        if len(historical_scores) < 2:
            return "insufficient_data"
        
        recent_avg = np.mean(historical_scores[-3:]) if len(historical_scores) >= 3 else historical_scores[-1]
        
        if current_score > recent_avg + 5:
            return "improving"
        elif current_score < recent_avg - 5:
            return "declining"
        else:
            return "stable"
    
    def identify_critical_factors(self, health_score: BusinessHealthScore) -> List[str]:
        """Identify factors most impacting overall health"""
        critical_factors = []
        
        # Find factors with scores below 60
        low_scoring_factors = [f for f in health_score.factors if f.score < 60]
        
        # Sort by impact (score * weight)
        low_scoring_factors.sort(key=lambda f: f.score * f.weight)
        
        for factor in low_scoring_factors[:3]:  # Top 3 critical factors
            critical_factors.append(
                f"{factor.category}: {factor.score}/100 (Impact: {factor.score * factor.weight:.1f})"
            )
        
        return critical_factors
    
    def generate_health_improvement_recommendations(self, health_score: BusinessHealthScore) -> List[Dict]:
        """Generate specific recommendations based on health score analysis"""
        recommendations = []
        
        # Overall health recommendations
        if health_score.overall < 50:
            recommendations.append({
                'priority': 'critical',
                'area': 'Overall Business Health',
                'recommendation': 'Immediate comprehensive review required across all business areas',
                'expected_impact': '15-25 point improvement in 6 months'
            })
        elif health_score.overall < 65:
            recommendations.append({
                'priority': 'high',
                'area': 'Business Performance',
                'recommendation': 'Focus on top 3 underperforming areas for quick wins',
                'expected_impact': '10-15 point improvement in 3 months'
            })
        
        # Category-specific recommendations
        if health_score.financial < 60:
            recommendations.append({
                'priority': 'high',
                'area': 'Financial Health',
                'recommendation': 'Implement cost optimization and revenue acceleration strategies',
                'expected_impact': '20 point improvement in financial score'
            })
        
        if health_score.customer < 60:
            recommendations.append({
                'priority': 'high',
                'area': 'Customer Health',
                'recommendation': 'Launch customer success initiatives and improve product experience',
                'expected_impact': '15 point improvement in customer score'
            })
        
        if health_score.operational < 60:
            recommendations.append({
                'priority': 'medium',
                'area': 'Operational Efficiency',
                'recommendation': 'Streamline processes and invest in productivity tools',
                'expected_impact': '10 point improvement in operational score'
            })
        
        return recommendations
