'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Filter, RefreshCw, Edit3 } from 'lucide-react';
import InsightCard from './InsightCard';
import { Insight, KPIData } from '@/types/business';

interface InsightEngineProps {
  insights: Insight[];
  kpis: KPIData[];
  onEditInsight?: (insight: Insight) => void;
  onRefreshInsights?: () => void;
  className?: string;
}

const InsightEngine: React.FC<InsightEngineProps> = ({
  insights,
  kpis,
  onEditInsight,
  onRefreshInsights,
  className = ''
}) => {
  const [filteredInsights, setFilteredInsights] = useState<Insight[]>(insights);
  const [selectedPriority, setSelectedPriority] = useState<string>('all');
  const [selectedKPI, setSelectedKPI] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'cards' | 'compact'>('cards');
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    let filtered = insights;

    // Filter by priority
    if (selectedPriority !== 'all') {
      filtered = filtered.filter(insight => insight.priority === selectedPriority);
    }

    // Filter by KPI
    if (selectedKPI !== 'all') {
      filtered = filtered.filter(insight => insight.kpiId === selectedKPI);
    }

    setFilteredInsights(filtered);
  }, [insights, selectedPriority, selectedKPI]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await onRefreshInsights?.();
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  const getKPITitle = (kpiId: string): string => {
    const kpi = kpis.find(k => k.id === kpiId);
    return kpi ? kpi.id.charAt(0).toUpperCase() + kpi.id.slice(1).replace('-', ' ') : kpiId;
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

  const priorityStats = {
    high: insights.filter(i => i.priority === 'high').length,
    medium: insights.filter(i => i.priority === 'medium').length,
    low: insights.filter(i => i.priority === 'low').length
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Business Insights
            </h2>
            <p className="text-gray-600">
              Data-driven insights using the What → So What → Now What framework
            </p>
          </div>
          
          <div className="flex items-center gap-3">
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>

        {/* Priority Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">{priorityStats.high}</span>
              </div>
              <div>
                <div className="font-semibold text-red-900">High Priority</div>
                <div className="text-sm text-red-700">Immediate attention</div>
              </div>
            </div>
          </div>
          
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">{priorityStats.medium}</span>
              </div>
              <div>
                <div className="font-semibold text-yellow-900">Medium Priority</div>
                <div className="text-sm text-yellow-700">Plan to address</div>
              </div>
            </div>
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">{priorityStats.low}</span>
              </div>
              <div>
                <div className="font-semibold text-blue-900">Low Priority</div>
                <div className="text-sm text-blue-700">Monitor</div>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>
          
          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Priorities</option>
            <option value="high">High Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="low">Low Priority</option>
          </select>

          <select
            value={selectedKPI}
            onChange={(e) => setSelectedKPI(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All KPIs</option>
            {kpis.map(kpi => (
              <option key={kpi.id} value={kpi.id}>
                {getKPITitle(kpi.id)}
              </option>
            ))}
          </select>

          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={() => setViewMode('cards')}
              className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                viewMode === 'cards' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
            >
              Cards
            </button>
            <button
              onClick={() => setViewMode('compact')}
              className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                viewMode === 'compact' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
            >
              Compact
            </button>
          </div>
        </div>
      </motion.div>

      {/* Insights Display */}
      <AnimatePresence mode="wait">
        {filteredInsights.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-center py-12"
          >
            <div className="text-gray-400 mb-4">
              <Filter className="w-12 h-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No insights found
            </h3>
            <p className="text-gray-600">
              Try adjusting your filters or refresh to generate new insights.
            </p>
          </motion.div>
        ) : (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className={
              viewMode === 'compact' 
                ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                : 'space-y-6'
            }
          >
            {filteredInsights.map((insight) => {
              const kpiData = kpis.find(kpi => kpi.id === insight.kpiId);
              if (!kpiData) return null;

              return (
                <motion.div
                  key={insight.id}
                  variants={itemVariants}
                  layout
                >
                  <InsightCard
                    insight={insight}
                    kpiData={kpiData}
                    onEdit={onEditInsight}
                    compact={viewMode === 'compact'}
                  />
                </motion.div>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Framework Explanation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-blue-50 border border-blue-200 rounded-lg p-6"
      >
        <h3 className="text-lg font-semibold text-blue-900 mb-4">
          What → So What → Now What Framework
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-blue-800 mb-2 flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                1
              </div>
              What (Observation)
            </h4>
            <p className="text-blue-700">
              Factual analysis of what the data shows. Pure observation without interpretation.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2 flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                2
              </div>
              So What (Impact)
            </h4>
            <p className="text-blue-700">
              Why this matters to the business. The implications and consequences for leadership.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2 flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                3
              </div>
              Now What (Action)
            </h4>
            <p className="text-blue-700">
              Specific actions leadership should take. Clear, actionable recommendations.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default InsightEngine;
