#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start backend server
echo "Starting backend server..."
python -m uvicorn src.api.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

# Wait for interrupt
echo "Servers running. Press Ctrl+C to stop."
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
