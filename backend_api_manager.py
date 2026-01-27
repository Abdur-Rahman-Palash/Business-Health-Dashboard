#!/usr/bin/env python3
"""
Backend API Auto-Insert Manager with AI Decision Making
Automatically detects, configures, and manages backend API connections
Includes automatic decision generation from business data
"""

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time

# Import decision engine and streamlit
from decision_engine import decision_engine
import streamlit as st

class BackendAPIManager:
    """Manages automatic backend API detection and data insertion"""
    
    def __init__(self):
        self.api_endpoints = [
            "https://business-health-dashboard-1.onrender.com",  # Current Render.com backend
            "https://business-health-dashboard.vercel.app",
            "https://executive-dashboard.vercel.app", 
            "http://localhost:8081",  # Updated to working port
            "http://localhost:8080",
            "http://localhost:3000",
            "http://localhost:8501"
        ]
        self.neubyte_endpoints = [
            "https://api.neubyte.tech",
            "https://neubyte.tech/api"
        ]
        self.active_endpoint = None
        self.last_health_check = None
        self.cache_timeout = 300  # 5 minutes
        self.data_cache = {}
        
    def auto_detect_backend(self) -> Optional[str]:
        """Auto-detect working backend API endpoint"""
        for endpoint in self.api_endpoints:
            try:
                # Try Streamlit health endpoint first
                response = requests.get(f"{endpoint}/_stcore/health", timeout=3)
                if response.status_code == 200 and response.text.strip() == "ok":
                    self.active_endpoint = endpoint
                    self.last_health_check = datetime.now()
                    return endpoint
                # Fallback to API health endpoint
                response = requests.get(f"{endpoint}/api/health", timeout=3)
                if response.status_code == 200:
                    self.active_endpoint = endpoint
                    self.last_health_check = datetime.now()
                    return endpoint
            except requests.exceptions.RequestException:
                continue
        return None
    
    def test_neubyte_connection(self, api_key: str = None) -> Tuple[bool, Dict]:
        """Test connection to neubyte.tech API"""
        headers = {}
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"
        
        for endpoint in self.neubyte_endpoints:
            try:
                response = requests.get(f"{endpoint}/v1/status", headers=headers, timeout=5)
                if response.status_code == 200:
                    return True, response.json()
            except:
                continue
        return False, {"error": "No neubyte.tech endpoint available"}
    
    def get_comprehensive_data(self, client_name: str = None) -> Dict:
        """Get comprehensive data with automatic decision making"""
        
        # Check if uploaded data is available in session state
        if hasattr(st, 'session_state') and st.session_state.get('has_uploaded_data'):
            processed_data = st.session_state.get('processed_file_data', {})
            
            if processed_data and processed_data.get('status') == 'success':
                # Use uploaded file data for decisions
                try:
                    decisions = decision_engine.analyze_business_health(processed_data)
                    
                    return {
                        'status': 'success',
                        'source': 'uploaded_file',
                        'data': {
                            'kpis': processed_data.get('kpis', []),
                            'business_health_score': processed_data.get('business_health_score', {}),
                            'insights': processed_data.get('insights', []),
                            'recommendations': processed_data.get('insights', []),  # Use insights as recommendations
                            'last_updated': processed_data.get('processed_at', datetime.now().isoformat())
                        },
                        'ai_decisions': decisions,
                        'has_decisions': True,
                        'decision_generated_at': datetime.now().isoformat(),
                        'file_info': {
                            'filename': processed_data.get('file_type', 'unknown'),
                            'processed_at': processed_data.get('processed_at')
                        }
                    }
                except Exception as e:
                    st.error(f"Error generating decisions from uploaded data: {e}")
        
        # Get base data
        data = self.get_data(client_name)
        
        # Generate automatic decisions if we have data
        if data and data.get('status') != 'no_data':
            try:
                # Use decision engine to generate decisions
                decisions = decision_engine.analyze_business_health(data.get('data', {}))
                
                # Add decisions to data
                data['ai_decisions'] = decisions
                data['has_decisions'] = True
                
                # Add decision timestamp
                data['decision_generated_at'] = datetime.now().isoformat()
                
            except Exception as e:
                # Fallback if decision engine fails
                data['ai_decisions'] = {
                    'error': f"Decision generation failed: {str(e)}",
                    'fallback_recommendations': [
                        "Monitor business metrics closely",
                        "Focus on customer satisfaction",
                        "Maintain operational efficiency",
                        "Watch market trends"
                    ]
                }
                data['has_decisions'] = False
        
        return data
    
    def get_ai_decisions_only(self, client_name: str = None) -> Dict:
        """Get only AI-generated decisions"""
        
        data = self.get_comprehensive_data(client_name)
        
        if data.get('has_decisions'):
            return data.get('ai_decisions', {})
        else:
            return {
                'status': 'no_decisions',
                'message': 'No decisions available - insufficient data',
                'recommendations': [
                    "Upload business data to enable AI decision making",
                    "Ensure KPIs and business health metrics are available",
                    "Check data quality and completeness"
                ]
            }
    
    def get_data(self, client_name: str = None) -> Dict:
        """Get data from backend API with fallback"""
        
        # Try to get fresh data from backend
        if self.active_endpoint:
            try:
                data = self._fetch_from_backend(client_name)
                if data:
                    return data
            except Exception as e:
                print(f"Backend fetch failed: {e}")
        
        # Fallback to cached data
        cache_key = f"{client_name or 'default'}_comprehensive"
        if cache_key in self.data_cache:
            cached_data, timestamp = self.data_cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_timeout):
                return cached_data
        
        # Final fallback - generate empty structure
        return self._generate_fallback_data()
    
    def _fetch_from_backend(self, client_name: str = None) -> Dict:
        """Fetch data from backend with multiple fallback strategies"""
        
        # Strategy 1: Try primary endpoint
        if not self.active_endpoint:
            self.auto_detect_backend()
        
        if self.active_endpoint:
            try:
                response = requests.get(f"{self.active_endpoint}/api/dashboard/complete", timeout=10)
                if response.status_code == 200:
                    return response.json()
            except:
                pass
        
        # Strategy 2: Try all endpoints
        for endpoint in self.api_endpoints:
            try:
                response = requests.get(f"{endpoint}/api/dashboard/complete", timeout=5)
                if response.status_code == 200:
                    self.active_endpoint = endpoint
                    return response.json()
            except:
                continue
        
        # Strategy 3: Try neubyte.tech if client_name provided
        if client_name:
            success, neubyte_data = self.test_neubyte_connection()
            if success:
                return self._convert_neubyte_data(neubyte_data)
        
        # Strategy 4: Generate fallback data
        return self._generate_fallback_data()
    
    def _convert_neubyte_data(self, neubyte_data: Dict) -> Dict:
        """Convert neubyte.tech data to dashboard format"""
        # This would be customized based on neubyte.tech actual API response format
        return {
            'status': 'success',
            'data': {
                'business_health_score': {
                    'overall': neubyte_data.get('health_score', 75),
                    'financial': neubyte_data.get('financial_health', 80),
                    'customer': neubyte_data.get('customer_health', 70),
                    'operational': neubyte_data.get('operational_health', 75),
                    'status': 'good'
                },
                'kpis': self._extract_kpis_from_neubyte(neubyte_data),
                'insights': neubyte_data.get('insights', []),
                'recommendations': neubyte_data.get('recommendations', []),
                'last_updated': datetime.now().isoformat()
            }
        }
    
    def _extract_kpis_from_neubyte(self, data: Dict) -> List[Dict]:
        """Extract KPIs from neubyte data format"""
        # This would be customized based on actual neubyte data structure
        return [
            {
                "id": "revenue",
                "name": "Total Revenue", 
                "value": data.get('revenue', 850000),
                "change": data.get('revenue_change', 5.2),
                "trend": "up",
                "category": "financial",
                "unit": "USD",
                "target": 1000000,
                "status": "good"
            }
        ]
    
    def _generate_fallback_data(self) -> Dict:
        """Generate empty structure - no mock data"""
        return {
            'status': 'no_data',
            'message': 'No data available - please upload files for analysis',
            'data': {
                'business_health_score': {
                    'overall': 0,
                    'financial': 0,
                    'customer': 0,
                    'operational': 0,
                    'status': 'no_data'
                },
                'kpis': [],
                'insights': [],
                'recommendations': [],
                'last_updated': datetime.now().isoformat()
            }
        }
    
    def get_health_status(self) -> Dict:
        """Get health status of all API endpoints"""
        status = {
            'primary_endpoint': self.active_endpoint,
            'endpoints_tested': len(self.api_endpoints),
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'cache_size': len(self.data_cache),
            'endpoints': {}
        }
        
        for endpoint in self.api_endpoints:
            try:
                response = requests.get(f"{endpoint}/api/health", timeout=2)
                status['endpoints'][endpoint] = {
                    'status': 'healthy' if response.status_code == 200 else 'error',
                    'response_time': response.elapsed.total_seconds(),
                    'status_code': response.status_code
                }
            except:
                status['endpoints'][endpoint] = {
                    'status': 'unreachable',
                    'response_time': None,
                    'status_code': None
                }
        
        return status
    
    def clear_cache(self):
        """Clear the data cache"""
        self.data_cache.clear()
    
    def refresh_data(self, client_name: str = None) -> Dict:
        """Force refresh data from backend"""
        cache_key = f"dashboard_data_{client_name or 'default'}"
        if cache_key in self.data_cache:
            del self.data_cache[cache_key]
        return self.get_comprehensive_data(client_name)

# Global instance
api_manager = BackendAPIManager()
