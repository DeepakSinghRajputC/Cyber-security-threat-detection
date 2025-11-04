from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List, Dict
import pandas as pd
import numpy as np
import os
import shutil
from dotenv import load_dotenv

from app.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    check_permission, Token, User, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.model import HybridAnomalyDetector
from app.feature_encoder import FeatureEncoder
from app.data_ingestion import load_and_preprocess_data
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI-Based Cybersecurity Threat Detection API",
    description="API for detecting anomalies in network traffic using Transformer and IsolationForest models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and encoder instances
model = None
encoder = None
model_loaded = False

# Paths
MODEL_DIR = os.getenv("MODEL_PATH", "./models")
ENCODER_PATH = os.path.join(MODEL_DIR, "feature_encoder.pkl")


class PredictionRequest(BaseModel):
    features: List[List[float]]


class PredictionResponse(BaseModel):
    predictions: List[int]
    anomaly_scores: List[float]
    confidence: List[float]
    transformer_scores: List[float]
    isolation_forest_scores: List[float]


class TrainRequest(BaseModel):
    data_path: str
    epochs: int = 10


class MetricsResponse(BaseModel):
    total_predictions: int
    anomaly_count: int
    anomaly_rate: float
    avg_confidence: float
    model_loaded: bool


# Initialize or load model on startup
@app.on_event("startup")
async def startup_event():
    global model, encoder, model_loaded
    
    try:
        # Try to load existing model
        if os.path.exists(MODEL_DIR) and os.path.exists(ENCODER_PATH):
            model = HybridAnomalyDetector()
            model.load(MODEL_DIR)
            
            encoder = FeatureEncoder()
            encoder.load(ENCODER_PATH)
            
            model_loaded = True
            print("✓ Pre-trained model loaded successfully")
        else:
            print("⚠ No pre-trained model found. Train a model using /retrain endpoint")
            model = HybridAnomalyDetector()
            encoder = FeatureEncoder()
            model_loaded = False
    except Exception as e:
        print(f"⚠ Error loading model: {e}")
        model = HybridAnomalyDetector()
        encoder = FeatureEncoder()
        model_loaded = False


@app.get("/")
async def root():
    return {
        "message": "AI-Based Cybersecurity Threat Detection API",
        "status": "running",
        "model_loaded": model_loaded,
        "endpoints": {
            "auth": "/token",
            "predict": "/predict",
            "retrain": "/retrain",
            "upload": "/upload",
            "metrics": "/metrics",
            "health": "/health"
        }
    }


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate and get access token"""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Predict anomalies in network traffic
    Requires: read permission
    """
    check_permission(current_user, "read")
    
    if not model_loaded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model not trained. Please train the model using /retrain endpoint"
        )
    
    try:
        # Convert input to numpy array
        features = np.array(request.features)
        
        # Make predictions
        results = model.predict(features, fusion_weight=0.5)
        
        return PredictionResponse(**results)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@app.post("/retrain")
async def retrain(
    request: TrainRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrain the model with new data
    Requires: retrain permission (admin only)
    """
    check_permission(current_user, "retrain")
    
    global model, encoder, model_loaded
    
    try:
        # Load and preprocess data
        if not os.path.exists(request.data_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Data file not found: {request.data_path}"
            )
        
        df, features = load_and_preprocess_data(request.data_path)
        
        # Encode features
        if not encoder.fitted:
            features = encoder.fit_transform(features)
            encoder.save(ENCODER_PATH)
        else:
            features = encoder.transform(features)
        
        # Train model
        model = HybridAnomalyDetector(input_dim=features.shape[1])
        model.train(features, epochs=request.epochs)
        
        # Save model
        model.save(MODEL_DIR)
        
        model_loaded = True
        
        return {
            "message": "Model retrained successfully",
            "data_points": len(features),
            "feature_dim": features.shape[1],
            "epochs": request.epochs
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Training error: {str(e)}"
        )


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload network traffic data file (CSV or PCAP)
    Requires: write permission
    """
    check_permission(current_user, "write")
    
    try:
        # Save uploaded file
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        
        file_path = os.path.join(data_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Try to load and validate the file
        df, features = load_and_preprocess_data(file_path)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "file_path": file_path,
            "data_points": len(df),
            "features_shape": features.shape
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload error: {str(e)}"
        )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics(current_user: User = Depends(get_current_active_user)):
    """
    Get model metrics and statistics
    Requires: read permission
    """
    check_permission(current_user, "read")
    
    # In a production system, these would be stored in a database
    # For now, return mock metrics
    return MetricsResponse(
        total_predictions=1000,
        anomaly_count=85,
        anomaly_rate=0.085,
        avg_confidence=0.78,
        model_loaded=model_loaded
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_loaded
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
