# Project Report Outline

## 1. Executive Summary
- **Goal**: Classify smart home commands.
- **Solution**: Hybrid Pipeline (HF Embeddings + Vertex AI AutoML).
- **Result**: F1 Score achieved, success of CI/CD pipeline.

## 2. Methodology
### 2.1 Dataset Analysis
- Source: Kaggle Smart Home Commands.
- Distribution: Visuals of 'Action' vs 'Category'.
### 2.2 Feature Engineering (HuggingFace)
- Why Embeddings? Converting semantic meaning to dense vectors.
- Model Choice: `all-MiniLM-L6-v2` (Speed vs Performance trade-off).
### 2.3 Model Training (Vertex AI)
- AutoML benefits (Hyperparameter tuning, model selection).
- Training cost and time analysis.

## 3. MLOps Pipeline Architecture
- **Diagram**: [Data] -> [GitHub Action (Docker/Embed)] -> [GCS] -> [Vertex Pipeline] -> [Endpoint].
- **Tools**: GitHub Actions, Docker, Google Cloud Storage, Vertex AI.

## 4. Evaluation Results
- Confusion Matrix (screenshot from Vertex UI).
- Comparison with baseline.

## 5. Challenges & Lessons Learned
- Integration complexity (GCP Auth).
- Cost management (Spot instances vs On-demand).

## 6. Conclusion & Future Work
- Add voice audio input (Speech-to-Text).
- Deploy App to Cloud Run.
