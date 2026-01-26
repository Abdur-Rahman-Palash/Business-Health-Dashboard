#!/usr/bin/env python3
"""
Advanced File Analyzer for All Business Formats
Comprehensive analysis for decision making
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import io

class AdvancedFileAnalyzer:
    """Advanced analysis for all business file formats"""
    
    def __init__(self):
        self.business_keywords = {
            'financial': [
                'revenue', 'profit', 'loss', 'income', 'expense', 'budget', 'cost',
                'investment', 'roi', 'margin', 'cash flow', 'balance sheet', 'p&l',
                'earnings', 'sales', 'turnover', 'growth', 'decline', 'increase',
                'financial', 'money', 'price', 'amount', 'total', 'sum'
            ],
            'customer': [
                'customer', 'client', 'satisfaction', 'retention', 'churn', 'acquisition',
                'loyalty', 'feedback', 'complaint', 'nps', 'csat', 'user', 'market share',
                'customer service', 'support', 'experience'
            ],
            'operational': [
                'efficiency', 'productivity', 'operations', 'process', 'workflow',
                'inventory', 'supply chain', 'logistics', 'quality', 'performance',
                'kpi', 'metrics', 'dashboard', 'analysis', 'report', 'output'
            ],
            'strategic': [
                'strategy', 'goal', 'objective', 'mission', 'vision', 'plan',
                'initiative', 'project', 'roadmap', 'timeline', 'milestone',
                'risk', 'opportunity', 'threat', 'swot', 'competitive', 'market'
            ]
        }
        
        self.decision_keywords = {
            'urgent': ['urgent', 'immediate', 'critical', 'asap', 'priority', 'emergency', 'now'],
            'opportunity': ['opportunity', 'growth', 'expand', 'new', 'potential', 'market', 'innovation'],
            'risk': ['risk', 'threat', 'challenge', 'issue', 'problem', 'concern', 'danger'],
            'action': ['action', 'implement', 'execute', 'launch', 'start', 'begin', 'do', 'should']
        }
    
    def analyze_csv_advanced(self, df: pd.DataFrame, file_name: str) -> Dict:
        """Advanced CSV analysis for decision making"""
        
        # Basic info
        analysis = {
            'file_name': file_name,
            'file_type': 'CSV',
            'analysis_timestamp': datetime.now().isoformat(),
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'data_types': df.dtypes.to_dict()
        }
        
        # Data quality assessment
        analysis['data_quality'] = self.assess_data_quality(df)
        
        # Business category detection
        analysis['business_category'] = self.detect_business_category(df)
        
        # Financial metrics extraction
        analysis['financial_metrics'] = self.extract_financial_metrics_from_df(df)
        
        # Trend analysis
        analysis['trend_analysis'] = self.analyze_trends(df)
        
        # Key insights
        analysis['insights'] = self.generate_insights_from_df(df)
        
        # Decision recommendations
        analysis['recommendations'] = self.generate_recommendations_from_df(df)
        
        # Decision score
        analysis['decision_score'] = self.calculate_decision_score_for_df(df)
        
        return analysis
    
    def analyze_excel_advanced(self, df: pd.DataFrame, file_name: str) -> Dict:
        """Advanced Excel analysis"""
        # Similar to CSV but with Excel-specific features
        analysis = self.analyze_csv_advanced(df, file_name)
        analysis['file_type'] = 'Excel'
        return analysis
    
    def analyze_pdf_advanced(self, text: str, file_name: str) -> Dict:
        """Advanced PDF analysis"""
        analysis = {
            'file_name': file_name,
            'file_type': 'PDF',
            'analysis_timestamp': datetime.now().isoformat(),
            'content_length': len(text),
            'word_count': len(text.split())
        }
        
        # Business category analysis
        analysis['business_category'] = self.detect_business_category_from_text(text)
        
        # Financial metrics extraction
        analysis['financial_metrics'] = self.extract_financial_metrics_from_text(text)
        
        # Sentiment analysis
        analysis['sentiment'] = self.analyze_sentiment(text)
        
        # Urgency analysis
        analysis['urgency'] = self.analyze_urgency_from_text(text)
        
        # Key insights
        analysis['insights'] = self.extract_insights_from_text(text)
        
        # Decision recommendations
        analysis['recommendations'] = self.generate_recommendations_from_text(text)
        
        # Decision score
        analysis['decision_score'] = self.calculate_decision_score_for_text(text)
        
        return analysis
    
    def analyze_json_advanced(self, data: Dict, file_name: str) -> Dict:
        """Advanced JSON analysis"""
        analysis = {
            'file_name': file_name,
            'file_type': 'JSON',
            'analysis_timestamp': datetime.now().isoformat(),
            'data_structure': self.analyze_json_structure(data)
        }
        
        # Convert to DataFrame if possible
        df = None
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            # Look for arrays in the dict
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    df = pd.DataFrame(value)
                    break
        
        if df is not None:
            csv_analysis = self.analyze_csv_advanced(df, file_name)
            analysis.update(csv_analysis)
            analysis['file_type'] = 'JSON (Tabular)'
        else:
            # Analyze as structured data
            analysis['business_category'] = self.detect_business_category_from_json(data)
            analysis['insights'] = self.generate_insights_from_json(data)
            analysis['recommendations'] = self.generate_recommendations_from_json(data)
            analysis['decision_score'] = {'score': 50, 'level': 'informational', 'requires_action': False}
        
        return analysis
    
    def analyze_txt_advanced(self, text: str, file_name: str) -> Dict:
        """Advanced text file analysis"""
        analysis = self.analyze_pdf_advanced(text, file_name)
        analysis['file_type'] = 'Text'
        return analysis
    
    def assess_data_quality(self, df: pd.DataFrame) -> Dict:
        """Assess data quality"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        # Check for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        quality_score = 100
        if missing_cells > 0:
            quality_score -= (missing_cells / total_cells) * 30
        if duplicate_rows > 0:
            quality_score -= (duplicate_rows / len(df)) * 20
        
        return {
            'total_cells': total_cells,
            'missing_cells': missing_cells,
            'missing_percentage': (missing_cells / total_cells) * 100 if total_cells > 0 else 0,
            'duplicate_rows': duplicate_rows,
            'duplicate_percentage': (duplicate_rows / len(df)) * 100 if len(df) > 0 else 0,
            'numeric_columns': len(numeric_cols),
            'quality_score': max(0, quality_score),
            'quality_grade': 'A' if quality_score >= 90 else 'B' if quality_score >= 70 else 'C' if quality_score >= 50 else 'D'
        }
    
    def detect_business_category(self, df: pd.DataFrame) -> Dict:
        """Detect business category from DataFrame"""
        columns_text = ' '.join(df.columns.astype(str).str.lower())
        sample_data = ' '.join(df.head(100).astype(str).values.flatten()).lower()
        combined_text = columns_text + ' ' + sample_data
        
        return self.detect_business_category_from_text(combined_text)
    
    def detect_business_category_from_text(self, text: str) -> Dict:
        """Detect business category from text"""
        category_scores = {}
        text_lower = text.lower()
        
        for category, keywords in self.business_keywords.items():
            score = 0
            found_keywords = []
            
            for keyword in keywords:
                count = text_lower.count(keyword)
                if count > 0:
                    score += count
                    found_keywords.append(keyword)
            
            category_scores[category] = {
                'score': score,
                'keywords_found': found_keywords,
                'percentage': (score / len(text.split())) * 100 if text.split() else 0
            }
        
        # Determine primary category
        primary_category = max(category_scores.keys(), key=lambda k: category_scores[k]['score'])
        
        return {
            'category_scores': category_scores,
            'primary_category': primary_category,
            'dominant_score': category_scores[primary_category]['score'],
            'confidence': 'high' if category_scores[primary_category]['score'] > 5 else 'medium'
        }
    
    def extract_financial_metrics_from_df(self, df: pd.DataFrame) -> Dict:
        """Extract financial metrics from DataFrame"""
        metrics = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_lower = col.lower()
            col_data = df[col].dropna()
            
            if len(col_data) > 0:
                if any(keyword in col_lower for keyword in ['revenue', 'sales', 'income']):
                    metrics['revenue'] = {
                        'total': col_data.sum(),
                        'average': col_data.mean(),
                        'max': col_data.max(),
                        'min': col_data.min(),
                        'trend': self.calculate_trend(col_data)
                    }
                
                elif any(keyword in col_lower for keyword in ['profit', 'margin']):
                    metrics['profit'] = {
                        'total': col_data.sum(),
                        'average': col_data.mean(),
                        'max': col_data.max(),
                        'min': col_data.min(),
                        'trend': self.calculate_trend(col_data)
                    }
                
                elif any(keyword in col_lower for keyword in ['cost', 'expense']):
                    metrics['cost'] = {
                        'total': col_data.sum(),
                        'average': col_data.mean(),
                        'max': col_data.max(),
                        'min': col_data.min(),
                        'trend': self.calculate_trend(col_data)
                    }
                
                else:
                    # Generic numeric column
                    metrics[col] = {
                        'total': col_data.sum(),
                        'average': col_data.mean(),
                        'max': col_data.max(),
                        'min': col_data.min(),
                        'trend': self.calculate_trend(col_data)
                    }
        
        return metrics
    
    def extract_financial_metrics_from_text(self, text: str) -> Dict:
        """Extract financial metrics from text"""
        metrics = {}
        
        # Currency patterns
        currency_pattern = r'[\$£€]?\s*[\d,]+\.?\d*\s*(?:million|billion|thousand|k|m|b)?'
        currency_matches = re.findall(currency_pattern, text, re.IGNORECASE)
        
        # Percentage patterns
        percentage_pattern = r'\d+\.?\d*\s*%'
        percentage_matches = re.findall(percentage_pattern, text, re.IGNORECASE)
        
        metrics['currency_mentions'] = len(currency_matches)
        metrics['percentage_mentions'] = len(percentage_matches)
        metrics['currency_values'] = currency_matches[:5]  # First 5 matches
        metrics['percentage_values'] = percentage_matches[:5]  # First 5 matches
        
        return metrics
    
    def calculate_trend(self, data: pd.Series) -> str:
        """Calculate trend direction"""
        if len(data) < 2:
            return 'insufficient_data'
        
        # Simple linear trend
        x = np.arange(len(data))
        try:
            slope = np.polyfit(x, data, 1)[0]
            if slope > 0.01:
                return 'increasing'
            elif slope < -0.01:
                return 'decreasing'
            else:
                return 'stable'
        except:
            return 'unknown'
    
    def analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze trends in the data"""
        trends = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if len(df[col].dropna()) >= 3:
                trend = self.calculate_trend(df[col].dropna())
                trends[col] = trend
        
        return trends
    
    def generate_insights_from_df(self, df: pd.DataFrame) -> List[Dict]:
        """Generate insights from DataFrame"""
        insights = []
        
        # Data size insights
        insights.append({
            'type': 'data_overview',
            'title': 'Data Overview',
            'description': f'Dataset contains {len(df):,} rows and {len(df.columns)} columns',
            'importance': 'medium'
        })
        
        # Financial insights
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['revenue', 'sales', 'profit']):
                total = df[col].sum()
                avg = df[col].mean()
                insights.append({
                    'type': 'financial_metric',
                    'title': f'{col.title()} Analysis',
                    'description': f'Total {col}: ${total:,.2f}, Average: ${avg:.2f}',
                    'importance': 'high'
                })
        
        # Data quality insights
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 10:
            insights.append({
                'type': 'data_quality',
                'title': 'Data Quality Alert',
                'description': f'{missing_pct:.1f}% of data is missing - consider data cleaning',
                'importance': 'high'
            })
        
        return insights
    
    def generate_recommendations_from_df(self, df: pd.DataFrame) -> List[Dict]:
        """Generate recommendations from DataFrame"""
        recommendations = []
        
        # Financial recommendations
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            col_lower = col.lower()
            
            if any(keyword in col_lower for keyword in ['revenue', 'sales']):
                total = df[col].sum()
                if total > 0:
                    recommendations.append({
                        'title': 'Revenue Optimization',
                        'description': f'Total revenue of ${total:,.2f} detected. Implement revenue tracking and growth strategies.',
                        'priority': 'high',
                        'category': 'financial',
                        'actionable': True
                    })
            
            elif any(keyword in col_lower for keyword in ['cost', 'expense']):
                total = df[col].sum()
                if total > 0:
                    recommendations.append({
                        'title': 'Cost Management',
                        'description': f'Total costs of ${total:,.2f} identified. Review cost optimization opportunities.',
                        'priority': 'medium',
                        'category': 'financial',
                        'actionable': True
                    })
        
        # Data quality recommendations
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 5:
            recommendations.append({
                'title': 'Data Quality Improvement',
                'description': f'{missing_pct:.1f}% missing data. Implement data validation and cleaning processes.',
                'priority': 'medium',
                'category': 'operational',
                'actionable': True
            })
        
        return recommendations
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        positive_words = [
            'growth', 'increase', 'improve', 'success', 'achieve', 'excellent',
            'strong', 'positive', 'opportunity', 'profit', 'gain', 'win', 'good'
        ]
        
        negative_words = [
            'decline', 'decrease', 'loss', 'fail', 'problem', 'issue', 'challenge',
            'risk', 'threat', 'concern', 'difficult', 'poor', 'weak', 'bad'
        ]
        
        text_lower = text.lower()
        positive_count = sum(text_lower.count(word) for word in positive_words)
        negative_count = sum(text_lower.count(word) for word in negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0
            sentiment_label = 'neutral'
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            if sentiment_score > 0.2:
                sentiment_label = 'positive'
            elif sentiment_score < -0.2:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
        
        return {
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'total_sentiment_words': total_sentiment_words
        }
    
    def analyze_urgency_from_text(self, text: str) -> Dict:
        """Analyze urgency from text"""
        text_lower = text.lower()
        urgency_scores = {}
        
        for urgency_type, keywords in self.decision_keywords.items():
            score = 0
            found_keywords = []
            
            for keyword in keywords:
                count = text_lower.count(keyword)
                if count > 0:
                    score += count
                    found_keywords.append(keyword)
            
            urgency_scores[urgency_type] = {
                'score': score,
                'keywords_found': found_keywords
            }
        
        # Determine overall urgency level
        total_urgency = urgency_scores['urgent']['score'] + urgency_scores['risk']['score']
        opportunity_score = urgency_scores['opportunity']['score']
        
        if total_urgency > opportunity_score * 2:
            urgency_level = 'high'
        elif total_urgency > opportunity_score:
            urgency_level = 'medium'
        else:
            urgency_level = 'low'
        
        return {
            'urgency_scores': urgency_scores,
            'overall_urgency': urgency_level,
            'requires_immediate_attention': urgency_scores['urgent']['score'] > 0
        }
    
    def extract_insights_from_text(self, text: str) -> List[Dict]:
        """Extract insights from text"""
        insights = []
        
        # Look for sentences with numbers and business terms
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                has_numbers = bool(re.search(r'\d+', sentence))
                has_business_terms = any(
                    term in sentence.lower() 
                    for keywords in self.business_keywords.values() 
                    for term in keywords
                )
                
                if has_numbers and has_business_terms:
                    insights.append({
                        'type': 'metric_insight',
                        'title': 'Business Metric Found',
                        'description': sentence,
                        'importance': 'high' if any(word in sentence.lower() for word in ['revenue', 'profit', 'growth']) else 'medium'
                    })
        
        return insights[:10]
    
    def generate_recommendations_from_text(self, text: str) -> List[Dict]:
        """Generate recommendations from text"""
        recommendations = []
        
        # Analyze business category
        category_analysis = self.detect_business_category_from_text(text)
        primary_category = category_analysis['primary_category']
        
        # Analyze urgency
        urgency_analysis = self.analyze_urgency_from_text(text)
        
        # Category-based recommendations
        if primary_category == 'financial':
            recommendations.append({
                'title': 'Financial Performance Review',
                'description': 'Document contains financial information. Schedule financial review and implement monitoring.',
                'priority': 'high' if urgency_analysis['overall_urgency'] == 'high' else 'medium',
                'category': 'financial',
                'actionable': True
            })
        
        elif primary_category == 'customer':
            recommendations.append({
                'title': 'Customer Experience Enhancement',
                'description': 'Focus on customer metrics and satisfaction improvement programs.',
                'priority': 'medium',
                'category': 'customer',
                'actionable': True
            })
        
        # Urgency-based recommendations
        if urgency_analysis['requires_immediate_attention']:
            recommendations.append({
                'title': 'Immediate Action Required',
                'description': 'Document indicates urgent matters. Executive review recommended within 48 hours.',
                'priority': 'high',
                'category': 'strategic',
                'actionable': True
            })
        
        return recommendations
    
    def calculate_decision_score_for_df(self, df: pd.DataFrame) -> Dict:
        """Calculate decision score for DataFrame"""
        score = 50  # Base score
        
        # Add points for financial data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['revenue', 'profit', 'sales']):
                score += 20
                break
        
        # Add points for data size
        if len(df) > 100:
            score += 10
        
        # Add points for data quality
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct < 5:
            score += 10
        
        # Determine level
        if score >= 80:
            level = 'executive'
        elif score >= 60:
            level = 'managerial'
        elif score >= 40:
            level = 'operational'
        else:
            level = 'informational'
        
        return {
            'score': min(100, score),
            'level': level,
            'requires_action': score >= 60,
            'confidence': 'high' if score >= 70 else 'medium'
        }
    
    def calculate_decision_score_for_text(self, text: str) -> Dict:
        """Calculate decision score for text"""
        score = 50  # Base score
        
        # Add points for business keywords
        for keywords in self.business_keywords.values():
            for keyword in keywords:
                if keyword in text.lower():
                    score += 2
                    break
        
        # Add points for urgency
        urgency_analysis = self.analyze_urgency_from_text(text)
        if urgency_analysis['requires_immediate_attention']:
            score += 20
        
        # Add points for financial terms
        financial_metrics = self.extract_financial_metrics_from_text(text)
        if financial_metrics['currency_mentions'] > 0:
            score += 15
        
        # Determine level
        if score >= 80:
            level = 'executive'
        elif score >= 60:
            level = 'managerial'
        elif score >= 40:
            level = 'operational'
        else:
            level = 'informational'
        
        return {
            'score': min(100, score),
            'level': level,
            'requires_action': score >= 60,
            'confidence': 'high' if score >= 70 else 'medium'
        }
    
    def analyze_json_structure(self, data: Dict) -> Dict:
        """Analyze JSON structure"""
        structure = {
            'type': type(data).__name__,
            'size': len(data) if hasattr(data, '__len__') else 0
        }
        
        if isinstance(data, dict):
            structure['keys'] = list(data.keys())[:10]  # First 10 keys
            structure['key_count'] = len(data.keys())
        
        elif isinstance(data, list):
            structure['item_types'] = list(set(type(item).__name__ for item in data[:10]))
            structure['sample_item'] = data[0] if data else None
        
        return structure
    
    def detect_business_category_from_json(self, data: Dict) -> Dict:
        """Detect business category from JSON"""
        # Convert JSON to text for analysis
        text = json.dumps(data, default=str).lower()
        return self.detect_business_category_from_text(text)
    
    def generate_insights_from_json(self, data: Dict) -> List[Dict]:
        """Generate insights from JSON"""
        insights = []
        
        if isinstance(data, dict):
            insights.append({
                'type': 'structure',
                'title': 'JSON Structure',
                'description': f'JSON object with {len(data)} key-value pairs',
                'importance': 'low'
            })
        
        elif isinstance(data, list):
            insights.append({
                'type': 'structure',
                'title': 'JSON Array',
                'description': f'JSON array with {len(data)} items',
                'importance': 'low'
            })
        
        return insights
    
    def generate_recommendations_from_json(self, data: Dict) -> List[Dict]:
        """Generate recommendations from JSON"""
        recommendations = []
        
        # Check if it's tabular data
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            recommendations.append({
                'title': 'Data Analysis Opportunity',
                'description': 'JSON contains structured data. Consider converting to CSV for better analysis.',
                'priority': 'medium',
                'category': 'operational',
                'actionable': True
            })
        
        return recommendations
    
    def display_comprehensive_analysis(self, analysis_result: Dict):
        """Display comprehensive analysis results"""
        st.header("📊 Comprehensive Business Analysis")
        
        # File Info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📁 File Type", analysis_result['file_type'])
        with col2:
            st.metric("📅 Analyzed", analysis_result['analysis_timestamp'][:10])
        with col3:
            if 'rows' in analysis_result:
                st.metric("📊 Data Rows", f"{analysis_result['rows']:,}")
            else:
                st.metric("📝 Word Count", f"{analysis_result.get('word_count', 0):,}")
        
        # Decision Score
        if 'decision_score' in analysis_result:
            decision_score = analysis_result['decision_score']
            st.subheader("🎯 Decision-Making Score")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Score", f"{decision_score['score']}/100")
            with col2:
                st.metric("Level", decision_score['level'].title())
            with col3:
                action_color = "🔴" if decision_score['requires_action'] else "🟢"
                st.metric("Action Needed", f"{action_color} {'Yes' if decision_score['requires_action'] else 'No'}")
            with col4:
                st.metric("Confidence", decision_score['confidence'].title())
        
        # Business Category
        if 'business_category' in analysis_result:
            st.subheader("📈 Business Category Analysis")
            category = analysis_result['business_category']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Primary Category", category['primary_category'].title())
                st.metric("Confidence", category['confidence'].title())
            with col2:
                st.metric("Dominant Score", category['dominant_score'])
            
            # Category breakdown
            if 'category_scores' in category:
                for cat_name, cat_data in category['category_scores'].items():
                    if cat_data['score'] > 0:
                        with st.expander(f"📊 {cat_name.title()} Analysis"):
                            st.write(f"**Score:** {cat_data['score']}")
                            st.write(f"**Keywords:** {', '.join(cat_data['keywords_found'])}")
                            st.progress(min(1.0, cat_data['score'] / 10))
        
        # Financial Metrics
        if 'financial_metrics' in analysis_result and analysis_result['financial_metrics']:
            st.subheader("💰 Financial Metrics")
            metrics = analysis_result['financial_metrics']
            
            for metric_name, metric_data in metrics.items():
                if isinstance(metric_data, dict) and 'total' in metric_data:
                    with st.expander(f"💵 {metric_name.title()}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total", f"${metric_data['total']:,.2f}")
                            st.metric("Average", f"${metric_data['average']:,.2f}")
                        with col2:
                            st.metric("Max", f"${metric_data['max']:,.2f}")
                            st.metric("Min", f"${metric_data['min']:,.2f}")
                        if 'trend' in metric_data:
                            st.metric("Trend", metric_data['trend'].title())
                elif isinstance(metric_data, dict):
                    with st.expander(f"📊 {metric_name.title()}"):
                        for key, value in metric_data.items():
                            st.write(f"**{key.title()}:** {value}")
        
        # Data Quality (for CSV/Excel)
        if 'data_quality' in analysis_result:
            st.subheader("🔍 Data Quality Assessment")
            quality = analysis_result['data_quality']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Quality Score", f"{quality['quality_score']:.1f}/100")
                st.metric("Grade", quality['quality_grade'])
            with col2:
                st.metric("Missing Data", f"{quality['missing_percentage']:.1f}%")
                st.metric("Duplicates", f"{quality['duplicate_percentage']:.1f}%")
            with col3:
                st.metric("Total Cells", f"{quality['total_cells']:,}")
                st.metric("Numeric Columns", quality['numeric_columns'])
        
        # Insights
        if 'insights' in analysis_result and analysis_result['insights']:
            st.subheader("💡 Key Business Insights")
            
            for insight in analysis_result['insights']:
                icon = "🔴" if insight['importance'] == 'high' else "🟡" if insight['importance'] == 'medium' else "🟢"
                with st.expander(f"{icon} {insight['title']}"):
                    st.write(insight['description'])
        
        # Recommendations
        if 'recommendations' in analysis_result and analysis_result['recommendations']:
            st.subheader("🎯 Business Recommendations")
            
            for rec in analysis_result['recommendations']:
                priority_color = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                with st.expander(f"{priority_color} {rec['title']}"):
                    st.write(rec['description'])
                    st.write(f"**Category:** {rec['category'].title()}")
                    st.write(f"**Priority:** {rec['priority'].title()}")
                    st.write(f"**Actionable:** {'Yes' if rec['actionable'] else 'No'}")
        
        # Sentiment Analysis (for text files)
        if 'sentiment' in analysis_result:
            st.subheader("😊 Sentiment Analysis")
            sentiment = analysis_result['sentiment']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sentiment", sentiment['sentiment_label'].title())
                st.metric("Score", f"{sentiment['sentiment_score']:.2f}")
            with col2:
                st.metric("Positive Words", sentiment['positive_words'])
                st.metric("Negative Words", sentiment['negative_words'])
            with col3:
                st.metric("Total Sentiment Words", sentiment['total_sentiment_words'])
        
        # Urgency Analysis (for text files)
        if 'urgency' in analysis_result:
            st.subheader("⚡ Urgency Analysis")
            urgency = analysis_result['urgency']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Overall Urgency", urgency['overall_urgency'].title())
                st.metric("Immediate Attention", "Yes" if urgency['requires_immediate_attention'] else "No")
            with col2:
                for urgency_type, data in urgency['urgency_scores'].items():
                    if data['score'] > 0:
                        st.write(f"**{urgency_type.title()}:** {data['score']} mentions")

# Global instance
advanced_file_analyzer = AdvancedFileAnalyzer()
