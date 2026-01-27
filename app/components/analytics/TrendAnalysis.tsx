'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { TrendingUp, Calendar, BarChart3, Activity, ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface TrendAnalysisProps {
  className?: string;
}

// Mock time-series data for trend analysis
const monthlyData = [
  { month: 'Jan', revenue: 820000, profit: 115000, customers: 8500, growth: 12.5 },
  { month: 'Feb', revenue: 845000, profit: 121000, customers: 8720, growth: 14.2 },
  { month: 'Mar', revenue: 890000, profit: 128000, customers: 9150, growth: 16.8 },
  { month: 'Apr', revenue: 910000, profit: 132000, customers: 9380, growth: 15.3 },
  { month: 'May', revenue: 920000, profit: 135000, customers: 9620, growth: 13.7 },
  { month: 'Jun', revenue: 895000, profit: 129000, customers: 9450, growth: 11.2 },
  { month: 'Jul', revenue: 880000, profit: 125000, customers: 9280, growth: 9.8 },
  { month: 'Aug', revenue: 865000, profit: 122000, customers: 9120, growth: 8.4 },
  { month: 'Sep', revenue: 850000, profit: 118000, customers: 8950, growth: 7.1 },
  { month: 'Oct', revenue: 840000, profit: 115000, customers: 8780, growth: 5.6 },
  { month: 'Nov', revenue: 835000, profit: 112000, customers: 8620, growth: 4.2 },
  { month: 'Dec', revenue: 850000, profit: 119000, customers: 8750, growth: 8.5 }
];

