import { ThresholdRule, KPIId, HealthStatus } from '@/types/business';

// Business Threshold Rules for Executive Decision Making
// These thresholds determine health status and trigger insights

export const thresholdRules: Record<KPIId, ThresholdRule> = {
  'revenue': {
    kpiId: 'revenue',
    excellent: { min: 1000000 }, // $1M+
    good: { min: 500000, max: 999999 }, // $500K-$999K
    warning: { min: 250000, max: 499999 }, // $250K-$499K
    critical: { max: 249999 } // <$250K
  },
  
  'revenue-growth': {
    kpiId: 'revenue-growth',
    excellent: { min: 20 }, // 20%+
    good: { min: 10, max: 19.9 }, // 10-19.9%
    warning: { min: 0, max: 9.9 }, // 0-9.9%
    critical: { max: -0.1 } // Negative growth
  },
  
  'profit-margin': {
    kpiId: 'profit-margin',
    excellent: { min: 20 }, // 20%+
    good: { min: 15, max: 19.9 }, // 15-19.9%
    warning: { min: 10, max: 14.9 }, // 10-14.9%
    critical: { max: 9.9 } // <10%
  },
  
  'expense-ratio': {
    kpiId: 'expense-ratio',
    excellent: { max: 70 }, // <=70%
    good: { min: 70.1, max: 80 }, // 70.1-80%
    warning: { min: 80.1, max: 90 }, // 80.1-90%
    critical: { min: 90.1 } // >90%
  },
  
  'customer-health': {
    kpiId: 'customer-health',
    excellent: { min: 85 }, // 85+
    good: { min: 70, max: 84.9 }, // 70-84.9
    warning: { min: 50, max: 69.9 }, // 50-69.9
    critical: { max: 49.9 } // <50
  },

  'churn-rate': {
    kpiId: 'churn-rate',
    excellent: { max: 2 }, // <2%
    good: { min: 2.1, max: 5 }, // 2.1-5%
    warning: { min: 5.1, max: 10 }, // 5.1-10%
    critical: { min: 10.1 } // >10%
  },

  'clv': {
    kpiId: 'clv',
    excellent: { min: 10000 }, // $10k+
    good: { min: 5000, max: 9999 }, // $5k-$9.9k
    warning: { min: 2000, max: 4999 }, // $2k-$4.9k
    critical: { max: 1999 } // <$2k
  }
};

// Calculate health status based on value and thresholds
export const calculateHealthStatus = (
  kpiId: KPIId, 
  value: number
): HealthStatus => {
  const rule = thresholdRules[kpiId];
  if (!rule) {
    return 'good'; // Default to good if no rule exists
  }

  // Check critical first (highest priority)
  if (
    (rule.critical.min !== undefined && value >= rule.critical.min) ||
    (rule.critical.max !== undefined && value <= rule.critical.max)
  ) {
    return 'critical';
  }

  // Check warning
  if (
    (rule.warning.min !== undefined && value >= rule.warning.min) ||
    (rule.warning.max !== undefined && value <= rule.warning.max)
  ) {
    return 'warning';
  }

  // Check good
  if (
    (rule.good.min !== undefined && value >= rule.good.min) ||
    (rule.good.max !== undefined && value <= rule.good.max)
  ) {
    return 'good';
  }

  // Check excellent
  if (
    (rule.excellent.min !== undefined && value >= rule.excellent.min) ||
    (rule.excellent.max !== undefined && value <= rule.excellent.max)
  ) {
    return 'excellent';
  }

  return 'good'; // Default fallback
};

// Get threshold explanation for business users
export const getThresholdExplanation = (
  kpiId: KPIId, 
  value: number, 
  status: HealthStatus
): string => {
  const rule = thresholdRules[kpiId];
  if (!rule) {
    return `No threshold rules defined for this KPI.`;
  }

  const explanations: Record<HealthStatus, string> = {
    excellent: `Excellent performance: Value of ${value} exceeds our highest expectations and indicates outstanding business health.`,
    good: `Good performance: Value of ${value} meets business expectations and indicates solid operational health.`,
    warning: `Warning: Value of ${value} is below optimal range and requires attention to prevent further decline.`,
    critical: `Critical: Value of ${value} is in the danger zone and requires immediate leadership intervention.`
  };

  return explanations[status];
};

// Check if value is within threshold range
export const isWithinThreshold = (
  kpiId: KPIId, 
  value: number, 
  status: HealthStatus
): boolean => {
  const rule = thresholdRules[kpiId];
  if (!rule) return true;

  const threshold = rule[status];
  if (!threshold) return false;

  const minCheck = threshold.min !== undefined ? value >= threshold.min : true;
  const maxCheck = threshold.max !== undefined ? value <= threshold.max : true;

  return minCheck && maxCheck;
};
