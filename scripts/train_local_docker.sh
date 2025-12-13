#!/bin/bash
set -e

echo "🚀 Starting Local Docker Training (Plan D)..."

# 1. Build the image for linux/amd64 (Emulation on M4 Mac)
echo "🔨 Building x86 Training Image (this may take a few minutes for emulation)..."
docker buildx build --platform linux/amd64 -t aig130-trainer -f Dockerfile.train .

# 2. Run the container and mount the local model_artifacts directory
echo "🏃 Running Training Container..."
# Ensure local directory exists
mkdir -p model_artifacts

# Run with volume mount to extract the model
docker run --platform linux/amd64 --rm \
    -v "$(pwd)/model_artifacts:/app/model_artifacts" \
    aig130-trainer

echo "✅ Training Complete!"
echo "💾 Model saved to: $(pwd)/model_artifacts/model.joblib"
echo "👉 Now you can git commit and push this file!"
