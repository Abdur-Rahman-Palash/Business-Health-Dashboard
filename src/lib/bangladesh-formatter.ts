/**
 * Bangladesh-specific formatting utilities
 * BDT currency, Bengali numbers, local date formats
 */

export interface BangladeshFormatOptions {
  showCurrency?: boolean;
  language?: 'en' | 'bn';
  decimals?: number;
}

// Bengali number mapping
const BENGALI_DIGITS = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];

/**
 * Format number as Bangladeshi Taka
 */
export function formatBDT(
  amount: number, 
  options: BangladeshFormatOptions = {}
): string {
  const { showCurrency = true, language = 'en', decimals = 2 } = options;
  
  // Format with commas (Bangladeshi style: lakh, crore)
  const formattedAmount = formatBangladeshiNumber(amount, decimals);
  
  // Convert to Bengali digits if needed
  const displayAmount = language === 'bn' 
    ? convertToBengaliDigits(formattedAmount)
    : formattedAmount;
  
  return showCurrency ? `৳${displayAmount}` : displayAmount;
}

/**
 * Format number in Bangladeshi style (lakh, crore system)
 */
function formatBangladeshiNumber(num: number, decimals: number): string {
  const absNum = Math.abs(num);
  const sign = num < 0 ? '-' : '';
  
  if (absNum >= 10000000) { // 1 crore or more
    const crore = absNum / 10000000;
    return `${sign}${crore.toFixed(decimals)} কোটি`;
  } else if (absNum >= 100000) { // 1 lakh or more
    const lakh = absNum / 100000;
    return `${sign}${lakh.toFixed(decimals)} লাখ`;
  } else {
    return `${sign}${absNum.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`;
  }
}

/**
 * Convert English digits to Bengali digits
 */
function convertToBengaliDigits(numStr: string): string {
  return numStr.replace(/\d/g, (digit) => BENGALI_DIGITS[parseInt(digit)]);
}

/**
 * Format date for Bangladeshi context
 */
export function formatBangladeshDate(
  date: Date | string,
  language: 'en' | 'bn' = 'en'
): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  };
  
  if (language === 'bn') {
    return dateObj.toLocaleDateString('bn-BD', options);
  } else {
    return dateObj.toLocaleDateString('en-BD', options);
  }
}

/**
 * Bangladesh business industries
 */
export const BANGLADESH_INDUSTRIES = [
  { id: 'garments', name: 'Garments & Textile', nameBn: 'পোশাক ও টেক্সটাইল' },
  { id: 'it_services', name: 'IT Services', nameBn: 'আইটি সার্ভিসেস' },
  { id: 'trading', name: 'Trading & Retail', nameBn: 'ট্রেডিং ও খুচরা বিক্রি' },
  { id: 'manufacturing', name: 'Manufacturing', nameBn: 'উৎপাদন' },
  { id: 'pharmaceuticals', name: 'Pharmaceuticals', nameBn: 'ঔষধ' },
  { id: 'banking', name: 'Banking & Finance', nameBn: 'ব্যাংকিং ও অর্থায়ন' },
  { id: 'telecom', name: 'Telecommunications', nameBn: 'টেলিযোগাযোগ' },
  { id: 'agriculture', name: 'Agriculture', nameBn: 'কৃষি' },
  { id: 'construction', name: 'Construction', nameBn: 'নির্মাণ' },
  { id: 'transport', name: 'Transport & Logistics', nameBn: 'পরিবহন ও লজিস্টিকস' }
] as const;

/**
 * Bangladesh-specific KPI templates
 */
export const BANGLADESH_KPI_TEMPLATES = {
  garments: {
    revenue: { target: 50000000, unit: 'BDT' },
    export_ratio: { target: 0.8, unit: 'percentage' },
    compliance_score: { target: 95, unit: 'percentage' },
    worker_efficiency: { target: 85, unit: 'percentage' }
  },
  it_services: {
    revenue: { target: 10000000, unit: 'BDT' },
    client_retention: { target: 0.9, unit: 'percentage' },
    project_delivery: { target: 95, unit: 'percentage' },
    employee_utilization: { target: 75, unit: 'percentage' }
  },
  trading: {
    revenue: { target: 20000000, unit: 'BDT' },
    inventory_turnover: { target: 6, unit: 'times' },
    gross_margin: { target: 0.25, unit: 'percentage' },
    supplier_score: { target: 80, unit: 'percentage' }
  }
} as const;

/**
 * Bangladesh business size classification
 */
export function getBusinessSize(employeeCount: number): {
  size: string;
  sizeBn: string;
  category: 'micro' | 'small' | 'medium' | 'large';
} {
  if (employeeCount <= 10) {
    return {
      size: 'Micro Enterprise',
      sizeBn: 'ক্ষুদ্র উদ্যোগ',
      category: 'micro'
    };
  } else if (employeeCount <= 50) {
    return {
      size: 'Small Enterprise',
      sizeBn: 'ছোট উদ্যোগ',
      category: 'small'
    };
  } else if (employeeCount <= 200) {
    return {
      size: 'Medium Enterprise',
      sizeBn: 'মাঝারি উদ্যোগ',
      category: 'medium'
    };
  } else {
    return {
      size: 'Large Enterprise',
      sizeBn: 'বড় উদ্যোগ',
      category: 'large'
    };
  }
}
