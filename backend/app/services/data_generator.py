import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

class BusinessDataGenerator:
    """Generates realistic synthetic business data for analysis"""
    
    def __init__(self):
        self.start_date = datetime.now() - timedelta(days=365)
        np.random.seed(42)  # For reproducible results
        
    def generate_comprehensive_business_data(self) -> Dict[str, Any]:
        """Generate complete business dataset"""
        return {
            'customers': self.generate_customer_data(),
            'sales': self.generate_sales_data(),
            'expenses': self.generate_expense_data(),
            'marketing': self.generate_marketing_data()
        }
    
    def generate_customer_data(self, num_customers: int = 1000) -> List[Dict]:
        """Generate realistic customer data with RFM characteristics"""
        customers = []
        
        # Define customer segments with different characteristics
        segments = {
            'Enterprise': {'weight': 0.1, 'avg_revenue': 50000, 'avg_orders': 50, 'churn_rate': 0.05},
            'Mid-Market': {'weight': 0.25, 'avg_revenue': 15000, 'avg_orders': 25, 'churn_rate': 0.08},
            'Small Business': {'weight': 0.40, 'avg_revenue': 3000, 'avg_orders': 10, 'churn_rate': 0.12},
            'Startup': {'weight': 0.25, 'avg_revenue': 500, 'avg_orders': 3, 'churn_rate': 0.20}
        }
        
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
        
        for i in range(num_customers):
            # Select segment based on weights
            segment = np.random.choice(list(segments.keys()), 
                                     p=[s['weight'] for s in segments.values()])
            segment_config = segments[segment]
            
            # Generate acquisition date (more recent customers are more likely)
            days_ago = np.random.exponential(scale=200)  # Exponential distribution
            acquisition_date = self.start_date + timedelta(days=min(days_ago, 365))
            
            # Generate revenue with some variance
            revenue = np.random.normal(segment_config['avg_revenue'], 
                                    segment_config['avg_revenue'] * 0.3)
            revenue = max(100, revenue)  # Minimum revenue
            
            # Generate order count
            orders = np.random.poisson(segment_config['avg_orders'])
            orders = max(1, orders)
            
            # Generate last order date (more recent for active customers)
            if np.random.random() > segment_config['churn_rate']:
                # Active customer
                days_since_last_order = np.random.exponential(scale=30)
                last_order_date = datetime.now() - timedelta(days=min(days_since_last_order, 90))
            else:
                # Churned customer
                days_since_last_order = np.random.uniform(90, 365)
                last_order_date = datetime.now() - timedelta(days=days_since_last_order)
            
            # Generate satisfaction score (correlated with segment and recency)
            base_satisfaction = {'Enterprise': 85, 'Mid-Market': 75, 'Small Business': 70, 'Startup': 65}[segment]
            recency_factor = max(0, 1 - (datetime.now() - last_order_date).days / 365)
            satisfaction = base_satisfaction + (recency_factor - 0.5) * 20 + np.random.normal(0, 10)
            satisfaction = max(0, min(100, satisfaction))
            
            # Calculate churn probability
            churn_prob = self._calculate_churn_probability(
                revenue, orders, (datetime.now() - last_order_date).days, satisfaction
            )
            
            customers.append({
                'customer_id': f'CUST_{i+1:06d}',
                'acquisition_date': acquisition_date.strftime('%Y-%m-%d'),
                'total_revenue': round(revenue, 2),
                'order_count': orders,
                'last_order_date': last_order_date.strftime('%Y-%m-%d'),
                'segment': segment,
                'region': np.random.choice(regions),
                'satisfaction_score': round(satisfaction, 1),
                'churn_probability': round(churn_prob, 3)
            })
        
        return customers
    
    def generate_sales_data(self, num_transactions: int = 10000) -> List[Dict]:
        """Generate sales transactions with realistic patterns"""
        transactions = []
        product_categories = ['Software', 'Hardware', 'Services', 'Support', 'Training']
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
        
        # Generate time series with seasonality and trend
        dates = []
        current_date = self.start_date
        while current_date <= datetime.now():
            dates.append(current_date)
            current_date += timedelta(days=1)
        
        for i in range(num_transactions):
            # Select date with more transactions recently (growth trend)
            date_weights = np.exp(np.linspace(-2, 0, len(dates)))  # Exponential growth
            date_weights = date_weights / date_weights.sum()
            transaction_date = np.random.choice(dates, p=date_weights)
            
            # Add seasonality (higher sales in certain months)
            month_factor = 1.0
            if transaction_date.month in [11, 12]:  # Holiday season
                month_factor = 1.3
            elif transaction_date.month in [6, 7]:  # Summer slowdown
                month_factor = 0.8
            
            # Generate transaction amount with log-normal distribution
            base_amount = np.random.lognormal(mean=8, sigma=1)  # ~$3,000 average
            amount = base_amount * month_factor
            
            # Apply some business rules
            customer_tier = np.random.choice(['Enterprise', 'Mid-Market', 'Small Business'], 
                                           p=[0.1, 0.3, 0.6])
            if customer_tier == 'Enterprise':
                amount *= np.random.uniform(2, 5)
            elif customer_tier == 'Mid-Market':
                amount *= np.random.uniform(1, 2)
            
            # Calculate margin (typically 20-40% for software, lower for hardware)
            category = np.random.choice(product_categories)
            if category == 'Software':
                margin_rate = np.random.normal(0.35, 0.05)
            elif category == 'Services':
                margin_rate = np.random.normal(0.25, 0.08)
            else:
                margin_rate = np.random.normal(0.15, 0.05)
            
            margin_rate = max(0.05, min(0.50, margin_rate))
            margin = amount * margin_rate
            
            transactions.append({
                'transaction_id': f'TXN_{i+1:08d}',
                'customer_id': f'CUST_{np.random.randint(1, 1000):06d}',
                'date': transaction_date.strftime('%Y-%m-%d'),
                'amount': round(amount, 2),
                'product_category': category,
                'region': np.random.choice(regions),
                'margin': round(margin, 2)
            })
        
        return transactions
    
    def generate_expense_data(self, num_expenses: int = 500) -> List[Dict]:
        """Generate realistic expense data"""
        expenses = []
        categories = {
            'Salaries': {'weight': 0.4, 'is_fixed': True, 'avg_amount': 15000},
            'Rent': {'weight': 0.15, 'is_fixed': True, 'avg_amount': 8000},
            'Marketing': {'weight': 0.15, 'is_fixed': False, 'avg_amount': 5000},
            'R&D': {'weight': 0.12, 'is_fixed': False, 'avg_amount': 7000},
            'Sales': {'weight': 0.08, 'is_fixed': False, 'avg_amount': 3000},
            'Operations': {'weight': 0.06, 'is_fixed': False, 'avg_amount': 2000},
            'Admin': {'weight': 0.04, 'is_fixed': True, 'avg_amount': 1500}
        }
        
        departments = ['Engineering', 'Sales', 'Marketing', 'Operations', 'Finance', 'HR']
        
        for i in range(num_expenses):
            category = np.random.choice(list(categories.keys()), 
                                       p=[c['weight'] for c in categories.values()])
            config = categories[category]
            
            # Generate date with some clustering around month-end
            days_in_month = 30
            day_of_month = np.random.choice(
                list(range(1, days_in_month + 1)) + [days_in_month] * 5
            )
            
            expense_date = self.start_date + timedelta(
                days=np.random.randint(0, 365),
                hours=np.random.randint(9, 17)
            )
            
            # Generate amount with some variance
            amount = np.random.normal(config['avg_amount'], config['avg_amount'] * 0.2)
            amount = max(100, amount)
            
            # Add inflation trend (expenses increase over time)
            inflation_factor = 1 + (expense_date - self.start_date).days / 365 * 0.03
            amount *= inflation_factor
            
            expenses.append({
                'expense_id': f'EXP_{i+1:06d}',
                'category': category,
                'amount': round(amount, 2),
                'date': expense_date.strftime('%Y-%m-%d'),
                'description': f'{category} - {np.random.choice(["Q1", "Q2", "Q3", "Q4"])} {expense_date.year}',
                'department': np.random.choice(departments),
                'is_fixed': config['is_fixed']
            })
        
        return expenses
    
    def generate_marketing_data(self, num_campaigns: int = 200) -> List[Dict]:
        """Generate marketing campaign data"""
        campaigns = []
        channels = ['Google Ads', 'Facebook', 'LinkedIn', 'Email', 'Content', 'SEO', 'Events']
        
        for i in range(num_campaigns):
            channel = np.random.choice(channels)
            
            # Channel-specific characteristics
            channel_config = {
                'Google Ads': {'avg_spend': 3000, 'conversion_rate': 0.02},
                'Facebook': {'avg_spend': 2000, 'conversion_rate': 0.015},
                'LinkedIn': {'avg_spend': 2500, 'conversion_rate': 0.025},
                'Email': {'avg_spend': 500, 'conversion_rate': 0.08},
                'Content': {'avg_spend': 1500, 'conversion_rate': 0.03},
                'SEO': {'avg_spend': 1000, 'conversion_rate': 0.05},
                'Events': {'avg_spend': 5000, 'conversion_rate': 0.01}
            }
            
            config = channel_config[channel]
            
            # Generate campaign date
            campaign_date = self.start_date + timedelta(days=np.random.randint(0, 365))
            
            # Generate spend with variance
            spend = np.random.normal(config['avg_spend'], config['avg_spend'] * 0.3)
            spend = max(100, spend)
            
            # Generate leads based on spend and channel efficiency
            lead_efficiency = {
                'Google Ads': 0.5,
                'Facebook': 0.8,
                'LinkedIn': 0.3,
                'Email': 2.0,
                'Content': 1.5,
                'SEO': 1.0,
                'Events': 0.2
            }
            
            leads = int(spend * lead_efficiency[channel] * np.random.uniform(0.8, 1.2))
            leads = max(1, leads)
            
            # Generate conversions with some variance
            conversion_rate = config['conversion_rate'] * np.random.uniform(0.7, 1.3)
            conversion_rate = max(0.005, min(0.15, conversion_rate))
            
            campaigns.append({
                'campaign_id': f'CAMP_{i+1:06d}',
                'channel': channel,
                'amount': round(spend, 2),
                'date': campaign_date.strftime('%Y-%m-%d'),
                'leads_generated': leads,
                'conversion_rate': round(conversion_rate, 4)
            })
        
        return campaigns
    
    def _calculate_churn_probability(self, revenue: float, orders: int, 
                                   days_since_last_order: int, satisfaction: float) -> float:
        """Calculate churn probability based on customer metrics"""
        # Base probability from satisfaction
        satisfaction_factor = (100 - satisfaction) / 100
        
        # Recency factor (higher for longer time since last order)
        recency_factor = min(1.0, days_since_last_order / 180)
        
        # Engagement factor (based on order frequency)
        engagement_factor = max(0, 1 - (orders / 50))
        
        # Value factor (higher value customers have slightly lower churn)
        value_factor = max(0.5, 1 - (revenue / 100000) * 0.2)
        
        # Combine factors with weights
        churn_prob = (
            satisfaction_factor * 0.3 +
            recency_factor * 0.4 +
            engagement_factor * 0.2 +
            value_factor * 0.1
        )
        
        return max(0, min(1, churn_prob))
