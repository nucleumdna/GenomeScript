#!/bin/bash
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

echo "Virtual environment is ready! Use 'source venv/bin/activate' to activate it." 