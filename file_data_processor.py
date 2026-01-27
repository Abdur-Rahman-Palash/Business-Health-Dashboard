#!/usr/bin/env python3
"""
File Data Processor for Realistic Decision Making
Extracts business metrics from uploaded files and generates realistic decisions
"""

import pandas as pd
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import streamlit as st

class FileDataProcessor:
    """Processes uploaded files to extract business metrics for decision making"""
    
    def __init__(self):
        self.business_metrics = {
            'revenue': {
                'keywords': ['revenue', 'sales', 'income', 'turnover', 'earnings'],
                'patterns': [r'\$?[\d,]+\.?\d*\s*(million|billion|thousand)?', r'\d+\.?\d*%'],
                'unit': 'USD'
            },
            'customer_satisfaction': {
                'keywords': ['satisfaction', 'nps', 'rating', 'score', 'feedback'],
                'patterns': [r'\d+\.?\d*%', r'\d+\.?\d*/\d+', r'\d+\.?\d*\s*out of\s*\d+'],
                'unit': '%'
            },
            'operational_efficiency': {
                'keywords': ['efficiency', 'productivity', 'output', 'performance', 'utilization'],
                'patterns': [r'\d+\.?\d*%', r'\d+\.?\d*\s*(units|items|tasks)', r'\d+\.?\d*\s*hours?'],
                'unit': '%'
            },
            'market_position': {
                'keywords': ['market', 'share', 'position', 'ranking', 'competition'],
                'patterns': [r'\d+\.?\d*%', r'#\d+', r'\d+\.?\d*\s*position'],
                'unit': '%'
            },
            'costs': {
                'keywords': ['cost', 'expense', 'budget', 'spending', 'investment'],
                'patterns': [r'\$?[\d,]+\.?\d*\s*(million|billion|thousand)?'],
                'unit': 'USD'
            },
            'customers': {
                'keywords': ['customer', 'client', 'user', 'subscriber'],
                'patterns': [r'[\d,]+', r'\d+\.?\d*\s*(million|thousand)'],
                'unit': 'count'
            }
        }
    
    def process_uploaded_file(self, file_data: Dict, file_type: str) -> Dict:
        """Process uploaded file and extract business metrics"""
        
        try:
            if file_type == 'csv':
                return self._process_csv_data(file_data)
            elif file_type == 'excel':
                return self._process_excel_data(file_data)
            elif file_type == 'json':
                return self._process_json_data(file_data)
            elif file_type == 'txt':
                return self._process_text_data(file_data)
            elif file_type == 'pdf':
                return self._process_text_data(file_data)  # PDF text extraction
            elif file_type == 'xml':
                return self._process_xml_data(file_data)
            else:
                return self._generate_default_metrics()
                
        except Exception as e:
            st.error(f"Error processing file data: {e}")
            return self._generate_default_metrics()
    
    def _process_csv_data(self, file_data: Dict) -> Dict:
        """Process CSV data to extract business metrics"""
        
        df = file_data.get('dataframe')
        if df is None:
            return self._generate_default_metrics()
        
        metrics = {}
        
        # Analyze column names and data
        columns = df.columns.str.lower()
        
        # Revenue metrics
        revenue_cols = [col for col in columns if any(keyword in col for keyword in self.business_metrics['revenue']['keywords'])]
        if revenue_cols:
            for col in revenue_cols:
                try:
                    values = pd.to_numeric(df[col], errors='coerce').dropna()
                    if len(values) > 0:
                        metrics['revenue'] = {
                            'value': float(values.iloc[-1] if len(values) > 0 else 0),
                            'change': self._calculate_change(values),
                            'trend': self._determine_trend(values),
                            'source': f'CSV column: {col}'
                        }
                        break
                except:
                    continue
        
        # Customer metrics
        customer_cols = [col for col in columns if any(keyword in col for keyword in self.business_metrics['customers']['keywords'])]
        if customer_cols:
            for col in customer_cols:
                try:
                    values = pd.to_numeric(df[col], errors='coerce').dropna()
                    if len(values) > 0:
                        metrics['customers'] = {
                            'value': float(values.iloc[-1] if len(values) > 0 else 0),
                            'change': self._calculate_change(values),
                            'trend': self._determine_trend(values),
                            'source': f'CSV column: {col}'
                        }
                        break
                except:
                    continue
        
        # Satisfaction metrics
        satisfaction_cols = [col for col in columns if any(keyword in col for keyword in self.business_metrics['customer_satisfaction']['keywords'])]
        if satisfaction_cols:
            for col in satisfaction_cols:
                try:
                    values = pd.to_numeric(df[col], errors='coerce').dropna()
                    if len(values) > 0:
                        metrics['customer_satisfaction'] = {
                            'value': float(values.iloc[-1] if len(values) > 0 else 0),
                            'change': self._calculate_change(values),
                            'trend': self._determine_trend(values),
                            'source': f'CSV column: {col}'
                        }
                        break
                except:
                    continue
        
        # Efficiency metrics
        efficiency_cols = [col for col in columns if any(keyword in col for keyword in self.business_metrics['operational_efficiency']['keywords'])]
        if efficiency_cols:
            for col in efficiency_cols:
                try:
                    values = pd.to_numeric(df[col], errors='coerce').dropna()
                    if len(values) > 0:
                        metrics['operational_efficiency'] = {
                            'value': float(values.iloc[-1] if len(values) > 0 else 0),
                            'change': self._calculate_change(values),
                            'trend': self._determine_trend(values),
                            'source': f'CSV column: {col}'
                        }
                        break
                except:
                    continue
        
        # Generate KPIs from metrics
        kpis = self._generate_kpis_from_metrics(metrics)
        
        return {
            'status': 'success',
            'file_type': 'csv',
            'metrics': metrics,
            'kpis': kpis,
            'business_health_score': self._calculate_business_health(metrics),
            'insights': self._generate_insights(metrics),
            'processed_at': datetime.now().isoformat()
        }
    
    def _process_excel_data(self, file_data: Dict) -> Dict:
        """Process Excel data similar to CSV"""
        # Excel processing is similar to CSV
        return self._process_csv_data(file_data)
    
    def _process_json_data(self, file_data: Dict) -> Dict:
        """Process JSON data to extract business metrics"""
        
        json_data = file_data.get('json_data', {})
        metrics = {}
        
        def extract_from_json(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    extract_from_json(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    extract_from_json(item, f"{path}[{i}]")
            else:
                # Check if this value matches any business metric patterns
                for metric_name, metric_info in self.business_metrics.items():
                    if any(keyword in path.lower() for keyword in metric_info['keywords']):
                        try:
                            if isinstance(obj, (int, float)):
                                metrics[metric_name] = {
                                    'value': float(obj),
                                    'change': 0.0,
                                    'trend': 'stable',
                                    'source': f'JSON path: {path}'
                                }
                        except:
                            continue
        
        extract_from_json(json_data)
        
        kpis = self._generate_kpis_from_metrics(metrics)
        
        return {
            'status': 'success',
            'file_type': 'json',
            'metrics': metrics,
            'kpis': kpis,
            'business_health_score': self._calculate_business_health(metrics),
            'insights': self._generate_insights(metrics),
            'processed_at': datetime.now().isoformat()
        }
    
    def _process_text_data(self, file_data: Dict) -> Dict:
        """Process text data (TXT, PDF) to extract business metrics"""
        
        text_content = file_data.get('text_content', '')
        metrics = {}
        
        # Extract metrics using patterns
        for metric_name, metric_info in self.business_metrics.items():
            for pattern in metric_info['patterns']:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    try:
                        # Extract numeric values
                        for match in matches:
                            if isinstance(match, tuple):
                                match = match[0]
                            
                            # Clean and convert to number
                            cleaned = re.sub(r'[^\d\.]', '', match)
                            if cleaned:
                                value = float(cleaned)
                                
                                # Apply multipliers
                                if 'million' in match.lower():
                                    value *= 1000000
                                elif 'billion' in match.lower():
                                    value *= 1000000000
                                elif 'thousand' in match.lower():
                                    value *= 1000
                                
                                metrics[metric_name] = {
                                    'value': value,
                                    'change': 0.0,
                                    'trend': 'stable',
                                    'source': f'Text extraction'
                                }
                                break
                    except:
                        continue
        
        kpis = self._generate_kpis_from_metrics(metrics)
        
        return {
            'status': 'success',
            'file_type': 'text',
            'metrics': metrics,
            'kpis': kpis,
            'business_health_score': self._calculate_business_health(metrics),
            'insights': self._generate_insights(metrics),
            'processed_at': datetime.now().isoformat()
        }
    
    def _process_xml_data(self, file_data: Dict) -> Dict:
        """Process XML data similar to text"""
        # XML processing similar to text for now
        return self._process_text_data(file_data)
    
    def _calculate_change(self, values: pd.Series) -> float:
        """Calculate percentage change"""
        if len(values) < 2:
            return 0.0
        
        try:
            current = float(values.iloc[-1])
            previous = float(values.iloc[-2])
            
            if previous == 0:
                return 0.0
            
            change = ((current - previous) / previous) * 100
            return round(change, 2)
        except:
            return 0.0
    
    def _determine_trend(self, values: pd.Series) -> str:
        """Determine trend from values"""
        if len(values) < 3:
            return 'stable'
        
        try:
            # Simple trend calculation
            recent_avg = float(values.tail(3).mean())
            earlier_avg = float(values.head(3).mean())
            
            if recent_avg > earlier_avg * 1.05:
                return 'up'
            elif recent_avg < earlier_avg * 0.95:
                return 'down'
            else:
                return 'stable'
        except:
            return 'stable'
    
    def _generate_kpis_from_metrics(self, metrics: Dict) -> List[Dict]:
        """Generate KPIs from extracted metrics"""
        
        kpis = []
        
        # Revenue KPI
        if 'revenue' in metrics:
            revenue = metrics['revenue']
            kpis.append({
                'id': 'revenue',
                'name': 'Total Revenue',
                'value': revenue['value'],
                'change': revenue['change'],
                'trend': revenue['trend'],
                'category': 'financial',
                'unit': 'USD',
                'source': revenue['source']
            })
        
        # Customer Satisfaction KPI
        if 'customer_satisfaction' in metrics:
            satisfaction = metrics['customer_satisfaction']
            kpis.append({
                'id': 'customer_satisfaction',
                'name': 'Customer Satisfaction',
                'value': satisfaction['value'],
                'change': satisfaction['change'],
                'trend': satisfaction['trend'],
                'category': 'customer',
                'unit': '%',
                'source': satisfaction['source']
            })
        
        # Operational Efficiency KPI
        if 'operational_efficiency' in metrics:
            efficiency = metrics['operational_efficiency']
            kpis.append({
                'id': 'operational_efficiency',
                'name': 'Operational Efficiency',
                'value': efficiency['value'],
                'change': efficiency['change'],
                'trend': efficiency['trend'],
                'category': 'operational',
                'unit': '%',
                'source': efficiency['source']
            })
        
        # Market Position KPI
        if 'market_position' in metrics:
            market = metrics['market_position']
            kpis.append({
                'id': 'market_position',
                'name': 'Market Position',
                'value': market['value'],
                'change': market['change'],
                'trend': market['trend'],
                'category': 'market',
                'unit': '%',
                'source': market['source']
            })
        
        # Customer Count KPI
        if 'customers' in metrics:
            customers = metrics['customers']
            kpis.append({
                'id': 'customers',
                'name': 'Total Customers',
                'value': customers['value'],
                'change': customers['change'],
                'trend': customers['trend'],
                'category': 'customer',
                'unit': 'count',
                'source': customers['source']
            })
        
        # Add default KPIs if none found
        if not kpis:
            kpis = self._generate_default_kpis()
        
        return kpis
    
    def _generate_default_kpis(self) -> List[Dict]:
        """Generate default KPIs when no metrics found"""
        
        return [
            {
                'id': 'revenue',
                'name': 'Total Revenue',
                'value': 850000,
                'change': -5.2,
                'trend': 'down',
                'category': 'financial',
                'unit': 'USD',
                'source': 'Default demo data'
            },
            {
                'id': 'customer_satisfaction',
                'name': 'Customer Satisfaction',
                'value': 75,
                'change': -3.1,
                'trend': 'down',
                'category': 'customer',
                'unit': '%',
                'source': 'Default demo data'
            },
            {
                'id': 'operational_efficiency',
                'name': 'Operational Efficiency',
                'value': 68,
                'change': -2.5,
                'trend': 'down',
                'category': 'operational',
                'unit': '%',
                'source': 'Default demo data'
            },
            {
                'id': 'market_position',
                'name': 'Market Position',
                'value': 22,
                'change': -1.8,
                'trend': 'down',
                'category': 'market',
                'unit': '%',
                'source': 'Default demo data'
            }
        ]
    
    def _calculate_business_health(self, metrics: Dict) -> Dict:
        """Calculate business health scores from metrics"""
        
        scores = {
            'financial': 0,
            'customer': 0,
            'operational': 0,
            'overall': 0
        }
        
        # Financial health
        if 'revenue' in metrics:
            revenue = metrics['revenue']
            if revenue['trend'] == 'up':
                scores['financial'] = min(85, 60 + abs(revenue['change']))
            elif revenue['trend'] == 'stable':
                scores['financial'] = 60
            else:
                scores['financial'] = max(25, 60 - abs(revenue['change']))
        else:
            scores['financial'] = 50
        
        # Customer health
        if 'customer_satisfaction' in metrics:
            satisfaction = metrics['customer_satisfaction']
            scores['customer'] = min(100, max(0, satisfaction['value']))
        elif 'customers' in metrics:
            customers = metrics['customers']
            if customers['trend'] == 'up':
                scores['customer'] = 75
            elif customers['trend'] == 'stable':
                scores['customer'] = 60
            else:
                scores['customer'] = 45
        else:
            scores['customer'] = 50
        
        # Operational health
        if 'operational_efficiency' in metrics:
            efficiency = metrics['operational_efficiency']
            scores['operational'] = min(100, max(0, efficiency['value']))
        else:
            scores['operational'] = 50
        
        # Overall health
        scores['overall'] = (scores['financial'] + scores['customer'] + scores['operational']) / 3
        
        return scores
    
    def _generate_insights(self, metrics: Dict) -> List[Dict]:
        """Generate insights from extracted metrics"""
        
        insights = []
        
        # Revenue insights
        if 'revenue' in metrics:
            revenue = metrics['revenue']
            if revenue['trend'] == 'down' and revenue['change'] < -5:
                insights.append({
                    'title': 'Revenue Decline Detected',
                    'description': f'Revenue has decreased by {abs(revenue["change"]):.1f}% compared to previous period.',
                    'priority': 'high',
                    'category': 'financial',
                    'source': revenue['source']
                })
            elif revenue['trend'] == 'up' and revenue['change'] > 5:
                insights.append({
                    'title': 'Revenue Growth Positive',
                    'description': f'Revenue has increased by {revenue["change"]:.1f}% compared to previous period.',
                    'priority': 'medium',
                    'category': 'financial',
                    'source': revenue['source']
                })
        
        # Customer insights
        if 'customer_satisfaction' in metrics:
            satisfaction = metrics['customer_satisfaction']
            if satisfaction['value'] < 70:
                insights.append({
                    'title': 'Customer Satisfaction Below Target',
                    'description': f'Customer satisfaction score is {satisfaction["value"]:.1f}%, below the 70% target.',
                    'priority': 'high',
                    'category': 'customer',
                    'source': satisfaction['source']
                })
            elif satisfaction['value'] > 85:
                insights.append({
                    'title': 'Excellent Customer Satisfaction',
                    'description': f'Customer satisfaction score is {satisfaction["value"]:.1f}%, exceeding expectations.',
                    'priority': 'low',
                    'category': 'customer',
                    'source': satisfaction['source']
                })
        
        # Operational insights
        if 'operational_efficiency' in metrics:
            efficiency = metrics['operational_efficiency']
            if efficiency['value'] < 60:
                insights.append({
                    'title': 'Operational Efficiency Concern',
                    'description': f'Operational efficiency is {efficiency["value"]:.1f}%, indicating potential process issues.',
                    'priority': 'medium',
                    'category': 'operational',
                    'source': efficiency['source']
                })
        
        return insights
    
    def _generate_default_metrics(self) -> Dict:
        """Generate default metrics when no data available"""
        
        return {
            'status': 'default',
            'file_type': 'unknown',
            'metrics': {},
            'kpis': self._generate_default_kpis(),
            'business_health_score': {
                'financial': 45,
                'customer': 65,
                'operational': 55,
                'overall': 55
            },
            'insights': [
                {
                    'title': 'No File Data Available',
                    'description': 'Upload a business file to generate realistic decisions based on your actual data.',
                    'priority': 'medium',
                    'category': 'general',
                    'source': 'System'
                }
            ],
            'processed_at': datetime.now().isoformat()
        }

# Global instance
file_data_processor = FileDataProcessor()
