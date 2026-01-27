'use client';

import React from 'react';
import { motion } from 'framer-motion';
import KPIMeaningCard from './KPIMeaningCard';
import { KPIData } from '@/types/business';

interface KPIMeaningLayerProps {
  kpis: KPIData[];
  className?: string;
}

const KPIMeaningLayer: React.FC<KPIMeaningLayerProps> = ({ 
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

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Section Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-8"
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-3">
          Business Metrics Explained
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Understand what each metric means for your business and why it matters for executive decision-making.
        </p>
      </motion.div>

      {/* KPI Cards Grid */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        {kpis.map((kpi, index) => (
          <motion.div
            key={kpi.id}
            variants={itemVariants}
            custom={index}
          >
            <KPIMeaningCard kpi={kpi} />
          </motion.div>
        ))}
      </motion.div>

      {/* Business Context Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8"
      >
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          Executive Context
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-blue-800 mb-1">Financial Health</h4>
            <p className="text-blue-700">
              Revenue, growth, and profitability metrics indicate your business&#39;s financial sustainability and growth capacity.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-1">Operational Efficiency</h4>
            <p className="text-blue-700">
              Expense ratios and margins show how efficiently you convert revenue into profit and manage costs.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-1">Customer Success</h4>
            <p className="text-blue-700">
              Customer health metrics predict future revenue, reduce acquisition costs, and indicate brand strength.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default KPIMeaningLayer;
