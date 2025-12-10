"""
Configuration settings for Smart Home Intent Classification Pipeline
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data settings
DATA_FILE = "dataset.csv"
RANDOM_SEED = 42

# Google Cloud Platform (GCP) settings
# REQUIRED: You MUST replace this with your actual GCP Project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "aig130p3") 
REGION = os.environ.get("GCP_REGION", "us-central1")

# Resource Names (Must match task.md)
BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "aig130-project3-data")
REPO_NAME = "aig130-repo"
IMAGE_NAME = "smart-home-app"
SERVICE_NAME = "smart-home-app"

# Model settings
MODEL_DISPLAY_NAME = "smart-home-intent-model"
TRAIN_TEST_SPLIT_RATIO = 0.8
BATCH_SIZE = 32

# HuggingFace settings
HF_MODEL_NAME = "bert-base-uncased"

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
