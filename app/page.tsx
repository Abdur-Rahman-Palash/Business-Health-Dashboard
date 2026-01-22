'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Brain, Shield, Target, FileText, RefreshCw, Menu, Activity } from 'lucide-react';

// Import components
import KPIMeaningLayer from '@/components/kpi-meaning/KPIMeaningLayer';
import InsightEngine from '@/components/insights/InsightEngine';
import BusinessHealthDashboard from '@/components/business-health/BusinessHealthDashboard';
import ExecutiveRecommendationsPanel from '@/components/recommendations/ExecutiveRecommendationsPanel';
import ExecutiveSummary from '@/components/executive-summary/ExecutiveSummary';
import AnalyticsDashboard from '@/components/analytics/AnalyticsDashboard';
import ThemeToggle from '@/components/ui/ThemeToggle';
import InteractiveFilters from '@/components/filters/InteractiveFilters';
import ExecutiveKPICards from '@/components/kpi-cards/ExecutiveKPICards';
import StreamlitEmbed from '@/components/streamlit/StreamlitEmbed';

// Import services and types
import { mockAPI } from '@/services/mock-api';
import type { DashboardData, Insight, Recommendation } from '@/types/business';

const ExecutiveDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [isMenuOpen, setIsMenuOpen] = useState<boolean>(false);
  const [filters, setFilters] = useState({
    dateRange: { start: '', end: '' },
    region: 'all',
    product: 'all'
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await mockAPI.getDashboardData();
      if (response.success) {
        setDashboardData({
          ...response.data,
          lastUpdated: response.timestamp
        });
      } else {
        setError(response.message || 'Failed to load dashboard data');
      }
    } catch (err) {
      setError('An error occurred while loading dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleEditInsight = (insight: Insight) => {
    console.log('Edit insight:', insight);
    // In a real implementation, this would open an edit modal
  };

  const handleRefreshInsights = () => {
    loadDashboardData();
  };

  const handleActionRecommendation = (recommendation: Recommendation) => {
    console.log('Take action on recommendation:', recommendation);
    
    // Create a more interactive action handling
    const actionMessage = `🎯 Action Initiated: "${recommendation.title}"\n\n📋 Description: ${recommendation.description}\n\n🎯 Expected Impact: ${recommendation.expectedImpact}\n\n⏰ Timeframe: ${recommendation.timeframe}\n💪 Effort Required: ${recommendation.effort}\n🔍 Confidence: ${recommendation.confidence}\n\n📊 Action Type: ${recommendation.actionType}\n\n✅ This action has been logged and will be tracked for implementation.`;
    
    // Show a more detailed alert
    if (confirm(`Are you sure you want to take action on this recommendation?\n\n"${recommendation.title}"\n\nClick OK to proceed or Cancel to abort.`)) {
      alert(actionMessage);
      
      // In a real implementation, you would:
      // 1. Send the action to your backend API
      // 2. Create a task in your project management system
      // 3. Notify relevant team members
      // 4. Update the recommendation status
      // 5. Log the action for audit trail
      
      console.log('Action confirmed and processed:', {
        recommendationId: recommendation.id,
        title: recommendation.title,
        actionType: recommendation.actionType,
        timestamp: new Date().toISOString(),
        status: 'initiated'
      });
      
      // Optional: Show success message
      // You could use a toast notification library here
      console.log('✅ Recommendation action successfully initiated!');
    } else {
      console.log('❌ Action cancelled by user');
    }
  };

  const handleFiltersChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
    // In a real implementation, this would trigger data refetch with filters
  };

  const handleFiltersReset = () => {
    setFilters({
      dateRange: { start: '', end: '' },
      region: 'all',
      product: 'all'
    });
    // In a real implementation, this would reset the data
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'kpi-meaning', label: 'KPI Meaning', icon: Brain },
    { id: 'analytics', label: 'Analytics', icon: Activity },
    { id: 'streamlit', label: 'Streamlit Dashboard', icon: Activity },
    { id: 'insights', label: 'Insights', icon: Target },
    { id: 'health', label: 'Business Health', icon: Shield },
    { id: 'recommendations', label: 'Recommendations', icon: Target },
    { id: 'summary', label: 'Executive Summary', icon: FileText }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (error || !dashboardData) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-lg font-medium mb-4">{error}</div>
          <button
            onClick={loadDashboardData}
            className="flex items-center gap-2 mx-auto px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0 h-auto sm:h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Executive Business Health Dashboard
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              <ThemeToggle />
              <div className="text-sm text-gray-500 dark:text-gray-400">
                Last updated: {new Date(dashboardData.lastUpdated).toLocaleString()}
              </div>
              <button
                onClick={loadDashboardData}
                className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
              >
                <RefreshCw className="w-4 h-4 text-gray-700 dark:text-gray-300" />
                <span className="text-gray-700 dark:text-gray-300">Refresh</span>
              </button>
              <button
                onClick={() => setIsMenuOpen(true)}
                className="lg:hidden flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
                aria-label="Open navigation menu"
              >
                <Menu className="w-5 h-5 text-gray-700 dark:text-gray-300" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="hidden lg:flex gap-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {isMenuOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 z-50 bg-black/40"
          onClick={() => setIsMenuOpen(false)}
        >
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 25 }}
            className="fixed right-0 top-0 h-full w-72 max-w-[85vw] bg-white dark:bg-gray-800 shadow-xl border-l border-gray-200 dark:border-gray-700 p-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Navigation</h2>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-sm text-gray-700 dark:text-gray-300"
              >
                Close
              </button>
            </div>
            <div className="space-y-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => {
                      setActiveTab(tab.id);
                      setIsMenuOpen(false);
                    }}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg border transition-colors ${
                      isActive
                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'
                        : 'border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters Section */}
        <div className="mb-8">
          <InteractiveFilters
            filters={filters}
            onFiltersChange={handleFiltersChange}
            onReset={handleFiltersReset}
          />
        </div>

        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'overview' && (
            <div className="space-y-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                  Business Intelligence Overview
                </h2>
                <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
                  Comprehensive business insights and decision support for executive leadership. 
                  Navigate through each section to understand your business health, risks, and opportunities.
                </p>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                      <BarChart3 className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardData.kpis.length}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">KPIs Tracked</div>
                    </div>
                  </div>
                </div>

                <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg flex items-center justify-center">
                      <Target className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardData.insights.length}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Active Insights</div>
                    </div>
                  </div>
                </div>

                <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center">
                      <Shield className="w-6 h-6 text-red-600 dark:text-red-400" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardData.risks.length}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Risk Indicators</div>
                    </div>
                  </div>
                </div>

                <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                      <Target className="w-6 h-6 text-green-600 dark:text-green-400" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardData.recommendations.length}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Recommendations</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Quick Access Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => setActiveTab('kpi-meaning')}
                >
                  <Brain className="w-8 h-8 text-blue-500 dark:text-blue-400 mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">KPI Meaning</h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    Understand what each metric means for your business and why it matters.
                  </p>
                </motion.div>

                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => setActiveTab('insights')}
                >
                  <Target className="w-8 h-8 text-yellow-500 dark:text-yellow-400 mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Business Insights</h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    Data-driven insights using the What → So What → Now What framework.
                  </p>
                </motion.div>

                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => setActiveTab('summary')}
                >
                  <FileText className="w-8 h-8 text-green-500 dark:text-green-400 mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Executive Summary</h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    One-page summary of business health, risks, and opportunities.
                  </p>
                </motion.div>
              </div>

              {/* Executive KPI Cards */}
              <ExecutiveKPICards kpis={dashboardData.kpis} />
            </div>
          )}

          {activeTab === 'kpi-meaning' && (
            <KPIMeaningLayer kpis={dashboardData.kpis} />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsDashboard kpis={dashboardData.kpis} />
          )}

          {activeTab === 'streamlit' && (
            <StreamlitEmbed 
              streamlitUrl="https://business-health-dashboard-production.up.railway.app"
              height="900px"
              showControls={true}
            />
          )}

          {activeTab === 'insights' && (
            <InsightEngine
              insights={dashboardData.insights}
              kpis={dashboardData.kpis}
              onEditInsight={handleEditInsight}
              onRefreshInsights={handleRefreshInsights}
            />
          )}

          {activeTab === 'health' && (
            <BusinessHealthDashboard
              risks={dashboardData.risks}
              kpis={dashboardData.kpis}
              businessHealthScore={dashboardData.businessHealthScore}
            />
          )}

          {activeTab === 'recommendations' && (
            <ExecutiveRecommendationsPanel
              recommendations={dashboardData.recommendations}
              insights={dashboardData.insights}
              kpis={dashboardData.kpis}
              onAction={handleActionRecommendation}
            />
          )}

          {activeTab === 'summary' && (
            <ExecutiveSummary summary={dashboardData.executiveSummary} />
          )}
        </motion.div>
      </main>
    </div>
  );
};

export default ExecutiveDashboard;
