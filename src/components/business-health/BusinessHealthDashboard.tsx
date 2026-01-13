'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Shield, AlertTriangle, TrendingUp, Activity, TrendingDown } from 'lucide-react';
import RiskIndicator from './RiskIndicator';
import { RiskIndicator as RiskIndicatorType, KPIData, BusinessHealthScore } from '@/types/business';

interface BusinessHealthDashboardProps {
  risks: RiskIndicatorType[];
  kpis: KPIData[];
  businessHealthScore: BusinessHealthScore;
  className?: string;
}

const BusinessHealthDashboard: React.FC<BusinessHealthDashboardProps> = ({
  risks,
  kpis,
  businessHealthScore,
  className = ''
}) => {
  const getHealthScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getHealthScoreBg = (score: number): string => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 60) return 'bg-yellow-50 border-yellow-200';
    if (score >= 40) return 'bg-orange-50 border-orange-200';
    return 'bg-red-50 border-red-200';
  };

  const getHealthStatusText = (status: string): string => {
    switch (status) {
      case 'excellent': return 'Excellent Health';
      case 'good': return 'Good Health';
      case 'warning': return 'Warning';
      case 'critical': return 'Critical';
      default: return 'Unknown';
    }
  };

  const riskStats = {
    critical: risks.filter(r => r.status === 'critical').length,
    warning: risks.filter(r => r.status === 'warning').length,
    good: risks.filter(r => r.status === 'good').length,
    excellent: risks.filter(r => r.status === 'excellent').length
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.4
      }
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-3">
          Business Health & Risk Indicators
        </h2>
        <p className="text-gray-600">
          Real-time risk monitoring and business health assessment for executive decision-making.
        </p>
      </motion.div>

      {/* Overall Health Score */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className={`rounded-lg border-2 ${getHealthScoreBg(businessHealthScore.overall)} p-6`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-sm">
              <Shield className="w-8 h-8 text-gray-700" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                Overall Business Health
              </h3>
              <p className="text-sm text-gray-600">
                {getHealthStatusText(businessHealthScore.status)}
              </p>
            </div>
          </div>
          
          <div className="text-right">
            <div className={`text-4xl font-bold ${getHealthScoreColor(businessHealthScore.overall)}`}>
              {businessHealthScore.overall}
            </div>
            <div className="text-sm text-gray-500">out of 100</div>
          </div>
        </div>

        {/* Category Scores */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="text-center">
            <div className="text-2xl font-semibold text-blue-600">
              {businessHealthScore.financial}
            </div>
            <div className="text-sm text-gray-600">Financial</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-semibold text-green-600">
              {businessHealthScore.operational}
            </div>
            <div className="text-sm text-gray-600">Operational</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-semibold text-purple-600">
              {businessHealthScore.customer}
            </div>
            <div className="text-sm text-gray-600">Customer</div>
          </div>
        </div>
      </motion.div>

      {/* Risk Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <div>
              <div className="text-xl font-bold text-red-900">{riskStats.critical}</div>
              <div className="text-sm text-red-700">Critical Risks</div>
            </div>
          </div>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <TrendingDown className="w-5 h-5 text-yellow-500" />
            <div>
              <div className="text-xl font-bold text-yellow-900">{riskStats.warning}</div>
              <div className="text-sm text-yellow-700">Warning Risks</div>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <Activity className="w-5 h-5 text-blue-500" />
            <div>
              <div className="text-xl font-bold text-blue-900">{riskStats.good}</div>
              <div className="text-sm text-blue-700">Good Status</div>
            </div>
          </div>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-5 h-5 text-green-500" />
            <div>
              <div className="text-xl font-bold text-green-900">{riskStats.excellent}</div>
              <div className="text-sm text-green-700">Excellent</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Risk Indicators List */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Active Risk Indicators
        </h3>
        
        {risks.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12 bg-green-50 border border-green-200 rounded-lg"
          >
            <Shield className="w-12 h-12 text-green-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-green-900 mb-2">
              All Systems Healthy
            </h3>
            <p className="text-green-700">
              No active risk indicators detected. Business is performing within normal parameters.
            </p>
          </motion.div>
        ) : (
          <div className="space-y-4">
            {risks.map((risk) => {
              const kpiData = kpis.find(kpi => kpi.id === risk.kpiId);
              if (!kpiData) return null;

              return (
                <motion.div
                  key={risk.id}
                  variants={itemVariants}
                >
                  <RiskIndicator
                    risk={risk}
                    kpiData={kpiData}
                    showDetails={true}
                  />
                </motion.div>
              );
            })}
          </div>
        )}
      </motion.div>

      {/* Health Factors Breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="bg-gray-50 border border-gray-200 rounded-lg p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Health Score Breakdown
        </h3>
        <div className="space-y-3">
          {businessHealthScore.factors.map((factor, index) => (
            <div key={factor.category} className="flex items-center gap-4">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">
                    {factor.category}
                  </span>
                  <span className="text-sm text-gray-600">
                    {factor.score}/100 (Weight: {(factor.weight * 100).toFixed(0)}%)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${factor.score}%` }}
                    transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                    className={`h-2 rounded-full ${
                      factor.score >= 80 ? 'bg-green-500' :
                      factor.score >= 60 ? 'bg-yellow-500' :
                      factor.score >= 40 ? 'bg-orange-500' : 'bg-red-500'
                    }`}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default BusinessHealthDashboard;
