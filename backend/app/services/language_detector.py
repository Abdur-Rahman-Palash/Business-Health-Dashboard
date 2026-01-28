#!/usr/bin/env python3
"""
Intelligent Language Detection Service
Detects company origin and displays results in appropriate language
"""

import re
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class Language(Enum):
    BANGLA = "bn"
    ENGLISH = "en"

@dataclass
class CompanyInfo:
    """Company information extracted from data"""
    name: str
    country: str
    is_bangladeshi: bool
    language: Language
    confidence: float

class LanguageDetector:
    """Intelligent language detection based on company data"""
    
    def __init__(self):
        self.bangladesh_keywords = [
            # Country indicators
            'bangladesh', 'bengal', 'dhaka', 'chittagong', 'khulna', 'rajshahi', 'sylhet', 'barisal', 'rangpur',
            'mymensingh', 'narayanganj', 'comilla', 'feni', 'brahmanbaria', 'chandpur',
            
            # Bangla words
            'লিমিটেড', 'লি.', 'প্রাইভেট', 'প্রা.', 'ইন্ডাস্ট্রিজ', 'গ্রুপ', 'কর্পোরেশন', 'এন্টারপ্রাইজ',
            'ম্যানুফ্যাকচারিং', 'টেক্সটাইল', 'গার্মেন্টস', 'এক্সপোর্ট', 'ইমপোর্ট', 'ট্রেডিং',
            
            # Common Bangladeshi company patterns
            'bd', '.bd', 'bangladeshi', 'bengali',
            
            # Local suffixes
            'ltd', 'limited', 'private', 'group', 'industries', 'corporation', 'enterprise'
        ]
        
        self.bangladeshi_domains = [
            '.com.bd', '.bd', '.net.bd', '.org.bd', '.edu.bd', '.gov.bd'
        ]
        
        self.bangladeshi_banks = [
            'dbbl', 'dutch bangla', 'brac bank', 'grameen bank', 'ific', 'pubali',
            'sonali', 'janata', 'agrani', 'rupali', 'basic', 'city bank', 'ebl',
            'southeast bank', 'trust bank', 'ibbl', 'al-arafah', 'social islami',
            'standard bank', 'prime bank', 'dhaka bank', 'mercantile', 'ncc bank'
        ]
        
        self.bangladeshi_company_patterns = [
            r'.*\s+(?:Ltd|Limited|Group|Industries|Corporation|Enterprise)\s*$',
            r'.*\s+(?:লিমিটেড|গ্রুপ|ইন্ডাস্ট্রিজ)\s*$',
            r'.*Bangladesh.*',
            r'.*Dhaka.*',
            r'.*\s+BD$',
            r'.*\s+Bangla.*'
        ]
    
    def detect_company_origin(self, company_name: str, email: str = "", website: str = "", 
                            address: str = "", phone: str = "") -> CompanyInfo:
        """Detect company origin and determine appropriate language"""
        
        company_name_lower = company_name.lower()
        email_lower = email.lower()
        website_lower = website.lower()
        address_lower = address.lower()
        
        # Initialize detection scores
        bangla_score = 0
        english_score = 1  # Default to English
        
        # Check company name patterns
        for pattern in self.bangladeshi_company_patterns:
            if re.match(pattern, company_name, re.IGNORECASE):
                bangla_score += 3
        
        # Check for Bangladesh keywords
        for keyword in self.bangladesh_keywords:
            if keyword in company_name_lower:
                bangla_score += 2
            if keyword in address_lower:
                bangla_score += 2
        
        # Check email domain
        for domain in self.bangladeshi_domains:
            if domain in email_lower:
                bangla_score += 3
            if domain in website_lower:
                bangla_score += 3
        
        # Check for Bangladeshi banks
        for bank in self.bangladeshi_banks:
            if bank in company_name_lower:
                bangla_score += 2
        
        # Check phone number pattern (Bangladesh mobile numbers start with +880 or 01)
        if phone.startswith('+880') or (phone.startswith('01') and len(phone) >= 11):
            bangla_score += 2
        
        # Check for Bangla characters in company name
        if any('\u0980' <= char <= '\u09FF' for char in company_name):
            bangla_score += 5
        
        # Determine language based on scores
        if bangla_score >= 3:
            language = Language.BANGLA
            is_bangladeshi = True
            country = "Bangladesh"
            confidence = min(bangla_score / 10, 1.0)
        else:
            language = Language.ENGLISH
            is_bangladeshi = False
            country = "International"
            confidence = min(1.0 - (bangla_score / 10), 1.0)
        
        return CompanyInfo(
            name=company_name,
            country=country,
            is_bangladeshi=is_bangladeshi,
            language=language,
            confidence=confidence
        )
    
    def detect_from_dataframe(self, df: pd.DataFrame) -> List[CompanyInfo]:
        """Detect company origins from a DataFrame"""
        companies = []
        
        for index, row in df.iterrows():
            company_name = str(row.get('company_name', row.get('name', row.get('Company', ''))))
            email = str(row.get('email', row.get('Email', '')))
            website = str(row.get('website', row.get('Website', '')))
            address = str(row.get('address', row.get('Address', '')))
            phone = str(row.get('phone', row.get('Phone', '')))
            
            if company_name and company_name != 'nan':
                company_info = self.detect_company_origin(
                    company_name, email, website, address, phone
                )
                companies.append(company_info)
        
        return companies
    
    def get_language_config(self, language: Language) -> Dict:
        """Get language-specific configuration"""
        if language == Language.BANGLA:
            return {
                'direction': 'rtl' if any('\u0590' <= char <= '\u05FF' for char in 'বাংলা') else 'ltr',
                'font_family': 'Hind Siliguri, SolaimanLipi, Arial',
                'date_format': 'bn-BD',
                'number_format': 'bn-BD',
                'currency': 'BDT',
                'timezone': 'Asia/Dhaka'
            }
        else:
            return {
                'direction': 'ltr',
                'font_family': 'Inter, Arial, sans-serif',
                'date_format': 'en-US',
                'number_format': 'en-US',
                'currency': 'USD',
                'timezone': 'UTC'
            }

# Global language detector instance
language_detector = LanguageDetector()
