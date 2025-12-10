#!/bin/bash

# Build and run the container locally
# Usage: ./scripts/run_local.sh

echo "Building Docker image..."
docker-compose build app

echo "Starting application..."
docker-compose up app
