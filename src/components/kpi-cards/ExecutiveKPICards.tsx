'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  ArrowUpRight, 
  ArrowDownRight,
  DollarSign,
  Users,
  Target,
  Zap
} from 'lucide-react';
import { KPIData } from '@/types/business';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';

interface ExecutiveKPICardsProps {
  kpis: KPIData[];
  className?: string;
}

const ExecutiveKPICards: React.FC<ExecutiveKPICardsProps> = ({
  kpis,
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

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4" />;
      case 'down':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'text-green-600 dark:text-green-400';
      case 'down':
        return 'text-red-600 dark:text-red-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'excellent':
        return 'border-green-500 bg-green-50 dark:bg-green-900/20';
      case 'good':
        return 'border-blue-500 bg-blue-50 dark:bg-blue-900/20';
      case 'warning':
        return 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
      case 'critical':
        return 'border-red-500 bg-red-50 dark:bg-red-900/20';
      default:
        return 'border-gray-300 bg-gray-50 dark:bg-gray-800';
    }
  };

  const getHealthBadgeColor = (status: string) => {
    switch (status) {
      case 'excellent':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      case 'good':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'financial':
        return <DollarSign className="w-5 h-5" />;
      case 'customer':
        return <Users className="w-5 h-5" />;
      case 'operational':
        return <Zap className="w-5 h-5" />;
      default:
        return <Target className="w-5 h-5" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'financial':
        return 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30';
      case 'customer':
        return 'text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/30';
      case 'operational':
        return 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30';
      default:
        return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-900/30';
    }
  };

  const formatValue = (value: number, unit: string) => {
    if (unit === 'USD') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    }
    if (unit === '%') {
      return `${value.toFixed(1)}%`;
    }
    if (unit === 'Score (-100 to 100)' || unit === 'Score (0-100)') {
      return value.toString();
    }
    return value.toLocaleString();
  };

  const calculateChangePercentage = (current: number, previous: number) => {
    if (previous === 0) return 0;
    return ((current - previous) / previous * 100);
  };

  // Group KPIs by category and select top performers
  const financialKPIs = kpis.filter(k => getKPIDefinition(k.id).category === 'financial').slice(0, 3);
  const customerKPIs = kpis.filter(k => getKPIDefinition(k.id).category === 'customer').slice(0, 3);
  const operationalKPIs = kpis.filter(k => getKPIDefinition(k.id).category === 'operational').slice(0, 3);

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Financial KPIs */}
      {financialKPIs.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Financial Performance
          </h3>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-3 gap-4"
          >
            {financialKPIs.map((kpi) => {
              const definition = getKPIDefinition(kpi.id);
              const changePercentage = calculateChangePercentage(kpi.currentValue, kpi.previousValue);
              
              return (
                <motion.div
                  key={kpi.id}
                  variants={itemVariants}
                  className={`p-6 rounded-lg border-2 ${getHealthColor(kpi.healthStatus)} hover:shadow-lg transition-shadow cursor-pointer`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`p-2 rounded-lg ${getCategoryColor(definition.category)}`}>
                      {getCategoryIcon(definition.category)}
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getHealthBadgeColor(kpi.healthStatus)}`}>
                      {kpi.healthStatus.toUpperCase()}
                    </span>
                  </div>
                  
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                    {definition.name}
                  </h4>
                  
                  <div className="mb-4">
                    <div className="text-2xl font-bold text-gray-900 dark:text-white">
                      {formatValue(kpi.currentValue, definition.unit)}
                    </div>
                    <div className="flex items-center gap-2 mt-2">
                      <div className={`flex items-center gap-1 ${getTrendColor(kpi.trend)}`}>
                        {kpi.trend === 'up' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                        <span className="text-sm font-medium">
                          {Math.abs(changePercentage).toFixed(1)}%
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        vs last period
                      </span>
                    </div>
                  </div>
                  
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Target</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {formatValue(kpi.targetValue, definition.unit)}
                      </span>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${Math.min((kpi.currentValue / kpi.targetValue) * 100, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        </section>
      )}

      {/* Customer KPIs */}
      {customerKPIs.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            Customer Metrics
          </h3>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-3 gap-4"
          >
            {customerKPIs.map((kpi) => {
              const definition = getKPIDefinition(kpi.id);
              const changePercentage = calculateChangePercentage(kpi.currentValue, kpi.previousValue);
              
              return (
                <motion.div
                  key={kpi.id}
                  variants={itemVariants}
                  className={`p-6 rounded-lg border-2 ${getHealthColor(kpi.healthStatus)} hover:shadow-lg transition-shadow cursor-pointer`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`p-2 rounded-lg ${getCategoryColor(definition.category)}`}>
                      {getCategoryIcon(definition.category)}
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getHealthBadgeColor(kpi.healthStatus)}`}>
                      {kpi.healthStatus.toUpperCase()}
                    </span>
                  </div>
                  
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                    {definition.name}
                  </h4>
                  
                  <div className="mb-4">
                    <div className="text-2xl font-bold text-gray-900 dark:text-white">
                      {formatValue(kpi.currentValue, definition.unit)}
                    </div>
                    <div className="flex items-center gap-2 mt-2">
                      <div className={`flex items-center gap-1 ${getTrendColor(kpi.trend)}`}>
                        {kpi.trend === 'up' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                        <span className="text-sm font-medium">
                          {Math.abs(changePercentage).toFixed(1)}%
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        vs last period
                      </span>
                    </div>
                  </div>
                  
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Target</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {formatValue(kpi.targetValue, definition.unit)}
                      </span>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-purple-600 dark:bg-purple-400 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${Math.min((kpi.currentValue / kpi.targetValue) * 100, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        </section>
      )}

      {/* Operational KPIs */}
      {operationalKPIs.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-green-600 dark:text-green-400" />
            Operational Efficiency
          </h3>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-3 gap-4"
          >
            {operationalKPIs.map((kpi) => {
              const definition = getKPIDefinition(kpi.id);
              const changePercentage = calculateChangePercentage(kpi.currentValue, kpi.previousValue);
              
              return (
                <motion.div
                  key={kpi.id}
                  variants={itemVariants}
                  className={`p-6 rounded-lg border-2 ${getHealthColor(kpi.healthStatus)} hover:shadow-lg transition-shadow cursor-pointer`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`p-2 rounded-lg ${getCategoryColor(definition.category)}`}>
                      {getCategoryIcon(definition.category)}
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getHealthBadgeColor(kpi.healthStatus)}`}>
                      {kpi.healthStatus.toUpperCase()}
                    </span>
                  </div>
                  
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                    {definition.name}
                  </h4>
                  
                  <div className="mb-4">
                    <div className="text-2xl font-bold text-gray-900 dark:text-white">
                      {formatValue(kpi.currentValue, definition.unit)}
                    </div>
                    <div className="flex items-center gap-2 mt-2">
                      <div className={`flex items-center gap-1 ${getTrendColor(kpi.trend)}`}>
                        {kpi.trend === 'up' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                        <span className="text-sm font-medium">
                          {Math.abs(changePercentage).toFixed(1)}%
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        vs last period
                      </span>
                    </div>
                  </div>
                  
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Target</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {formatValue(kpi.targetValue, definition.unit)}
                      </span>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-green-600 dark:bg-green-400 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${Math.min((kpi.currentValue / kpi.targetValue) * 100, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        </section>
      )}
    </div>
  );
};

export default ExecutiveKPICards;
