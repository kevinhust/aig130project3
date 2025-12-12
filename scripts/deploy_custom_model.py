from google.cloud import aiplatform
import os
import sys

# Add src to python path to import config
sys.path.append(os.path.abspath("src"))
import config

def deploy_model():
    print("🚀 Starting Custom Model Deployment...")
    
    # 1. Initialize
    aiplatform.init(
        project=config.PROJECT_ID,
        location=config.REGION,
        staging_bucket=f"gs://{config.BUCKET_NAME}"
    )

    # 2. Upload Model to Vertex AI
    # We use the pre-built Scikit-learn container provided by Google
    # Updated to sklearn-cpu.1-3 for compatibility with scikit-learn 1.3.x
    serving_container = "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-3:latest"
    
    # Model artifact *directory* path (local)
    # The SDK will upload this directory's contents to GCS automatically for 'upload'
    # Wait, aiplatform.Model.upload expects `artifact_uri` (GCS) usually, OR `local_model` in some SDK versions.
    # Standard way: Upload to GCS first manually? Or let SDK do it?
    # SDK method: aiplatform.Model.upload(..., artifact_uri=...)
    # So we need to put it on GCS first.
    
    # Upload to GCS using Python SDK (no gsutil dependency)
    gcs_model_uri = f"gs://{config.BUCKET_NAME}/custom_model_artifacts/"
    local_model_path = "model_artifacts/model.joblib"
    blob_name = "custom_model_artifacts/model.joblib"
    
    print(f"📂 Current Dir: {os.getcwd()}")
    if not os.path.exists(local_model_path):
        print(f"❌ Error: Model file not found at {local_model_path}")
        print("Listing directory:")
        for root, dirs, files in os.walk("."):
            for file in files:
                print(os.path.join(root, file))
        sys.exit(1)
        
    print(f"📤 Uploading {local_model_path} to {gcs_model_uri}...")
    
    from google.cloud import storage
    storage_client = storage.Client(project=config.PROJECT_ID)
    bucket = storage_client.get_bucket(config.BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_model_path)

    print("✅ Uploaded model artifacts.")
    
    print("📦 Registering Model in Vertex AI...")
    model = aiplatform.Model.upload(
        display_name="smart-home-custom-rf",
        artifact_uri=gcs_model_uri,
        serving_container_image_uri=serving_container,
        description="Custom RandomForest trained locally via scikit-learn"
    )
    print(f"✅ Model Uploaded: {model.resource_name}")

    # 3. Create/Get Endpoint
    endpoint_name = config.ENDPOINT_DISPLAY_NAME
    endpoints = aiplatform.Endpoint.list(filter=f'display_name="{endpoint_name}"')
    
    if endpoints:
        endpoint = endpoints[0]
        print(f"🔹 Found existing endpoint: {endpoint.resource_name}")
    else:
        print(f"🔹 Creating new endpoint: {endpoint_name}...")
        endpoint = aiplatform.Endpoint.create(display_name=endpoint_name)
    
    # 4. Deploy Model to Endpoint
    print(f"🚀 Deploying model to endpoint... (This takes 10-15 mins)")
    # machine_type=n1-standard-2 is standard
    # traffic_split={"0": 100} directs 100% traffic to the new model
    model.deploy(
        endpoint=endpoint,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
        traffic_split={"0": 100}, 
        deploy_request_timeout=1200
    )
    
    print("🎉 Deployment Complete!")
    print(f"👉 Endpoint ID: {endpoint.resource_name}")

if __name__ == "__main__":
    deploy_model()
