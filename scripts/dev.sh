#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    # Install python3-distutils if needed
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y python3-distutils
    fi
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
    fi
fi

# Create necessary directories
mkdir -p test_data
mkdir -p logs
mkdir -p src/{compiler,vm,genomics,ai,blockchain,api,utils}

# Setup test data
./scripts/setup_test_data.sh

# Start backend server in background
echo "Starting backend server..."
python -m uvicorn src.api.main:app --reload --port 8000 &
BACKEND_PID=$!

# Install and start frontend
echo "Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
npm start &
FRONTEND_PID=$!

# Create frontend structure if it doesn't exist
if [ ! -d "frontend/public" ]; then
    echo "Creating frontend structure..."
    mkdir -p frontend/{public,src/components,src/api}
    
    # Copy template files from the repository
    cp -r frontend-templates/* frontend/
fi

# Wait for user interrupt
echo "Development environment running. Press Ctrl+C to stop."
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait 