'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { FileText, TrendingUp, AlertTriangle, Target, Calendar, Download } from 'lucide-react';
import type { ExecutiveSummary } from '@/types/business';

interface ExecutiveSummaryProps {
  summary: ExecutiveSummary;
  className?: string;
}

const ExecutiveSummary: React.FC<ExecutiveSummaryProps> = ({ 
  summary, 
  className = '' 
}) => {
  const getHealthStatusColor = (status: string): string => {
    switch (status) {
      case 'excellent': return 'text-green-600 bg-green-50 border-green-200';
      case 'good': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'warning': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'critical': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handleDownload = () => {
    // In a real implementation, this would generate and download a PDF
    const summaryText = `
Executive Business Summary - ${summary.period}
Generated: ${formatDate(summary.generatedAt)}

Overall Health: ${summary.overallHealth.toUpperCase()}

KEY HIGHLIGHTS:
${summary.keyHighlights.map((highlight, index) => `${index + 1}. ${highlight}`).join('\n')}

TOP RISKS:
${summary.topRisks.map((risk, index) => `${index + 1}. ${risk.title}: ${risk.description}`).join('\n')}

TOP OPPORTUNITIES:
${summary.topOpportunities.map((opp, index) => `${index + 1}. ${opp.title}: ${opp.description}`).join('\n')}

EXECUTIVE NARRATIVE:
${summary.narrative}
    `;

    const blob = new Blob([summaryText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `executive-summary-${summary.period}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden ${className}`}
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold mb-2">Executive Summary</h1>
            <div className="flex items-center gap-4 text-blue-100">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>{summary.period}</span>
              </div>
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                <span>Generated {formatDate(summary.generatedAt)}</span>
              </div>
            </div>
          </div>
          
          <button
            onClick={handleDownload}
            className="flex items-center gap-2 px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
          >
            <Download className="w-4 h-4" />
            Download
          </button>
        </div>
      </div>

      {/* Overall Health Status */}
      <div className="p-6 pb-4">
        <div className={`inline-flex items-center gap-3 px-4 py-3 rounded-lg border-2 ${getHealthStatusColor(summary.overallHealth)}`}>
          <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
            <FileText className="w-4 h-4 text-gray-700" />
          </div>
          <div>
            <div className="font-semibold text-lg">
              Overall Business Health: {summary.overallHealth.charAt(0).toUpperCase() + summary.overallHealth.slice(1)}
            </div>
            <div className="text-sm opacity-75">
              Current assessment of business performance
            </div>
          </div>
        </div>
      </div>

      {/* Key Highlights */}
      <div className="px-6 pb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Target className="w-5 h-5 text-blue-600" />
          Key Highlights
        </h2>
        <div className="space-y-3">
          {summary.keyHighlights.map((highlight, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="flex items-start gap-3"
            >
              <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 mt-0.5">
                {index + 1}
              </div>
              <p className="text-gray-700 leading-relaxed">{highlight}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Risks and Opportunities Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 px-6 pb-6">
        {/* Top Risks */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-5">
          <h2 className="text-lg font-semibold text-red-900 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Top Risks
          </h2>
          <div className="space-y-4">
            {summary.topRisks.map((risk, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.2 + index * 0.1 }}
                className="bg-white rounded-lg p-4 border border-red-100"
              >
                <h3 className="font-medium text-red-900 mb-2">{risk.title}</h3>
                <p className="text-sm text-red-700 leading-relaxed">{risk.description}</p>
                <div className="mt-2 text-xs text-red-600 font-medium">
                  Related KPI: {risk.kpiId.replace('-', ' ').charAt(0).toUpperCase() + risk.kpiId.slice(1).replace('-', ' ')}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Top Opportunities */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-5">
          <h2 className="text-lg font-semibold text-green-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Top Opportunities
          </h2>
          <div className="space-y-4">
            {summary.topOpportunities.map((opportunity, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.2 + index * 0.1 }}
                className="bg-white rounded-lg p-4 border border-green-100"
              >
                <h3 className="font-medium text-green-900 mb-2">{opportunity.title}</h3>
                <p className="text-sm text-green-700 leading-relaxed">{opportunity.description}</p>
                <div className="mt-2 text-xs text-green-600 font-medium">
                  Related KPI: {opportunity.kpiId.replace('-', ' ').charAt(0).toUpperCase() + opportunity.kpiId.slice(1).replace('-', ' ')}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Executive Narrative */}
      <div className="bg-gray-50 px-6 py-6 border-t border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Executive Narrative</h2>
        <div className="bg-white rounded-lg p-5 border border-gray-200">
          <p className="text-gray-700 leading-relaxed whitespace-pre-line">
            {summary.narrative}
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-100 px-6 py-4 border-t border-gray-200">
        <div className="flex flex-col sm:flex-row sm:justify-between gap-2 text-sm text-gray-600">
          <div>
            This summary is generated automatically based on current business metrics and insights.
          </div>
          <div>
            Last updated: {formatDate(summary.generatedAt)}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ExecutiveSummary;
