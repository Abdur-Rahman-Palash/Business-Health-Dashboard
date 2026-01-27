'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, ArrowDown, Search, Target, Clock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { Recommendation, Insight, KPIData } from '@/types/business';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';

interface RecommendationCardProps {
  recommendation: Recommendation;
  insight: Insight;
  kpiData: KPIData;
  onAction?: (recommendation: Recommendation) => void;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  insight,
  kpiData,
  onAction
}) => {
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [actionTaken, setActionTaken] = useState(false);
  
  const definition = getKPIDefinition(recommendation.kpiId);

  const getActionIcon = (actionType: string) => {
    switch (actionType) {
      case 'increase': return <ArrowUp className="w-5 h-5 text-green-500" />;
      case 'reduce': return <ArrowDown className="w-5 h-5 text-red-500" />;
      case 'investigate': return <Search className="w-5 h-5 text-blue-500" />;
      case 'prioritize': return <Target className="w-5 h-5 text-purple-500" />;
      case 'maintain': return <CheckCircle className="w-5 h-5 text-gray-500" />;
      default: return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getTimeframeColor = (timeframe: string): string => {
    switch (timeframe) {
      case 'immediate': return 'bg-red-100 text-red-700 border-red-200';
      case 'short-term': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'long-term': return 'bg-blue-100 text-blue-700 border-blue-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getEffortColor = (effort: string): string => {
    switch (effort) {
      case 'low': return 'bg-green-100 text-green-700 border-green-200';
      case 'medium': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'high': return 'bg-red-100 text-red-700 border-red-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getConfidenceColor = (confidence: string): string => {
    switch (confidence) {
      case 'high': return 'bg-green-100 text-green-700 border-green-200';
      case 'medium': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'low': return 'bg-red-100 text-red-700 border-red-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const handleAction = async () => {
    if (actionTaken) {
      console.log('Action already taken for this recommendation');
      return;
    }
    
    setIsActionLoading(true);
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Call the parent action handler
      await onAction?.(recommendation);
      
      // Mark action as taken
      setActionTaken(true);
      
      console.log('Action successfully executed for recommendation:', recommendation.title);
    } catch (error) {
      console.error('Error executing action:', error);
    } finally {
      setIsActionLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
    >
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            {getActionIcon(recommendation.actionType)}
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {recommendation.title}
            </h3>
            <p className="text-gray-600 text-sm leading-relaxed mb-3">
              {recommendation.description}
            </p>
            
            {/* Linked Insight */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-3">
              <div className="flex items-center gap-2 mb-1">
                <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-bold">i</span>
                </div>
                <span className="text-xs font-medium text-blue-800">Based on Insight:</span>
              </div>
              <p className="text-xs text-blue-700 pl-6">
                {insight.title}
              </p>
            </div>

            {/* Expected Impact */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <Target className="w-4 h-4 text-green-600" />
                <span className="text-xs font-medium text-green-800">Expected Impact:</span>
              </div>
              <p className="text-xs text-green-700">
                {recommendation.expectedImpact}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Metadata */}
      <div className="px-6 pb-4">
        <div className="flex flex-wrap gap-2">
          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getTimeframeColor(recommendation.timeframe)}`}>
            <Clock className="w-3 h-3 inline mr-1" />
            {recommendation.timeframe}
          </span>
          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getEffortColor(recommendation.effort)}`}>
            Effort: {recommendation.effort}
          </span>
          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getConfidenceColor(recommendation.confidence)}`}>
            Confidence: {recommendation.confidence}
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 border border-gray-200">
            {definition.name}
          </span>
        </div>
      </div>

      {/* Action Button */}
      <div className="px-6 pb-6 pt-2 border-t border-gray-100">
        <button
          onClick={handleAction}
          disabled={isActionLoading || actionTaken}
          className={`w-full font-medium py-3 px-4 rounded-lg transition-all flex items-center justify-center gap-2 ${
            actionTaken 
              ? 'bg-green-500 hover:bg-green-600 text-white' 
              : isActionLoading
              ? 'bg-gray-400 text-white cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
          }`}
        >
          {isActionLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Processing Action...
            </>
          ) : actionTaken ? (
            <>
              <CheckCircle className="w-4 h-4" />
              Action Taken ✓
            </>
          ) : (
            <>
              <Target className="w-4 h-4" />
              Take Action on This Recommendation
            </>
          )}
        </button>
        
        {actionTaken && (
          <div className="mt-2 text-center text-sm text-green-600">
            ✅ Action successfully initiated and tracked
          </div>
        )}
      </div>

      {/* KPI Context */}
      <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <span className="text-gray-500">Related KPI:</span>
            <span className="font-medium text-gray-900">{definition.name}</span>
            <span className="text-gray-400">
              Current: {kpiData.currentValue} {definition.unit}
            </span>
          </div>
          <div className="text-gray-500">
            Action Type: <span className="font-medium text-gray-700 capitalize">{recommendation.actionType}</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default RecommendationCard;
