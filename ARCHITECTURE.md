# System Architecture

## Overview
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                              │
├─────────────────────────────────────────────────────────────────────────┤
│  React Dashboard (Port 3000)                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │   Login      │  │  Metrics     │  │   Alerts     │                  │
│  │  Component   │  │   Grid       │  │    List      │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│  ┌──────────────┐  ┌──────────────┐                                    │
│  │  Model Chart │  │   Upload     │                                    │
│  │              │  │   Control    │                                    │
│  └──────────────┘  └──────────────┘                                    │
└─────────────────────────────────────────────────────────────────────────┘
                              ↕ HTTPS/REST API
┌─────────────────────────────────────────────────────────────────────────┐
│                        API Layer (FastAPI)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  Port 8000                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │ /token       │  │  /predict    │  │  /retrain    │                  │
│  │ (Auth)       │  │  (Predict)   │  │  (Admin)     │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │  /upload     │  │  /metrics    │  │  /health     │                  │
│  │  (Upload)    │  │  (Stats)     │  │  (Status)    │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│                                                                          │
│  Middleware:                                                            │
│  ├─ CORS                                                                │
│  ├─ JWT Authentication                                                  │
│  └─ RBAC (Role-Based Access Control)                                   │
└─────────────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                                │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐    ┌─────────────────────┐                    │
│  │   Auth Module       │    │  Data Ingestion     │                    │
│  ├─────────────────────┤    ├─────────────────────┤                    │
│  │ - JWT Token Gen     │    │ - PCAP Converter    │                    │
│  │ - Password Hash     │    │ - CSV Parser        │                    │
│  │ - User Management   │    │ - Preprocessing     │                    │
│  │ - Permission Check  │    │ - Validation        │                    │
│  └─────────────────────┘    └─────────────────────┘                    │
│                                                                          │
│  ┌─────────────────────┐    ┌─────────────────────┐                    │
│  │  Feature Encoder    │    │   Model Manager     │                    │
│  ├─────────────────────┤    ├─────────────────────┤                    │
│  │ - Label Encoding    │    │ - Model Loading     │                    │
│  │ - Normalization     │    │ - Model Saving      │                    │
│  │ - Scaling           │    │ - Version Control   │                    │
│  └─────────────────────┘    └─────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────────────┐
│                      Machine Learning Layer                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │            Hybrid Anomaly Detection Model                    │        │
│  ├─────────────────────────────────────────────────────────────┤        │
│  │                                                              │        │
│  │  ┌──────────────────────┐    ┌──────────────────────┐      │        │
│  │  │  Transformer Model   │    │  IsolationForest     │      │        │
│  │  ├──────────────────────┤    ├──────────────────────┤      │        │
│  │  │ - Multi-head Attn    │    │ - Tree Ensemble      │      │        │
│  │  │ - Encoder Layers     │    │ - 100 Estimators     │      │        │
│  │  │ - Self-supervised    │    │ - Contamination 10%  │      │        │
│  │  │ - Input: 7 features  │    │ - Anomaly Detection  │      │        │
│  │  │ - Output: Score 0-1  │    │ - Output: Score 0-1  │      │        │
│  │  └──────────────────────┘    └──────────────────────┘      │        │
│  │              ↓                          ↓                   │        │
│  │         ┌─────────────────────────────────────┐            │        │
│  │         │      Score Fusion Engine            │            │        │
│  │         ├─────────────────────────────────────┤            │        │
│  │         │ - Weighted Average (w=0.5)          │            │        │
│  │         │ - Confidence Calculation            │            │        │
│  │         │ - Threshold: 0.5                    │            │        │
│  │         │ - Output: Final Anomaly Score       │            │        │
│  │         └─────────────────────────────────────┘            │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────────────┐
│                          Data Layer                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │  Models/     │  │    Data/     │  │    Logs/     │                  │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤                  │
│  │ - *.pt       │  │ - *.csv      │  │ - *.log      │                  │
│  │ - *.pkl      │  │ - *.pcap     │  │              │                  │
│  │ - *.json     │  │              │  │              │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│                                                                          │
│  Demo Data: sample_traffic.csv (1000 samples)                          │
│  - 900 normal traffic patterns                                          │
│  - 100 anomalous patterns                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Authentication Flow
```
User → Login Form → POST /token → JWT Token → Stored in LocalStorage
```

### 2. Prediction Flow
```
Upload Data → PCAP/CSV → Preprocessing → Feature Extraction → 
Feature Encoding → Model Prediction → Score Fusion → 
Anomaly Classification → Dashboard Display
```

### 3. Training Flow
```
Upload Training Data → Data Validation → Preprocessing → 
Feature Engineering → Model Training → Model Saving → 
Metrics Calculation → Update Dashboard
```

## Network Features (7 dimensions)

1. **Protocol**: TCP (6), UDP (17), ICMP (1)
2. **Length**: Packet size in bytes
3. **TTL**: Time to Live value
4. **Flags**: TCP flags or protocol-specific flags
5. **Source Port**: Origin port number
6. **Destination Port**: Target port number
7. **Time Delta**: Time difference from previous packet

## User Roles & Permissions

```
┌──────────┬─────────┬───────┬─────────┐
│   Role   │  Read   │ Write │ Retrain │
├──────────┼─────────┼───────┼─────────┤
│  Admin   │    ✓    │   ✓   │    ✓    │
│ Analyst  │    ✓    │   ✓   │    ✗    │
│  Viewer  │    ✓    │   ✗   │    ✗    │
└──────────┴─────────┴───────┴─────────┘
```

## Deployment Architecture

### Docker Compose Setup
```
┌─────────────────────────────────────────┐
│        Docker Compose Network           │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────┐  ┌───────────────┐ │
│  │   Frontend     │  │   Backend     │ │
│  │   Container    │  │   Container   │ │
│  │                │  │               │ │
│  │  Node:18       │  │  Python:3.11  │ │
│  │  Port: 3000    │  │  Port: 8000   │ │
│  │  Vite + React  │  │  FastAPI      │ │
│  └────────────────┘  └───────────────┘ │
│         ↑                    ↑          │
│         └────────┬───────────┘          │
│                  │                      │
│            Docker Network               │
│                                         │
│  Volumes:                               │
│  - ./backend/models:/app/models        │
│  - ./backend/data:/app/data            │
│  - ./demo_data:/app/demo_data          │
└─────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: FastAPI
- **ML Libraries**: PyTorch, scikit-learn, transformers
- **Auth**: python-jose, passlib
- **Data Processing**: pandas, numpy, scapy
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Password Hashing**: Bcrypt for password storage
3. **RBAC**: Role-based access control
4. **CORS**: Cross-origin resource sharing configuration
5. **Input Validation**: Pydantic models for request validation
6. **HTTPS Ready**: Production-ready security headers

## Scalability Considerations

- Stateless API design for horizontal scaling
- Model serving can be separated into dedicated service
- Add database layer for persistence
- Implement caching (Redis) for frequently accessed data
- Load balancing for high availability
- Message queue (RabbitMQ/Kafka) for async processing
