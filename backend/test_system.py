"""
Basic tests for the cybersecurity threat detection system
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from app import auth
        from app import model
        from app import data_ingestion
        from app import feature_encoder
        import main
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_auth_module():
    """Test authentication module"""
    try:
        from app.auth import verify_password, get_password_hash, fake_users_db
        
        # Test password hashing
        password = "test123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed), "Password verification failed"
        
        # Test fake users exist
        assert "admin" in fake_users_db, "Admin user not found"
        assert "analyst" in fake_users_db, "Analyst user not found"
        assert "viewer" in fake_users_db, "Viewer user not found"
        
        print("✓ Authentication module tests passed")
        return True
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False

def test_data_ingestion():
    """Test data ingestion module"""
    try:
        from app.data_ingestion import DataPreprocessor
        import pandas as pd
        import numpy as np
        
        # Create sample data
        df = pd.DataFrame({
            'timestamp': [1.0, 2.0, 3.0],
            'protocol': [6, 17, 6],
            'length': [100, 200, 150],
            'ttl': [64, 64, 64],
            'flags': [2, 0, 2],
            'src_port': [1024, 2048, 3072],
            'dst_port': [80, 443, 8080]
        })
        
        # Test preprocessing
        preprocessor = DataPreprocessor()
        processed_df = preprocessor.preprocess(df)
        features = preprocessor.extract_features(processed_df)
        
        assert features.shape[0] == 3, "Feature extraction failed"
        assert features.shape[1] == 7, "Wrong number of features"
        
        print("✓ Data ingestion tests passed")
        return True
    except Exception as e:
        print(f"✗ Data ingestion test failed: {e}")
        return False

def test_feature_encoder():
    """Test feature encoder module"""
    try:
        from app.feature_encoder import FeatureEncoder
        import numpy as np
        
        # Create sample features
        features = np.array([
            [6, 100, 64, 2, 1024, 80, 0.1],
            [17, 200, 64, 0, 2048, 443, 0.2],
            [6, 150, 64, 2, 3072, 8080, 0.15]
        ])
        
        # Test encoding
        encoder = FeatureEncoder()
        encoded = encoder.fit_transform(features)
        
        assert encoded.shape == features.shape, "Encoding shape mismatch"
        assert encoder.fitted, "Encoder not fitted"
        
        print("✓ Feature encoder tests passed")
        return True
    except Exception as e:
        print(f"✗ Feature encoder test failed: {e}")
        return False

def test_model_initialization():
    """Test model initialization"""
    try:
        from app.model import HybridAnomalyDetector
        
        # Initialize model
        model = HybridAnomalyDetector(input_dim=7)
        
        assert model.input_dim == 7, "Wrong input dimension"
        assert hasattr(model, 'transformer_model'), "Transformer model not initialized"
        assert hasattr(model, 'isolation_forest'), "IsolationForest not initialized"
        
        print("✓ Model initialization tests passed")
        return True
    except Exception as e:
        print(f"✗ Model initialization test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Cybersecurity Threat Detection System Tests")
    print("="*60 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Authentication", test_auth_module),
        ("Data Ingestion", test_data_ingestion),
        ("Feature Encoder", test_feature_encoder),
        ("Model Initialization", test_model_initialization),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
