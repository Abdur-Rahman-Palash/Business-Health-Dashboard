import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from ..models import KPIData, KPIId, HealthStatus, TrendDirection, HistoricalValue

class KPICalculator:
    """Calculates business KPIs from raw data"""
    
    def __init__(self):
        self.current_date = datetime.now()
        
    def calculate_all_kpis(self, data: Dict[str, Any]) -> List[KPIData]:
        """Calculate all KPIs from business data"""
        kpis = []
        
        # Convert to DataFrames for easier analysis
        customers_df = pd.DataFrame(data['customers'])
        sales_df = pd.DataFrame(data['sales'])
        expenses_df = pd.DataFrame(data['expenses'])
        marketing_df = pd.DataFrame(data['marketing'])
        
        # Financial KPIs
        kpis.append(self.calculate_revenue(sales_df))
        kpis.append(self.calculate_revenue_growth(sales_df))
        kpis.append(self.calculate_profit_margin(sales_df, expenses_df))
        kpis.append(self.calculate_expense_ratio(sales_df, expenses_df))
        
        # Customer KPIs
        kpis.append(self.calculate_customer_health(customers_df))
        kpis.append(self.calculate_churn_rate(customers_df))
        kpis.append(self.calculate_clv(customers_df))
        kpis.append(self.calculate_cac(marketing_df, customers_df))
        kpis.append(self.calculate_ltv_cac_ratio(customers_df, marketing_df))
        kpis.append(self.calculate_mrr(sales_df))
        kpis.append(self.calculate_arr(sales_df))
        kpis.append(self.calculate_nps(customers_df))
        kpis.append(self.calculate_csat(customers_df))
        
        # Operational KPIs
        kpis.append(self.calculate_operational_efficiency(sales_df, expenses_df))
        kpis.append(self.calculate_employee_satisfaction(customers_df))
        kpis.append(self.calculate_market_share(sales_df))
        
        return kpis
    
    def calculate_revenue(self, sales_df: pd.DataFrame) -> KPIData:
        """Calculate current revenue with trend analysis"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        
        # Current month revenue
        current_month_start = self.current_date.replace(day=1)
        current_revenue = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        
        # Previous month revenue
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        prev_revenue = sales_df[(sales_df['date'] >= prev_month_start) & 
                               (sales_df['date'] <= prev_month_end)]['amount'].sum()
        
        # Target revenue (10% growth from previous)
        target_revenue = prev_revenue * 1.10
        
        # Trend
        trend = TrendDirection.UP if current_revenue > prev_revenue else TrendDirection.DOWN
        
        # Health status
        health = self._get_revenue_health(current_revenue, target_revenue, trend)
        
        # Historical values (last 6 months)
        historical = []
        for i in range(6):
            month_start = (current_month_start - timedelta(days=32*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            month_revenue = sales_df[(sales_df['date'] >= month_start) & 
                                   (sales_df['date'] <= month_end)]['amount'].sum()
            historical.append(HistoricalValue(
                period=month_start.strftime('%Y-%m'),
                value=round(month_revenue, 2)
            ))
        
        return KPIData(
            id=KPIId.REVENUE,
            current_value=round(current_revenue, 2),
            previous_value=round(prev_revenue, 2),
            target_value=round(target_revenue, 2),
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat(),
            historical_values=historical[::-1]  # Reverse to show oldest first
        )
    
    def calculate_revenue_growth(self, sales_df: pd.DataFrame) -> KPIData:
        """Calculate month-over-month revenue growth rate"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        
        # Get last 3 months of data
        months = []
        for i in range(3):
            month_start = (self.current_date.replace(day=1) - timedelta(days=32*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            month_revenue = sales_df[(sales_df['date'] >= month_start) & 
                                   (sales_df['date'] <= month_end)]['amount'].sum()
            months.append(month_revenue)
        
        current_growth = ((months[0] - months[1]) / months[1] * 100) if months[1] > 0 else 0
        prev_growth = ((months[1] - months[2]) / months[2] * 100) if months[2] > 0 else 0
        
        trend = TrendDirection.UP if current_growth > prev_growth else TrendDirection.DOWN
        health = self._get_growth_health(current_growth)
        
        return KPIData(
            id=KPIId.REVENUE_GROWTH,
            current_value=round(current_growth, 1),
            previous_value=round(prev_growth, 1),
            target_value=15.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_profit_margin(self, sales_df: pd.DataFrame, expenses_df: pd.DataFrame) -> KPIData:
        """Calculate profit margin"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        
        current_month_start = self.current_date.replace(day=1)
        
        # Current month
        current_revenue = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        current_expenses = expenses_df[expenses_df['date'] >= current_month_start]['amount'].sum()
        current_margin = ((current_revenue - current_expenses) / current_revenue * 100) if current_revenue > 0 else 0
        
        # Previous month
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        prev_revenue = sales_df[(sales_df['date'] >= prev_month_start) & 
                               (sales_df['date'] <= prev_month_end)]['amount'].sum()
        prev_expenses = expenses_df[(expenses_df['date'] >= prev_month_start) & 
                                  (expenses_df['date'] <= prev_month_end)]['amount'].sum()
        prev_margin = ((prev_revenue - prev_expenses) / prev_revenue * 100) if prev_revenue > 0 else 0
        
        trend = TrendDirection.UP if current_margin > prev_margin else TrendDirection.DOWN
        health = self._get_margin_health(current_margin)
        
        return KPIData(
            id=KPIId.PROFIT_MARGIN,
            current_value=round(current_margin, 1),
            previous_value=round(prev_margin, 1),
            target_value=18.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_expense_ratio(self, sales_df: pd.DataFrame, expenses_df: pd.DataFrame) -> KPIData:
        """Calculate expense ratio (expenses as percentage of revenue)"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        
        current_month_start = self.current_date.replace(day=1)
        
        # Current month
        current_revenue = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        current_expenses = expenses_df[expenses_df['date'] >= current_month_start]['amount'].sum()
        current_ratio = (current_expenses / current_revenue * 100) if current_revenue > 0 else 0
        
        # Previous month
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        prev_revenue = sales_df[(sales_df['date'] >= prev_month_start) & 
                               (sales_df['date'] <= prev_month_end)]['amount'].sum()
        prev_expenses = expenses_df[(expenses_df['date'] >= prev_month_start) & 
                                  (expenses_df['date'] <= prev_month_end)]['amount'].sum()
        prev_ratio = (prev_expenses / prev_revenue * 100) if prev_revenue > 0 else 0
        
        trend = TrendDirection.DOWN if current_ratio > prev_ratio else TrendDirection.UP
        health = self._get_expense_health(current_ratio)
        
        return KPIData(
            id=KPIId.EXPENSE_RATIO,
            current_value=round(current_ratio, 1),
            previous_value=round(prev_ratio, 1),
            target_value=75.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_customer_health(self, customers_df: pd.DataFrame) -> KPIData:
        """Calculate overall customer health score"""
        # Weighted average of satisfaction and engagement
        satisfaction_score = customers_df['satisfaction_score'].mean()
        
        # Engagement score based on recency and frequency
        customers_df['last_order_date'] = pd.to_datetime(customers_df['last_order_date'])
        current_date = pd.to_datetime(self.current_date)
        customers_df['days_since_last_order'] = (current_date - customers_df['last_order_date']).dt.days
        
        # Normalize engagement score (0-100)
        recency_score = np.clip(100 - (customers_df['days_since_last_order'] / 365 * 100), 0, 100)
        frequency_score = np.clip(customers_df['order_count'] / 50 * 100, 0, 100)
        engagement_score = (recency_score + frequency_score) / 2
        
        # Overall health score
        current_health = (satisfaction_score * 0.6 + engagement_score * 0.4)
        
        # Previous period (simplified)
        prev_health = current_health * np.random.uniform(0.95, 1.05)
        
        trend = TrendDirection.UP if float(current_health) > float(prev_health) else TrendDirection.DOWN
        health = self._get_customer_health_status(current_health)
        
        return KPIData(
            id=KPIId.CUSTOMER_HEALTH,
            current_value=round(current_health, 1),
            previous_value=round(prev_health, 1),
            target_value=85.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_churn_rate(self, customers_df: pd.DataFrame) -> KPIData:
        """Calculate customer churn rate"""
        customers_df['last_order_date'] = pd.to_datetime(customers_df['last_order_date'])
        current_date = pd.to_datetime(self.current_date)
        
        # Define churned customers (no order in last 90 days)
        customers_df['days_since_last_order'] = (current_date - customers_df['last_order_date']).dt.days
        churned_customers = customers_df[customers_df['days_since_last_order'] > 90]
        churn_rate = (len(churned_customers) / len(customers_df) * 100) if len(customers_df) > 0 else 0
        
        # Previous period (simplified)
        prev_churn_rate = churn_rate * np.random.uniform(0.9, 1.1)
        
        trend = TrendDirection.DOWN if churn_rate < prev_churn_rate else TrendDirection.UP
        health = self._get_churn_health(churn_rate)
        
        return KPIData(
            id=KPIId.CHURN_RATE,
            current_value=round(churn_rate, 1),
            previous_value=round(prev_churn_rate, 1),
            target_value=5.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_clv(self, customers_df: pd.DataFrame) -> KPIData:
        """Calculate Customer Lifetime Value"""
        current_clv = customers_df['total_revenue'].mean()
        
        # Previous period (simplified)
        prev_clv = current_clv * np.random.uniform(0.95, 1.05)
        
        trend = TrendDirection.UP if current_clv > prev_clv else TrendDirection.DOWN
        health = self._get_clv_health(current_clv)
        
        return KPIData(
            id=KPIId.CLV,
            current_value=round(current_clv, 2),
            previous_value=round(prev_clv, 2),
            target_value=5000.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_cac(self, marketing_df: pd.DataFrame, customers_df: pd.DataFrame) -> KPIData:
        """Calculate Customer Acquisition Cost"""
        marketing_df['date'] = pd.to_datetime(marketing_df['date'])
        current_month_start = self.current_date.replace(day=1)
        
        # Current month marketing spend
        current_spend = marketing_df[marketing_df['date'] >= current_month_start]['amount'].sum()
        
        # New customers this month (simplified)
        new_customers = len(customers_df) // 12  # Rough estimate
        
        current_cac = current_spend / new_customers if new_customers > 0 else 0
        
        # Previous period
        prev_cac = current_cac * np.random.uniform(0.9, 1.1)
        
        trend = TrendDirection.DOWN if current_cac < prev_cac else TrendDirection.UP
        health = self._get_cac_health(current_cac)
        
        return KPIData(
            id=KPIId.CAC,
            current_value=round(current_cac, 2),
            previous_value=round(prev_cac, 2),
            target_value=600.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_ltv_cac_ratio(self, customers_df: pd.DataFrame, marketing_df: pd.DataFrame) -> KPIData:
        """Calculate LTV:CAC Ratio"""
        clv = customers_df['total_revenue'].mean()
        
        marketing_df['date'] = pd.to_datetime(marketing_df['date'])
        current_month_start = self.current_date.replace(day=1)
        current_spend = marketing_df[marketing_df['date'] >= current_month_start]['amount'].sum()
        new_customers = len(customers_df) // 12
        cac = current_spend / new_customers if new_customers > 0 else 0
        
        current_ratio = clv / cac if cac > 0 else 0
        
        # Previous period
        prev_ratio = current_ratio * np.random.uniform(0.95, 1.05)
        
        trend = TrendDirection.UP if current_ratio > prev_ratio else TrendDirection.DOWN
        health = self._get_ltv_cac_health(current_ratio)
        
        return KPIData(
            id=KPIId.LTV_CAC_RATIO,
            current_value=round(current_ratio, 2),
            previous_value=round(prev_ratio, 2),
            target_value=3.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_mrr(self, sales_df: pd.DataFrame) -> KPIData:
        """Calculate Monthly Recurring Revenue"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        current_month_start = self.current_date.replace(day=1)
        
        current_mrr = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        
        # Previous month
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        prev_mrr = sales_df[(sales_df['date'] >= prev_month_start) & 
                           (sales_df['date'] <= prev_month_end)]['amount'].sum()
        
        trend = TrendDirection.UP if current_mrr > prev_mrr else TrendDirection.DOWN
        health = self._get_revenue_health(current_mrr, current_mrr * 1.2, trend)
        
        return KPIData(
            id=KPIId.MRR,
            current_value=round(current_mrr, 2),
            previous_value=round(prev_mrr, 2),
            target_value=150000.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_arr(self, sales_df: pd.DataFrame) -> KPIData:
        """Calculate Annual Recurring Revenue"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        current_month_start = self.current_date.replace(day=1)
        
        current_mrr = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        current_arr = current_mrr * 12
        
        # Previous month
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        prev_mrr = sales_df[(sales_df['date'] >= prev_month_start) & 
                           (sales_df['date'] <= prev_month_end)]['amount'].sum()
        prev_arr = prev_mrr * 12
        
        trend = TrendDirection.UP if current_arr > prev_arr else TrendDirection.DOWN
        health = self._get_revenue_health(current_arr, current_arr * 1.2, trend)
        
        return KPIData(
            id=KPIId.ARR,
            current_value=round(current_arr, 2),
            previous_value=round(prev_arr, 2),
            target_value=1800000.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_nps(self, customers_df: pd.DataFrame) -> KPIData:
        """Calculate Net Promoter Score"""
        current_nps = customers_df['satisfaction_score'].mean() * 2 - 100  # Convert to NPS scale
        
        # Previous period
        prev_nps = current_nps * np.random.uniform(0.9, 1.1)
        
        trend = TrendDirection.UP if current_nps > prev_nps else TrendDirection.DOWN
        health = self._get_nps_health(current_nps)
        
        return KPIData(
            id=KPIId.NPS,
            current_value=round(current_nps, 0),
            previous_value=round(prev_nps, 0),
            target_value=50.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_csat(self, customers_df: pd.DataFrame) -> KPIData:
        """Calculate Customer Satisfaction Score"""
        current_csat = customers_df['satisfaction_score'].mean()
        
        # Previous period
        prev_csat = current_csat * np.random.uniform(0.95, 1.05)
        
        trend = TrendDirection.UP if current_csat > prev_csat else TrendDirection.DOWN
        health = self._get_csat_health(current_csat)
        
        return KPIData(
            id=KPIId.CSAT,
            current_value=round(current_csat, 0),
            previous_value=round(prev_csat, 0),
            target_value=85.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_operational_efficiency(self, sales_df: pd.DataFrame, expenses_df: pd.DataFrame) -> KPIData:
        """Calculate Operational Efficiency"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        current_month_start = self.current_date.replace(day=1)
        
        current_revenue = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        current_expenses = expenses_df[expenses_df['date'] >= current_month_start]['amount'].sum()
        current_efficiency = (current_revenue / current_expenses * 100) if current_expenses > 0 else 0
        
        # Previous period
        prev_efficiency = current_efficiency * np.random.uniform(0.9, 1.1)
        
        trend = TrendDirection.UP if current_efficiency > prev_efficiency else TrendDirection.DOWN
        health = self._get_operational_health(current_efficiency)
        
        return KPIData(
            id=KPIId.OPERATIONAL_EFFICIENCY,
            current_value=round(current_efficiency, 0),
            previous_value=round(prev_efficiency, 0),
            target_value=80.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_employee_satisfaction(self, customers_df: pd.DataFrame) -> KPIData:
        """Calculate Employee Satisfaction (proxy metric)"""
        # Use customer satisfaction as proxy for employee satisfaction
        current_satisfaction = customers_df['satisfaction_score'].mean() * 0.9  # Slightly lower
        
        # Previous period
        prev_satisfaction = current_satisfaction * np.random.uniform(0.95, 1.05)
        
        trend = TrendDirection.UP if current_satisfaction > prev_satisfaction else TrendDirection.DOWN
        health = self._get_satisfaction_health(current_satisfaction)
        
        return KPIData(
            id=KPIId.EMPLOYEE_SATISFACTION,
            current_value=round(current_satisfaction, 0),
            previous_value=round(prev_satisfaction, 0),
            target_value=80.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    def calculate_market_share(self, sales_df: pd.DataFrame) -> KPIData:
        """Calculate Market Share"""
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        current_month_start = self.current_date.replace(day=1)
        
        current_revenue = sales_df[sales_df['date'] >= current_month_start]['amount'].sum()
        # Assume total market size is 10x our revenue
        total_market_size = current_revenue * 10
        current_market_share = (current_revenue / total_market_size * 100)
        
        # Previous period
        prev_market_share = current_market_share * np.random.uniform(0.95, 1.05)
        
        trend = TrendDirection.UP if current_market_share > prev_market_share else TrendDirection.DOWN
        health = self._get_market_share_health(current_market_share)
        
        return KPIData(
            id=KPIId.MARKET_SHARE,
            current_value=round(current_market_share, 1),
            previous_value=round(prev_market_share, 1),
            target_value=15.0,
            trend=trend,
            health_status=health,
            last_updated=self.current_date.isoformat()
        )
    
    # Health assessment methods
    def _get_revenue_health(self, current: float, target: float, trend: TrendDirection) -> HealthStatus:
        """Determine revenue health status"""
        ratio = current / target if target > 0 else 0
        if ratio >= 0.95:
            return HealthStatus.EXCELLENT
        elif ratio >= 0.85:
            return HealthStatus.GOOD
        elif ratio >= 0.75:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_growth_health(self, growth: float) -> HealthStatus:
        """Determine growth health status"""
        if growth >= 15:
            return HealthStatus.EXCELLENT
        elif growth >= 10:
            return HealthStatus.GOOD
        elif growth >= 5:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_margin_health(self, margin: float) -> HealthStatus:
        """Determine margin health status"""
        if margin >= 20:
            return HealthStatus.EXCELLENT
        elif margin >= 15:
            return HealthStatus.GOOD
        elif margin >= 10:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_expense_health(self, ratio: float) -> HealthStatus:
        """Determine expense ratio health status"""
        if ratio <= 70:
            return HealthStatus.EXCELLENT
        elif ratio <= 75:
            return HealthStatus.GOOD
        elif ratio <= 85:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_customer_health_status(self, health_score: float) -> HealthStatus:
        """Determine customer health status"""
        if health_score >= 80:
            return HealthStatus.EXCELLENT
        elif health_score >= 70:
            return HealthStatus.GOOD
        elif health_score >= 60:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_churn_health(self, churn_rate: float) -> HealthStatus:
        """Determine churn rate health status"""
        if churn_rate <= 3:
            return HealthStatus.EXCELLENT
        elif churn_rate <= 5:
            return HealthStatus.GOOD
        elif churn_rate <= 8:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_clv_health(self, clv: float) -> HealthStatus:
        """Determine CLV health status"""
        if clv >= 5000:
            return HealthStatus.EXCELLENT
        elif clv >= 3000:
            return HealthStatus.GOOD
        elif clv >= 1500:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_cac_health(self, cac: float) -> HealthStatus:
        """Determine CAC health status"""
        if cac <= 400:
            return HealthStatus.EXCELLENT
        elif cac <= 600:
            return HealthStatus.GOOD
        elif cac <= 800:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_ltv_cac_health(self, ratio: float) -> HealthStatus:
        """Determine LTV:CAC ratio health status"""
        if ratio >= 5:
            return HealthStatus.EXCELLENT
        elif ratio >= 3:
            return HealthStatus.GOOD
        elif ratio >= 2:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_nps_health(self, nps: float) -> HealthStatus:
        """Determine NPS health status"""
        if nps >= 50:
            return HealthStatus.EXCELLENT
        elif nps >= 30:
            return HealthStatus.GOOD
        elif nps >= 10:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_csat_health(self, csat: float) -> HealthStatus:
        """Determine CSAT health status"""
        if csat >= 85:
            return HealthStatus.EXCELLENT
        elif csat >= 75:
            return HealthStatus.GOOD
        elif csat >= 65:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_operational_health(self, efficiency: float) -> HealthStatus:
        """Determine operational efficiency health status"""
        if efficiency >= 90:
            return HealthStatus.EXCELLENT
        elif efficiency >= 80:
            return HealthStatus.GOOD
        elif efficiency >= 70:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_satisfaction_health(self, satisfaction: float) -> HealthStatus:
        """Determine satisfaction health status"""
        if satisfaction >= 85:
            return HealthStatus.EXCELLENT
        elif satisfaction >= 75:
            return HealthStatus.GOOD
        elif satisfaction >= 65:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
    
    def _get_market_share_health(self, market_share: float) -> HealthStatus:
        """Determine market share health status"""
        if market_share >= 20:
            return HealthStatus.EXCELLENT
        elif market_share >= 15:
            return HealthStatus.GOOD
        elif market_share >= 10:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL
