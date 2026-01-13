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
      case 'critical': return 'border-red-200 bg-red-50';
      case 'warning': return 'border-yellow-200 bg-yellow-50';
      case 'good': return 'border-blue-200 bg-blue-50';
      case 'excellent': return 'border-green-200 bg-green-50';
      default: return 'border-gray-200 bg-gray-50';
    }
  };

  const getStatusIcon = (status: HealthStatus) => {
    switch (status) {
      case 'critical': return <AlertTriangle className="w-5 h-5 text-red-500" />;
      case 'warning': return <TrendingDown className="w-5 h-5 text-yellow-500" />;
      case 'good': return <Info className="w-5 h-5 text-blue-500" />;
      case 'excellent': return <Info className="w-5 h-5 text-green-500" />;
      default: return <Info className="w-5 h-5 text-gray-500" />;
    }
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
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
            <h3 className="font-semibold text-gray-900 mb-1">
              {risk.title}
            </h3>
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-600">{definition.name}</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(risk.severity)}`}>
                {risk.severity} severity
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Explanation */}
      <div className="px-4 pb-3">
        <p className="text-sm text-gray-700 leading-relaxed">
          {risk.explanation}
        </p>
      </div>

      {/* Detailed Information */}
      {showDetails && (
        <div className="border-t border-gray-200 bg-white bg-opacity-50">
          {/* Threshold Logic */}
          <div className="p-4 pb-3">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-6 h-6 bg-gray-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                i
              </div>
              <h4 className="font-medium text-gray-900 text-sm">Threshold Logic</h4>
            </div>
            <p className="text-sm text-gray-600 pl-8">
              {risk.thresholdLogic}
            </p>
          </div>

          {/* Consecutive Periods */}
          <div className="px-4 pb-4">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">
                Triggered for {getConsecutivePeriodsText(risk.consecutivePeriods)}
              </span>
            </div>
          </div>

          {/* KPI Context */}
          <div className="px-4 pb-4 pt-2 border-t border-gray-100">
            <div className="flex items-center justify-between text-sm">
              <div>
                <span className="text-gray-500">Current Value:</span>
                <span className="ml-2 font-medium text-gray-900">
                  {kpiData.currentValue} {definition.unit}
                </span>
              </div>
              <div>
                <span className="text-gray-500">Status:</span>
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
