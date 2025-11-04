import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os


class FeatureEncoder:
    """Encode and normalize features for model training"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.fitted = False
    
    def fit(self, features: np.ndarray, categorical_indices: list = None):
        """
        Fit encoders to the data
        
        Args:
            features: Feature array
            categorical_indices: List of indices for categorical features
        """
        if categorical_indices:
            for idx in categorical_indices:
                le = LabelEncoder()
                le.fit(features[:, idx].astype(str))
                self.label_encoders[idx] = le
        
        self.scaler.fit(features)
        self.fitted = True
    
    def transform(self, features: np.ndarray, categorical_indices: list = None) -> np.ndarray:
        """
        Transform features using fitted encoders
        
        Args:
            features: Feature array
            categorical_indices: List of indices for categorical features
            
        Returns:
            Transformed feature array
        """
        features = features.copy()
        
        if categorical_indices:
            for idx in categorical_indices:
                if idx in self.label_encoders:
                    features[:, idx] = self.label_encoders[idx].transform(
                        features[:, idx].astype(str)
                    )
        
        if self.fitted:
            features = self.scaler.transform(features)
        
        return features
    
    def fit_transform(self, features: np.ndarray, categorical_indices: list = None) -> np.ndarray:
        """
        Fit and transform in one step
        
        Args:
            features: Feature array
            categorical_indices: List of indices for categorical features
            
        Returns:
            Transformed feature array
        """
        self.fit(features, categorical_indices)
        return self.transform(features, categorical_indices)
    
    def save(self, path: str):
        """Save encoder to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'fitted': self.fitted
        }, path)
    
    def load(self, path: str):
        """Load encoder from disk"""
        data = joblib.load(path)
        self.label_encoders = data['label_encoders']
        self.scaler = data['scaler']
        self.fitted = data['fitted']
