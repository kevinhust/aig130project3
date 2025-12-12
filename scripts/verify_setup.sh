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
    
    # Check for required APIs
    echo "Checking enabled GCP APIs..."
    REQUIRED_APIS=(
        "artifactregistry.googleapis.com"
        "run.googleapis.com"
        "aiplatform.googleapis.com"
        "cloudresourcemanager.googleapis.com"
        "storage-component.googleapis.com"
    )
    
    CHANGES_NEEDED=false
    for api in "${REQUIRED_APIS[@]}"; do
        if ! gcloud services list --enabled --filter="config.name:$api" --format="value(config.name)" | grep -q "$api"; then
            echo "❌ API '$api' is NOT enabled."
            CHANGES_NEEDED=true
        else
            echo "✅ API '$api' is enabled."
        fi
    done

    if [ "$CHANGES_NEEDED" = true ]; then
        echo "⚠️  Some required APIs are missing. Run the following command to enable them:"
        echo "gcloud services enable ${REQUIRED_APIS[*]}"
    fi

else
    echo "⚠️  gcloud CLI is NOT installed (required for deployment)"
fi

echo "Detailed verification complete."
