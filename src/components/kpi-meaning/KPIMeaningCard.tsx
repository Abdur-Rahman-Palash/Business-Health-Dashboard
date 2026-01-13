'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Info, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { KPIData, KPIDefinition, HealthStatus, TrendDirection } from '@/types/business';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';

interface KPIMeaningCardProps {
  kpi: KPIData;
  showDetails?: boolean;
  onToggle?: () => void;
}

const KPIMeaningCard: React.FC<KPIMeaningCardProps> = ({ 
  kpi, 
  showDetails = false,
  onToggle 
}) => {
  const [isExpanded, setIsExpanded] = useState(showDetails);
  const definition = getKPIDefinition(kpi.id);

  const getHealthColor = (status: HealthStatus): string => {
    switch (status) {
      case 'excellent': return 'text-green-600 bg-green-50 border-green-200';
      case 'good': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'warning': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'critical': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getTrendIcon = (trend: TrendDirection) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-red-500" />;
      case 'stable': return <Minus className="w-4 h-4 text-gray-500" />;
      default: return null;
    }
  };

  const formatValue = (value: number, unit: string): string => {
    if (unit === 'USD') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value);
    } else if (unit === '%') {
      return `${value.toFixed(1)}%`;
    } else if (unit === 'Score (0-100)') {
      return `${value.toFixed(1)}`;
    }
    return value.toString();
  };

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
    onToggle?.();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
    >
      {/* Header */}
      <div 
        className="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
        onClick={handleToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="text-lg font-semibold text-gray-900">
                {definition.name}
              </h3>
              {getTrendIcon(kpi.trend)}
              <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getHealthColor(kpi.healthStatus)}`}>
                {kpi.healthStatus.charAt(0).toUpperCase() + kpi.healthStatus.slice(1)}
              </span>
            </div>
            
            <div className="flex items-baseline gap-4">
              <span className="text-2xl font-bold text-gray-900">
                {formatValue(kpi.currentValue, definition.unit)}
              </span>
              {kpi.previousValue !== kpi.currentValue && (
                <span className="text-sm text-gray-500">
                  from {formatValue(kpi.previousValue, definition.unit)}
                </span>
              )}
              <span className="text-sm text-gray-400">
                Target: {formatValue(kpi.targetValue, definition.unit)}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <Info className="w-4 h-4 text-gray-400" />
            </button>
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronDown className="w-5 h-5 text-gray-400" />
            </motion.div>
          </div>
        </div>
      </div>

      {/* Expanded Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: 'auto' }}
            exit={{ height: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-6 border-t border-gray-100">
              <div className="pt-4 space-y-4">
                {/* Business Meaning */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    What This Means
                  </h4>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {definition.businessMeaning}
                  </p>
                </div>

                {/* Why It Matters */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    Why It Matters
                  </h4>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {definition.whyItMatters}
                  </p>
                </div>

                {/* Performance Indicators */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                    <h5 className="text-sm font-medium text-green-800 mb-1">
                      Good Performance
                    </h5>
                    <p className="text-xs text-green-700">
                      {definition.goodValueIndicator}
                    </p>
                  </div>
                  <div className="bg-red-50 p-3 rounded-lg border border-red-200">
                    <h5 className="text-sm font-medium text-red-800 mb-1">
                      Poor Performance
                    </h5>
                    <p className="text-xs text-red-700">
                      {definition.badValueIndicator}
                    </p>
                  </div>
                </div>

                {/* Historical Context */}
                {kpi.historicalValues.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">
                      Recent Performance
                    </h4>
                    <div className="flex gap-2 flex-wrap">
                      {kpi.historicalValues.slice(-3).map((period, index) => (
                        <div 
                          key={period.period}
                          className="bg-gray-50 px-3 py-2 rounded-lg border border-gray-200"
                        >
                          <div className="text-xs text-gray-500">{period.period}</div>
                          <div className="text-sm font-medium text-gray-900">
                            {formatValue(period.value, definition.unit)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default KPIMeaningCard;
