#!/usr/bin/env python3
"""
Client Management and API Key Configuration System
Manages multiple clients, API keys, and configurations with auto-setup
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import streamlit as st
import hashlib

class ClientManager:
    """Manages client configurations and API keys with auto-setup"""
    
    def __init__(self):
        self.clients_file = "client_configs.json"
        self.clients = self.load_clients()
        self.default_client = {
            "name": "Default Client",
            "api_key": None,
            "api_endpoint": "auto-detect",
            "industry": "General",
            "created": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "settings": {
                "auto_refresh": True,
                "ai_analysis": True,
                "alert_thresholds": {
                    "revenue_decline": -5,
                    "churn_rate": 8,
                    "satisfaction_min": 70
                }
            }
        }
    
    def load_clients(self) -> Dict:
        """Load client configurations from file"""
        try:
            if os.path.exists(self.clients_file):
                with open(self.clients_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_clients(self):
        """Save client configurations to file"""
        try:
            with open(self.clients_file, 'w') as f:
                json.dump(self.clients, f, indent=2)
        except:
            pass
    
    def add_client(self, name: str, api_key: str = None, **kwargs) -> bool:
        """Add a new client with auto-configuration"""
        if not name or name in self.clients:
            return False
        
        client_config = {
            "name": name,
            "api_key": api_key,
            "api_endpoint": kwargs.get('api_endpoint', 'auto-detect'),
            "industry": kwargs.get('industry', 'General'),
            "created": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "client_id": self.generate_client_id(name),
            "settings": kwargs.get('settings', self.default_client['settings'].copy())
        }
        
        # Auto-configure based on industry
        self.auto_configure_industry(client_config)
        
        self.clients[name] = client_config
        self.save_clients()
        return True
    
    def generate_client_id(self, name: str) -> str:
        """Generate unique client ID"""
        timestamp = str(int(datetime.now().timestamp()))
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"client_{name_hash}_{timestamp}"
    
    def auto_configure_industry(self, client_config: Dict):
        """Auto-configure client based on industry"""
        industry = client_config.get('industry', 'General').lower()
        
        industry_configs = {
            'technology': {
                'alert_thresholds': {
                    'revenue_decline': -3,
                    'churn_rate': 5,
                    'satisfaction_min': 80
                },
                'kpis': ['mrr', 'arr', 'churn_rate', 'cac', 'ltv']
            },
            'retail': {
                'alert_thresholds': {
                    'revenue_decline': -8,
                    'churn_rate': 12,
                    'satisfaction_min': 75
                },
                'kpis': ['sales_per_sqft', 'inventory_turnover', 'customer_retention']
            },
            'manufacturing': {
                'alert_thresholds': {
                    'revenue_decline': -5,
                    'churn_rate': 3,
                    'satisfaction_min': 70
                },
                'kpis': ['production_efficiency', 'downtime', 'quality_rate']
            },
            'finance': {
                'alert_thresholds': {
                    'revenue_decline': -2,
                    'churn_rate': 2,
                    'satisfaction_min': 85
                },
                'kpis': ['aum', 'net_new_assets', 'client_satisfaction']
            },
            'healthcare': {
                'alert_thresholds': {
                    'revenue_decline': -4,
                    'churn_rate': 6,
                    'satisfaction_min': 80
                },
                'kpis': ['patient_satisfaction', 'readmission_rate', 'bed_occupancy']
            }
        }
        
        if industry in industry_configs:
            client_config['settings']['alert_thresholds'].update(
                industry_configs[industry]['alert_thresholds']
            )
            client_config['industry_kpis'] = industry_configs[industry]['kpis']
    
    def get_client(self, name: str) -> Optional[Dict]:
        """Get client configuration"""
        if name in self.clients:
            # Update last accessed
            self.clients[name]['last_accessed'] = datetime.now().isoformat()
            self.save_clients()
            return self.clients[name]
        return None
    
    def update_client(self, name: str, **kwargs) -> bool:
        """Update client configuration"""
        if name not in self.clients:
            return False
        
        for key, value in kwargs.items():
            if key == 'settings' and isinstance(value, dict):
                self.clients[name]['settings'].update(value)
            else:
                self.clients[name][key] = value
        
        self.clients[name]['last_accessed'] = datetime.now().isoformat()
        self.save_clients()
        return True
    
    def delete_client(self, name: str) -> bool:
        """Delete client configuration"""
        if name in self.clients:
            del self.clients[name]
            self.save_clients()
            return True
        return False
    
    def list_clients(self) -> List[str]:
        """List all client names"""
        return list(self.clients.keys())
    
    def get_client_api_key(self, name: str) -> Optional[str]:
        """Get client API key securely"""
        client = self.get_client(name)
        return client.get('api_key') if client else None
    
    def validate_api_key(self, api_key: str, endpoint: str = None) -> bool:
        """Validate API key against endpoint"""
        if not api_key:
            return False
        
        # This would be customized based on actual API validation
        try:
            import requests
            headers = {'Authorization': f'Bearer {api_key}'}
            test_url = endpoint or 'https://api.neubyte.tech/v1/status'
            response = requests.get(test_url, headers=headers, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def auto_setup_client(self, name: str, industry: str = None, api_key: str = None) -> Dict:
        """Auto-setup a new client with minimal input"""
        if not name:
            return {"success": False, "error": "Client name required"}
        
        # Auto-detect industry if not provided
        if not industry:
            industry = self.detect_industry_from_name(name)
        
        # Add client with auto-configuration
        success = self.add_client(
            name=name,
            api_key=api_key,
            industry=industry
        )
        
        if success:
            client = self.get_client(name)
            return {
                "success": True,
                "client": client,
                "message": f"Client '{name}' auto-configured for {industry} industry"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to add client '{name}'"
            }
    
    def detect_industry_from_name(self, name: str) -> str:
        """Auto-detect industry from client name"""
        name_lower = name.lower()
        
        industry_keywords = {
            'technology': ['tech', 'software', 'saas', 'app', 'digital', 'cloud'],
            'retail': ['store', 'shop', 'retail', 'market', 'sales'],
            'manufacturing': ['manufactur', 'factory', 'production', 'industrial'],
            'finance': ['bank', 'financial', 'investment', 'insurance', 'capital'],
            'healthcare': ['health', 'medical', 'hospital', 'clinic', 'pharma']
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                return industry
        
        return 'General'
    
    def get_client_summary(self) -> Dict:
        """Get summary of all clients"""
        total_clients = len(self.clients)
        active_clients = len([
            c for c in self.clients.values() 
            if self.is_client_active(c)
        ])
        
        industries = {}
        for client in self.clients.values():
            industry = client.get('industry', 'General')
            industries[industry] = industries.get(industry, 0) + 1
        
        return {
            "total_clients": total_clients,
            "active_clients": active_clients,
            "industries": industries,
            "last_updated": datetime.now().isoformat()
        }
    
    def is_client_active(self, client: Dict) -> bool:
        """Check if client is active based on last access"""
        try:
            last_accessed = datetime.fromisoformat(client.get('last_accessed', ''))
            days_since_access = (datetime.now() - last_accessed).days
            return days_since_access <= 30  # Active if accessed within 30 days
        except:
            return False

# Streamlit UI Components
def render_client_manager_ui(manager: ClientManager):
    """Render client management UI in Streamlit"""
    st.header("🏢 Client Management")
    
    # Client Summary
    summary = manager.get_client_summary()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Clients", summary['total_clients'])
    
    with col2:
        st.metric("Active Clients", summary['active_clients'])
    
    with col3:
        st.metric("Industries", len(summary['industries']))
    
    # Add New Client Section
    st.subheader("➕ Add New Client")
    
    with st.form("add_client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client Name*", placeholder="Enter client name")
            industry = st.selectbox(
                "Industry",
                ["Auto-Detect", "Technology", "Retail", "Manufacturing", "Finance", "Healthcare", "General"],
                help="Industry-specific auto-configuration"
            )
        
        with col2:
            api_key = st.text_input("API Key (Optional)", type="password", 
                                   help="API key for enhanced data sources")
            api_endpoint = st.text_input("Custom API Endpoint (Optional)", 
                                        placeholder="https://api.example.com")
        
        submitted = st.form_submit_button("🚀 Auto-Setup Client", type="primary")
        
        if submitted:
            if not client_name:
                st.error("Client name is required")
            else:
                industry_to_use = None if industry == "Auto-Detect" else industry
                result = manager.auto_setup_client(
                    name=client_name,
                    industry=industry_to_use,
                    api_key=api_key if api_key else None
                )
                
                if result['success']:
                    st.success(result['message'])
                    if api_endpoint:
                        manager.update_client(client_name, api_endpoint=api_endpoint)
                    st.rerun()
                else:
                    st.error(result['error'])
    
    # Existing Clients
    if manager.clients:
        st.subheader("📋 Existing Clients")
        
        for client_name, client_data in manager.clients.items():
            with st.expander(f"🏢 {client_name}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Industry:** {client_data.get('industry', 'General')}")
                    st.write(f"**Client ID:** {client_data.get('client_id', 'N/A')}")
                    st.write(f"**Created:** {client_data.get('created', 'N/A')[:10]}")
                
                with col2:
                    api_key_status = "✅ Configured" if client_data.get('api_key') else "❌ Not Set"
                    st.write(f"**API Key:** {api_key_status}")
                    st.write(f"**Endpoint:** {client_data.get('api_endpoint', 'Auto-Detect')}")
                    active_status = "🟢 Active" if manager.is_client_active(client_data) else "🔴 Inactive"
                    st.write(f"**Status:** {active_status}")
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{client_name}"):
                        if manager.delete_client(client_name):
                            st.success(f"Client '{client_name}' deleted")
                            st.rerun()
                    
                    if st.button(f"✏️ Edit", key=f"edit_{client_name}"):
                        st.session_state[f'edit_{client_name}'] = True
                
                # Edit form (shown when edit button clicked)
                if st.session_state.get(f'edit_{client_name}'):
                    with st.form(f"edit_form_{client_name}"):
                        st.write("**Edit Client Configuration**")
                        new_api_key = st.text_input("New API Key", type="password", 
                                                   value=client_data.get('api_key', ''))
                        new_endpoint = st.text_input("API Endpoint", 
                                                    value=client_data.get('api_endpoint', ''))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save"):
                                manager.update_client(client_name, 
                                                   api_key=new_api_key if new_api_key else None,
                                                   api_endpoint=new_endpoint if new_endpoint else None)
                                st.success("Client updated")
                                st.session_state[f'edit_{client_name}'] = False
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f'edit_{client_name}'] = False
                                st.rerun()
    else:
        st.info("No clients configured yet. Add your first client above!")

# Initialize global client manager
if 'client_manager' not in st.session_state:
    st.session_state.client_manager = ClientManager()
