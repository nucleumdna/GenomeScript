#!/bin/bash

# Kill any existing processes on ports 3000 and 8000
kill $(lsof -t -i:3000) 2>/dev/null
kill $(lsof -t -i:8000) 2>/dev/null

# Activate virtual environment
source venv/bin/activate

# Start backend server in background
echo "Starting backend server..."
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend in background
echo "Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

# Function to cleanup processes on exit
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Setup cleanup on script exit
trap cleanup INT TERM

# Keep script running
echo "Development servers running. Press Ctrl+C to stop."
wait