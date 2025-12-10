from kfp import dsl
from kfp import compiler
from google_cloud_pipeline_components.v1.automl.training_job import (
    AutoMLTabularTrainingJobRunOp
)
from google_cloud_pipeline_components.v1.endpoint import (
    EndpointCreateOp, ModelDeployOp
)
from google_cloud_pipeline_components.v1.dataset import (
    TabularDatasetCreateOp
)

@dsl.pipeline(
    name="smart-home-intent-classification",
    description="AutoML Tabular pipeline for smart home commands"
)
def pipeline(
    project: str,
    location: str,
    bucket_uri: str,
    display_name: str,
    dataset_csv_uri: str,  # gs://.../training_data.csv
):
    # 0. Create Managed Dataset from CSV
    dataset_op = TabularDatasetCreateOp(
        project=project,
        location=location,
        display_name=display_name,
        gcs_source=dataset_csv_uri,
    )

    # 1. Train AutoML Model
    training_op = AutoMLTabularTrainingJobRunOp(
        project=project,
        location=location,
        display_name=display_name,
        optimization_prediction_type="classification",
        budget_milli_node_hours=1000,  # 1 hour budget (minimum)
        column_transformations=[
            {"numeric": {"column_name": "emb_0"}},
            # We rely on AutoML inference for columns not explicitly listed, 
            # or list key columns if needed. 
        ],
        dataset=dataset_op.outputs["dataset"],
        target_column="target_intent",
    )

    # 2. Create Endpoint
    endpoint_op = EndpointCreateOp(
        project=project,
        location=location,
        display_name=f"{display_name}-endpoint",
    )

    # 3. Deploy Model
    ModelDeployOp(
        model=training_op.outputs["model"],
        endpoint=endpoint_op.outputs["endpoint"],
        dedicated_resources_machine_type="n1-standard-2",
        dedicated_resources_min_replica_count=1,
        dedicated_resources_max_replica_count=1,
    )

if __name__ == "__main__":
    import config
    from google.cloud import aiplatform

    # 1. Compile
    pipeline_path = "vertex_pipeline.json"
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=pipeline_path
    )
    print(f"✅ Pipeline compiled to {pipeline_path}")

    # 2. Submit to Vertex AI
    print(f"🚀 Submitting pipeline to Vertex AI ({config.REGION})...")
    
    # Initialize Vertex AI SDK
    aiplatform.init(
        project=config.PROJECT_ID,
        location=config.REGION,
        staging_bucket=f"gs://{config.BUCKET_NAME}"
    )

    # Define job
    job = aiplatform.PipelineJob(
        display_name=f"{config.MODEL_DISPLAY_NAME}-pipeline",
        template_path=pipeline_path,
        parameter_values={
            "project": config.PROJECT_ID,
            "location": config.REGION,
            "bucket_uri": f"gs://{config.BUCKET_NAME}",
            "display_name": config.MODEL_DISPLAY_NAME,
            "dataset_csv_uri": f"gs://{config.BUCKET_NAME}/{config.DATA_FILE}",
        },
        enable_caching=True
    )

    # Submit
    job.submit()
    print(f"🎉 Job submitted! View status here: {job._dashboard_uri()}")
