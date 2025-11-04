# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

---

## Endpoints

### 1. Authentication

#### POST /token
Get an access token by logging in.

**Request:**
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 2. Prediction

#### POST /predict
Predict anomalies in network traffic data.

**Permissions Required:** `read`

**Request Body:**
```json
{
  "features": [
    [6, 500, 64, 2, 1024, 443, 0.1],
    [17, 200, 65, 0, 2048, 80, 0.2]
  ]
}
```

**Feature Format:**
1. Protocol (6=TCP, 17=UDP, 1=ICMP)
2. Packet length
3. TTL (Time to Live)
4. Flags
5. Source port
6. Destination port
7. Time delta

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[6, 500, 64, 2, 1024, 443, 0.1]]
  }'
```

**Response:**
```json
{
  "predictions": [0],
  "anomaly_scores": [0.234],
  "confidence": [0.532],
  "transformer_scores": [0.189],
  "isolation_forest_scores": [0.279]
}
```

**Response Fields:**
- `predictions`: 0 = normal, 1 = anomaly
- `anomaly_scores`: Fused anomaly score (0-1)
- `confidence`: Confidence level (0-1)
- `transformer_scores`: Transformer model scores
- `isolation_forest_scores`: IsolationForest scores

---

### 3. Model Management

#### POST /retrain
Retrain the model with new data.

**Permissions Required:** `retrain` (admin only)

**Request Body:**
```json
{
  "data_path": "../demo_data/sample_traffic.csv",
  "epochs": 10
}
```

**Request:**
```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data_path": "../demo_data/sample_traffic.csv",
    "epochs": 10
  }'
```

**Response:**
```json
{
  "message": "Model retrained successfully",
  "data_points": 1000,
  "feature_dim": 7,
  "epochs": 10
}
```

---

### 4. Data Upload

#### POST /upload
Upload network traffic data (CSV or PCAP format).

**Permissions Required:** `write`

**Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/traffic.csv"
```

**Supported Formats:**
- CSV files with columns: timestamp, src_ip, dst_ip, protocol, length, ttl, flags, src_port, dst_port
- PCAP files (automatically converted to CSV)

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "traffic.csv",
  "file_path": "./data/traffic.csv",
  "data_points": 500,
  "features_shape": [500, 7]
}
```

---

### 5. Metrics

#### GET /metrics
Get model performance metrics and statistics.

**Permissions Required:** `read`

**Request:**
```bash
curl -X GET "http://localhost:8000/metrics" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "total_predictions": 1000,
  "anomaly_count": 85,
  "anomaly_rate": 0.085,
  "avg_confidence": 0.78,
  "model_loaded": true
}
```

---

### 6. Health Check

#### GET /health
Check API health status.

**No authentication required**

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

### 7. API Information

#### GET /
Get API information and available endpoints.

**No authentication required**

**Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "AI-Based Cybersecurity Threat Detection API",
  "status": "running",
  "model_loaded": true,
  "endpoints": {
    "auth": "/token",
    "predict": "/predict",
    "retrain": "/retrain",
    "upload": "/upload",
    "metrics": "/metrics",
    "health": "/health"
  }
}
```

---

## User Roles and Permissions

| Role | Username | Password | Permissions |
|------|----------|----------|-------------|
| Admin | admin | admin123 | read, write, retrain |
| Analyst | analyst | analyst123 | read, write |
| Viewer | viewer | viewer123 | read |

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "User does not have retrain permission"
}
```

### 400 Bad Request
```json
{
  "detail": "Model not trained. Please train the model using /retrain endpoint"
}
```

### 404 Not Found
```json
{
  "detail": "Data file not found: /path/to/file.csv"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Prediction error: <error message>"
}
```

---

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- Test API calls directly from the browser
- See request/response schemas
- Authenticate and make authorized requests

---

## Example Workflow

### 1. Login
```bash
TOKEN=$(curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')
```

### 2. Upload Data
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@network_traffic.csv"
```

### 3. Retrain Model
```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data_path": "./data/network_traffic.csv",
    "epochs": 15
  }'
```

### 4. Make Predictions
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      [6, 500, 64, 2, 1024, 443, 0.1],
      [17, 1500, 255, 255, 31337, 12345, 5.0]
    ]
  }'
```

### 5. Check Metrics
```bash
curl -X GET "http://localhost:8000/metrics" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Rate Limiting

Currently, there are no rate limits enforced. For production use, consider implementing:
- Request rate limiting
- Token expiration (default: 30 minutes)
- API key management

---

## CORS Configuration

CORS is enabled for all origins in development. For production:
1. Update `allow_origins` in `main.py`
2. Specify your frontend domain
3. Configure appropriate CORS headers

---

## WebSocket Support

WebSocket support for real-time updates is not currently implemented but can be added for:
- Live threat detection notifications
- Real-time metric updates
- Model training progress

---

## Best Practices

1. **Always use HTTPS in production**
2. **Rotate JWT secret keys regularly**
3. **Implement proper logging**
4. **Set up monitoring and alerting**
5. **Use strong passwords**
6. **Validate and sanitize all inputs**
7. **Keep dependencies updated**