const TrendAnalysis: React.FC<TrendAnalysisProps> = ({ className = '' }) => {
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

  // Calculate MoM growth rates
  const calculateMoMGrowth = (data: number[]) => {
    return data.slice(1).map((value, index) => {
      const previousValue = data[index];
      return ((value - previousValue) / previousValue * 100).toFixed(1);
    });
  };

  const revenueGrowth = calculateMoMGrowth(monthlyData.map(d => d.revenue));
  const profitGrowth = calculateMoMGrowth(monthlyData.map(d => d.profit));
  const customerGrowth = calculateMoMGrowth(monthlyData.map(d => d.customers));

  // Create growth data for chart
  const growthData = monthlyData.slice(1).map((data, index) => ({
    month: data.month,
    revenueGrowth: parseFloat(revenueGrowth[index]),
    profitGrowth: parseFloat(profitGrowth[index]),
    customerGrowth: parseFloat(customerGrowth[index])
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900 dark:text-white mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(1)}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const ValueTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900 dark:text-white mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: ${entry.value.toLocaleString()}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const getGrowthIcon = (growth: number) => {
    if (growth > 0) return <ArrowUpRight className="w-4 h-4 text-green-600 dark:text-green-400" />;
    if (growth < 0) return <ArrowDownRight className="w-4 h-4 text-red-600 dark:text-red-400" />;
    return <div className="w-4 h-4 bg-gray-400 rounded-full" />;
  };

  const getGrowthColor = (growth: number) => {
    if (growth > 10) return 'text-green-600 dark:text-green-400';
    if (growth > 5) return 'text-blue-600 dark:text-blue-400';
    if (growth > 0) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  // Calculate current month performance
  const currentMonth = monthlyData[monthlyData.length - 1];
  const previousMonth = monthlyData[monthlyData.length - 2];
  const currentMoMGrowth = ((currentMonth.revenue - previousMonth.revenue) / previousMonth.revenue * 100);

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-3">
          <Calendar className="w-8 h-8 text-green-600 dark:text-green-400" />
          Time-Based Trend Analysis
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Month-over-Month growth analysis and trend identification for strategic planning.
        </p>
      </motion.div>

      {/* Current Month Summary */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-4 gap-4"
      >
        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <BarChart3 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                ${currentMonth.revenue.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Current Revenue</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getGrowthIcon(currentMoMGrowth)}
            <span className={`text-sm font-medium ${getGrowthColor(currentMoMGrowth)}`}>
              {currentMoMGrowth.toFixed(1)}% MoM
            </span>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                ${currentMonth.profit.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Current Profit</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getGrowthIcon(((currentMonth.profit - previousMonth.profit) / previousMonth.profit * 100))}
            <span className={`text-sm font-medium ${getGrowthColor(((currentMonth.profit - previousMonth.profit) / previousMonth.profit * 100))}`}>
              {(((currentMonth.profit - previousMonth.profit) / previousMonth.profit * 100)).toFixed(1)}% MoM
            </span>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
              <Activity className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentMonth.customers.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Active Customers</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getGrowthIcon(((currentMonth.customers - previousMonth.customers) / previousMonth.customers * 100))}
            <span className={`text-sm font-medium ${getGrowthColor(((currentMonth.customers - previousMonth.customers) / previousMonth.customers * 100))}`}>
              {(((currentMonth.customers - previousMonth.customers) / previousMonth.customers * 100)).toFixed(1)}% MoM
            </span>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
              <Calendar className="w-5 h-5 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentMonth.growth.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Growth Rate</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getGrowthIcon(currentMonth.growth - previousMonth.growth)}
            <span className={`text-sm font-medium ${getGrowthColor(currentMonth.growth - previousMonth.growth)}`}>
              {(currentMonth.growth - previousMonth.growth).toFixed(1)}% pts
            </span>
          </div>
        </motion.div>
      </motion.div>

      {/* Trend Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Revenue & Profit Trend */}
        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Revenue & Profit Trends
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={monthlyData}>
              <defs>
                <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="profitGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.1}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" strokeOpacity={0.5} />
              <XAxis 
                dataKey="month" 
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6b7280', fontSize: 12 }}
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6b7280', fontSize: 12 }}
                tickFormatter={(value) => `$${(value/1000).toFixed(0)}k`}
              />
              <Tooltip content={<ValueTooltip />} />
              <Legend />
              <Area
                type="monotone"
                dataKey="revenue"
                stroke="#3b82f6"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#revenueGradient)"
                animationDuration={1500}
              />
              <Area
                type="monotone"
                dataKey="profit"
                stroke="#10b981"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#profitGradient)"
                animationDuration={1500}
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* MoM Growth Rates */}
        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Month-over-Month Growth Rates
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={growthData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" strokeOpacity={0.5} />
              <XAxis 
                dataKey="month" 
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6b7280', fontSize: 12 }}
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6b7280', fontSize: 12 }}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line
                type="monotone"
                dataKey="revenueGrowth"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ fill: '#3b82f6', r: 4 }}
                animationDuration={1500}
              />
              <Line
                type="monotone"
                dataKey="profitGrowth"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ fill: '#10b981', r: 4 }}
                animationDuration={1500}
              />
              <Line
                type="monotone"
                dataKey="customerGrowth"
                stroke="#8b5cf6"
                strokeWidth={2}
                dot={{ fill: '#8b5cf6', r: 4 }}
                animationDuration={1500}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Trend Insights */}
      <motion.div
        variants={itemVariants}
        className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6"
      >
        <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-4">
          Trend Analysis Insights
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Revenue Trend</h4>
            <p className="text-blue-700 dark:text-blue-300">
              Revenue peaked in May ($920K) then declined through October, showing recent recovery in December.
              Current growth rate of 8.5% indicates positive momentum.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Profit Margin Analysis</h4>
            <p className="text-blue-700 dark:text-blue-300">
              Profit margins remained stable around 14-15% despite revenue fluctuations, indicating good cost control.
              Recent improvement in December suggests operational efficiency gains.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Customer Growth</h4>
            <p className="text-blue-700 dark:text-blue-300">
              Customer growth slowed from peak 16.8% in March to current 8.5%, suggesting market maturation.
              Focus shifting from acquisition to retention and expansion.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Seasonal Patterns</h4>
            <p className="text-blue-700 dark:text-blue-300">
              Clear seasonal pattern with Q1 strength, mid-year softness, and Q4 recovery.
              Planning should account for these predictable fluctuations.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default TrendAnalysis;
