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
  },

  'cac': {
    id: 'cac',
    name: 'Customer Acquisition Cost',
    description: 'Total cost of sales and marketing to acquire a single new customer.',
    businessMeaning: 'How much you spend to convince a customer to buy your product/service. This directly impacts your profitability.',
    whyItMatters: 'High CAC makes growth expensive and unsustainable. Lower CAC means more efficient marketing and better unit economics.',
    goodValueIndicator: 'CAC should be less than 1/3 of Customer Lifetime Value (CLV). Stable or declining CAC indicates efficient acquisition.',
    badValueIndicator: 'Rising CAC or CAC:CAC ratio above 1:3 indicates inefficient marketing or competitive pressure.',
    unit: 'USD',
    category: 'financial'
  },

  'ltv-cac-ratio': {
    id: 'ltv-cac-ratio',
    name: 'LTV:CAC Ratio',
    description: 'Ratio of Customer Lifetime Value to Customer Acquisition Cost.',
    businessMeaning: 'How much value you get for each dollar spent acquiring customers. This measures the sustainability of your growth model.',
    whyItMatters: 'The LTV:CAC ratio determines if your business model is fundamentally viable. It guides investment decisions and growth strategy.',
    goodValueIndicator: 'Ratio of 3:1 or higher is considered healthy. Shows sustainable unit economics and profitable growth.',
    badValueIndicator: 'Ratio below 2:1 indicates unsustainable acquisition costs and potential business model issues.',
    unit: 'Ratio',
    category: 'financial'
  },

  'mrr': {
    id: 'mrr',
    name: 'Monthly Recurring Revenue',
    description: 'Predictable revenue generated each month from subscription-based customers.',
    businessMeaning: 'The stable, predictable portion of your revenue that you can count on each month from ongoing subscriptions.',
    whyItMatters: 'MRR indicates business stability and growth momentum. It helps with financial planning, investor relations, and resource allocation.',
    goodValueIndicator: 'Consistent month-over-month growth with low volatility. Shows healthy subscription business and customer retention.',
    badValueIndicator: 'Declining MRR or high volatility indicates churn issues, pricing problems, or market challenges.',
    unit: 'USD',
    category: 'financial'
  },

  'arr': {
    id: 'arr',
    name: 'Annual Recurring Revenue',
    description: 'Total recurring revenue normalized to an annual basis from all subscription customers.',
    businessMeaning: 'The total value of your subscription contracts expressed on an annual basis. This shows the scale of your recurring business.',
    whyItMatters: 'ARR is the primary metric for subscription businesses, indicating long-term revenue potential and business scale.',
    goodValueIndicator: 'Strong ARR growth with low churn indicates healthy subscription business and customer satisfaction.',
    badValueIndicator: 'Stagnant or declining ARR signals market saturation, competitive pressure, or product issues.',
    unit: 'USD',
    category: 'financial'
  },

  'nps': {
    id: 'nps',
    name: 'Net Promoter Score',
    description: 'Measure of customer loyalty and willingness to recommend your company to others.',
    businessMeaning: 'How likely your customers are to recommend your business to friends, family, or colleagues. This predicts organic growth.',
    whyItMatters: 'NPS correlates with revenue growth and customer retention. High NPS customers become brand advocates and reduce acquisition costs.',
    goodValueIndicator: 'Score above 50 indicates excellent customer loyalty and strong word-of-mouth potential.',
    badValueIndicator: 'Score below 0 indicates more detractors than promoters, suggesting serious customer satisfaction issues.',
    unit: 'Score (-100 to 100)',
    category: 'customer'
  },

  'csat': {
    id: 'csat',
    name: 'Customer Satisfaction Score',
    description: 'Direct measure of customer satisfaction with specific interactions or overall experience.',
    businessMeaning: 'How satisfied customers are with your products, services, or interactions. This indicates immediate customer experience quality.',
    whyItMatters: 'CSAT predicts retention, reduces support costs, and identifies service improvement opportunities. High satisfaction drives repeat business.',
    goodValueIndicator: 'Score above 80% indicates satisfied customers who are likely to stay and recommend your business.',
    badValueIndicator: 'Score below 70% indicates dissatisfied customers at risk of churn.',
    unit: '%',
    category: 'customer'
  },

  'operational-efficiency': {
    id: 'operational-efficiency',
    name: 'Operational Efficiency',
    description: 'Ratio of output to input in business operations, measuring process effectiveness.',
    businessMeaning: 'How efficiently your business converts resources (time, money, people) into value. This indicates operational excellence.',
    whyItMatters: 'High efficiency reduces costs, improves margins, and enables competitive pricing. It directly impacts profitability and scalability.',
    goodValueIndicator: 'Score above 75% indicates streamlined operations and effective resource utilization.',
    badValueIndicator: 'Score below 60% suggests operational waste, process issues, or technology gaps.',
    unit: 'Score (0-100)',
    category: 'operational'
  },

  'employee-satisfaction': {
    id: 'employee-satisfaction',
    name: 'Employee Satisfaction Score',
    description: 'Measure of how happy and engaged employees are with their work and company.',
    businessMeaning: 'How satisfied your team is with their jobs, management, and company culture. This predicts retention and productivity.',
    whyItMatters: 'Happy employees provide better customer service, innovate more, and stay longer. Low satisfaction increases turnover costs and hurts service quality.',
    goodValueIndicator: 'Score above 75% indicates engaged workforce likely to stay and perform well.',
    badValueIndicator: 'Score below 65% indicates risk of turnover, productivity issues, and cultural problems.',
    unit: 'Score (0-100)',
    category: 'operational'
  },

  'market-share': {
    id: 'market-share',
    name: 'Market Share',
    description: 'Percentage of total market sales that your business captures.',
    businessMeaning: 'Your position relative to competitors in the total market. This indicates competitive strength and brand recognition.',
    whyItMatters: 'Market share correlates with pricing power, brand influence, and growth potential. It affects investor perception and strategic options.',
    goodValueIndicator: 'Growing market share indicates competitive advantage and effective market penetration.',
    badValueIndicator: 'Declining market share suggests competitive pressure, product issues, or marketing challenges.',
    unit: '%',
    category: 'financial'
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
