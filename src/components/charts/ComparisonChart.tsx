'use client';

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { KPIData } from '@/types/business';
import { getKPIDefinition } from '@/lib/business-logic/kpi-definitions';

interface ComparisonChartProps {
  kpis: KPIData[];
  height?: number;
  showGrid?: boolean;
  compareMetric?: 'current' | 'previous' | 'target';
}

const ComparisonChart: React.FC<ComparisonChartProps> = ({
  kpis,
  height = 400,
  showGrid = true,
  compareMetric = 'current'
}) => {
  // Prepare data for comparison chart
  const chartData = kpis.map(kpi => {
    const definition = getKPIDefinition(kpi.id);
    return {
      name: definition.name,
      current: kpi.currentValue,
      previous: kpi.previousValue,
      target: kpi.targetValue,
      unit: definition.unit
    };
  });

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900 dark:text-white mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toLocaleString()} {data.unit}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const formatYAxis = (value: number, unit: string) => {
    if (unit === 'USD') {
      return `$${value >= 1000000 ? `${(value/1000000).toFixed(1)}M` : value >= 1000 ? `${(value/1000).toFixed(0)}k` : value}`;
    }
    return `${value}${unit === '%' ? '%' : ''}`;
  };

  return (
    <div className="w-full" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          {showGrid && <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" strokeOpacity={0.5} />}
          <XAxis 
            dataKey="name" 
            angle={-45}
            textAnchor="end"
            height={100}
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 11 }}
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={(value) => formatYAxis(value, chartData[0]?.unit || '')}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="rect"
          />
          
          {compareMetric === 'current' && (
            <Bar 
              dataKey="current" 
              fill="#2563eb" 
              name="Current Value"
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            />
          )}
          
          {compareMetric === 'previous' && (
            <Bar 
              dataKey="previous" 
              fill="#64748b" 
              name="Previous Value"
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            />
          )}
          
          {compareMetric === 'target' && (
            <Bar 
              dataKey="target" 
              fill="#10b981" 
              name="Target Value"
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            />
          )}

          {/* Show all bars when no specific metric is selected */}
          {!compareMetric && (
            <>
              <Bar 
                dataKey="current" 
                fill="#2563eb" 
                name="Current Value"
                radius={[4, 4, 0, 0]}
                animationDuration={1500}
              />
              <Bar 
                dataKey="previous" 
                fill="#64748b" 
                name="Previous Value"
                radius={[4, 4, 0, 0]}
                animationDuration={1500}
              />
              <Bar 
                dataKey="target" 
                fill="#10b981" 
                name="Target Value"
                radius={[4, 4, 0, 0]}
                animationDuration={1500}
              />
            </>
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ComparisonChart;
