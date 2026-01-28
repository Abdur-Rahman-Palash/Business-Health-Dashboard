#!/usr/bin/env python3
"""
Bilingual Decision Engine
Provides business recommendations in both Bangla and English
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json

class Language(Enum):
    BANGLA = "bn"
    ENGLISH = "en"

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class DecisionRecommendation:
    """Business decision recommendation"""
    title_en: str
    title_bn: str
    description_en: str
    description_bn: str
    action_en: str
    action_bn: str
    priority: Priority
    impact_score: float
    implementation_time: str
    resources_needed: List[str]
    kpi_affected: str

class BilingualDecisionEngine:
    """Generates business recommendations in both languages"""
    
    def __init__(self):
        self.recommendations_templates = self._initialize_recommendation_templates()
        self.business_terms = self._initialize_business_terms()
    
    def _initialize_recommendation_templates(self) -> Dict[str, Dict]:
        """Initialize bilingual recommendation templates"""
        return {
            'revenue_growth': {
                'en': {
                    'high': {
                        'title': 'Critical: Revenue Decline Detected',
                        'description': 'Your revenue has decreased by {percentage}% in the last period. Immediate action required to reverse this trend.',
                        'action': 'Implement aggressive sales strategy and review pricing structure',
                        'implementation_time': '1-2 weeks',
                        'resources': ['Sales Team', 'Marketing Budget', 'Pricing Analyst']
                    },
                    'medium': {
                        'title': 'Revenue Growth Opportunity',
                        'description': 'Revenue growth is slowing down. Consider new market expansion or product diversification.',
                        'action': 'Explore new customer segments and product lines',
                        'implementation_time': '2-4 weeks',
                        'resources': ['Market Research', 'Product Development', 'Sales Team']
                    },
                    'low': {
                        'title': 'Maintain Revenue Growth',
                        'description': 'Revenue is growing steadily. Continue current strategies and monitor market trends.',
                        'action': 'Scale successful initiatives and optimize operations',
                        'implementation_time': 'Ongoing',
                        'resources': ['Operations Team', 'Analytics Tools']
                    }
                },
                'bn': {
                    'high': {
                        'title': 'সতর্কতা: আয় হ্রাস পেয়েছে',
                        'description': 'আপনার আয় গত সময়ে {percentage}% কমেছে। এই প্রবণতা ঠেকাতে তাৎক্ষণিক ব্যবস্থা প্রয়োজন।',
                        'action': 'আক্রমনাত্মক বিক্রয় কৌশল বাস্তবায়ন এবং মূল্য কাঠামো পর্যালোচনা করুন',
                        'implementation_time': '১-২ সপ্তাহ',
                        'resources': ['বিক্রয় দল', 'মার্কেটিং বাজেট', 'মূল্য বিশ্লেষক']
                    },
                    'medium': {
                        'title': 'আয় বৃদ্ধির সুযোগ',
                        'description': 'আয় বৃদ্ধির গতি কমছে। নতুন বাজার সম্প্রসারণ বা পণ্য বৈচিত্র্য বিবেচনা করুন।',
                        'action': 'নতুন গ্রাহক সেগমেন্ট এবং পণ্য লাইন অন্বেষণ করুন',
                        'implementation_time': '২-৪ সপ্তাহ',
                        'resources': ['বাজার গবেষণা', 'পণ্য উন্নয়ন', 'বিক্রয় দল']
                    },
                    'low': {
                        'title': 'আয় বৃদ্ধি বজায় রাখুন',
                        'description': 'আয় স্থিতিশীলভাবে বাড়ছে। বর্তমান কৌশলগুলি চালিয়ে যান এবং বাজার প্রবণতা পর্যবেক্ষণ করুন।',
                        'action': 'সফল উদ্যোগগুলি স্কেল করুন এবং অপারেশন অপ্টিমাইজ করুন',
                        'implementation_time': 'চলমান',
                        'resources': ['অপারেশন দল', 'বিশ্লেষণ সরঞ্জাম']
                    }
                }
            },
            'customer_retention': {
                'en': {
                    'high': {
                        'title': 'Urgent: High Customer Churn Rate',
                        'description': 'Customer churn rate is {percentage}%, which is above industry average. Immediate retention strategies needed.',
                        'action': 'Implement customer feedback system and improve service quality',
                        'implementation_time': '1-3 weeks',
                        'resources': ['Customer Service Team', 'CRM System', 'Training Budget']
                    },
                    'medium': {
                        'title': 'Customer Retention Improvement',
                        'description': 'Customer retention can be improved. Focus on customer experience and loyalty programs.',
                        'action': 'Develop customer loyalty initiatives and enhance support',
                        'implementation_time': '3-6 weeks',
                        'resources': ['Marketing Team', 'Customer Success', 'Loyalty Program Budget']
                    },
                    'low': {
                        'title': 'Maintain Customer Satisfaction',
                        'description': 'Customer retention is good. Continue excellent service and monitor satisfaction levels.',
                        'action': 'Maintain service quality and gather regular feedback',
                        'implementation_time': 'Ongoing',
                        'resources': ['Customer Service Team', 'Feedback Tools']
                    }
                },
                'bn': {
                    'high': {
                        'title': 'জরুরি: গ্রাহক ক্ষয়ক্ষতি বেশি',
                        'description': 'গ্রাহক ক্ষয়ক্ষতির হার {percentage}%, যা শিল্প গড়ের উপরে। তাৎক্ষণিক ধরে রাখার কৌশল প্রয়োজন।',
                        'action': 'গ্রাহক প্রতিক্রিয়া ব্যবস্থা বাস্তবায়ন এবং সেবা মান উন্নত করুন',
                        'implementation_time': '১-৩ সপ্তাহ',
                        'resources': ['গ্রাহক সেবা দল', 'সিআরএম সিস্টেম', 'প্রশিক্ষণ বাজেট']
                    },
                    'medium': {
                        'title': 'গ্রাহক ধরে রাখার উন্নতি',
                        'description': 'গ্রাহক ধরে রাখা উন্নত করা যেতে পারে। গ্রাহক অভিজ্ঞতা এবং আনুগত্য প্রোগ্রামের উপর ফোকাস করুন।',
                        'action': 'গ্রাহক আনুগত্য উদ্যোগ তৈরি করুন এবং সহায়তা বাড়ান',
                        'implementation_time': '৩-৬ সপ্তাহ',
                        'resources': ['মার্কেটিং দল', 'গ্রাহক সাফল্য', 'আনুগত্য প্রোগ্রাম বাজেট']
                    },
                    'low': {
                        'title': 'গ্রাহক সন্তুষ্টি বজায় রাখুন',
                        'description': 'গ্রাহক ধরে রাখা ভালো। চমৎকার সেবা চালিয়ে যান এবং সন্তুষ্টি স্তর পর্যবেক্ষণ করুন।',
                        'action': 'সেবা মান বজায় রাখুন এবং নিয়মিত প্রতিক্রিয়া সংগ্রহ করুন',
                        'implementation_time': 'চলমান',
                        'resources': ['গ্রাহক সেবা দল', 'প্রতিক্রিয়া সরঞ্জাম']
                    }
                }
            },
            'cost_optimization': {
                'en': {
                    'high': {
                        'title': 'Critical: High Operating Costs',
                        'description': 'Operating costs are {percentage}% above industry benchmarks. Immediate cost-cutting measures required.',
                        'action': 'Review all expenses and implement cost reduction strategies',
                        'implementation_time': '2-4 weeks',
                        'resources': ['Finance Team', 'Operations', 'Process Consultants']
                    },
                    'medium': {
                        'title': 'Cost Optimization Opportunity',
                        'description': 'Costs can be optimized without impacting quality. Focus on operational efficiency.',
                        'action': 'Implement lean processes and negotiate better supplier terms',
                        'implementation_time': '4-8 weeks',
                        'resources': ['Operations Team', 'Procurement', 'Process Improvement Tools']
                    },
                    'low': {
                        'title': 'Maintain Cost Efficiency',
                        'description': 'Cost structure is optimal. Continue monitoring and regular optimization reviews.',
                        'action': 'Maintain efficient operations and periodic cost reviews',
                        'implementation_time': 'Quarterly',
                        'resources': ['Finance Team', 'Management']
                    }
                },
                'bn': {
                    'high': {
                        'title': 'সতর্কতা: উচ্চ পরিচালন ব্যয়',
                        'description': 'পরিচালন ব্যয় শিল্প বেঞ্চমার্কের {percentage}% উপরে। তাৎক্ষণিক খরচ কমানোর ব্যবস্থা প্রয়োজন।',
                        'action': 'সব ব্যয় পর্যালোচনা করুন এবং খরচ হ্রাস কৌশল বাস্তবায়ন করুন',
                        'implementation_time': '২-৪ সপ্তাহ',
                        'resources': ['আর্থিক দল', 'অপারেশন', 'প্রক্রিয়া কনসালট্যান্ট']
                    },
                    'medium': {
                        'title': 'খরচ অপ্টিমাইজেশন সুযোগ',
                        'description': 'মান প্রভাবিত না করে খরচ অপ্টিমাইজ করা যেতে পারে। অপারেশনাল দক্ষতার উপর ফোকাস করুন।',
                        'action': 'লিন প্রক্রিয়া বাস্তবায়ন এবং সরবরাহকারী শর্তাবলী আলোচনা করুন',
                        'implementation_time': '৪-৮ সপ্তাহ',
                        'resources': ['অপারেশন দল', 'ক্রয়', 'প্রক্রিয়া উন্নতি সরঞ্জাম']
                    },
                    'low': {
                        'title': 'খরচ দক্ষতা বজায় রাখুন',
                        'description': 'খরচ কাঠামো অপ্টিমাল। পর্যবেক্ষণ চালিয়ে যান এবং নিয়মিত অপ্টিমাইজেশন পর্যালোচনা করুন।',
                        'action': 'দক্ষ অপারেশন বজায় রাখুন এবং পর্যায়ক্রমিক খরচ পর্যালোচনা করুন',
                        'implementation_time': 'ত্রৈমাসিক',
                        'resources': ['আর্থিক দল', 'ব্যবস্থাপনা']
                    }
                }
            },
            'market_expansion': {
                'en': {
                    'high': {
                        'title': 'Strategic: Market Expansion Opportunity',
                        'description': 'Strong market position indicates readiness for expansion. Consider new geographic markets.',
                        'action': 'Develop market entry strategy and expansion plan',
                        'implementation_time': '3-6 months',
                        'resources': ['Business Development', 'Market Research', 'Legal Team', 'Expansion Budget']
                    },
                    'medium': {
                        'title': 'Market Growth Potential',
                        'description': 'Current market shows growth potential. Explore adjacent markets or customer segments.',
                        'action': 'Research adjacent markets and develop growth initiatives',
                        'implementation_time': '2-4 months',
                        'resources': ['Marketing Team', 'Sales Team', 'Market Analysis Tools']
                    },
                    'low': {
                        'title': 'Market Position Monitoring',
                        'description': 'Maintain current market position and monitor opportunities for future growth.',
                        'action': 'Continue market analysis and competitive monitoring',
                        'implementation_time': 'Ongoing',
                        'resources': ['Market Research Team', 'Analytics Tools']
                    }
                },
                'bn': {
                    'high': {
                        'title': 'কৌশলগত: বাজার সম্প্রসারণ সুযোগ',
                        'description': 'শক্তিশালী বাজার অবস্থান সম্প্রসারণের জন্য প্রস্তুততা নির্দেশ করে। নতুন ভৌগলিক বাজার বিবেচনা করুন।',
                        'action': 'বাজার প্রবেশ কৌশল এবং সম্প্রসারণ পরিকল্পনা তৈরি করুন',
                        'implementation_time': '৩-৬ মাস',
                        'resources': ['ব্যবসা উন্নয়ন', 'বাজার গবেষণা', 'আইনী দল', 'সম্প্রসারণ বাজেট']
                    },
                    'medium': {
                        'title': 'বাজার প্রবৃদ্ধির সম্ভাবনা',
                        'description': 'বর্তমান বাজার প্রবৃদ্ধির সম্ভাবনা দেখায়। সংলগ্ন বাজার বা গ্রাহক সেগমেন্ট অন্বেষণ করুন।',
                        'action': 'সংলগ্ন বাজার গবেষণা করুন এবং প্রবৃদ্ধি উদ্যোগ তৈরি করুন',
                        'implementation_time': '২-৪ মাস',
                        'resources': ['মার্কেটিং দল', 'বিক্রয় দল', 'বাজার বিশ্লেষণ সরঞ্জাম']
                    },
                    'low': {
                        'title': 'বাজার অবস্থান পর্যবেক্ষণ',
                        'description': 'বর্তমান বাজার অবস্থান বজায় রাখুন এবং ভবিষ্যতের প্রবৃদ্ধির সুযোগ পর্যবেক্ষণ করুন।',
                        'action': 'বাজার বিশ্লেষণ এবং প্রতিযোগিতামূলক পর্যবেক্ষণ চালিয়ে যান',
                        'implementation_time': 'চলমান',
                        'resources': ['বাজার গবেষণা দল', 'বিশ্লেষণ সরঞ্জাম']
                    }
                }
            }
        }
    
    def _initialize_business_terms(self) -> Dict[str, Dict[str, str]]:
        """Initialize bilingual business terms"""
        return {
            'revenue': {'en': 'Revenue', 'bn': 'আয়'},
            'profit': {'en': 'Profit', 'bn': 'মুনাফা'},
            'customers': {'en': 'Customers', 'bn': 'গ্রাহক'},
            'costs': {'en': 'Costs', 'bn': 'খরচ'},
            'growth': {'en': 'Growth', 'bn': 'প্রবৃদ্ধি'},
            'churn': {'en': 'Churn Rate', 'bn': 'ক্ষয়ক্ষতি হার'},
            'retention': {'en': 'Customer Retention', 'bn': 'গ্রাহক ধরে রাখা'},
            'expansion': {'en': 'Market Expansion', 'bn': 'বাজার সম্প্রসারণ'},
            'efficiency': {'en': 'Operational Efficiency', 'bn': 'অপারেশনাল দক্ষতা'},
            'satisfaction': {'en': 'Customer Satisfaction', 'bn': 'গ্রাহক সন্তুষ্টি'},
            'market_share': {'en': 'Market Share', 'bn': 'বাজার অংশ'},
            'roi': {'en': 'Return on Investment', 'bn': 'বিনিয়োগ প্রত্যাবর্তন'},
            'break_even': {'en': 'Break-Even Point', 'bn': 'ব্রেক-ইভেন পয়েন্ট'},
            'cash_flow': {'en': 'Cash Flow', 'bn': 'নগদ প্রবাহ'},
            'debt': {'en': 'Debt Ratio', 'bn': '�ণ অনুপাত'},
            'inventory': {'en': 'Inventory Turnover', 'bn': 'ইনভেন্টরি টার্নওভার'},
            'productivity': {'en': 'Productivity', 'bn': 'উৎপাদনশীলতা'},
            'quality': {'en': 'Quality Metrics', 'bn': 'গুণমান মেট্রিক্স'},
            'innovation': {'en': 'Innovation Index', 'bn': 'উদ্ভাবন সূচক'},
            'sustainability': {'en': 'Sustainability Score', 'bn': 'স্থায়িত্ব স্কোর'}
        }
    
    def generate_recommendations(
        self, 
        kpi_data: Dict[str, float], 
        language: Language = Language.ENGLISH,
        industry: str = "general"
    ) -> List[DecisionRecommendation]:
        """Generate bilingual decision recommendations based on KPI data"""
        
        recommendations = []
        
        # Analyze revenue trends
        revenue_growth = kpi_data.get('revenue_growth', 0)
        if revenue_growth < -10:
            priority = Priority.HIGH
        elif revenue_growth < 0:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW
        
        revenue_rec = self._create_recommendation(
            'revenue_growth', priority, revenue_growth, language
        )
        recommendations.append(revenue_rec)
        
        # Analyze customer retention
        churn_rate = kpi_data.get('churn_rate', 0)
        if churn_rate > 0.15:  # 15%+
            priority = Priority.HIGH
        elif churn_rate > 0.10:  # 10%+
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW
        
        retention_rec = self._create_recommendation(
            'customer_retention', priority, churn_rate * 100, language
        )
        recommendations.append(retention_rec)
        
        # Analyze cost efficiency
        cost_ratio = kpi_data.get('cost_ratio', 0.7)
        if cost_ratio > 0.85:  # 85%+
            priority = Priority.HIGH
        elif cost_ratio > 0.75:  # 75%+
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW
        
        cost_rec = self._create_recommendation(
            'cost_optimization', priority, (cost_ratio - 0.7) * 100, language
        )
        recommendations.append(cost_rec)
        
        # Analyze market position
        market_share = kpi_data.get('market_share', 0.1)
        if market_share > 0.2:  # 20%+
            priority = Priority.HIGH
        elif market_share > 0.15:  # 15%+
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW
        
        expansion_rec = self._create_recommendation(
            'market_expansion', priority, market_share * 100, language
        )
        recommendations.append(expansion_rec)
        
        # Sort by priority and impact score
        recommendations.sort(key=lambda x: (
            0 if x.priority == Priority.HIGH else 1 if x.priority == Priority.MEDIUM else 2,
            -x.impact_score
        ))
        
        return recommendations
    
    def _create_recommendation(
        self, 
        category: str, 
        priority: Priority, 
        percentage: float, 
        language: Language
    ) -> DecisionRecommendation:
        """Create a single recommendation"""
        
        template = self.recommendations_templates[category][language.value][priority.value]
        
        # Calculate impact score based on priority and percentage
        if priority == Priority.HIGH:
            impact_score = min(0.9 + abs(percentage) / 100, 1.0)
        elif priority == Priority.MEDIUM:
            impact_score = min(0.6 + abs(percentage) / 200, 0.8)
        else:
            impact_score = min(0.3 + abs(percentage) / 300, 0.5)
        
        # Determine KPI affected
        kpi_map = {
            'revenue_growth': 'Revenue',
            'customer_retention': 'Customer Retention',
            'cost_optimization': 'Cost Efficiency',
            'market_expansion': 'Market Share'
        }
        
        return DecisionRecommendation(
            title_en=template['title'],
            title_bn=template['title'],
            description_en=template['description'].format(percentage=abs(percentage)),
            description_bn=template['description'].format(percentage=abs(percentage)),
            action_en=template['action'],
            action_bn=template['action'],
            priority=priority,
            impact_score=impact_score,
            implementation_time=template['implementation_time'],
            resources_needed=template['resources'],
            kpi_affected=kpi_map[category]
        )
    
    def get_business_term(self, term: str, language: Language) -> str:
        """Get business term in specified language"""
        if term in self.business_terms:
            return self.business_terms[term][language.value]
        return term
    
    def format_recommendation_for_display(
        self, 
        recommendation: DecisionRecommendation, 
        language: Language
    ) -> Dict[str, Any]:
        """Format recommendation for display in specified language"""
        
        if language == Language.BANGLA:
            return {
                'title': recommendation.title_bn,
                'description': recommendation.description_bn,
                'action': recommendation.action_bn,
                'priority': recommendation.priority.value,
                'impact_score': recommendation.impact_score,
                'implementation_time': recommendation.implementation_time,
                'resources_needed': recommendation.resources_needed,
                'kpi_affected': self.get_business_term(recommendation.kpi_affected.lower(), language)
            }
        else:
            return {
                'title': recommendation.title_en,
                'description': recommendation.description_en,
                'action': recommendation.action_en,
                'priority': recommendation.priority.value,
                'impact_score': recommendation.impact_score,
                'implementation_time': recommendation.implementation_time,
                'resources_needed': recommendation.resources_needed,
                'kpi_affected': recommendation.kpi_affected
            }
    
    def export_recommendations_json(
        self, 
        recommendations: List[DecisionRecommendation], 
        language: Language
    ) -> str:
        """Export recommendations as JSON in specified language"""
        
        formatted_recs = []
        for rec in recommendations:
            formatted_rec = self.format_recommendation_for_display(rec, language)
            formatted_recs.append(formatted_rec)
        
        return json.dumps(formatted_recs, ensure_ascii=False, indent=2)

# Global bilingual decision engine instance
bilingual_decision_engine = BilingualDecisionEngine()
