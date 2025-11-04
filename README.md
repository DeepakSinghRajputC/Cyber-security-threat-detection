# AI-Based Cybersecurity Threat Detection System

A full-stack application for detecting anomalies in network traffic using advanced machine learning techniques including Transformer models and IsolationForest algorithms.

## 🚀 Features

- **Data Ingestion & Preprocessing**: Support for both CSV and PCAP file formats
- **PCAP-to-CSV Converter**: Extract network features from packet captures
- **Hybrid ML Model**: Combines Transformer neural networks with IsolationForest for robust anomaly detection
- **Feature Encoding**: Advanced feature engineering and normalization
- **Anomaly Score Fusion**: Intelligent fusion of multiple model predictions
- **FastAPI Backend**: RESTful API with JWT-based RBAC (Role-Based Access Control)
- **React Dashboard**: Modern, responsive UI with real-time metrics visualization
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 📊 System Architecture

```
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── auth.py      # JWT authentication & RBAC
│   │   ├── model.py     # Transformer + IsolationForest models
│   │   ├── data_ingestion.py  # PCAP converter & preprocessing
│   │   ├── feature_encoder.py # Feature encoding utilities
│   ├── main.py          # FastAPI application entry point
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend Docker configuration
├── frontend/            # React + Tailwind dashboard
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Dashboard page
│   │   └── utils/       # API client utilities
│   ├── package.json     # Node.js dependencies
│   └── Dockerfile       # Frontend Docker configuration
├── demo_data/           # Sample network traffic data
└── docker-compose.yml   # Docker Compose configuration
```

## 🛠️ Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/DeepakSinghRajputC/Cyber-security-threat-detection.git
cd Cyber-security-threat-detection
```

2. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Manual Installation

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Generate demo data**
```bash
python generate_demo_data.py
```

6. **Run the backend server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

4. **Access the dashboard**
Open http://localhost:3000 in your browser

## 🔐 Authentication

The system uses JWT-based authentication with three predefined roles:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin | admin123 | admin | read, write, retrain |
| analyst | analyst123 | analyst | read, write |
| viewer | viewer123 | viewer | read |

## 📡 API Endpoints

### Authentication
- `POST /token` - Login and get access token

### Predictions
- `POST /predict` - Predict anomalies in network traffic
- `GET /metrics` - Get model performance metrics

### Model Management
- `POST /retrain` - Retrain the model with new data (admin only)
- `POST /upload` - Upload network traffic data (CSV or PCAP)

### Health
- `GET /health` - Health check endpoint
- `GET /` - API information

## 🎯 Usage

### 1. Login to the Dashboard
- Navigate to http://localhost:3000
- Use one of the demo credentials to login

### 2. Upload Network Traffic Data
- Click "Upload Data" button
- Select a CSV or PCAP file
- The system will automatically process and display the data

### 3. Retrain the Model
- Click "Retrain Model" button (admin only)
- The system will train using the demo data
- View training progress and results

### 4. View Anomaly Detections
- Dashboard displays real-time metrics
- View recent alerts with severity levels
- Analyze model confidence scores
- Compare Transformer and IsolationForest predictions

## 🧪 Model Details

### Transformer Model
- **Architecture**: Multi-head attention with encoder layers
- **Input**: 7 network traffic features
- **Output**: Anomaly score (0-1)
- **Training**: Self-supervised with MSE loss

### IsolationForest Model
- **Algorithm**: Tree-based ensemble method
- **Contamination**: 10% (configurable)
- **Estimators**: 100 trees
- **Output**: Anomaly score (0-1)

### Score Fusion
- **Method**: Weighted average
- **Default Weight**: 0.5 (equal weight to both models)
- **Threshold**: 0.5 for anomaly classification

### Network Features
1. Protocol (TCP, UDP, ICMP)
2. Packet Length
3. Time-To-Live (TTL)
4. TCP Flags
5. Source Port
6. Destination Port
7. Time Delta

## 📊 Demo Data

The repository includes pre-generated demo data with:
- **1000 samples** (900 normal, 100 anomalous)
- **Normal traffic**: Standard HTTP/HTTPS patterns
- **Anomalous traffic**: Port scans, unusual protocols, extreme packet sizes

Generate new demo data:
```bash
cd backend
python generate_demo_data.py
```

## 🔧 Configuration

### Backend Environment Variables
```env
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MODEL_PATH=./models/trained_model.pkl
DATA_PATH=./data/network_traffic.csv
HOST=0.0.0.0
PORT=8000
```

### Frontend Environment Variables
```env
VITE_API_URL=http://localhost:8000
```

## 🐳 Docker Commands

```bash
# Build and start services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

## 📈 Monitoring & Metrics

The dashboard displays:
- **Total Predictions**: Number of traffic samples analyzed
- **Anomalies Detected**: Count of identified threats
- **Anomaly Rate**: Percentage of anomalous traffic
- **Average Confidence**: Model confidence scores
- **Model Score Comparison**: Real-time chart of model predictions
- **Recent Alerts**: Detailed threat information with severity levels

## 🧩 Extension Points

- Add more sophisticated feature engineering
- Integrate with real-time network monitoring tools
- Implement model versioning and A/B testing
- Add database persistence for predictions and metrics
- Create automated alert notifications
- Integrate with SIEM systems
- Add more ML models (AutoEncoder, LSTM, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👥 Authors

- Deepak Singh Rajput

## 🙏 Acknowledgments

- PyTorch for deep learning framework
- scikit-learn for machine learning utilities
- FastAPI for modern API development
- React and Tailwind CSS for frontend development
- Scapy for packet processing

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a boilerplate/demo application. For production use, implement additional security measures, use a real database, and configure proper authentication mechanisms.
