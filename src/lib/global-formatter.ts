/**
 * Global formatting utilities for worldwide markets
 * Multi-currency, multi-language, international compliance
 */

export interface GlobalFormatOptions {
  currency?: string;
  language?: string;
  region?: string;
  decimals?: number;
  locale?: string;
}

// Global currency configurations
export const GLOBAL_CURRENCIES = {
  USD: { symbol: '$', code: 'USD', locale: 'en-US', decimals: 2 },
  EUR: { symbol: '€', code: 'EUR', locale: 'de-DE', decimals: 2 },
  GBP: { symbol: '£', code: 'GBP', locale: 'en-GB', decimals: 2 },
  JPY: { symbol: '¥', code: 'JPY', locale: 'ja-JP', decimals: 0 },
  CNY: { symbol: '¥', code: 'CNY', locale: 'zh-CN', decimals: 2 },
  INR: { symbol: '₹', code: 'INR', locale: 'en-IN', decimals: 2 },
  BDT: { symbol: '৳', code: 'BDT', locale: 'bn-BD', decimals: 2 },
  CAD: { symbol: 'C$', code: 'CAD', locale: 'en-CA', decimals: 2 },
  AUD: { symbol: 'A$', code: 'AUD', locale: 'en-AU', decimals: 2 },
  SGD: { symbol: 'S$', code: 'SGD', locale: 'en-SG', decimals: 2 },
  MYR: { symbol: 'RM', code: 'MYR', locale: 'en-MY', decimals: 2 },
  THB: { symbol: '฿', code: 'THB', locale: 'th-TH', decimals: 2 },
  PHP: { symbol: '₱', code: 'PHP', locale: 'en-PH', decimals: 2 },
  IDR: { symbol: 'Rp', code: 'IDR', locale: 'en-ID', decimals: 0 },
  VND: { symbol: '₫', code: 'VND', locale: 'en-VN', decimals: 0 }
} as const;

// Global language support
export const GLOBAL_LANGUAGES = {
  'en': { name: 'English', native: 'English', rtl: false },
  'es': { name: 'Spanish', native: 'Español', rtl: false },
  'fr': { name: 'French', native: 'Français', rtl: false },
  'de': { name: 'German', native: 'Deutsch', rtl: false },
  'it': { name: 'Italian', native: 'Italiano', rtl: false },
  'pt': { name: 'Portuguese', native: 'Português', rtl: false },
  'ru': { name: 'Russian', native: 'Русский', rtl: false },
  'ja': { name: 'Japanese', native: '日本語', rtl: false },
  'zh': { name: 'Chinese', native: '中文', rtl: false },
  'ko': { name: 'Korean', native: '한국어', rtl: false },
  'ar': { name: 'Arabic', native: 'العربية', rtl: true },
  'hi': { name: 'Hindi', native: 'हिन्दी', rtl: false },
  'bn': { name: 'Bengali', native: 'বাংলা', rtl: false },
  'tr': { name: 'Turkish', native: 'Türkçe', rtl: false },
  'pl': { name: 'Polish', native: 'Polski', rtl: false },
  'nl': { name: 'Dutch', native: 'Nederlands', rtl: false },
  'sv': { name: 'Swedish', native: 'Svenska', rtl: false },
  'da': { name: 'Danish', native: 'Dansk', rtl: false },
  'no': { name: 'Norwegian', native: 'Norsk', rtl: false },
  'fi': { name: 'Finnish', native: 'Suomi', rtl: false }
} as const;

