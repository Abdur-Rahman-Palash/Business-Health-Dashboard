import os
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np

class AIInsightEngine:
    """Enhanced AI-powered insight generation using Hugging Face models"""
    
    def __init__(self):
        self.hf_token = os.getenv('HF_DDwIbjeMXSlikAmBuxItRGYVkyJtuHAgMZ', None)
        self.api_base = "https://api-inference.huggingface.co/models"
        
    def generate_insights_with_ai(self, kpis: List[Dict], business_data: Dict[str, Any]) -> List[Dict]:
        """Generate enhanced insights using Hugging Face AI models"""
        insights = []
        
        if not self.hf_token:
            # Fallback to rule-based insights if no token
            return self._generate_rule_based_insights(kpis, business_data)
        
        try:
            # Prepare business context for AI analysis
            context = self._prepare_business_context(kpis, business_data)
            
            # Generate insights using different AI models
            revenue_insights = self._analyze_revenue_with_ai(context)
            customer_insights = self._analyze_customers_with_ai(context)
            risk_insights = self._analyze_risks_with_ai(context)
            
            insights.extend(revenue_insights)
            insights.extend(customer_insights)
            insights.extend(risk_insights)
            
        except Exception as e:
            print(f"AI insight generation failed: {e}")
            # Fallback to rule-based insights
            insights = self._generate_rule_based_insights(kpis, business_data)
        
        return insights
    
    def _prepare_business_context(self, kpis: List[Dict], business_data: Dict[str, Any]) -> str:
        """Prepare business context for AI analysis"""
        # Extract key metrics
        revenue_kpi = next((kpi for kpi in kpis if kpi.get('id') == 'revenue'), None)
        customer_kpi = next((kpi for kpi in kpis if kpi.get('id') == 'customer-health'), None)
        churn_kpi = next((kpi for kpi in kpis if kpi.get('id') == 'churn-rate'), None)
        
        context = f"""
        Business Performance Analysis for {datetime.now().strftime('%B %Y')}:
        
        Key Metrics:
        - Current Revenue: ${revenue_kpi.get('current_value', 0):,.0f} (Target: ${revenue_kpi.get('target_value', 0):,.0f})
        - Customer Health: {customer_kpi.get('current_value', 0):.1f}% (Target: {customer_kpi.get('target_value', 0):.1f}%)
        - Churn Rate: {churn_kpi.get('current_value', 0):.1f}% (Target: {churn_kpi.get('target_value', 0):.1f}%)
        
        Data Summary:
        - Total Customers: {len(business_data.get('customers', []))}
        - Total Sales Transactions: {len(business_data.get('sales', []))}
        - Total Expense Records: {len(business_data.get('expenses', []))}
        
        Please analyze this business data and provide:
        1. Key performance insights
        2. Risk identification
        3. Actionable recommendations
        4. Strategic opportunities
        
        Format response as JSON with insights array.
        """
        
        return context
    
    def _analyze_revenue_with_ai(self, context: str) -> List[Dict]:
        """Use Hugging Face for revenue analysis"""
        try:
            # Use a business analysis model
            payload = {
                "inputs": context,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.3,
                    "return_full_text": False
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            # Try using a business analysis model
            response = requests.post(
                f"{self.api_base}/mistralai/Mixtral-8x7B-Instruct-v0.1",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_ai_insights(result, "revenue")
            else:
                print(f"Revenue analysis API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Revenue analysis failed: {e}")
            return []
    
    def _analyze_customers_with_ai(self, context: str) -> List[Dict]:
        """Use Hugging Face for customer analysis"""
        try:
            payload = {
                "inputs": f"{context}\n\nFocus specifically on customer behavior, satisfaction, and retention patterns.",
                "parameters": {
                    "max_new_tokens": 400,
                    "temperature": 0.3
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_base}/mistralai/Mixtral-8x7B-Instruct-v0.1",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_ai_insights(result, "customer")
            else:
                return []
                
        except Exception as e:
            print(f"Customer analysis failed: {e}")
            return []
    
    def _analyze_risks_with_ai(self, context: str) -> List[Dict]:
        """Use Hugging Face for risk analysis"""
        try:
            payload = {
                "inputs": f"{context}\n\nIdentify potential business risks, financial vulnerabilities, and operational challenges.",
                "parameters": {
                    "max_new_tokens": 400,
                    "temperature": 0.2
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_base}/mistralai/Mixtral-8x7B-Instruct-v0.1",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_ai_insights(result, "risk")
            else:
                return []
                
        except Exception as e:
            print(f"Risk analysis failed: {e}")
            return []
    
    def _parse_ai_insights(self, ai_response: Dict, insight_type: str) -> List[Dict]:
        """Parse AI response into structured insights"""
        insights = []
        
        try:
            if isinstance(ai_response, list) and len(ai_response) > 0:
                text_response = ai_response[0].get('generated_text', '')
            elif isinstance(ai_response, dict):
                text_response = ai_response.get('generated_text', '')
            else:
                text_response = str(ai_response)
            
            # Try to extract JSON from response
            if '{' in text_response and '}' in text_response:
                start_idx = text_response.find('{')
                end_idx = text_response.rfind('}') + 1
                json_str = text_response[start_idx:end_idx]
                
                try:
                    parsed = json.loads(json_str)
                    if 'insights' in parsed:
                        for insight in parsed['insights']:
                            insights.append({
                                'title': insight.get('title', f'AI {insight_type.title()} Insight'),
                                'description': insight.get('description', ''),
                                'category': insight_type,
                                'priority': self._assess_priority(insight),
                                'confidence': 'high',
                                'source': 'ai',
                                'generated_at': datetime.now().isoformat()
                            })
                except json.JSONDecodeError:
                    # Fallback: create insight from text
                    insights.append({
                        'title': f'AI {insight_type.title()} Analysis',
                        'description': text_response[:200] + '...' if len(text_response) > 200 else text_response,
                        'category': insight_type,
                        'priority': 'medium',
                        'confidence': 'medium',
                        'source': 'ai',
                        'generated_at': datetime.now().isoformat()
                    })
            else:
                # Create insight from raw text
                insights.append({
                    'title': f'AI {insight_type.title()} Analysis',
                    'description': text_response[:200] + '...' if len(text_response) > 200 else text_response,
                    'category': insight_type,
                    'priority': 'medium',
                    'confidence': 'medium',
                    'source': 'ai',
                    'generated_at': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"Failed to parse AI insights: {e}")
            
        return insights[:3]  # Return top 3 insights
    
    def _assess_priority(self, insight: Dict) -> str:
        """Assess priority of an insight"""
        description = insight.get('description', '').lower()
        
        high_priority_keywords = ['critical', 'urgent', 'severe', 'significant decline', 'major risk', 'immediate attention']
        medium_priority_keywords = ['concerning', 'moderate', 'improvement needed', 'monitor']
        
        for keyword in high_priority_keywords:
            if keyword in description:
                return 'high'
        
        for keyword in medium_priority_keywords:
            if keyword in description:
                return 'medium'
        
        return 'low'
    
    def _generate_rule_based_insights(self, kpis: List[Dict], business_data: Dict[str, Any]) -> List[Dict]:
        """Fallback rule-based insights when AI is not available"""
        insights = []
        
        # Revenue insights
        revenue_kpi = next((kpi for kpi in kpis if kpi.get('id') == 'revenue'), None)
        if revenue_kpi:
            current = revenue_kpi.get('current_value', 0)
            target = revenue_kpi.get('target_value', 0)
            if current < target * 0.8:
                insights.append({
                    'title': 'Revenue Below Target',
                    'description': f'Revenue is ${(target - current):,.0f} below target, representing {(current/target)*100:.1f}% achievement.',
                    'category': 'revenue',
                    'priority': 'high',
                    'confidence': 'high',
                    'source': 'rule-based',
                    'generated_at': datetime.now().isoformat()
                })
        
        # Customer insights
        customers_df = pd.DataFrame(business_data.get('customers', []))
        if len(customers_df) > 0:
            avg_satisfaction = customers_df['satisfaction_score'].mean()
            if avg_satisfaction < 70:
                insights.append({
                    'title': 'Low Customer Satisfaction',
                    'description': f'Average customer satisfaction is {avg_satisfaction:.1f}%, below the 70% threshold.',
                    'category': 'customer',
                    'priority': 'high',
                    'confidence': 'high',
                    'source': 'rule-based',
                    'generated_at': datetime.now().isoformat()
                })
        
        # Churn insights
        if len(customers_df) > 0:
            customers_df['last_order_date'] = pd.to_datetime(customers_df['last_order_date'])
            current_date = pd.to_datetime(datetime.now())
            customers_df['days_since_last_order'] = (current_date - customers_df['last_order_date']).dt.days
            high_risk_customers = customers_df[customers_df['days_since_last_order'] > 90]
            churn_rate = len(high_risk_customers) / len(customers_df) * 100
            
            if churn_rate > 10:
                insights.append({
                    'title': 'High Customer Churn Risk',
                    'description': f'{churn_rate:.1f}% of customers are at high risk of churn (no orders in 90+ days).',
                    'category': 'risk',
                    'priority': 'high',
                    'confidence': 'high',
                    'source': 'rule-based',
                    'generated_at': datetime.now().isoformat()
                })
        
        return insights
    
    def generate_executive_summary_with_ai(self, insights: List[Dict], kpis: List[Dict]) -> Dict:
        """Generate AI-powered executive summary"""
        if not self.hf_token:
            return self._generate_basic_executive_summary(insights, kpis)
        
        try:
            # Prepare context for executive summary
            insights_text = "\n".join([f"- {insight.get('title', '')}: {insight.get('description', '')}" for insight in insights[:5]])
            
            context = f"""
            Create an executive summary for C-level leadership based on the following business insights:
            
            {insights_text}
            
            Key Performance Indicators:
            {json.dumps(kpis[:5], indent=2)}
            
            Please provide:
            1. Overall business health assessment
            2. Top 3 strategic priorities
            3. Key risks and opportunities
            4. Recommended actions
            
            Format as a professional executive summary.
            """
            
            payload = {
                "inputs": context,
                "parameters": {
                    "max_new_tokens": 600,
                    "temperature": 0.3
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_base}/mistralai/Mixtral-8x7B-Instruct-v0.1",
                json=payload,
                headers=headers,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                summary_text = result[0].get('generated_text', '') if isinstance(result, list) else result.get('generated_text', '')
                
                return {
                    'summary': summary_text,
                    'health_assessment': self._extract_health_assessment(summary_text),
                    'priorities': self._extract_priorities(summary_text),
                    'generated_at': datetime.now().isoformat(),
                    'source': 'ai'
                }
            else:
                return self._generate_basic_executive_summary(insights, kpis)
                
        except Exception as e:
            print(f"Executive summary generation failed: {e}")
            return self._generate_basic_executive_summary(insights, kpis)
    
    def _generate_basic_executive_summary(self, insights: List[Dict], kpis: List[Dict]) -> Dict:
        """Generate basic executive summary without AI"""
        high_priority_insights = [i for i in insights if i.get('priority') == 'high']
        
        summary = f"""
        Executive Business Summary - {datetime.now().strftime('%B %Y')}
        
        Overall Assessment: {len(high_priority_insights)} high-priority issues identified requiring immediate attention.
        
        Key Concerns:
        {chr(10).join([f"• {insight.get('title', '')}" for insight in high_priority_insights[:3]])}
        
        Recommendations:
        • Address high-priority insights through cross-functional initiatives
        • Implement monitoring systems for early risk detection
        • Focus on customer retention and revenue optimization
        """
        
        return {
            'summary': summary,
            'health_assessment': 'warning' if len(high_priority_insights) > 2 else 'good',
            'priorities': [insight.get('title', '') for insight in high_priority_insights[:3]],
            'generated_at': datetime.now().isoformat(),
            'source': 'rule-based'
        }
    
    def _extract_health_assessment(self, text: str) -> str:
        """Extract health assessment from AI text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['excellent', 'strong', 'healthy', 'positive']):
            return 'excellent'
        elif any(word in text_lower for word in ['good', 'stable', 'positive']):
            return 'good'
        elif any(word in text_lower for word in ['concerning', 'warning', 'caution']):
            return 'warning'
        else:
            return 'critical'
    
    def _extract_priorities(self, text: str) -> List[str]:
        """Extract priorities from AI text"""
        # Simple extraction - look for numbered lists or bullet points
        lines = text.split('\n')
        priorities = []
        
        for line in lines:
            line = line.strip()
            if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '•', '-']):
                # Extract the priority item
                priority = line[2:].strip() if line[2:] == '. ' else line[1:].strip()
                if priority and len(priority) > 10:
                    priorities.append(priority[:50])  # Limit length
        
        return priorities[:3]  # Return top 3 priorities
