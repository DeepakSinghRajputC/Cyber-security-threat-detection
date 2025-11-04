import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity } from 'lucide-react';

function ModelChart({ data, title, type = 'line' }) {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-xl font-bold text-white mb-4 flex items-center">
        <Activity className="w-6 h-6 mr-2 text-blue-400" />
        {title}
      </h2>
      
      <ResponsiveContainer width="100%" height={300}>
        {type === 'line' ? (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: '1px solid #475569',
                borderRadius: '0.5rem'
              }}
            />
            <Legend />
            <Line type="monotone" dataKey="transformer" stroke="#3b82f6" strokeWidth={2} />
            <Line type="monotone" dataKey="isolation" stroke="#10b981" strokeWidth={2} />
            <Line type="monotone" dataKey="fused" stroke="#f59e0b" strokeWidth={2} />
          </LineChart>
        ) : (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: '1px solid #475569',
                borderRadius: '0.5rem'
              }}
            />
            <Legend />
            <Bar dataKey="value" fill="#3b82f6" />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}

export default ModelChart;