// Global business regions and their characteristics
export const GLOBAL_REGIONS = {
  'north-america': {
    name: 'North America',
    currencies: ['USD', 'CAD'],
    languages: ['en', 'es', 'fr'],
    compliance: ['SOC2', 'HIPAA', 'CCPA'] as string[],
    businessCulture: 'direct',
    workingDays: 'mon-fri',
    timezone: 'UTC-5 to UTC-8'
  },
  'europe': {
    name: 'Europe',
    currencies: ['EUR', 'GBP'],
    languages: ['en', 'de', 'fr', 'es', 'it', 'nl', 'sv', 'da', 'no', 'fi', 'pl'],
    compliance: ['GDPR', 'ISO27001'] as string[],
    businessCulture: 'formal',
    workingDays: 'mon-fri',
    timezone: 'UTC+0 to UTC+2'
  },
  'asia-pacific': {
    name: 'Asia Pacific',
    currencies: ['JPY', 'CNY', 'INR', 'SGD', 'MYR', 'THB', 'PHP', 'IDR', 'VND'],
    languages: ['en', 'zh', 'ja', 'ko', 'hi', 'bn', 'th', 'vi', 'id'],
    compliance: ['PDPA', 'PDPO'] as string[],
    businessCulture: 'relationship-focused',
    workingDays: 'mon-fri',
    timezone: 'UTC+5:30 to UTC+10'
  },
  'latin-america': {
    name: 'Latin America',
    currencies: ['BRL', 'MXN', 'ARS', 'CLP', 'COP', 'PEN'],
    languages: ['es', 'pt'],
    compliance: ['LGPD', 'LFPDPPP'] as string[],
    businessCulture: 'relationship-focused',
    workingDays: 'mon-fri',
    timezone: 'UTC-3 to UTC-5'
  },
  'middle-east-africa': {
    name: 'Middle East & Africa',
    currencies: ['SAR', 'AED', 'ZAR', 'EGP', 'NGN'],
    languages: ['en', 'ar', 'fr', 'pt'],
    compliance: ['PDPL', 'POPIA'] as string[],
    businessCulture: 'relationship-focused',
    workingDays: 'sun-thu',
    timezone: 'UTC+2 to UTC+4'
  }
} as const;

/**
 * Format currency for global markets
 */
export function formatGlobalCurrency(
  amount: number,
  currency: string = 'USD',
  options: GlobalFormatOptions = {}
): string {
  const currencyConfig = GLOBAL_CURRENCIES[currency as keyof typeof GLOBAL_CURRENCIES];
  
  if (!currencyConfig) {
    return amount.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD'
    });
  }
  
  const locale = options.locale || currencyConfig.locale;
  const decimals = options.decimals !== undefined ? options.decimals : currencyConfig.decimals;
  
  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currencyConfig.code,
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(amount);
  } catch (error) {
    // Fallback to basic formatting
    return `${currencyConfig.symbol}${amount.toLocaleString(locale, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    })}`;
  }
}

/**
 * Format date for global markets
 */
export function formatGlobalDate(
  date: Date | string,
  locale: string = 'en-US',
  options: Intl.DateTimeFormatOptions = {}
): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options
  };
  
  return dateObj.toLocaleDateString(locale, defaultOptions);
}

/**
 * Format numbers for global markets
 */
export function formatGlobalNumber(
  number: number,
  locale: string = 'en-US',
  options: Intl.NumberFormatOptions = {}
): string {
  return number.toLocaleString(locale, options);
}

/**
 * Get business culture insights for region
 */
export function getBusinessCulture(region: keyof typeof GLOBAL_REGIONS) {
  return GLOBAL_REGIONS[region];
}

/**
 * Global compliance requirements
 */
export const GLOBAL_COMPLIANCE = {
  GDPR: {
    name: 'GDPR',
    region: 'Europe',
    requirements: ['data-consent', 'right-to-delete', 'data-portability', 'privacy-by-design'],
    fines: '€20M or 4% of global revenue'
  },
  SOC2: {
    name: 'SOC 2',
    region: 'North America',
    requirements: ['security', 'availability', 'confidentiality', 'privacy'],
    fines: 'Contractual penalties'
  },
  CCPA: {
    name: 'CCPA',
    region: 'California',
    requirements: ['right-to-know', 'right-to-delete', 'opt-out', 'non-discrimination'],
    fines: '$7,500 per violation'
  },
  PDPA: {
    name: 'PDPA',
    region: 'Singapore',
    requirements: ['consent', 'purpose-limitation', 'accuracy', 'security'],
    fines: 'SGD 1M'
  },
  LGPD: {
    name: 'LGPD',
    region: 'Brazil',
    requirements: ['consent', 'purpose', 'data-minimization', 'security'],
    fines: '2% of revenue'
  }
} as const;

/**
 * Check compliance requirements for market
 */
export function getComplianceRequirements(region: string): string[] {
  const regionConfig = GLOBAL_REGIONS[region as keyof typeof GLOBAL_REGIONS];
  return regionConfig?.compliance || [];
}

