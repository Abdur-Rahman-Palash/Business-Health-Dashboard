'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, TrendingDown, Clock, Info } from 'lucide-react';
import type { RiskIndicator, KPIData, HealthStatus } from '@/types/business';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';

interface RiskIndicatorProps {
  risk: RiskIndicator;
  kpiData: KPIData;
  showDetails?: boolean;
}

const RiskIndicator: React.FC<RiskIndicatorProps> = ({ 
  risk, 
  kpiData, 
  showDetails = true 
}) => {
  const definition = getKPIDefinition(risk.kpiId);

  const getStatusColor = (status: HealthStatus): string => {
    switch (status) {
      case 'critical': return 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20';
      case 'warning': return 'border-yellow-200 dark:border-yellow-800 bg-yellow-50 dark:bg-yellow-900/20';
      case 'good': return 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20';
      case 'excellent': return 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20';
      default: return 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800';
    }
  };

  const getStatusIcon = (status: HealthStatus) => {
    switch (status) {
      case 'critical': return <AlertTriangle className="w-5 h-5 text-red-500 dark:text-red-400" />;
      case 'warning': return <TrendingDown className="w-5 h-5 text-yellow-500 dark:text-yellow-400" />;
      case 'good': return <Info className="w-5 h-5 text-blue-500 dark:text-blue-400" />;
      case 'excellent': return <Info className="w-5 h-5 text-green-500 dark:text-green-400" />;
      default: return <Info className="w-5 h-5 text-gray-500 dark:text-gray-400" />;
    }
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity) {
      case 'high': return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
      case 'medium': return 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30';
      case 'low': return 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30';
      default: return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-900/30';
    }
  };

  const getConsecutivePeriodsText = (periods: number): string => {
    if (periods === 1) return '1 consecutive period';
    return `${periods} consecutive periods`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      className={`rounded-lg border-2 ${getStatusColor(risk.status)} overflow-hidden`}
    >
      {/* Header */}
      <div className="p-4 pb-3">
        <div className="flex items-start gap-3">
          {getStatusIcon(risk.status)}
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              {risk.title}
            </h3>
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-600 dark:text-gray-400">{definition.name}</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(risk.severity)}`}>
                {risk.severity} severity
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Explanation */}
      <div className="px-4 pb-3">
        <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
          {risk.explanation}
        </p>
      </div>

      {/* Detailed Information */}
      {showDetails && (
        <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 bg-opacity-50 dark:bg-opacity-50">
          {/* Threshold Logic */}
          <div className="p-4 pb-3">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-6 h-6 bg-gray-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                i
              </div>
              <h4 className="font-medium text-gray-900 dark:text-white text-sm">Threshold Logic</h4>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 pl-8">
              {risk.thresholdLogic}
            </p>
          </div>

          {/* Consecutive Periods */}
          <div className="px-4 pb-4">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Triggered for {getConsecutivePeriodsText(risk.consecutivePeriods)}
              </span>
            </div>
          </div>

          {/* KPI Context */}
          <div className="px-4 pb-4 pt-2 border-t border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between text-sm">
              <div>
                <span className="text-gray-500 dark:text-gray-400">Current Value:</span>
                <span className="ml-2 font-medium text-gray-900 dark:text-white">
                  {kpiData.currentValue} {definition.unit}
                </span>
              </div>
              <div>
                <span className="text-gray-500 dark:text-gray-400">Status:</span>
                <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(risk.status)}`}>
                  {risk.status}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default RiskIndicator;
