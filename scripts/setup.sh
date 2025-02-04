#!/bin/bash

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "python3 not found. Please install Python 3 first."
    echo "You can install it using Homebrew: brew install python3"
    exit 1
fi

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install development dependencies
python3 -m pip install pytest pytest-cov pytest-asyncio black isort mypy pylint ipython

# Create project structure
mkdir -p src/compiler
mkdir -p tests
touch src/__init__.py
touch src/compiler/__init__.py

# Run tests
python3 -m pytest tests/test_lexer_debug.py -v 