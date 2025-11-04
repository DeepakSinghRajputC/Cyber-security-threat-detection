import React from 'react';
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react';

function AlertsList({ alerts }) {
  const getSeverityColor = (score) => {
    if (score > 0.8) return 'border-red-500 bg-red-500/10';
    if (score > 0.6) return 'border-yellow-500 bg-yellow-500/10';
    return 'border-green-500 bg-green-500/10';
  };

  const getSeverityIcon = (score) => {
    if (score > 0.6) return <AlertTriangle className="w-5 h-5 text-red-400" />;
    return <CheckCircle className="w-5 h-5 text-green-400" />;
  };

  const getSeverityLabel = (score) => {
    if (score > 0.8) return 'Critical';
    if (score > 0.6) return 'High';
    if (score > 0.4) return 'Medium';
    return 'Low';
  };

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-xl font-bold text-white mb-4 flex items-center">
        <AlertTriangle className="w-6 h-6 mr-2 text-red-400" />
        Recent Alerts
      </h2>
      
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {alerts.length === 0 ? (
          <p className="text-gray-400 text-center py-8">No alerts to display</p>
        ) : (
          alerts.map((alert, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-lg border ${getSeverityColor(alert.score)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  {getSeverityIcon(alert.score)}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-white">
                        {alert.type || 'Anomaly Detected'}
                      </h3>
                      <span className={`text-sm px-2 py-1 rounded ${
                        alert.score > 0.8 ? 'bg-red-500/20 text-red-300' :
                        alert.score > 0.6 ? 'bg-yellow-500/20 text-yellow-300' :
                        'bg-green-500/20 text-green-300'
                      }`}>
                        {getSeverityLabel(alert.score)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-400 mt-1">
                      {alert.description || `Anomaly score: ${alert.score.toFixed(3)}`}
                    </p>
                    <div className="flex items-center mt-2 text-xs text-gray-500">
                      <Clock className="w-3 h-3 mr-1" />
                      {alert.timestamp || new Date().toLocaleString()}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                <div className="bg-slate-700/50 p-2 rounded">
                  <span className="text-gray-400">Confidence:</span>
                  <span className="text-white ml-2 font-semibold">
                    {(alert.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="bg-slate-700/50 p-2 rounded">
                  <span className="text-gray-400">Score:</span>
                  <span className="text-white ml-2 font-semibold">
                    {alert.score.toFixed(3)}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AlertsList;
