'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { KPIData } from '@/types/business';
import TrendChart from '../charts/TrendChart';
import CustomerSegmentation from './CustomerSegmentation';
import TrendAnalysis from './TrendAnalysis';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';
import { LineChart as LineChartIcon, Activity, TrendingUp, Users, Calendar } from 'lucide-react';

interface AnalyticsDashboardProps {
  kpis: KPIData[];
  className?: string;
}

const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({
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

  // Group KPIs by category
  const financialKPIs = kpis.filter(k => getKPIDefinition(k.id).category === 'financial');
  const customerKPIs = kpis.filter(k => getKPIDefinition(k.id).category === 'customer');
  const operationalKPIs = kpis.filter(k => getKPIDefinition(k.id).category === 'operational');

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-3">
          <Activity className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          Interactive Analytics
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Visual analysis of key performance trends over time.
        </p>
      </motion.div>

      {/* Financial Section */}
      <section>
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-blue-500 dark:text-blue-400" />
          Financial Performance
        </h3>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
        >
          {financialKPIs.map((kpi) => {
            const def = getKPIDefinition(kpi.id);
            return (
              <motion.div
                key={kpi.id}
                variants={itemVariants}
                className="bg-white p-6 rounded-lg shadow-sm border border-gray-200"
              >
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-gray-900">{def.name}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full border ${
                    kpi.healthStatus === 'excellent' ? 'bg-green-50 text-green-700 border-green-200' :
                    kpi.healthStatus === 'good' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                    kpi.healthStatus === 'warning' ? 'bg-yellow-50 text-yellow-700 border-yellow-200' :
                    'bg-red-50 text-red-700 border-red-200'
                  }`}>
                    {kpi.healthStatus.toUpperCase()}
                  </span>
                </div>
                <TrendChart kpi={kpi} height={250} />
              </motion.div>
            );
          })}
        </motion.div>
      </section>

      {/* Customer Section */}
      <section>
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-purple-500 dark:text-purple-400" />
          Customer Metrics
        </h3>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
        >
          {customerKPIs.map((kpi) => {
            const def = getKPIDefinition(kpi.id);
            return (
              <motion.div
                key={kpi.id}
                variants={itemVariants}
                className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{def.name}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full border ${
                    kpi.healthStatus === 'excellent' ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800' :
                    kpi.healthStatus === 'good' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800' :
                    kpi.healthStatus === 'warning' ? 'bg-yellow-50 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800' :
                    'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800'
                  }`}>
                    {kpi.healthStatus.toUpperCase()}
                  </span>
                </div>
                <TrendChart kpi={kpi} height={250} />
              </motion.div>
            );
          })}
        </motion.div>
      </section>

      {/* Customer Segmentation */}
      <section>
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
          <Users className="w-5 h-5 text-green-500 dark:text-green-400" />
          Customer Segmentation
        </h3>
        <CustomerSegmentation />
      </section>

      {/* Trend Analysis */}
      <section>
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
          <Calendar className="w-5 h-5 text-orange-500 dark:text-orange-400" />
          Time-Based Trend Analysis
        </h3>
        <TrendAnalysis />
      </section>

      {/* Operational Section (if any) */}
      {operationalKPIs.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <LineChartIcon className="w-5 h-5 text-gray-500" />
            Operational Metrics
          </h3>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {operationalKPIs.map((kpi) => {
              const def = getKPIDefinition(kpi.id);
              return (
                <motion.div
                  key={kpi.id}
                  variants={itemVariants}
                  className="bg-white p-6 rounded-lg shadow-sm border border-gray-200"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="font-semibold text-gray-900">{def.name}</h4>
                    <span className={`text-xs px-2 py-1 rounded-full border ${
                      kpi.healthStatus === 'excellent' ? 'bg-green-50 text-green-700 border-green-200' :
                      kpi.healthStatus === 'good' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                      kpi.healthStatus === 'warning' ? 'bg-yellow-50 text-yellow-700 border-yellow-200' :
                      'bg-red-50 text-red-700 border-red-200'
                    }`}>
                      {kpi.healthStatus.toUpperCase()}
                    </span>
                  </div>
                  <TrendChart kpi={kpi} height={250} />
                </motion.div>
              );
            })}
          </motion.div>
        </section>
      )}
    </div>
  );
};

export default AnalyticsDashboard;
