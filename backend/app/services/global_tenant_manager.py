#!/usr/bin/env python3
"""
Global Multi-Tenant Manager for Executive Dashboard
Supports worldwide deployment with regional compliance
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import uuid
from enum import Enum

class Region(Enum):
    NORTH_AMERICA = "north-america"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia-pacific"
    LATIN_AMERICA = "latin-america"
    MIDDLE_EAST_AFRICA = "middle-east-africa"

class ComplianceFramework(Enum):
    GDPR = "GDPR"
    SOC2 = "SOC2"
    CCPA = "CCPA"
    PDPA = "PDPA"
    LGPD = "LGPD"
    PDPL = "PDPL"

@dataclass
class TenantConfig:
    """Global tenant configuration"""
    tenant_id: str
    company_name: str
    region: Region
    currency: str
    language: str
    timezone: str
    compliance_frameworks: List[ComplianceFramework]
    industry: str
    size: str
    created_at: datetime
    is_active: bool = True

class GlobalTenantManager:
    """Manages multi-tenant global deployment"""
    
    def __init__(self):
        self.tenants: Dict[str, TenantConfig] = {}
        self.region_configs = self._initialize_region_configs()
        self.compliance_configs = self._initialize_compliance_configs()
    
    def _initialize_region_configs(self) -> Dict[Region, Dict]:
        """Initialize regional configurations"""
        return {
            Region.NORTH_AMERICA: {
                'currencies': ['USD', 'CAD'],
                'languages': ['en', 'es', 'fr'],
                'timezone': 'UTC-5 to UTC-8',
                'working_days': 'mon-fri',
                'business_culture': 'direct',
                'data_residency': 'US/Canada'
            },
            Region.EUROPE: {
                'currencies': ['EUR', 'GBP'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'nl', 'sv', 'da', 'no', 'fi', 'pl'],
                'timezone': 'UTC+0 to UTC+2',
                'working_days': 'mon-fri',
                'business_culture': 'formal',
                'data_residency': 'EU'
            },
            Region.ASIA_PACIFIC: {
                'currencies': ['JPY', 'CNY', 'INR', 'SGD', 'MYR', 'THB', 'PHP', 'IDR', 'VND'],
                'languages': ['en', 'zh', 'ja', 'ko', 'hi', 'bn', 'th', 'vi', 'id'],
                'timezone': 'UTC+5:30 to UTC+10',
                'working_days': 'mon-fri',
                'business_culture': 'relationship-focused',
                'data_residency': 'Local'
            },
            Region.LATIN_AMERICA: {
                'currencies': ['BRL', 'MXN', 'ARS', 'CLP', 'COP', 'PEN'],
                'languages': ['es', 'pt'],
                'timezone': 'UTC-3 to UTC-5',
                'working_days': 'mon-fri',
                'business_culture': 'relationship-focused',
                'data_residency': 'Local'
            },
            Region.MIDDLE_EAST_AFRICA: {
                'currencies': ['SAR', 'AED', 'ZAR', 'EGP', 'NGN'],
                'languages': ['en', 'ar', 'fr', 'pt'],
                'timezone': 'UTC+2 to UTC+4',
                'working_days': 'sun-thu',
                'business_culture': 'relationship-focused',
                'data_residency': 'Local'
            }
        }
    
    def _initialize_compliance_configs(self) -> Dict[ComplianceFramework, Dict]:
        """Initialize compliance framework configurations"""
        return {
            ComplianceFramework.GDPR: {
                'region': Region.EUROPE,
                'requirements': [
                    'data_consent',
                    'right_to_delete',
                    'data_portability',
                    'privacy_by_design',
                    'data_protection_officer',
                    'breach_notification_72h'
                ],
                'data_retention_max_days': 365,
                'consent_required': True,
                'anonymization_required': True
            },
            ComplianceFramework.SOC2: {
                'region': Region.NORTH_AMERICA,
                'requirements': [
                    'security_controls',
                    'availability_monitoring',
                    'confidentiality_protection',
                    'privacy_controls',
                    'audit_logging'
                ],
                'data_retention_max_days': 2555,  # 7 years
                'consent_required': False,
                'anonymization_required': False
            },
            ComplianceFramework.CCPA: {
                'region': Region.NORTH_AMERICA,
                'requirements': [
                    'right_to_know',
                    'right_to_delete',
                    'opt_out_sale',
                    'non_discrimination',
                    'business_transparency'
                ],
                'data_retention_max_days': 365,
                'consent_required': False,
                'anonymization_required': False
            },
            ComplianceFramework.PDPA: {
                'region': Region.ASIA_PACIFIC,
                'requirements': [
                    'consent_management',
                    'purpose_limitation',
                    'data_accuracy',
                    'security_protection',
                    'retention_limits'
                ],
                'data_retention_max_days': 365,
                'consent_required': True,
                'anonymization_required': True
            },
            ComplianceFramework.LGPD: {
                'region': Region.LATIN_AMERICA,
                'requirements': [
                    'consent_management',
                    'purpose_specification',
                    'data_minimization',
                    'security_measures',
                    'accountability'
                ],
                'data_retention_max_days': 365,
                'consent_required': True,
                'anonymization_required': True
            },
            ComplianceFramework.PDPL: {
                'region': Region.MIDDLE_EAST_AFRICA,
                'requirements': [
                    'consent_collection',
                    'purpose_declaration',
                    'data_quality',
                    'security_controls',
                    'cross_border_transfer_rules'
                ],
                'data_retention_max_days': 365,
                'consent_required': True,
                'anonymization_required': True
            }
        }
    
    def create_tenant(
        self,
        company_name: str,
        region: Region,
        currency: str,
        language: str,
        industry: str,
        size: str
    ) -> TenantConfig:
        """Create a new global tenant"""
        
        # Validate region-currency compatibility
        region_config = self.region_configs[region]
        if currency not in region_config['currencies']:
            raise ValueError(f"Currency {currency} not supported in region {region.value}")
        
        # Validate region-language compatibility
        if language not in region_config['languages']:
            raise ValueError(f"Language {language} not supported in region {region.value}")
        
        # Determine required compliance frameworks
        compliance_frameworks = self._get_required_compliance(region)
        
        tenant = TenantConfig(
            tenant_id=str(uuid.uuid4()),
            company_name=company_name,
            region=region,
            currency=currency,
            language=language,
            timezone=self._get_default_timezone(region),
            compliance_frameworks=compliance_frameworks,
            industry=industry,
            size=size,
            created_at=datetime.utcnow()
        )
        
        self.tenants[tenant.tenant_id] = tenant
        return tenant
    
    def _get_required_compliance(self, region: Region) -> List[ComplianceFramework]:
        """Get required compliance frameworks for region"""
        compliance_map = {
            Region.NORTH_AMERICA: [ComplianceFramework.SOC2, ComplianceFramework.CCPA],
            Region.EUROPE: [ComplianceFramework.GDPR],
            Region.ASIA_PACIFIC: [ComplianceFramework.PDPA],
            Region.LATIN_AMERICA: [ComplianceFramework.LGPD],
            Region.MIDDLE_EAST_AFRICA: [ComplianceFramework.PDPL]
        }
        return compliance_map.get(region, [])
    
    def _get_default_timezone(self, region: Region) -> str:
        """Get default timezone for region"""
        timezone_map = {
            Region.NORTH_AMERICA: 'America/New_York',
            Region.EUROPE: 'Europe/London',
            Region.ASIA_PACIFIC: 'Asia/Singapore',
            Region.LATIN_AMERICA: 'America/Sao_Paulo',
            Region.MIDDLE_EAST_AFRICA: 'Asia/Dubai'
        }
        return timezone_map[region]
    
    def get_tenant(self, tenant_id: str) -> Optional[TenantConfig]:
        """Get tenant configuration"""
        return self.tenants.get(tenant_id)
    
    def update_tenant(self, tenant_id: str, **kwargs) -> bool:
        """Update tenant configuration"""
        if tenant_id not in self.tenants:
            return False
        
        tenant = self.tenants[tenant_id]
        for key, value in kwargs.items():
            if hasattr(tenant, key):
                setattr(tenant, key, value)
        
        return True
    
    def get_tenants_by_region(self, region: Region) -> List[TenantConfig]:
        """Get all tenants in a specific region"""
        return [tenant for tenant in self.tenants.values() if tenant.region == region]
    
    def get_compliance_requirements(self, tenant_id: str) -> Dict[str, Any]:
        """Get compliance requirements for tenant"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return {}
        
        requirements = {}
        for framework in tenant.compliance_frameworks:
            requirements[framework.value] = self.compliance_configs[framework]
        
        return requirements
    
    def validate_compliance(self, tenant_id: str) -> Dict[str, bool]:
        """Validate tenant compliance status"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return {}
        
        compliance_status = {}
        for framework in tenant.compliance_frameworks:
            # This would integrate with actual compliance monitoring systems
            compliance_status[framework.value] = True  # Placeholder
        
        return compliance_status
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Get global deployment statistics"""
        stats = {
            'total_tenants': len(self.tenants),
            'tenants_by_region': {},
            'tenants_by_currency': {},
            'tenants_by_language': {},
            'compliance_coverage': {}
        }
        
        for tenant in self.tenants.values():
            # Region stats
            region = tenant.region.value
            stats['tenants_by_region'][region] = stats['tenants_by_region'].get(region, 0) + 1
            
            # Currency stats
            currency = tenant.currency
            stats['tenants_by_currency'][currency] = stats['tenants_by_currency'].get(currency, 0) + 1
            
            # Language stats
            language = tenant.language
            stats['tenants_by_language'][language] = stats['tenants_by_language'].get(language, 0) + 1
            
            # Compliance stats
            for framework in tenant.compliance_frameworks:
                stats['compliance_coverage'][framework.value] = stats['compliance_coverage'].get(framework.value, 0) + 1
        
        return stats
    
    def export_tenant_config(self, tenant_id: str) -> Dict[str, Any]:
        """Export tenant configuration for backup/migration"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return {}
        
        return {
            'tenant_id': tenant.tenant_id,
            'company_name': tenant.company_name,
            'region': tenant.region.value,
            'currency': tenant.currency,
            'language': tenant.language,
            'timezone': tenant.timezone,
            'compliance_frameworks': [f.value for f in tenant.compliance_frameworks],
            'industry': tenant.industry,
            'size': tenant.size,
            'created_at': tenant.created_at.isoformat(),
            'is_active': tenant.is_active
        }
    
    def import_tenant_config(self, config: Dict[str, Any]) -> Optional[TenantConfig]:
        """Import tenant configuration from backup/migration"""
        try:
            tenant = TenantConfig(
                tenant_id=config['tenant_id'],
                company_name=config['company_name'],
                region=Region(config['region']),
                currency=config['currency'],
                language=config['language'],
                timezone=config['timezone'],
                compliance_frameworks=[ComplianceFramework(f) for f in config['compliance_frameworks']],
                industry=config['industry'],
                size=config['size'],
                created_at=datetime.fromisoformat(config['created_at']),
                is_active=config.get('is_active', True)
            )
            
            self.tenants[tenant.tenant_id] = tenant
            return tenant
        except Exception as e:
            print(f"Failed to import tenant config: {e}")
            return None

# Global tenant manager instance
global_tenant_manager = GlobalTenantManager()
