#!/usr/bin/env python3
"""
Advanced PDF Analyzer for Business Intelligence
Extracts comprehensive business insights from PDF documents
"""

import streamlit as st
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple
import io

class AdvancedPDFAnalyzer:
    """Advanced PDF analysis for business decision making"""
    
    def __init__(self):
        self.business_keywords = {
            'financial': [
                'revenue', 'profit', 'loss', 'income', 'expense', 'budget', 'cost',
                'investment', 'roi', 'margin', 'cash flow', 'balance sheet', 'p&l',
                'earnings', 'sales', 'turnover', 'growth', 'decline', 'increase'
            ],
            'customer': [
                'customer', 'client', 'satisfaction', 'retention', 'churn', 'acquisition',
                'loyalty', 'feedback', 'complaint', 'nps', 'csat', 'user', 'market share'
            ],
            'operational': [
                'efficiency', 'productivity', 'operations', 'process', 'workflow',
                'inventory', 'supply chain', 'logistics', 'quality', 'performance',
                'kpi', 'metrics', 'dashboard', 'analysis', 'report'
            ],
            'strategic': [
                'strategy', 'goal', 'objective', 'mission', 'vision', 'plan',
                'initiative', 'project', 'roadmap', 'timeline', 'milestone',
                'risk', 'opportunity', 'threat', 'swot', 'competitive'
            ]
        }
        
        self.decision_keywords = {
            'urgent': ['urgent', 'immediate', 'critical', 'asap', 'priority', 'emergency'],
            'opportunity': ['opportunity', 'growth', 'expand', 'new', 'potential', 'market'],
            'risk': ['risk', 'threat', 'challenge', 'issue', 'problem', 'concern'],
            'action': ['action', 'implement', 'execute', 'launch', 'start', 'begin']
        }
    
    def analyze_pdf_content(self, pdf_text: str, file_name: str) -> Dict:
        """Comprehensive PDF analysis for business intelligence"""
        
        # Extract key metrics and numbers
        metrics = self.extract_financial_metrics(pdf_text)
        
        # Business category analysis
        category_analysis = self.analyze_business_categories(pdf_text)
        
        # Decision urgency analysis
        urgency_analysis = self.analyze_urgency(pdf_text)
        
        # Sentiment analysis
        sentiment_analysis = self.analyze_sentiment(pdf_text)
        
        # Key insights extraction
        insights = self.extract_key_insights(pdf_text)
        
        # Generate recommendations
        recommendations = self.generate_business_recommendations(
            pdf_text, metrics, category_analysis, urgency_analysis
        )
        
        # Executive summary
        executive_summary = self.generate_executive_summary(
            pdf_text, metrics, category_analysis, file_name
        )
        
        return {
            'file_name': file_name,
            'analysis_timestamp': datetime.now().isoformat(),
            'content_length': len(pdf_text),
            'word_count': len(pdf_text.split()),
            'metrics': metrics,
            'category_analysis': category_analysis,
            'urgency_analysis': urgency_analysis,
            'sentiment_analysis': sentiment_analysis,
            'insights': insights,
            'recommendations': recommendations,
            'executive_summary': executive_summary,
            'decision_score': self.calculate_decision_score(metrics, urgency_analysis, sentiment_analysis)
        }
    
    def extract_financial_metrics(self, text: str) -> Dict:
        """Extract financial metrics from text"""
        metrics = {}
        
        # Currency patterns
        currency_patterns = [
            r'\$[\d,]+\.?\d*',  # $1,234.56
            r'USD\s*[\d,]+\.?\d*',  # USD 1,234.56
            r'[\d,]+\.?\d*\s*USD',  # 1,234.56 USD
            r'[\d,]+\.?\d*\s*(?:million|billion|thousand)',  # 1.5 million
        ]
        
        # Percentage patterns
        percentage_patterns = [
            r'\d+\.?\d*%',  # 15.5%
            r'\d+\.?\d*\s*percent',  # 15.5 percent
        ]
        
        # Extract currency values
        currency_values = []
        for pattern in currency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            currency_values.extend(matches)
        
        # Extract percentages
        percentage_values = []
        for pattern in percentage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            percentage_values.extend(matches)
        
        # Look for specific financial terms
        financial_terms = {
            'revenue': r'(?:revenue|sales|turnover)[\s:]*\$?[\d,]+\.?\d*',
            'profit': r'(?:profit|income|earnings)[\s:]*\$?[\d,]+\.?\d*',
            'loss': r'(?:loss|deficit)[\s:]*\$?[\d,]+\.?\d*',
            'cost': r'(?:cost|expense)[\s:]*\$?[\d,]+\.?\d*',
            'growth': r'(?:growth|increase)[\s:]*\d+\.?\d*%',
            'margin': r'(?:margin)[\s:]*\d+\.?\d*%'
        }
        
        for term, pattern in financial_terms.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                metrics[term] = matches
        
        metrics['currency_mentions'] = len(currency_values)
        metrics['percentage_mentions'] = len(percentage_values)
        metrics['total_financial_terms'] = sum(len(v) for v in metrics.values() if isinstance(v, list))
        
        return metrics
    
    def analyze_business_categories(self, text: str) -> Dict:
        """Analyze business categories in the text"""
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
            'dominant_score': category_scores[primary_category]['score']
        }
    
    def analyze_urgency(self, text: str) -> Dict:
        """Analyze urgency and action items in the text"""
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
        total_urgency = sum(urgency_scores[ut]['score'] for ut in ['urgent', 'risk'])
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
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Basic sentiment analysis for business context"""
        positive_words = [
            'growth', 'increase', 'improve', 'success', 'achieve', 'excellent',
            'strong', 'positive', 'opportunity', 'profit', 'gain', 'win'
        ]
        
        negative_words = [
            'decline', 'decrease', 'loss', 'fail', 'problem', 'issue', 'challenge',
            'risk', 'threat', 'concern', 'difficult', 'poor', 'weak'
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
    
    def extract_key_insights(self, text: str) -> List[Dict]:
        """Extract key business insights from text"""
        insights = []
        
        # Look for sentences with numbers and business terms
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Ignore very short sentences
                # Check if sentence contains business metrics
                has_numbers = bool(re.search(r'\d+', sentence))
                has_business_terms = any(
                    term in sentence.lower() 
                    for keywords in self.business_keywords.values() 
                    for term in keywords
                )
                
                if has_numbers and has_business_terms:
                    insights.append({
                        'type': 'metric_insight',
                        'content': sentence,
                        'importance': 'high' if any(word in sentence.lower() for word in ['revenue', 'profit', 'growth']) else 'medium'
                    })
        
        # Look for action items
        action_patterns = [
            r'(?:should|must|need to|will|shall)\s+[\w\s]+',
            r'(?:recommend|suggest|propose)\s+[\w\s]+',
            r'(?:implement|execute|launch)\s+[\w\s]+'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                insights.append({
                    'type': 'action_item',
                    'content': match.strip(),
                    'importance': 'high'
                })
        
        return insights[:10]  # Limit to top 10 insights
    
    def generate_business_recommendations(self, text: str, metrics: Dict, 
                                        category_analysis: Dict, urgency_analysis: Dict) -> List[Dict]:
        """Generate business recommendations based on analysis"""
        recommendations = []
        
        # Financial recommendations
        if metrics.get('revenue'):
            recommendations.append({
                'title': 'Revenue Performance Review',
                'description': 'Document contains revenue data. Implement regular revenue tracking and variance analysis.',
                'priority': 'high' if urgency_analysis['overall_urgency'] == 'high' else 'medium',
                'category': 'financial',
                'actionable': True
            })
        
        # Category-based recommendations
        primary_category = category_analysis['primary_category']
        
        if primary_category == 'financial':
            recommendations.append({
                'title': 'Financial Health Monitoring',
                'description': 'Focus on financial metrics. Implement dashboard for real-time financial monitoring.',
                'priority': 'high',
                'category': 'financial',
                'actionable': True
            })
        
        elif primary_category == 'customer':
            recommendations.append({
                'title': 'Customer Experience Enhancement',
                'description': 'Document focuses on customer metrics. Implement customer satisfaction tracking and improvement programs.',
                'priority': 'medium',
                'category': 'customer',
                'actionable': True
            })
        
        # Urgency-based recommendations
        if urgency_analysis['requires_immediate_attention']:
            recommendations.append({
                'title': 'Immediate Action Required',
                'description': 'Document indicates urgent matters. Schedule executive review within 48 hours.',
                'priority': 'high',
                'category': 'strategic',
                'actionable': True
            })
        
        # Opportunity-based recommendations
        if urgency_analysis['urgency_scores']['opportunity']['score'] > 0:
            recommendations.append({
                'title': 'Growth Opportunity Exploration',
                'description': 'Document identifies growth opportunities. Conduct feasibility study and develop implementation plan.',
                'priority': 'medium',
                'category': 'strategic',
                'actionable': True
            })
        
        return recommendations
    
    def generate_executive_summary(self, text: str, metrics: Dict, 
                                 category_analysis: Dict, file_name: str) -> Dict:
        """Generate executive summary for quick decision making"""
        
        # Key findings
        key_findings = []
        
        if metrics['total_financial_terms'] > 10:
            key_findings.append("Document contains significant financial data requiring detailed analysis")
        
        if category_analysis['dominant_score'] > 5:
            key_findings.append(f"Primary focus on {category_analysis['primary_category']} matters")
        
        # Extract first few sentences as summary
        sentences = re.split(r'[.!?]+', text)
        summary_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
        
        return {
            'document_title': file_name,
            'key_findings': key_findings,
            'summary_text': ' '.join(summary_sentences),
            'primary_focus': category_analysis['primary_category'],
            'data_density': 'high' if metrics['total_financial_terms'] > 5 else 'medium',
            'action_items_count': len([s for s in sentences if any(word in s.lower() for word in ['should', 'must', 'recommend'])])
        }
    
    def calculate_decision_score(self, metrics: Dict, urgency_analysis: Dict, 
                               sentiment_analysis: Dict) -> Dict:
        """Calculate decision-making score"""
        
        # Base score from metrics
        metrics_score = min(100, metrics['total_financial_terms'] * 5)
        
        # Urgency impact
        urgency_multiplier = 1.5 if urgency_analysis['overall_urgency'] == 'high' else 1.2 if urgency_analysis['overall_urgency'] == 'medium' else 1.0
        
        # Sentiment adjustment
        sentiment_adjustment = 1.2 if sentiment_analysis['sentiment_label'] == 'positive' else 0.8 if sentiment_analysis['sentiment_label'] == 'negative' else 1.0
        
        # Final score
        final_score = min(100, (metrics_score * urgency_multiplier * sentiment_adjustment))
        
        # Decision level
        if final_score >= 80:
            decision_level = 'executive'
        elif final_score >= 60:
            decision_level = 'managerial'
        elif final_score >= 40:
            decision_level = 'operational'
        else:
            decision_level = 'informational'
        
        return {
            'score': round(final_score, 1),
            'level': decision_level,
            'requires_action': final_score >= 60,
            'confidence': 'high' if final_score >= 70 else 'medium' if final_score >= 40 else 'low'
        }
    
    def display_comprehensive_analysis(self, analysis_result: Dict):
        """Display comprehensive analysis results"""
        st.header("📊 Comprehensive Business Analysis")
        
        # Executive Summary
        with st.expander("📋 Executive Summary", expanded=True):
            exec_summary = analysis_result['executive_summary']
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Document:** {exec_summary['document_title']}")
                st.write(f"**Primary Focus:** {exec_summary['primary_focus'].title()}")
                st.write(f"**Data Density:** {exec_summary['data_density'].title()}")
            
            with col2:
                st.write(f"**Action Items:** {exec_summary['action_items_count']}")
                st.write(f"**Word Count:** {analysis_result['word_count']:,}")
            
            st.write("**Summary:**")
            st.write(exec_summary['summary_text'])
            
            if exec_summary['key_findings']:
                st.write("**Key Findings:**")
                for finding in exec_summary['key_findings']:
                    st.write(f"• {finding}")
        
        # Decision Score
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
        
        # Category Analysis
        st.subheader("📈 Business Category Analysis")
        category_analysis = analysis_result['category_analysis']
        
        for category, data in category_analysis['category_scores'].items():
            if data['score'] > 0:
                with st.expander(f"📊 {category.title()} Analysis (Score: {data['score']})"):
                    st.write(f"**Keywords Found:** {', '.join(data['keywords_found'])}")
                    st.write(f"**Percentage:** {data['percentage']:.2f}%")
                    st.progress(min(1.0, data['percentage'] / 10))
        
        # Financial Metrics
        if analysis_result['metrics']['total_financial_terms'] > 0:
            st.subheader("💰 Financial Metrics Found")
            metrics = analysis_result['metrics']
            
            for metric_type, values in metrics.items():
                if isinstance(values, list) and values:
                    st.write(f"**{metric_type.title()}:** {', '.join(values[:3])}")
        
        # Urgency Analysis
        st.subheader("⚡ Urgency & Priority Analysis")
        urgency = analysis_result['urgency_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Urgency", urgency['overall_urgency'].title())
            st.metric("Immediate Attention", "Yes" if urgency['requires_immediate_attention'] else "No")
        
        with col2:
            for urgency_type, data in urgency['urgency_scores'].items():
                if data['score'] > 0:
                    st.write(f"**{urgency_type.title()}:** {data['score']} mentions")
        
        # Key Insights
        if analysis_result['insights']:
            st.subheader("💡 Key Business Insights")
            
            for insight in analysis_result['insights']:
                icon = "🔴" if insight['importance'] == 'high' else "🟡"
                with st.expander(f"{icon} {insight['type'].title().replace('_', ' ')}"):
                    st.write(insight['content'])
        
        # Recommendations
        if analysis_result['recommendations']:
            st.subheader("🎯 Business Recommendations")
            
            for rec in analysis_result['recommendations']:
                priority_color = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                with st.expander(f"{priority_color} {rec['title']}"):
                    st.write(rec['description'])
                    st.write(f"**Category:** {rec['category'].title()}")
                    st.write(f"**Priority:** {rec['priority'].title()}")
                    st.write(f"**Actionable:** {'Yes' if rec['actionable'] else 'No'}")

# Global instance
advanced_pdf_analyzer = AdvancedPDFAnalyzer()
