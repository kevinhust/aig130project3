# AIG130 Project 3: Smart Home Intent Classification

This project implements a Machine Learning pipeline for classifying smart home voice commands (e.g., "Turn on the lights") using **HuggingFace** embeddings and **Google Cloud Vertex AI** AutoML.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Google Cloud Platform Account

### Running Locally
To start the application locally using Docker:

```bash
./scripts/run_local.sh
```

Or manually:
```bash
docker-compose up
```
The app will be available at http://localhost:8501

### Environment Setup
Check if you have the necessary tools installed:
```bash
./scripts/verify_setup.sh
```

## 🏗 Architecture

- **`src/app.py`**: Main Streamlit application.
- **`src/config.py`**: Centralized configuration.
- **`src/vertex_pipeline.py`**: Definition of Vertex AI Training Pipeline.
- **`Dockerfile`**: Multi-stage build for efficient production images.
- **`docker-compose.yml`**: Local development orchestration.
- **`.github/workflows`**: CI/CD pipeline for automated testing.

## 🛠 Configuration

Configuration is managed via `src/config.py` and environment variables. Key variables:
- `GCP_PROJECT_ID`: Your Google Cloud Project ID.
- `GCP_REGION`: Region for Vertex AI (default: us-central1).
- `VERTEX_ENDPOINT_ID`: ID of the deployed endpoint (for prediction).

## 📦 Deployment

The project is designed to be deployed to Google Cloud Run or GKE, using the Docker image built by the CI/CD pipeline.

1. **Build Image**: `docker build -t aig130-project3 .`
2. **Push to Artifact Registry**: `docker push ...`
3. **Deploy**: Use Cloud Run or follow `docs/demo_script.md`.

## 📚 Documentation
See the `docs/` directory for detailed reports, evaluation metrics, and reflection templates.
