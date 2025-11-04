import React, { useState, useEffect } from 'react';
import { Shield, LogOut, Upload, RefreshCw, Activity } from 'lucide-react';
import MetricsGrid from '../components/MetricsGrid';
import AlertsList from '../components/AlertsList';
import ModelChart from '../components/ModelChart';
import { getMetrics, uploadFile, retrain } from '../utils/api';

function Dashboard({ username, onLogout }) {
  const [metrics, setMetrics] = useState({
    total_predictions: 0,
    anomaly_count: 0,
    anomaly_rate: 0,
    avg_confidence: 0,
    model_loaded: false
  });
  
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [retrainStatus, setRetrainStatus] = useState('');

  // Load metrics on mount
  useEffect(() => {
    loadMetrics();
    generateMockAlerts();
    generateChartData();
  }, []);

  const loadMetrics = async () => {
    try {
      const data = await getMetrics();
      setMetrics(data);
    } catch (err) {
      console.error('Failed to load metrics:', err);
    }
  };

  const generateMockAlerts = () => {
    // Generate some mock alerts for demonstration
    const mockAlerts = [
      {
        type: 'Port Scan Detected',
        description: 'Multiple connection attempts to different ports from 192.168.1.100',
        score: 0.85,
        confidence: 0.92,
        timestamp: new Date(Date.now() - 300000).toLocaleString()
      },
      {
        type: 'Unusual Traffic Pattern',
        description: 'High volume of traffic to uncommon destination port',
        score: 0.72,
        confidence: 0.78,
        timestamp: new Date(Date.now() - 600000).toLocaleString()
      },
      {
        type: 'Suspicious Protocol Usage',
        description: 'ICMP traffic with unusual TTL values',
        score: 0.68,
        confidence: 0.85,
        timestamp: new Date(Date.now() - 900000).toLocaleString()
      },
      {
        type: 'Normal Traffic',
        description: 'Standard HTTP/HTTPS traffic pattern',
        score: 0.15,
        confidence: 0.95,
        timestamp: new Date(Date.now() - 1200000).toLocaleString()
      }
    ];
    setAlerts(mockAlerts);
  };

  const generateChartData = () => {
    // Generate mock chart data
    const data = [];
    for (let i = 0; i < 10; i++) {
      data.push({
        name: `T-${i}`,
        transformer: Math.random() * 0.3 + 0.1,
        isolation: Math.random() * 0.4 + 0.1,
        fused: Math.random() * 0.35 + 0.1
      });
    }
    setChartData(data);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setUploadStatus('Uploading...');
    
    try {
      const result = await uploadFile(file);
      setUploadStatus(`✓ File uploaded: ${result.data_points} data points`);
      setTimeout(() => setUploadStatus(''), 3000);
    } catch (err) {
      setUploadStatus(`✗ Upload failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRetrain = async () => {
    setLoading(true);
    setRetrainStatus('Retraining model...');
    
    try {
      const result = await retrain('../demo_data/sample_traffic.csv', 5);
      setRetrainStatus(`✓ Model retrained with ${result.data_points} samples`);
      loadMetrics();
      setTimeout(() => setRetrainStatus(''), 5000);
    } catch (err) {
      setRetrainStatus(`✗ Retrain failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-blue-400 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-white">
                  Cybersecurity Threat Detection
                </h1>
                <p className="text-sm text-gray-400">
                  AI-Powered Network Anomaly Detection
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300">Welcome, {username}</span>
              <button
                onClick={onLogout}
                className="flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Action Bar */}
        <div className="mb-6 flex items-center space-x-4">
          <label className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md cursor-pointer transition-colors">
            <Upload className="w-4 h-4 mr-2" />
            Upload Data
            <input
              type="file"
              onChange={handleFileUpload}
              accept=".csv,.pcap"
              className="hidden"
              disabled={loading}
            />
          </label>
          
          <button
            onClick={handleRetrain}
            disabled={loading}
            className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Retrain Model
          </button>

          <div className="flex-1" />
          
          <div className={`px-4 py-2 rounded-md ${
            metrics.model_loaded ? 'bg-green-500/20 text-green-300' : 'bg-yellow-500/20 text-yellow-300'
          }`}>
            <Activity className="w-4 h-4 inline mr-2" />
            {metrics.model_loaded ? 'Model Loaded' : 'Model Not Loaded'}
          </div>
        </div>

        {/* Status Messages */}
        {uploadStatus && (
          <div className="mb-4 p-3 bg-blue-500/20 border border-blue-500 rounded-md text-blue-300">
            {uploadStatus}
          </div>
        )}
        
        {retrainStatus && (
          <div className="mb-4 p-3 bg-green-500/20 border border-green-500 rounded-md text-green-300">
            {retrainStatus}
          </div>
        )}

        {/* Metrics Grid */}
        <MetricsGrid metrics={metrics} />

        {/* Charts and Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ModelChart 
            data={chartData} 
            title="Model Score Comparison"
            type="line"
          />
          <AlertsList alerts={alerts} />
        </div>

        {/* Additional Info */}
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
          <h2 className="text-xl font-bold text-white mb-4">System Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-gray-400">Model Type</p>
              <p className="text-white font-semibold">Transformer + IsolationForest</p>
            </div>
            <div>
              <p className="text-gray-400">Feature Dimensions</p>
              <p className="text-white font-semibold">7 features</p>
            </div>
            <div>
              <p className="text-gray-400">Fusion Strategy</p>
              <p className="text-white font-semibold">Weighted Average (0.5)</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
