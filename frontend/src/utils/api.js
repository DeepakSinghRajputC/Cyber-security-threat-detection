import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await api.post('/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

// Prediction API
export const predict = async (features) => {
  const response = await api.post('/predict', { features });
  return response.data;
};

// Retrain API
export const retrain = async (dataPath, epochs = 10) => {
  const response = await api.post('/retrain', { 
    data_path: dataPath, 
    epochs 
  });
  return response.data;
};

// Upload API
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Metrics API
export const getMetrics = async () => {
  const response = await api.get('/metrics');
  return response.data;
};

// Health check API
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