/**
 * Global business templates by industry and region
 */
export const GLOBAL_BUSINESS_TEMPLATES = {
  'technology': {
    'north-america': {
      kpis: ['ARR', 'MRR', 'CAC', 'LTV', 'Churn Rate', 'Net Revenue Retention'],
      benchmarks: { ARR: 10000000, CAC: 5000, LTV_CAC_Ratio: 3, Churn_Rate: 0.05 }
    },
    'europe': {
      kpis: ['ARR', 'MRR', 'CAC', 'LTV', 'Churn Rate', 'Net Revenue Retention'],
      benchmarks: { ARR: 8000000, CAC: 4000, LTV_CAC_Ratio: 3.5, Churn_Rate: 0.04 }
    },
    'asia-pacific': {
      kpis: ['ARR', 'MRR', 'CAC', 'LTV', 'Churn Rate', 'Net Revenue Retention'],
      benchmarks: { ARR: 5000000, CAC: 2000, LTV_CAC_Ratio: 4, Churn_Rate: 0.03 }
    }
  },
  'manufacturing': {
    'north-america': {
      kpis: ['Revenue', 'Production Efficiency', 'Quality Rate', 'Inventory Turnover', 'OEE'],
      benchmarks: { Revenue: 50000000, Production_Efficiency: 0.85, Quality_Rate: 0.98 }
    },
    'europe': {
      kpis: ['Revenue', 'Production Efficiency', 'Quality Rate', 'Inventory Turnover', 'OEE'],
      benchmarks: { Revenue: 40000000, Production_Efficiency: 0.88, Quality_Rate: 0.99 }
    },
    'asia-pacific': {
      kpis: ['Revenue', 'Production Efficiency', 'Quality Rate', 'Inventory Turnover', 'OEE'],
      benchmarks: { Revenue: 30000000, Production_Efficiency: 0.90, Quality_Rate: 0.97 }
    }
  },
  'retail': {
    'north-america': {
      kpis: ['Revenue', 'Gross Margin', 'Inventory Turnover', 'Customer Lifetime Value', 'Conversion Rate'],
      benchmarks: { Revenue: 20000000, Gross_Margin: 0.35, Inventory_Turnover: 8 }
    },
    'europe': {
      kpis: ['Revenue', 'Gross Margin', 'Inventory Turnover', 'Customer Lifetime Value', 'Conversion Rate'],
      benchmarks: { Revenue: 15000000, Gross_Margin: 0.40, Inventory_Turnover: 10 }
    },
    'asia-pacific': {
      kpis: ['Revenue', 'Gross Margin', 'Inventory Turnover', 'Customer Lifetime Value', 'Conversion Rate'],
      benchmarks: { Revenue: 10000000, Gross_Margin: 0.30, Inventory_Turnover: 12 }
    }
  }
} as const;

/**
 * Get industry template for specific region
 */
export function getGlobalIndustryTemplate(industry: string, region: string) {
  return GLOBAL_BUSINESS_TEMPLATES[industry as keyof typeof GLOBAL_BUSINESS_TEMPLATES]?.[region as keyof typeof GLOBAL_BUSINESS_TEMPLATES[keyof typeof GLOBAL_BUSINESS_TEMPLATES]] || null;
}

/**
 * Global timezone handling
 */
export function getGlobalTimezones(region: string): string[] {
  const regionConfig = GLOBAL_REGIONS[region as keyof typeof GLOBAL_REGIONS];
  if (!regionConfig) return [];
  
  // Return major timezones for the region
  const timezoneMap = {
    'north-america': ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles'],
    'europe': ['Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Europe/Rome', 'Europe/Madrid'],
    'asia-pacific': ['Asia/Tokyo', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Seoul', 'Asia/Mumbai', 'Asia/Dhaka'],
    'latin-america': ['America/Sao_Paulo', 'America/Mexico_City', 'America/Buenos_Aires', 'America/Lima'],
    'middle-east-africa': ['Asia/Dubai', 'Asia/Riyadh', 'Africa/Johannesburg', 'Africa/Cairo']
  };
  
  return timezoneMap[region as keyof typeof timezoneMap] || [];
}
