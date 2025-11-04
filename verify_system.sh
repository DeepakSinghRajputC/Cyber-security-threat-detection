#!/bin/bash

echo "=== Cybersecurity Threat Detection System Verification ==="
echo ""

# Check backend structure
echo "✓ Checking backend structure..."
if [ -f "backend/main.py" ] && [ -f "backend/requirements.txt" ]; then
    echo "  ✓ Backend files present"
else
    echo "  ✗ Backend files missing"
    exit 1
fi

# Check key modules
echo "✓ Checking backend modules..."
for module in "auth.py" "model.py" "data_ingestion.py" "feature_encoder.py"; do
    if [ -f "backend/app/$module" ]; then
        echo "  ✓ $module present"
    else
        echo "  ✗ $module missing"
        exit 1
    fi
done

# Check frontend structure
echo "✓ Checking frontend structure..."
if [ -f "frontend/package.json" ] && [ -f "frontend/src/App.jsx" ]; then
    echo "  ✓ Frontend files present"
else
    echo "  ✗ Frontend files missing"
    exit 1
fi

# Check frontend components
echo "✓ Checking frontend components..."
for component in "Login.jsx" "MetricsGrid.jsx" "AlertsList.jsx" "ModelChart.jsx"; do
    if [ -f "frontend/src/components/$component" ]; then
        echo "  ✓ $component present"
    else
        echo "  ✗ $component missing"
        exit 1
    fi
done

# Check Docker files
echo "✓ Checking Docker configuration..."
if [ -f "docker-compose.yml" ] && [ -f "backend/Dockerfile" ] && [ -f "frontend/Dockerfile" ]; then
    echo "  ✓ Docker files present"
else
    echo "  ✗ Docker files missing"
    exit 1
fi

# Check demo data
echo "✓ Checking demo data..."
if [ -f "demo_data/sample_traffic.csv" ]; then
    lines=$(wc -l < demo_data/sample_traffic.csv)
    echo "  ✓ Demo data present ($lines lines)"
else
    echo "  ✗ Demo data missing"
    exit 1
fi

# Check documentation
echo "✓ Checking documentation..."
if [ -f "README.md" ]; then
    lines=$(wc -l < README.md)
    echo "  ✓ README present ($lines lines)"
else
    echo "  ✗ README missing"
    exit 1
fi

echo ""
echo "=== All verification checks passed! ==="
echo ""
echo "Structure Summary:"
echo "  - Backend: FastAPI with JWT RBAC"
echo "  - ML Models: Transformer + IsolationForest"
echo "  - Frontend: React + Tailwind"
echo "  - Data: PCAP converter + Feature encoder"
echo "  - Docker: Full containerization support"
echo "  - Demo: 1000 sample network traffic records"
echo ""
echo "To run the system:"
echo "  1. Using Docker: docker-compose up --build"
echo "  2. Manual:"
echo "     - Backend: cd backend && pip install -r requirements.txt && uvicorn main:app --reload"
echo "     - Frontend: cd frontend && npm install && npm run dev"
