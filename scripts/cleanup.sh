#!/bin/bash

# Cleanup script to remove GCP resources created by this project
# Usage: ./scripts/cleanup.sh

# Load config
export PROJECT_ID="${GCP_PROJECT_ID:-aig130p3}"
export REGION="${GCP_REGION:-us-central1}"
export APP_NAME="smart-home-app"
export REPO_NAME="aig130-repo"

echo "⚠️  WARNING: This will delete resources in Project: $PROJECT_ID"
echo "Resources to be deleted:"
echo "1. Cloud Run Service: $APP_NAME"
echo "2. Vertex AI Endpoint (Undeploy & Delete)"
echo "3. Artifact Registry Image (Optional)"
echo ""
read -p "Are you sure you want to proceed? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# 1. Cloud Run
echo "🗑️  Deleting Cloud Run Service..."
gcloud run services delete $APP_NAME --region $REGION --quiet || echo "Service not found or already deleted"

# 2. Vertex AI (Requires finding IDs first)
echo "🔍 Finding Vertex AI Endpoint..."
ENDPOINT_ID=$(gcloud ai endpoints list --region=$REGION --filter="display_name=smart-home-intent-model-endpoint" --format="value(name)" | head -n 1)

if [ -n "$ENDPOINT_ID" ]; then
    echo "🔻 Checking for deployed models on Endpoint: $ENDPOINT_ID..."
    # List deployed model IDs
    DEPLOYED_MODELS=$(gcloud ai endpoints describe $ENDPOINT_ID --region=$REGION --format="value(deployedModels.id)")
    
    for MODEL_ID in $DEPLOYED_MODELS; do
        if [ -n "$MODEL_ID" ]; then
            echo "   Undeploying model $MODEL_ID..."
            gcloud ai endpoints undeploy-model $MODEL_ID --endpoint=$ENDPOINT_ID --region=$REGION --quiet
        fi
    done
    
    echo "🗑️  Deleting Endpoint: $ENDPOINT_ID..."
    gcloud ai endpoints delete $ENDPOINT_ID --region=$REGION --quiet
else
    echo "Endpoint not found."
fi

# 3. Vertex AI Model
echo "🔍 Finding Vertex AI Model..."
MODEL_ID=$(gcloud ai models list --region=$REGION --filter="display_name=smart-home-intent-model" --format="value(name)" | head -n 1)

if [ -n "$MODEL_ID" ]; then
    echo "🗑️  Deleting Model: $MODEL_ID..."
    gcloud ai models delete $MODEL_ID --region=$REGION --quiet
else
    echo "Model not found."
fi

# 4. Artifact Registry (Optional)
echo ""
echo "📦 Docker Images in Artifact Registry are NOT deleted by default."
echo "Storage costs are low, but you can delete them to be safe."
read -p "Do you want to delete the Docker Repository '$REPO_NAME' as well? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Deleting Artifact Registry Repository: $REPO_NAME..."
    gcloud artifacts repositories delete $REPO_NAME --location=$REGION --quiet
fi

echo "✅ Cleanup complete!"
echo "Note: GCS Bucket '$PROJECT_ID-data' was NOT deleted."
