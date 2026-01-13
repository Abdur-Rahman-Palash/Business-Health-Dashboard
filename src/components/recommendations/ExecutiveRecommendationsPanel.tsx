'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Target, Filter, CheckCircle, Clock, TrendingUp, AlertTriangle } from 'lucide-react';
import RecommendationCard from './RecommendationCard';
import { Recommendation, Insight, KPIData } from '@/types/business';

interface ExecutiveRecommendationsPanelProps {
  recommendations: Recommendation[];
  insights: Insight[];
  kpis: KPIData[];
  onAction?: (recommendation: Recommendation) => void;
  className?: string;
}

const ExecutiveRecommendationsPanel: React.FC<ExecutiveRecommendationsPanelProps> = ({
  recommendations,
  insights,
  kpis,
  onAction,
  className = ''
}) => {
  const [selectedActionType, setSelectedActionType] = useState<string>('all');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('all');
  const [selectedEffort, setSelectedEffort] = useState<string>('all');

  const filteredRecommendations = recommendations.filter(rec => {
    const matchesActionType = selectedActionType === 'all' || rec.actionType === selectedActionType;
    const matchesTimeframe = selectedTimeframe === 'all' || rec.timeframe === selectedTimeframe;
    const matchesEffort = selectedEffort === 'all' || rec.effort === selectedEffort;
    return matchesActionType && matchesTimeframe && matchesEffort;
  });

  const getInsightForRecommendation = (recommendation: Recommendation): Insight | undefined => {
    return insights.find(insight => insight.id === recommendation.insightId);
  };

  const getKPIForRecommendation = (recommendation: Recommendation): KPIData | undefined => {
    return kpis.find(kpi => kpi.id === recommendation.kpiId);
  };

  const getActionTypeStats = () => {
    const stats = {
      increase: recommendations.filter(r => r.actionType === 'increase').length,
      reduce: recommendations.filter(r => r.actionType === 'reduce').length,
      investigate: recommendations.filter(r => r.actionType === 'investigate').length,
      prioritize: recommendations.filter(r => r.actionType === 'prioritize').length,
      maintain: recommendations.filter(r => r.actionType === 'maintain').length
    };
    return stats;
  };

  const getUrgencyStats = () => {
    const immediate = recommendations.filter(r => r.timeframe === 'immediate').length;
    const shortTerm = recommendations.filter(r => r.timeframe === 'short-term').length;
    const longTerm = recommendations.filter(r => r.timeframe === 'long-term').length;
    return { immediate, shortTerm, longTerm };
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

  const actionStats = getActionTypeStats();
  const urgencyStats = getUrgencyStats();

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-3">
          What Should Leadership Do Next?
        </h2>
        <p className="text-gray-600">
          Action-oriented recommendations directly linked to business insights for executive decision-making.
        </p>
      </motion.div>

      {/* Quick Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <div>
              <div className="text-xl font-bold text-red-900">{urgencyStats.immediate}</div>
              <div className="text-sm text-red-700">Immediate Actions</div>
            </div>
          </div>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5 text-yellow-500" />
            <div>
              <div className="text-xl font-bold text-yellow-900">{urgencyStats.shortTerm}</div>
              <div className="text-sm text-yellow-700">Short-term</div>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-5 h-5 text-blue-500" />
            <div>
              <div className="text-xl font-bold text-blue-900">{urgencyStats.longTerm}</div>
              <div className="text-sm text-blue-700">Long-term</div>
            </div>
          </div>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-500" />
            <div>
              <div className="text-xl font-bold text-green-900">{recommendations.length}</div>
              <div className="text-sm text-green-700">Total Actions</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="flex flex-wrap items-center gap-4 p-4 bg-gray-50 rounded-lg"
      >
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <span className="text-sm font-medium text-gray-700">Filter by:</span>
        </div>
        
        <select
          value={selectedActionType}
          onChange={(e) => setSelectedActionType(e.target.value)}
          className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Actions</option>
          <option value="increase">Increase</option>
          <option value="reduce">Reduce</option>
          <option value="investigate">Investigate</option>
          <option value="prioritize">Prioritize</option>
          <option value="maintain">Maintain</option>
        </select>

        <select
          value={selectedTimeframe}
          onChange={(e) => setSelectedTimeframe(e.target.value)}
          className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Timeframes</option>
          <option value="immediate">Immediate</option>
          <option value="short-term">Short-term</option>
          <option value="long-term">Long-term</option>
        </select>

        <select
          value={selectedEffort}
          onChange={(e) => setSelectedEffort(e.target.value)}
          className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Efforts</option>
          <option value="low">Low Effort</option>
          <option value="medium">Medium Effort</option>
          <option value="high">High Effort</option>
        </select>
      </motion.div>

      {/* Recommendations List */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="space-y-6"
      >
        {filteredRecommendations.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12 bg-gray-50 rounded-lg"
          >
            <Target className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No recommendations found
            </h3>
            <p className="text-gray-600">
              Try adjusting your filters to see available recommendations.
            </p>
          </motion.div>
        ) : (
          filteredRecommendations.map((recommendation) => {
            const insight = getInsightForRecommendation(recommendation);
            const kpiData = getKPIForRecommendation(recommendation);
            
            if (!insight || !kpiData) return null;

            return (
              <motion.div
                key={recommendation.id}
                variants={itemVariants}
              >
                <RecommendationCard
                  recommendation={recommendation}
                  insight={insight}
                  kpiData={kpiData}
                  onAction={onAction}
                />
              </motion.div>
            );
          })
        )}
      </motion.div>

      {/* Action Framework Explanation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-blue-50 border border-blue-200 rounded-lg p-6"
      >
        <h3 className="text-lg font-semibold text-blue-900 mb-4">
          Executive Action Framework
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-blue-800 mb-2">Increase Actions</h4>
            <p className="text-blue-700">
              Focus on growth initiatives, revenue expansion, and market opportunities.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2">Reduce Actions</h4>
            <p className="text-blue-700">
              Cost optimization, efficiency improvements, and risk mitigation strategies.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2">Investigate Actions</h4>
            <p className="text-blue-700">
              Deep analysis, root cause identification, and data-driven exploration.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2">Prioritize Actions</h4>
            <p className="text-blue-700">
              Resource allocation, strategic focus, and competitive positioning.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2">Maintain Actions</h4>
            <p className="text-blue-700">
              Sustain success, protect advantages, and continue effective practices.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2">Time-based Planning</h4>
            <p className="text-blue-700">
              Balance immediate needs with strategic long-term initiatives.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ExecutiveRecommendationsPanel;
