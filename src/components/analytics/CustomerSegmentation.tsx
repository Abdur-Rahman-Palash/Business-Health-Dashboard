'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Users, TrendingUp, DollarSign, AlertTriangle, Star } from 'lucide-react';

interface CustomerSegmentationProps {
  className?: string;
}

// Mock customer segmentation data
const customerSegments = [
  {
    name: 'High-Value',
    value: 25,
    revenue: 450000,
    count: 1250,
    growth: 15,
    color: '#10b981',
    description: 'Top 20% of customers by revenue'
  },
  {
    name: 'At-Risk',
    value: 20,
    revenue: 180000,
    count: 2100,
    growth: -8,
    color: '#ef4444',
    description: 'Declining engagement or satisfaction'
  },
  {
    name: 'Growing',
    value: 30,
    revenue: 320000,
    count: 3400,
    growth: 22,
    color: '#3b82f6',
    description: 'Increasing revenue and engagement'
  },
  {
    name: 'Stable',
    value: 15,
    revenue: 150000,
    count: 1800,
    growth: 3,
    color: '#6b7280',
    description: 'Consistent but not growing'
  },
  {
    name: 'New',
    value: 10,
    revenue: 80000,
    count: 2500,
    growth: 45,
    color: '#8b5cf6',
    description: 'Acquired in last 6 months'
  }
];

const CustomerSegmentation: React.FC<CustomerSegmentationProps> = ({ className = '' }) => {
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

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900 dark:text-white mb-2">{data.name}</p>
          <div className="space-y-1 text-sm">
            <p className="text-gray-600 dark:text-gray-400">
              Customers: {data.count.toLocaleString()}
            </p>
            <p className="text-gray-600 dark:text-gray-400">
              Revenue: ${data.revenue.toLocaleString()}
            </p>
            <p className="text-gray-600 dark:text-gray-400">
              Growth: {data.growth}%
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  const getSegmentIcon = (segmentName: string) => {
    switch (segmentName) {
      case 'High-Value':
        return <Star className="w-5 h-5 text-green-600 dark:text-green-400" />;
      case 'At-Risk':
        return <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />;
      case 'Growing':
        return <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />;
      case 'Stable':
        return <Users className="w-5 h-5 text-gray-600 dark:text-gray-400" />;
      case 'New':
        return <DollarSign className="w-5 h-5 text-purple-600 dark:text-purple-400" />;
      default:
        return <Users className="w-5 h-5 text-gray-600 dark:text-gray-400" />;
    }
  };

  const getGrowthColor = (growth: number) => {
    if (growth > 10) return 'text-green-600 dark:text-green-400';
    if (growth > 0) return 'text-blue-600 dark:text-blue-400';
    if (growth > -5) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-3">
          <Users className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          Customer Segmentation Analysis
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Understanding customer value distribution and growth patterns for strategic decision-making.
        </p>
      </motion.div>

      {/* Overview Cards */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-3 gap-4"
      >
        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <Users className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {customerSegments.reduce((sum, seg) => sum + seg.count, 0).toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Total Customers</div>
            </div>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <DollarSign className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                ${customerSegments.reduce((sum, seg) => sum + seg.revenue, 0).toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Total Revenue</div>
            </div>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
              <TrendingUp className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {(customerSegments.reduce((sum, seg) => sum + seg.growth * seg.value, 0) / 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Weighted Growth</div>
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Pie Chart */}
        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Customer Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={customerSegments}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                animationDuration={1500}
              >
                {customerSegments.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Bar Chart */}
        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Revenue by Segment
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={customerSegments}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" strokeOpacity={0.5} />
              <XAxis 
                dataKey="name" 
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6b7280', fontSize: 11 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6b7280', fontSize: 12 }}
                tickFormatter={(value) => `$${(value/1000).toFixed(0)}k`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="revenue" 
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
                animationDuration={1500}
              />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Detailed Segment Analysis */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="space-y-4"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Segment Analysis</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {customerSegments.map((segment, index) => (
            <motion.div
              key={segment.name}
              variants={itemVariants}
              className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  {getSegmentIcon(segment.name)}
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white">
                      {segment.name}
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {segment.description}
                    </p>
                  </div>
                </div>
                <div 
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: segment.color }}
                />
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Customers</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {segment.count.toLocaleString()}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Revenue</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    ${segment.revenue.toLocaleString()}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Growth</span>
                  <span className={`font-medium ${getGrowthColor(segment.growth)}`}>
                    {segment.growth > 0 ? '+' : ''}{segment.growth}%
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Share</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {segment.value}%
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-4">
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className="h-2 rounded-full transition-all duration-500"
                    style={{ 
                      width: `${segment.value}%`,
                      backgroundColor: segment.color
                    }}
                  />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Strategic Insights */}
      <motion.div
        variants={itemVariants}
        className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6"
      >
        <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-4">
          Strategic Insights
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">High-Value Focus</h4>
            <p className="text-blue-700 dark:text-blue-300">
              25% of customers generate 56% of revenue. Prioritize retention and expansion programs.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">At-Risk Intervention</h4>
            <p className="text-blue-700 dark:text-blue-300">
              20% showing decline requires immediate customer success intervention.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Growth Opportunity</h4>
            <p className="text-blue-700 dark:text-blue-300">
              Growing segment (30%) shows highest potential for upsell and expansion.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">New Customer Pipeline</h4>
            <p className="text-blue-700 dark:text-blue-300">
              New customers (10%) show 45% growth rate - focus on onboarding success.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default CustomerSegmentation;
