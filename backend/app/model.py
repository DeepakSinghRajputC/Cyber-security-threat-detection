import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.ensemble import IsolationForest
from transformers import AutoModel, AutoTokenizer
import joblib
import os
from typing import Dict, List, Tuple
import json


class TransformerAnomalyDetector(nn.Module):
    """Transformer-based anomaly detection model"""
    
    def __init__(self, input_dim: int, hidden_dim: int = 128, num_heads: int = 4, num_layers: int = 2):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        
        # Input projection
        self.input_projection = nn.Linear(input_dim, hidden_dim)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output layers
        self.fc = nn.Linear(hidden_dim, hidden_dim // 2)
        self.output = nn.Linear(hidden_dim // 2, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        # x shape: (batch, seq_len, input_dim)
        x = self.input_projection(x)
        x = self.transformer(x)
        
        # Use mean pooling over sequence
        x = torch.mean(x, dim=1)
        
        x = self.relu(self.fc(x))
        x = self.sigmoid(self.output(x))
        return x


class HybridAnomalyDetector:
    """Hybrid model combining Transformer and IsolationForest"""
    
    def __init__(self, input_dim: int = 7):
        self.input_dim = input_dim
        self.transformer_model = TransformerAnomalyDetector(input_dim)
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transformer_model.to(self.device)
        self.trained = False
    
    def train_transformer(self, X: np.ndarray, epochs: int = 10, batch_size: int = 32):
        """Train the transformer model"""
        self.transformer_model.train()
        
        # Prepare data
        X_tensor = torch.FloatTensor(X).unsqueeze(1)  # Add sequence dimension
        dataset = torch.utils.data.TensorDataset(X_tensor)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # Use reconstruction loss
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.transformer_model.parameters(), lr=0.001)
        
        for epoch in range(epochs):
            total_loss = 0
            for batch in dataloader:
                x = batch[0].to(self.device)
                
                optimizer.zero_grad()
                output = self.transformer_model(x)
                
                # Self-supervised: predict if sample is normal (1) or not
                # For training, we assume most samples are normal
                target = torch.ones_like(output) * 0.9
                loss = criterion(output, target)
                
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if (epoch + 1) % 2 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
    
    def train_isolation_forest(self, X: np.ndarray):
        """Train the IsolationForest model"""
        self.isolation_forest.fit(X)
    
    def train(self, X: np.ndarray, epochs: int = 10):
        """Train both models"""
        print("Training Transformer model...")
        self.train_transformer(X, epochs=epochs)
        
        print("Training IsolationForest model...")
        self.train_isolation_forest(X)
        
        self.trained = True
        print("Training complete!")
    
    def predict_transformer(self, X: np.ndarray) -> np.ndarray:
        """Get predictions from transformer model"""
        self.transformer_model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).unsqueeze(1).to(self.device)
            scores = self.transformer_model(X_tensor).cpu().numpy().flatten()
        return scores
    
    def predict_isolation_forest(self, X: np.ndarray) -> np.ndarray:
        """Get predictions from IsolationForest"""
        # IsolationForest returns -1 for anomalies, 1 for normal
        # Convert to 0-1 scale (0 = normal, 1 = anomaly)
        predictions = self.isolation_forest.predict(X)
        scores = self.isolation_forest.score_samples(X)
        # Normalize scores to 0-1 range
        scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
        scores = 1 - scores  # Invert so higher = more anomalous
        return scores
    
    def predict(self, X: np.ndarray, fusion_weight: float = 0.5) -> Dict:
        """
        Predict using both models and fuse scores
        
        Args:
            X: Feature array
            fusion_weight: Weight for transformer vs isolation forest (0-1)
            
        Returns:
            Dictionary with predictions, scores, and confidence
        """
        transformer_scores = self.predict_transformer(X)
        isolation_scores = self.predict_isolation_forest(X)
        
        # Fuse scores (weighted average)
        fused_scores = (fusion_weight * transformer_scores + 
                       (1 - fusion_weight) * isolation_scores)
        
        # Threshold for anomaly detection
        threshold = 0.5
        predictions = (fused_scores > threshold).astype(int)
        
        # Calculate confidence
        confidence = np.abs(fused_scores - threshold) / threshold
        confidence = np.clip(confidence, 0, 1)
        
        return {
            'predictions': predictions.tolist(),
            'anomaly_scores': fused_scores.tolist(),
            'transformer_scores': transformer_scores.tolist(),
            'isolation_forest_scores': isolation_scores.tolist(),
            'confidence': confidence.tolist()
        }
    
    def save(self, model_dir: str):
        """Save models to disk"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save transformer
        torch.save(
            self.transformer_model.state_dict(),
            os.path.join(model_dir, 'transformer_model.pt')
        )
        
        # Save isolation forest
        joblib.dump(
            self.isolation_forest,
            os.path.join(model_dir, 'isolation_forest.pkl')
        )
        
        # Save metadata
        metadata = {
            'input_dim': self.input_dim,
            'trained': self.trained
        }
        with open(os.path.join(model_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f)
    
    def load(self, model_dir: str):
        """Load models from disk"""
        # Load metadata
        with open(os.path.join(model_dir, 'metadata.json'), 'r') as f:
            metadata = json.load(f)
        
        self.input_dim = metadata['input_dim']
        self.trained = metadata['trained']
        
        # Recreate transformer model
        self.transformer_model = TransformerAnomalyDetector(self.input_dim)
        self.transformer_model.load_state_dict(
            torch.load(os.path.join(model_dir, 'transformer_model.pt'),
                      map_location=self.device)
        )
        self.transformer_model.to(self.device)
        
        # Load isolation forest
        self.isolation_forest = joblib.load(
            os.path.join(model_dir, 'isolation_forest.pkl')
        )
