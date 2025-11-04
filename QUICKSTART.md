# Quick Start Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

## Quick Start with Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/DeepakSinghRajputC/Cyber-security-threat-detection.git
cd Cyber-security-threat-detection

# 2. Start the services
docker-compose up --build

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Manual Setup

### Backend

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Access at http://localhost:3000
```

## Login Credentials

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin | admin123 | Admin | Full access |
| analyst | analyst123 | Analyst | Read, Write |
| viewer | viewer123 | Viewer | Read only |

## API Usage

### Get Access Token
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Predict Anomalies
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[6, 500, 64, 2, 1024, 443, 0.1]]
  }'
```

### Retrain Model (Admin only)
```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data_path": "../demo_data/sample_traffic.csv",
    "epochs": 10
  }'
```

### Upload Data
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/your/file.csv"
```

## Features

### Data Processing
- **PCAP to CSV conversion**: Automatically extract network features
- **Feature encoding**: Normalize and encode network traffic data
- **Preprocessing**: Handle missing values and outliers

### Machine Learning
- **Transformer Model**: Neural network with attention mechanism
- **IsolationForest**: Tree-based anomaly detection
- **Score Fusion**: Combine predictions for better accuracy
- **Confidence Scores**: Measure prediction reliability

### Dashboard
- **Real-time Metrics**: View system statistics
- **Alert Management**: Monitor detected threats
- **Model Comparison**: Compare Transformer vs IsolationForest
- **Visualizations**: Interactive charts with Recharts

### Security
- **JWT Authentication**: Secure token-based auth
- **RBAC**: Role-based access control
- **Password Hashing**: Bcrypt for secure storage

## Troubleshooting

### Backend Issues
```bash
# Check if port 8000 is available
lsof -i :8000

# View backend logs
cd backend
uvicorn main:app --log-level debug
```

### Frontend Issues
```bash
# Check if port 3000 is available
lsof -i :3000

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Build for production
npm run build
```

### Docker Issues
```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Next Steps

1. **Upload Your Data**: Use real network traffic data
2. **Train the Model**: Retrain with your specific data
3. **Monitor Alerts**: Set up automated notifications
4. **Customize**: Adjust thresholds and parameters
5. **Integrate**: Connect with your existing security tools

## Support

For issues and questions:
- GitHub Issues: https://github.com/DeepakSinghRajputC/Cyber-security-threat-detection/issues
- Documentation: See README.md

## License

MIT License - See LICENSE file for details
