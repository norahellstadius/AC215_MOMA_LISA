from google.cloud import aiplatform as aip

PROJECT_ID = 'cookthis-400019'
REGION="us-east4"
BUCKET_NAME = "saved_predictions"
PIPELINE_ROOT = f"gs://{BUCKET_NAME}/pipeline_root/"
DISPLAY_NAME = "test"

job = aip.PipelineJob(
 display_name=DISPLAY_NAME,
 template_path="pipeline.yaml",
 pipeline_root=PIPELINE_ROOT,
 enable_caching=False,
)

job.run()