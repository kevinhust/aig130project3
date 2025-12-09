# AIG130 Project 3: Smart Home Voice Command MLOps

This project implements an end-to-end MLOps pipeline for classifying smart home voice commands using **HuggingFace** (for embeddings) and **Google Cloud Vertex AI** (for AutoML training).

## 📂 Repository Structure
```
.
├── .github/workflows/ml-pipeline.yml  # CI/CD: Builds Docker, runs embedding, triggers Vertex
├── data/                              # Place dataset.csv here
├── docs/                              # Report, demo scripts, etc.
├── src/
│   ├── app.py                         # Streamlit Demo App
│   ├── embed.py                       # Data Prep & Embedding Generation
│   ├── predict.py                     # Inference with Vertex Endpoint
│   └── vertex_pipeline.py             # KFP Pipeline Definition
├── Dockerfile                         # Env for embedding step
└── requirements.txt                   # Dependencies
```

## 🚀 Setup Instructions

### 1. Google Cloud Platform (GCP) Setup
1.  **Create a Project**: Name it `smart-home-mlops` (or similar).
2.  **Enable APIs**:
    - Vertex AI API
    - Cloud Storage API
    - Container Registry API (or Artifact Registry)
    - Cloud Build API (optional, for CI/CD)
3.  **Create Service Account**:
    - Go to IAM & Admin > Service Accounts.
    - Create new account (description: "GitHub Actions Runner").
    - **Roles**: `Storage Admin`, `Vertex AI Administrator`, `Service Account User`.
    - **Keys**: Create a JSON key and download it.
4.  **Create Storage Bucket**:
    - Name: `smart-home-data-bucket` (must be globally unique).
    - Region: `us-central1`.

### 2. GitHub Secrets
1.  Go to your GitHub Repo > Settings > Secrets and variables > Actions.
2.  Add New Repository Secret:
    - Name: `GCP_SA_KEY`
    - Value: Paste the content of the JSON key file.

### 3. Running Locally (Testing)
```bash
# Install dependencies
pip install -r requirements.txt

# Run embedding logic locally
python src/embed.py --input_file data/dataset.csv

# Run Streamlit App (after deploying endpoint)
streamlit run src/app.py
```

### 4. Deployment Check
- Push code to `main`.
- Go to **Actions** tab in GitHub to see the pipeline run.
- Check **Vertex AI Console** > Training / Pipelines to see the job.
- Once trained, deploy the model to an Endpoint via the console (if not fully automated in pipeline).
- Get the `ENDPOINT_ID` and use it in the Streamlit App.

## 💰 Cost Estimate
**Total Estimated Cost: < $2.00**
- **Storage**: < $0.01 (Dataset is tiny, ~50KB).
- **Vertex AI AutoML Training**: ~$1.00 - $1.50 (1 node hour minimum @ ~$2/hr, but likely faster or covered by free tier credits if new account).
- **Vertex AI Endpoint**: ~$0.10/hour. **CRITICAL: DELETE THE ENDPOINT AFTER DEMO**.
- **GitHub Actions**: Free (public repo tier).
