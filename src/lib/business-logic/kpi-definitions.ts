import { KPIDefinition, KPIId } from '@/types/business';

// Business KPI Definitions for Executive Decision Making
// Each KPI includes business meaning, not just technical definitions

export const kpiDefinitions: Record<KPIId, KPIDefinition> = {
  'revenue': {
    id: 'revenue',
    name: 'Total Revenue',
    description: 'Total income generated from all business operations before expenses.',
    businessMeaning: 'The total amount of money your business earns from selling products or services. This is the top-line measure of your business\'s market success and customer demand.',
    whyItMatters: 'Revenue drives growth, investor confidence, and operational capacity. Declining revenue signals market challenges, while growth indicates business expansion and market acceptance.',
    goodValueIndicator: 'Consistent growth month-over-month, meeting or exceeding targets. Shows strong market demand and effective sales execution.',
    badValueIndicator: 'Declining trend or stagnation below targets. Indicates market challenges, competitive pressure, or sales effectiveness issues.',
    unit: 'USD',
    category: 'financial'
  },
  
  'revenue-growth': {
    id: 'revenue-growth',
    name: 'Revenue Growth Rate',
    description: 'Percentage change in revenue compared to the previous period.',
    businessMeaning: 'How fast your business is growing compared to last period. This measures your business\'s momentum and market expansion success.',
    whyItMatters: 'Growth rate indicates business health, market competitiveness, and future potential. High growth attracts talent, investors, and partners. Low growth may signal market saturation or operational issues.',
    goodValueIndicator: '10-20% year-over-year growth for mature businesses, 20-50% for growth-stage companies. Shows sustainable expansion.',
    badValueIndicator: 'Negative growth or growth below 5% annually. Indicates market challenges, competitive losses, or strategic misalignment.',
    unit: '%',
    category: 'financial'
  },
  
  'profit-margin': {
    id: 'profit-margin',
    name: 'Profit Margin',
    description: 'Percentage of revenue remaining after all expenses are deducted.',
    businessMeaning: 'How efficiently your business converts revenue into actual profit. This measures your pricing power, cost control, and operational efficiency.',
    whyItMatters: 'Profit margin determines business sustainability, reinvestment capacity, and resilience to market shocks. Healthy margins enable strategic investments and weather economic downturns.',
    goodValueIndicator: '15-20% for most industries, higher for software/tech. Shows strong pricing power and cost management.',
    badValueIndicator: 'Below 10% consistently. Indicates pricing pressure, high costs, or operational inefficiencies.',
    unit: '%',
    category: 'financial'
  },
  
  'expense-ratio': {
    id: 'expense-ratio',
    name: 'Expense Ratio',
    description: 'Total expenses as a percentage of revenue.',
    businessMeaning: 'How much of your revenue is consumed by operating costs. This measures your cost structure efficiency and spending discipline.',
    whyItMatters: 'Expense ratio directly impacts profitability and cash flow. High expense ratios reduce flexibility, increase risk, and limit growth opportunities.',
    goodValueIndicator: 'Below 80% for most businesses. Shows disciplined spending and efficient operations.',
    badValueIndicator: 'Above 90% consistently. Indicates cost overruns, inefficient operations, or pricing problems.',
    unit: '%',
    category: 'financial'
  },
  
  'customer-health': {
    id: 'customer-health',
    name: 'Customer Health Score',
    description: 'Composite metric measuring customer satisfaction, retention, and engagement.',
    businessMeaning: 'How happy and engaged your customers are with your products/services. This predicts future revenue, reduces acquisition costs, and indicates brand strength.',
    whyItMatters: 'Healthy customers drive repeat business, referrals, and brand advocacy. Poor customer health leads to churn, increased acquisition costs, and brand damage.',
    goodValueIndicator: '80+ score indicates satisfied, loyal customers who will stay and recommend your business.',
    badValueIndicator: 'Below 60 indicates at-risk customers likely to churn and damage your reputation.',
    unit: 'Score (0-100)',
    category: 'customer'
  },
  
  'churn-rate': {
    id: 'churn-rate',
    name: 'Churn Rate',
    description: 'Percentage of customers who stopped using your product or service during a given period.',
    businessMeaning: 'The rate at which you are losing customers. It directly reflects product value, customer satisfaction, and competitive pressure.',
    whyItMatters: 'High churn kills growth. It is much more expensive to acquire new customers than to retain existing ones. Reducing churn is the fastest way to increase profitability.',
    goodValueIndicator: 'Below 5% annual churn (for B2B) or 2% monthly (for B2C) is generally healthy.',
    badValueIndicator: 'Rising churn trend or rates above 10% indicate serious product-market fit or service issues.',
    unit: '%',
    category: 'customer'
  },

  'clv': {
    id: 'clv',
    name: 'Customer Lifetime Value',
    description: 'Total revenue a business can expect from a single customer account throughout the business relationship.',
    businessMeaning: 'How much a customer is worth to your business over time. This helps determine how much you should spend to acquire them.',
    whyItMatters: 'CLV dictates your allowable Customer Acquisition Cost (CAC). Increasing CLV means you can spend more to grow and improves long-term profitability.',
    goodValueIndicator: 'CLV should be at least 3x your Customer Acquisition Cost (CAC). Rising CLV shows better retention and upsell success.',
    badValueIndicator: 'CLV:CAC ratio below 1:1 means you are losing money on every new customer.',
    unit: 'USD',
    category: 'customer'
  }
};

// Helper function to get KPI definition
export const getKPIDefinition = (kpiId: KPIId): KPIDefinition => {
  const definition = kpiDefinitions[kpiId];
  if (!definition) {
    throw new Error(`KPI definition not found for ID: ${kpiId}`);
  }
  return definition;
};

// Get all KPIs by category
export const getKPIsByCategory = (category: 'financial' | 'operational' | 'customer') => {
  return Object.values(kpiDefinitions).filter(kpi => kpi.category === category);
};

// Get all KPI IDs
export const getAllKPIIds = (): KPIId[] => {
  return Object.keys(kpiDefinitions) as KPIId[];
};
