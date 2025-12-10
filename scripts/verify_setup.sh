#!/bin/bash

# Verify development environment setup
# Usage: ./scripts/verify_setup.sh

echo "Checking environment..."

# Check Python
if command -v python3 &>/dev/null; then
    echo "✅ Python 3 is installed: $(python3 --version)"
else
    echo "❌ Python 3 is NOT installed"
fi

# Check Docker
if command -v docker &>/dev/null; then
    echo "✅ Docker is installed: $(docker --version)"
else
    echo "❌ Docker is NOT installed"
fi

# Check GCP CLI
if command -v gcloud &>/dev/null; then
    echo "✅ gcloud CLI is installed: $(gcloud --version | head -n 1)"
else
    echo "⚠️  gcloud CLI is NOT installed (required for deployment)"
fi

echo "Detailed verification complete."
