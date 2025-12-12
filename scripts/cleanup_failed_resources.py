from google.cloud import aiplatform
import sys
import os

# Add src to python path to import config
sys.path.append(os.path.abspath("src"))
import config

def cleanup_failed_resources():
    print("🧹 Starting Cleanup of Failed Resources...")
    aiplatform.init(project=config.PROJECT_ID, location=config.REGION)
    
    # 1. Cleanup Failed Pipeline Jobs
    try:
        jobs = aiplatform.PipelineJob.list()
        print(f"Found {len(jobs)} pipeline jobs.")
        for job in jobs:
            # Delete if failed (State 5) or cancelled (4)
            # Use job.state.name to be safe if local enum varies
            if job.state.name in ["PIPELINE_STATE_FAILED", "PIPELINE_STATE_CANCELLED"]:
                print(f"🗑️ Deleting Failed Pipeline: {job.display_name} ({job.name})")
                job.delete()
    except Exception as e:
        print(f"❌ Error cleaning pipelines: {e}")

    # 2. Cleanup Custom Jobs (e.g. from debug attempts)
    try:
        custom_jobs = aiplatform.CustomJob.list()
        for job in custom_jobs:
            if job.state.name in ["JOB_STATE_FAILED", "JOB_STATE_CANCELLED"]:
                print(f"🗑️ Deleting Failed Custom Job: {job.display_name} ({job.name})")
                job.delete()
    except Exception as e:
         print(f"❌ Error cleaning custom jobs: {e}")

    # 3. Cleanup Unused Endpoints?
    # Be careful here. We only want to delete endpoints that contain NO models?
    # Or rely on manual cleanup for endpoints to be safe.
    # User said "Delete previous failed resources", likely referring to the many failed pipeline runs.
    # So deleting failed jobs is the priority.
    
    print("✨ Cleanup Complete!")

if __name__ == "__main__":
    cleanup_failed_resources()
