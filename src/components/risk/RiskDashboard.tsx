'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { 
  Shield, 
  AlertTriangle, 
  TrendingDown, 
  Activity,
  Gauge,
  Eye,
  AlertCircle
} from 'lucide-react';
import { RiskIndicator, KPIData, BusinessHealthScore } from '@/types/business';
import RiskIndicatorCard from './RiskIndicatorCard';

interface RiskDashboardProps {
  risks: RiskIndicator[];
  kpis: KPIData[];
  businessHealthScore: BusinessHealthScore;
  className?: string;
}

const RiskDashboard: React.FC<RiskDashboardProps> = ({
  risks,
  kpis,
  businessHealthScore,
  className = ''
}) => {
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

  // Group risks by severity
  const criticalRisks = risks.filter(r => r.status === 'critical');
  const warningRisks = risks.filter(r => r.status === 'warning');
  const highSeverityRisks = risks.filter(r => r.severity === 'high');

  // Get KPI data for risks
  const getKPIData = (kpiId: string) => {
    return kpis.find(k => k.id === kpiId);
  };

  // Calculate risk metrics
  const totalRisks = risks.length;
  const riskPercentage = totalRisks > 0 ? (criticalRisks.length + warningRisks.length) / totalRisks * 100 : 0;

  const getHealthScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
    if (score >= 40) return 'text-orange-600 dark:text-orange-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getHealthScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900/30';
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900/30';
    if (score >= 40) return 'bg-orange-100 dark:bg-orange-900/30';
    return 'bg-red-100 dark:bg-red-900/30';
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Risk Overview Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-lg">
              <Shield className="w-6 h-6 text-red-600 dark:text-red-400" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Risk Dashboard</h2>
              <p className="text-gray-600 dark:text-gray-400">Visual indicators of business health and potential risks</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-center">
              <div className={`text-2xl font-bold ${getHealthScoreColor(businessHealthScore.overall)}`}>
                {businessHealthScore.overall}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Health Score</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                {totalRisks}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Active Risks</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Risk Level Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <div>
              <div className="text-lg font-bold text-gray-900 dark:text-white">{criticalRisks.length}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Critical</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <div>
              <div className="text-lg font-bold text-gray-900 dark:text-white">{warningRisks.length}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Warning</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
            <div>
              <div className="text-lg font-bold text-gray-900 dark:text-white">{highSeverityRisks.length}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">High Severity</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div className="flex items-center gap-3">
            <Activity className="w-3 h-3 text-blue-500" />
            <div>
              <div className="text-lg font-bold text-gray-900 dark:text-white">{riskPercentage.toFixed(1)}%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Risk Ratio</div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Health Score Visualization */}
      <motion.div
        variants={itemVariants}
        className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <Gauge className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          Business Health Score
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Overall Health Score */}
          <div className="text-center">
            <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getHealthScoreBgColor(businessHealthScore.overall)} mb-4`}>
              <div>
                <div className={`text-3xl font-bold ${getHealthScoreColor(businessHealthScore.overall)}`}>
                  {businessHealthScore.overall}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Overall</div>
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getHealthScoreBgColor(businessHealthScore.overall)} ${getHealthScoreColor(businessHealthScore.overall)}`}>
              {businessHealthScore.status.toUpperCase()}
            </div>
          </div>

          {/* Category Breakdown */}
          <div className="space-y-3">
            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-600 dark:text-gray-400">Financial</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{businessHealthScore.financial}</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${businessHealthScore.financial}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-600 dark:text-gray-400">Operational</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{businessHealthScore.operational}</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-green-600 dark:bg-green-400 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${businessHealthScore.operational}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-600 dark:text-gray-400">Customer</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{businessHealthScore.customer}</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-purple-600 dark:bg-purple-400 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${businessHealthScore.customer}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Risk Details */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="space-y-4"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Eye className="w-5 h-5 text-red-600 dark:text-red-400" />
          Risk Details
        </h3>
        
        {risks.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 text-center">
            <AlertCircle className="w-12 h-12 text-green-600 dark:text-green-400 mx-auto mb-4" />
            <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No Active Risks</h4>
            <p className="text-gray-600 dark:text-gray-400">
              All KPIs are within healthy ranges. Continue monitoring for any changes.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {risks.map((risk) => {
              const kpiData = getKPIData(risk.kpiId);
              return kpiData ? (
                <RiskIndicatorCard
                  key={risk.id}
                  risk={risk}
                  kpiData={kpiData}
                />
              ) : null;
            })}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default RiskDashboard;
