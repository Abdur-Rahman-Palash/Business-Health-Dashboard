'use client';

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { KPIData } from '@/types/business';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';

interface TrendChartProps {
  kpi: KPIData;
  height?: number;
  showGrid?: boolean;
  color?: string;
}

const TrendChart: React.FC<TrendChartProps> = ({
  kpi,
  height = 300,
  showGrid = true,
  color
}) => {
  const definition = getKPIDefinition(kpi.id);
  
  // Determine color based on health status if not provided
  const getHealthColor = () => {
    if (color) return color;
    switch (kpi.healthStatus) {
      case 'excellent': return '#16a34a'; // green-600
      case 'good': return '#2563eb'; // blue-600
      case 'warning': return '#ca8a04'; // yellow-600
      case 'critical': return '#dc2626'; // red-600
      default: return '#4b5563'; // gray-600
    }
  };

  const chartColor = getHealthColor();

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900">{label}</p>
          <p className="text-sm font-bold" style={{ color: chartColor }}>
            {payload[0].value.toLocaleString()} {definition.unit}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={kpi.historicalValues}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id={`colorGradient-${kpi.id}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={chartColor} stopOpacity={0.1}/>
              <stop offset="95%" stopColor={chartColor} stopOpacity={0}/>
            </linearGradient>
          </defs>
          {showGrid && <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />}
          <XAxis 
            dataKey="period" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            dy={10}
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={(value) => 
              definition.unit === 'USD' 
                ? `$${value >= 1000 ? `${(value/1000).toFixed(0)}k` : value}`
                : `${value}${definition.unit === '%' ? '%' : ''}`
            }
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="value"
            stroke={chartColor}
            strokeWidth={2}
            fillOpacity={1}
            fill={`url(#colorGradient-${kpi.id})`}
            animationDuration={1500}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendChart;
