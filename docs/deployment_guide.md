# Upgrade & Deployment Walkthrough - AIG130 Project 3

I have successfully upgraded the **Smart Home Intent Classification** project. This guide covers how to run it locally and deploy it to Google Cloud Platform (GCP).

## 1. Local Setup & Upgrades

### Key Improvements
- **Configuration**: `src/config.py` now centrally manages GCP settings.
- **Docker**: New `Dockerfile` (multi-stage) and `docker-compose.yml` for easy setup.
- **CI/CD**: `.github/workflows/ci_cd.yml` for automated testing and deployment.

### How to Run Locally
1. **Verify Environment**:
   ```bash
   ./scripts/verify_setup.sh
   ```
2. **Start App**:
   ```bash
   ./scripts/run_local.sh
   ```
   Open `http://localhost:8501` to use the app.

---

## 2. Automating with GitHub Actions (CI/CD)

I have configured `.github/workflows/ci_cd.yml` to automatically:
1.  **Test**: Run code checks.
2.  **Train**: Submit Vertex AI Pipeline job.
3.  **Deploy**: Build Docker image and deploy to Cloud Run.

### Setup Secrets
For this to work, you must add **Secrets** in your GitHub Repo:
`Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`

1.  **`GCP_PROJECT_ID`**: `aig130p3`
2.  **`GCP_SA_KEY`**: The JSON key of your Service Account.
    *   *Create SA Key*: `IAM & Admin` -> `Service Accounts` -> (Select Account) -> `Keys` -> `Add Key` -> `Create new key` -> `JSON`.
    *   *Permissions needed* (Add these roles):
        *   **Artifact Registry Writer** (to push Docker images)
        *   **Cloud Run Developer** (to deploy the app)
        *   **Storage Admin** (to upload data and store build artifacts)
        *   **Vertex AI User** (to submit training jobs)
        *   **Service Account User** (to run operations as this SA)

Once set, simple **Push to Main** to trigger the full pipeline!
```bash
git push
```

---

## 3. Manual Deployment (Optional Backup)

If you prefer to deploy manually or CI/CD fails, use these steps.

### Step 1: Set Variables
```bash
# REPLACE WITH YOUR ACTUAL PROJECT ID
export PROJECT_ID="aig130p3" 
export REGION="us-central1"
export REPO_NAME="aig130-repo"
export APP_NAME="smart-home-app"
```

### Step 2: Enable APIs & Create Repo
```bash
gcloud services enable artifactregistry.googleapis.com run.googleapis.com aiplatform.googleapis.com

gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for AIG130"
```

### Step 3: Train Model (Vertex AI)
1. **Create Bucket**: `gsutil mb -l $REGION gs://aig130-data-$PROJECT_ID`
2. **Upload Data**: `gsutil cp dataset.csv gs://aig130-data-$PROJECT_ID/`
3. **Run Pipeline**:
   (Update `src/config.py` with your new Bucket Name first!)
   ```bash
   python src/vertex_pipeline.py
   ```
   **Note**: This script will automatically:
   1. Compile the pipeline to JSON.
   2. Upload it to Vertex AI.
   3. Trigger the job.
   4. Print a link to the dashboard.

### Step 4: Deploy App (Cloud Run)
Once training is done, get your **Endpoint ID** from the Vertex AI Console.

```bash
# Build & Push Image
gcloud auth configure-docker $REGION-docker.pkg.dev
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$APP_NAME:v1 .
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$APP_NAME:v1

# Deploy
gcloud run deploy $APP_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$APP_NAME:v1 \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars=GCP_PROJECT_ID=$PROJECT_ID,GCP_REGION=$REGION,VERTEX_ENDPOINT_ID=YOUR_ENDPOINT_ID
```
