#!/usr/bin/env python3
"""
AI-Powered Decision Engine for Business Dashboard
Automatic decision making based on data analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

class DecisionEngine:
    """AI-powered decision making engine"""
    
    def __init__(self):
        self.decision_rules = {
            'revenue': {
                'critical_threshold': 0.8,
                'warning_threshold': 0.6,
                'actions': {
                    'critical': ['cost_cutting', 'revenue_boost', 'emergency_measures'],
                    'warning': ['monitor_closely', 'prepare_contingency', 'optimize_operations'],
                    'good': ['maintain_growth', 'expansion_planning', 'invest_innovation']
                }
            },
            'customer_satisfaction': {
                'critical_threshold': 0.7,
                'warning_threshold': 0.8,
                'actions': {
                    'critical': ['immediate_service_improvement', 'customer_recovery', 'management_intervention'],
                    'warning': ['service_training', 'feedback_collection', 'process_improvement'],
                    'good': ['maintain_quality', 'loyalty_programs', 'referral_incentives']
                }
            },
            'operational_efficiency': {
                'critical_threshold': 0.7,
                'warning_threshold': 0.8,
                'actions': {
                    'critical': ['process_reengineering', 'staff_retraining', 'technology_upgrade'],
                    'warning': ['performance_monitoring', 'incremental_improvements', 'resource_optimization'],
                    'good': ['continuous_improvement', 'best_practices_sharing', 'innovation_encouragement']
                }
            },
            'market_position': {
                'critical_threshold': 0.6,
                'warning_threshold': 0.75,
                'actions': {
                    'critical': ['market_research', 'competitive_analysis', 'strategy_pivot'],
                    'warning': ['market_monitoring', 'competitive_intelligence', 'positioning_adjustment'],
                    'good': ['market_expansion', 'brand_strengthening', 'thought_leadership']
                }
            }
        }
        
        self.decision_priorities = {
            'high': ['critical_revenue', 'critical_customers', 'critical_operations'],
            'medium': ['warning_revenue', 'warning_customers', 'warning_operations'],
            'low': ['good_performance', 'growth_opportunities', 'optimization']
        }
    
    def analyze_business_health(self, data: Dict) -> Dict:
        """Analyze business health and generate decisions"""
        
        # Extract key metrics
        kpis = data.get('kpis', [])
        business_health = data.get('business_health_score', {})
        
        # Calculate health scores
        health_scores = self._calculate_health_scores(kpis, business_health)
        
        # Generate decisions for each area
        decisions = {}
        
        for area, score in health_scores.items():
            decisions[area] = self._generate_area_decision(area, score, data)
        
        # Prioritize decisions
        prioritized_decisions = self._prioritize_decisions(decisions)
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(health_scores, prioritized_decisions)
        
        return {
            'health_scores': health_scores,
            'decisions': decisions,
            'prioritized_decisions': prioritized_decisions,
            'executive_summary': executive_summary,
            'generated_at': datetime.now().isoformat(),
            'confidence_score': self._calculate_confidence_score(health_scores, data)
        }
    
    def _calculate_health_scores(self, kpis: List, business_health: Dict) -> Dict:
        """Calculate health scores for different business areas"""
        
        scores = {
            'revenue': 0.0,
            'customer_satisfaction': 0.0,
            'operational_efficiency': 0.0,
            'market_position': 0.0
        }
        
        # Use business health scores if available
        if business_health:
            scores['revenue'] = business_health.get('financial', 0) / 100.0
            scores['customer_satisfaction'] = business_health.get('customer', 0) / 100.0
            scores['operational_efficiency'] = business_health.get('operational', 0) / 100.0
            scores['market_position'] = business_health.get('overall', 0) / 100.0
        
        # Enhance with KPI analysis
        for kpi in kpis:
            name = kpi.get('name', '').lower()
            value = kpi.get('value', 0)
            change = kpi.get('change', 0)
            
            if 'revenue' in name or 'sales' in name:
                scores['revenue'] = min(1.0, max(0.0, scores['revenue'] + (change / 100.0)))
            elif 'customer' in name or 'satisfaction' in name or 'nps' in name:
                scores['customer_satisfaction'] = min(1.0, max(0.0, scores['customer_satisfaction'] + (change / 100.0)))
            elif 'efficiency' in name or 'productivity' in name:
                scores['operational_efficiency'] = min(1.0, max(0.0, scores['operational_efficiency'] + (change / 100.0)))
            elif 'market' in name or 'share' in name:
                scores['market_position'] = min(1.0, max(0.0, scores['market_position'] + (change / 100.0)))
        
        return scores
    
    def _generate_area_decision(self, area: str, score: float, data: Dict) -> Dict:
        """Generate decision for a specific business area"""
        
        rules = self.decision_rules.get(area, {})
        critical_threshold = rules.get('critical_threshold', 0.7)
        warning_threshold = rules.get('warning_threshold', 0.8)
        actions = rules.get('actions', {})
        
        # Determine status
        if score < critical_threshold:
            status = 'critical'
            urgency = 'immediate'
            impact = 'high'
        elif score < warning_threshold:
            status = 'warning'
            urgency = 'within_week'
            impact = 'medium'
        else:
            status = 'good'
            urgency = 'within_month'
            impact = 'low'
        
        # Get recommended actions
        recommended_actions = actions.get(status, ['monitor'])
        
        # Generate specific recommendations
        specific_recommendations = self._generate_specific_recommendations(area, status, score, data)
        
        # Calculate risk level
        risk_level = self._calculate_risk_level(area, score, status)
        
        return {
            'area': area,
            'score': score,
            'status': status,
            'urgency': urgency,
            'impact': impact,
            'risk_level': risk_level,
            'recommended_actions': recommended_actions,
            'specific_recommendations': specific_recommendations,
            'success_metrics': self._define_success_metrics(area, status),
            'estimated_timeline': self._estimate_timeline(status),
            'resource_requirements': self._estimate_resources(area, status)
        }
    
    def _generate_specific_recommendations(self, area: str, status: str, score: float, data: Dict) -> List[str]:
        """Generate specific recommendations based on area and status"""
        
        recommendations = []
        
        if area == 'revenue':
            if status == 'critical':
                recommendations = [
                    "Implement immediate cost reduction measures targeting 15% reduction",
                    "Launch emergency sales campaign with 20% discount for quick cash flow",
                    "Renegotiate with suppliers for better payment terms",
                    "Consider temporary staff reduction or reduced hours"
                ]
            elif status == 'warning':
                recommendations = [
                    "Increase marketing spend by 10% focusing on high-conversion channels",
                    "Implement customer retention program to reduce churn",
                    "Optimize pricing strategy based on competitor analysis",
                    "Launch new product features to increase customer value"
                ]
            else:
                recommendations = [
                    "Invest in market expansion to adjacent segments",
                    "Develop strategic partnerships for growth",
                    "Increase R&D investment for long-term competitiveness",
                    "Consider acquisition opportunities for market share"
                ]
        
        elif area == 'customer_satisfaction':
            if status == 'critical':
                recommendations = [
                    "Implement 24/7 customer support escalation team",
                    "Offer immediate compensation for affected customers",
                    "Conduct emergency customer satisfaction survey",
                    "Appoint customer experience task force"
                ]
            elif status == 'warning':
                recommendations = [
                    "Implement proactive customer outreach program",
                    "Enhance product training for support staff",
                    "Improve product documentation and FAQs",
                    "Launch customer feedback collection campaign"
                ]
            else:
                recommendations = [
                    "Develop customer advocacy program",
                    "Implement customer success management",
                    "Create customer advisory board",
                    "Expand loyalty and rewards program"
                ]
        
        elif area == 'operational_efficiency':
            if status == 'critical':
                recommendations = [
                    "Conduct immediate process audit and optimization",
                    "Implement performance monitoring dashboard",
                    "Provide emergency staff training programs",
                    "Upgrade critical technology systems"
                ]
            elif status == 'warning':
                recommendations = [
                    "Implement continuous improvement program",
                    "Optimize resource allocation based on demand",
                    "Automate repetitive manual processes",
                    "Implement performance incentives"
                ]
            else:
                recommendations = [
                    "Invest in advanced automation technologies",
                    "Implement best practices sharing program",
                    "Develop innovation culture and incentives",
                    "Expand strategic partnerships for efficiency"
                ]
        
        elif area == 'market_position':
            if status == 'critical':
                recommendations = [
                    "Conduct emergency competitive analysis",
                    "Implement market research for new opportunities",
                    "Consider strategic pivot or repositioning",
                    "Strengthen brand messaging and differentiation"
                ]
            elif status == 'warning':
                recommendations = [
                    "Increase competitive intelligence efforts",
                    "Enhance product differentiation",
                    "Implement targeted marketing campaigns",
                    "Explore new market segments"
                ]
            else:
                recommendations = [
                    "Expand into new geographic markets",
                    "Develop strategic partnerships for growth",
                    "Invest in thought leadership and brand building",
                    "Consider mergers and acquisitions"
                ]
        
        return recommendations
    
    def _calculate_risk_level(self, area: str, score: float, status: str) -> str:
        """Calculate risk level for the area"""
        
        if status == 'critical':
            return 'high'
        elif status == 'warning':
            return 'medium'
        else:
            return 'low'
    
    def _define_success_metrics(self, area: str, status: str) -> List[str]:
        """Define success metrics for the decision"""
        
        if area == 'revenue':
            return [
                "Revenue growth rate > 15%",
                "Profit margin improvement > 5%",
                "Customer acquisition cost reduction > 20%",
                "Cash flow positive within 3 months"
            ]
        elif area == 'customer_satisfaction':
            return [
                "Customer satisfaction score > 85%",
                "Net Promoter Score > 50",
                "Customer churn rate < 5%",
                "Customer support response time < 2 hours"
            ]
        elif area == 'operational_efficiency':
            return [
                "Process efficiency improvement > 25%",
                "Resource utilization > 80%",
                "Error rate reduction > 50%",
                "Employee productivity increase > 15%"
            ]
        elif area == 'market_position':
            return [
                "Market share increase > 10%",
                "Brand awareness improvement > 20%",
                "Competitive advantage score > 75%",
                "New customer acquisition > 30%"
            ]
        
        return ["Overall business improvement"]
    
    def _estimate_timeline(self, status: str) -> str:
        """Estimate implementation timeline"""
        
        if status == 'critical':
            return "1-2 weeks (immediate action required)"
        elif status == 'warning':
            return "2-4 weeks (planned implementation)"
        else:
            return "1-3 months (strategic implementation)"
    
    def _estimate_resources(self, area: str, status: str) -> Dict:
        """Estimate resource requirements"""
        
        if status == 'critical':
            return {
                'budget': 'High - Emergency funds required',
                'staff': 'Cross-functional team needed',
                'technology': 'Immediate system upgrades required',
                'external_help': 'Consultants may be needed'
            }
        elif status == 'warning':
            return {
                'budget': 'Medium - Planned investment',
                'staff': 'Dedicated team members',
                'technology': 'System enhancements needed',
                'external_help': 'Optional expert consultation'
            }
        else:
            return {
                'budget': 'Low to Medium - Strategic investment',
                'staff': 'Existing team capacity',
                'technology': 'Gradual upgrades',
                'external_help': 'Long-term partnerships'
            }
    
    def _prioritize_decisions(self, decisions: Dict) -> List[Dict]:
        """Prioritize decisions based on urgency and impact"""
        
        decision_list = []
        
        for area, decision in decisions.items():
            decision_list.append({
                'area': area,
                'priority_score': self._calculate_priority_score(decision),
                'decision': decision
            })
        
        # Sort by priority score (higher = more urgent)
        decision_list.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return decision_list
    
    def _calculate_priority_score(self, decision: Dict) -> float:
        """Calculate priority score for a decision"""
        
        score = 0.0
        
        # Status weight
        status = decision.get('status', 'good')
        if status == 'critical':
            score += 100
        elif status == 'warning':
            score += 50
        else:
            score += 10
        
        # Impact weight
        impact = decision.get('impact', 'low')
        if impact == 'high':
            score += 30
        elif impact == 'medium':
            score += 20
        else:
            score += 10
        
        # Urgency weight
        urgency = decision.get('urgency', 'within_month')
        if urgency == 'immediate':
            score += 20
        elif urgency == 'within_week':
            score += 15
        else:
            score += 5
        
        # Risk level weight
        risk = decision.get('risk_level', 'low')
        if risk == 'high':
            score += 25
        elif risk == 'medium':
            score += 15
        else:
            score += 5
        
        return score
    
    def _generate_executive_summary(self, health_scores: Dict, prioritized_decisions: List[Dict]) -> Dict:
        """Generate executive summary for leadership"""
        
        # Overall health assessment
        overall_health = sum(health_scores.values()) / len(health_scores)
        
        # Critical issues
        critical_issues = [d for d in prioritized_decisions if d['decision']['status'] == 'critical']
        
        # Key opportunities
        good_areas = [d for d in prioritized_decisions if d['decision']['status'] == 'good']
        
        # Top 3 priorities
        top_priorities = prioritized_decisions[:3]
        
        return {
            'overall_health_score': overall_health,
            'health_assessment': self._get_health_assessment(overall_health),
            'critical_issues_count': len(critical_issues),
            'critical_issues': [d['area'] for d in critical_issues],
            'opportunities_count': len(good_areas),
            'opportunities': [d['area'] for d in good_areas],
            'top_priorities': [
                {
                    'rank': i + 1,
                    'area': d['area'],
                    'status': d['decision']['status'],
                    'urgency': d['decision']['urgency'],
                    'key_action': d['decision']['specific_recommendations'][0] if d['decision']['specific_recommendations'] else 'Monitor closely'
                }
                for i, d in enumerate(top_priorities)
            ],
            'recommended_focus': self._get_recommended_focus(overall_health, critical_issues),
            'next_review_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        }
    
    def _get_health_assessment(self, score: float) -> str:
        """Get health assessment based on score"""
        
        if score >= 0.8:
            return "Excellent - Business is performing well with strong growth potential"
        elif score >= 0.7:
            return "Good - Business is stable with room for improvement"
        elif score >= 0.6:
            return "Fair - Business needs attention in several areas"
        else:
            return "Poor - Business requires immediate intervention"
    
    def _get_recommended_focus(self, overall_health: float, critical_issues: List) -> str:
        """Get recommended focus for leadership"""
        
        if len(critical_issues) > 2:
            return "CRITICAL - Focus on stabilizing business operations and addressing critical issues immediately"
        elif len(critical_issues) > 0:
            return "HIGH PRIORITY - Address critical issues while maintaining operational stability"
        elif overall_health < 0.7:
            return "IMPROVEMENT - Focus on systematic improvements across all business areas"
        else:
            return "GROWTH - Focus on strategic growth and market expansion opportunities"
    
    def _calculate_confidence_score(self, health_scores: Dict, data: Dict) -> float:
        """Calculate confidence score for the decisions"""
        
        confidence = 0.5  # Base confidence
        
        # Data completeness
        if data.get('kpis'):
            confidence += 0.2
        if data.get('business_health_score'):
            confidence += 0.2
        
        # Data quality
        if len(health_scores) > 0:
            avg_score = sum(health_scores.values()) / len(health_scores)
            confidence += avg_score * 0.1
        
        return min(1.0, confidence)

# Global decision engine instance
decision_engine = DecisionEngine()
