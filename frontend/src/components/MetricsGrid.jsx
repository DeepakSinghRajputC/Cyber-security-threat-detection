import React from 'react';
import { Activity, Shield, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';

function MetricsCard({ title, value, icon: Icon, trend, color = 'blue' }) {
  const colorClasses = {
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    red: 'bg-red-500/10 text-red-400 border-red-500/20',
    green: 'bg-green-500/10 text-green-400 border-green-500/20',
    yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  };

  return (
    <div className={`p-6 rounded-lg border ${colorClasses[color]}`}>
      <div className="flex items-center justify-between mb-2">
        <Icon className="w-8 h-8" />
        {trend && (
          <span className={`text-sm flex items-center ${trend > 0 ? 'text-red-400' : 'text-green-400'}`}>
            <TrendingUp className="w-4 h-4 mr-1" />
            {Math.abs(trend)}%
          </span>
        )}
      </div>
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-sm text-gray-400 mt-1">{title}</p>
    </div>
  );
}

function MetricsGrid({ metrics }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <MetricsCard
        title="Total Predictions"
        value={metrics.total_predictions.toLocaleString()}
        icon={Activity}
        color="blue"
      />
      <MetricsCard
        title="Anomalies Detected"
        value={metrics.anomaly_count}
        icon={AlertTriangle}
        color="red"
        trend={8.5}
      />
      <MetricsCard
        title="Anomaly Rate"
        value={`${(metrics.anomaly_rate * 100).toFixed(1)}%`}
        icon={Shield}
        color="yellow"
      />
      <MetricsCard
        title="Avg Confidence"
        value={`${(metrics.avg_confidence * 100).toFixed(1)}%`}
        icon={CheckCircle}
        color="green"
      />
    </div>
  );
}

export default MetricsGrid;
