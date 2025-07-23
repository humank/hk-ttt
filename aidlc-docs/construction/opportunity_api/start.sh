#!/bin/bash

# Opportunity Management API Startup Script

echo "Starting Opportunity Management API..."

# Check if .env file exists, if not copy from example
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    # Run database migrations if needed
    # alembic upgrade head
    
    # Start the application
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
else
    echo "Running locally..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run database migrations if needed
    # alembic upgrade head
    
    # Start the application with reload for development
    echo "Starting development server..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi
