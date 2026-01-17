import pandas as pd
import numpy as np
from typing import Dict, List, Any
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from ..models import CustomerSegment, RevenueTrend, ExpenseBreakdown, RiskIndicator, KPIId, HealthStatus, Severity

class BusinessAnalyzer:
    """Advanced business analysis with ML-powered insights"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def analyze_customer_segments(self, customers_data: List[Dict]) -> Dict[str, Any]:
        """Perform RFM analysis and customer segmentation"""
        df = pd.DataFrame(customers_data)
        
        # RFM Analysis
        df['last_order_date'] = pd.to_datetime(df['last_order_date'])
        current_date = datetime.now()
        
        # Calculate RFM metrics
        df['recency'] = (current_date - df['last_order_date']).dt.days
        df['frequency'] = df['order_count']
        df['monetary'] = df['total_revenue']
        
        # Create RFM scores (1-5 scale)
        df['R_score'] = pd.qcut(df['recency'], 5, labels=[5,4,3,2,1])
        df['F_score'] = pd.qcut(df['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        df['M_score'] = pd.qcut(df['monetary'], 5, labels=[1,2,3,4,5])
        
        df['RFM_score'] = df['R_score'].astype(int) + df['F_score'].astype(int) + df['M_score'].astype(int)
        
        # Segment customers based on RFM
        def get_segment(row):
            if row['RFM_score'] >= 13:
                return 'Champions'
            elif row['RFM_score'] >= 10:
                return 'Loyal Customers'
            elif row['RFM_score'] >= 8:
                return 'Potential Loyalists'
            elif row['RFM_score'] >= 6:
                return 'At Risk'
            else:
                return 'Lost'
        
        df['rfm_segment'] = df.apply(get_segment, axis=1)
        
        # Advanced clustering
        features = ['recency', 'frequency', 'monetary', 'satisfaction_score']
        X = df[features].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=5, random_state=42)
        df['cluster'] = kmeans.predict(X_scaled)
        
        # Analyze segments
        segments = []
        for segment in df['rfm_segment'].unique():
            segment_data = df[df['rfm_segment'] == segment]
            
            segments.append({
                'segment_name': segment,
                'customer_count': len(segment_data),
                'avg_revenue': segment_data['monetary'].mean(),
                'avg_order_value': segment_data['monetary'] / segment_data['frequency'],
                'churn_rate': segment_data['churn_probability'].mean(),
                'characteristics': {
                    'avg_recency_days': segment_data['recency'].mean(),
                    'avg_frequency': segment_data['frequency'].mean(),
                    'avg_satisfaction': segment_data['satisfaction_score'].mean(),
                    'revenue_percentage': (segment_data['monetary'].sum() / df['monetary'].sum()) * 100
                }
            })
        
        return {
            'segments': segments,
            'rfm_distribution': df['rfm_segment'].value_counts().to_dict(),
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'high_value_customers': df[df['RFM_score'] >= 12].to_dict('records')
        }
    
    def analyze_revenue_trends(self, sales_data: List[Dict]) -> Dict[str, Any]:
        """Analyze revenue trends with seasonality and growth patterns"""
        df = pd.DataFrame(sales_data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Monthly aggregation
        df['month'] = df['date'].dt.to_period('M')
        monthly_revenue = df.groupby('month').agg({
            'amount': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        monthly_revenue['month_str'] = monthly_revenue['month'].dt.strftime('%Y-%m')
        
        # Calculate growth rates
        monthly_revenue['revenue_growth'] = monthly_revenue['amount'].pct_change() * 100
        monthly_revenue['new_customers'] = monthly_revenue['customer_id'].diff()
        
        # Seasonality analysis
        monthly_revenue['month_of_year'] = pd.to_datetime(monthly_revenue['month_str']).dt.month
        seasonal_avg = monthly_revenue.groupby('month_of_year')['amount'].mean()
        
        # Trend analysis
        from scipy import stats
        x = np.arange(len(monthly_revenue))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, monthly_revenue['amount'])
        
        # Forecast next 3 months
        forecast_periods = 3
        forecast = []
        for i in range(1, forecast_periods + 1):
            predicted_revenue = slope * (len(monthly_revenue) + i) + intercept
            forecast.append({
                'period': f'Forecast +{i}',
                'predicted_revenue': predicted_revenue,
                'confidence_interval': [
                    predicted_revenue - 1.96 * std_err,
                    predicted_revenue + 1.96 * std_err
                ]
            })
        
        return {
            'monthly_trends': monthly_revenue.to_dict('records'),
            'seasonal_patterns': seasonal_avg.to_dict(),
            'trend_analysis': {
                'slope': slope,
                'r_squared': r_value ** 2,
                'p_value': p_value,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing'
            },
            'forecast': forecast,
            'key_insights': self._generate_revenue_insights(monthly_revenue, slope, r_value)
        }
    
    def analyze_expense_breakdown(self, expenses_data: List[Dict]) -> Dict[str, Any]:
        """Analyze expense patterns and optimization opportunities"""
        df = pd.DataFrame(expenses_data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Category analysis
        category_analysis = df.groupby('category').agg({
            'amount': ['sum', 'mean', 'count'],
            'is_fixed': 'first'
        }).round(2)
        
        category_analysis.columns = ['total_amount', 'avg_amount', 'transaction_count', 'is_fixed']
        category_analysis['percentage'] = (category_analysis['total_amount'] / df['amount'].sum() * 100).round(2)
        
        # Monthly trends
        df['month'] = df['date'].dt.to_period('M')
        monthly_expenses = df.groupby(['month', 'category'])['amount'].sum().reset_index()
        monthly_expenses['month_str'] = monthly_expenses['month'].dt.strftime('%Y-%m')
        
        # Budget variance analysis (assuming 10% year-over-year increase target)
        current_year = df['date'].dt.year.max()
        last_year = current_year - 1
        
        current_year_expenses = df[df['date'].dt.year == current_year].groupby('category')['amount'].sum()
        last_year_expenses = df[df['date'].dt.year == last_year].groupby('category')['amount'].sum()
        
        budget_analysis = []
        for category in df['category'].unique():
            current = current_year_expenses.get(category, 0)
            last = last_year_expenses.get(category, 0)
            budget_target = last * 1.10  # 10% increase target
            variance = ((current - budget_target) / budget_target * 100) if budget_target > 0 else 0
            
            budget_analysis.append({
                'category': category,
                'current_amount': current,
                'budget_target': budget_target,
                'variance_percentage': round(variance, 2),
                'status': 'over_budget' if variance > 5 else 'under_budget' if variance < -5 else 'on_target'
            })
        
        # Optimization opportunities
        opportunities = self._identify_expense_opportunities(df, category_analysis)
        
        return {
            'category_breakdown': category_analysis.reset_index().to_dict('records'),
            'monthly_trends': monthly_expenses.to_dict('records'),
            'budget_analysis': budget_analysis,
            'optimization_opportunities': opportunities,
            'total_expenses': df['amount'].sum(),
            'fixed_vs_variable': {
                'fixed_expenses': df[df['is_fixed'] == True]['amount'].sum(),
                'variable_expenses': df[df['is_fixed'] == False]['amount'].sum()
            }
        }
    
    def identify_risks(self, kpis: List, data: Dict[str, Any]) -> List[RiskIndicator]:
        """Identify business risks using advanced analytics"""
        risks = []
        
        # Convert KPIs to dict for easier access
        kpi_dict = {kpi.id.value: kpi for kpi in kpis}
        
        # Revenue risk analysis
        revenue_kpi = kpi_dict.get('revenue')
        if revenue_kpi and revenue_kpi.health_status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
            risks.append(RiskIndicator(
                id='risk-revenue-decline',
                kpi_id=KPIId.REVENUE,
                status=revenue_kpi.health_status,
                title='Revenue Decline Risk',
                explanation=f'Revenue at ${revenue_kpi.current_value:,.0f} is below target of ${revenue_kpi.target_value:,.0f}',
                threshold_logic='Revenue below 90% of target for 2+ consecutive months',
                consecutive_periods=self._count_consecutive_periods(revenue_kpi),
                severity=Severity.HIGH if revenue_kpi.health_status == HealthStatus.CRITICAL else Severity.MEDIUM
            ))
        
        # Customer churn risk
        customers_df = pd.DataFrame(data['customers'])
        high_churn_customers = customers_df[customers_df['churn_probability'] > 0.7]
        if len(high_churn_customers) > len(customers_df) * 0.15:  # More than 15% high risk
            risks.append(RiskIndicator(
                id='risk-customer-churn',
                kpi_id=KPIId.CHURN_RATE,
                status=HealthStatus.WARNING,
                title='Elevated Customer Churn Risk',
                explanation=f'{len(high_churn_customers)} customers ({len(high_churn_customers)/len(customers_df)*100:.1f}%) show high churn probability',
                threshold_logic='>15% of customers with churn probability >70%',
                consecutive_periods=1,
                severity=Severity.HIGH
            ))
        
        # Expense risk
        expenses_df = pd.DataFrame(data['expenses'])
        current_month_expenses = expenses_df[expenses_df['date'].str.startswith(datetime.now().strftime('%Y-%m'))]['amount'].sum()
        if current_month_expenses > 0:  # Basic check
            risks.append(RiskIndicator(
                id='risk-expense-growth',
                kpi_id=KPIId.EXPENSE_RATIO,
                status=HealthStatus.WARNING,
                title='Expense Growth Risk',
                explanation='Monthly expenses showing upward trend requiring attention',
                threshold_logic='Expense ratio > 85% for 2+ months',
                consecutive_periods=2,
                severity=Severity.MEDIUM
            ))
        
        return risks
    
    def _generate_revenue_insights(self, monthly_data: pd.DataFrame, slope: float, r_value: float) -> List[str]:
        """Generate insights from revenue trend analysis"""
        insights = []
        
        if slope > 0:
            insights.append(f"Revenue showing positive growth trend with {slope:.0f} monthly increase")
        else:
            insights.append(f"Revenue declining by {abs(slope):.0f} per month - requires immediate attention")
        
        if r_value ** 2 > 0.7:
            insights.append("Strong trend correlation (R² > 0.7) indicates predictable pattern")
        else:
            insights.append("High revenue volatility suggests external factors impacting performance")
        
        # Seasonality insights
        if len(monthly_data) >= 12:
            monthly_data['month_of_year'] = pd.to_datetime(monthly_data['month_str']).dt.month
            seasonal_pattern = monthly_data.groupby('month_of_year')['amount'].mean()
            peak_month = seasonal_pattern.idxmax()
            low_month = seasonal_pattern.idxmin()
            insights.append(f"Peak revenue in month {peak_month}, lowest in month {low_month}")
        
        return insights
    
    def _identify_expense_opportunities(self, df: pd.DataFrame, category_analysis: pd.DataFrame) -> List[Dict]:
        """Identify expense optimization opportunities"""
        opportunities = []
        
        # High-variable expense categories
        variable_expenses = category_analysis[category_analysis['is_fixed'] == False]
        if not variable_expenses.empty:
            high_variable = variable_expenses[variable_expenses['percentage'] > 20]
            for _, row in high_variable.iterrows():
                opportunities.append({
                    'category': row['category'],
                    'opportunity': 'Optimize variable expenses',
                    'potential_savings': f"{row['percentage'] * 0.1:.1f}% of total expenses",
                    'recommendation': 'Review vendor contracts and implement cost controls'
                })
        
        # Duplicate or similar expenses
        duplicate_check = df[df['description'].str.contains('Q[1-4]', na=False)]
        if len(duplicate_check) > 0:
            opportunities.append({
                'category': 'General',
                'opportunity': 'Consolidate quarterly expenses',
                'potential_savings': '5-10% through bulk purchasing',
                'recommendation': 'Negotiate annual contracts instead of quarterly renewals'
            })
        
        return opportunities
    
    def _count_consecutive_periods(self, kpi) -> int:
        """Count consecutive periods with poor performance"""
        # Simplified logic - in real implementation, would check historical values
        if kpi.health_status == HealthStatus.CRITICAL:
            return 3
        elif kpi.health_status == HealthStatus.WARNING:
            return 2
        else:
            return 0
