# Base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY tests/ tests/

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 