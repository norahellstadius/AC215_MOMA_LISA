from kfp import dsl, compiler
from google.cloud import aiplatform as aip
from google.cloud import storage
import base64

@dsl.component(base_image="python:3.10", packages_to_install=["google-cloud-aiplatform", "google-cloud-storage"])
def predict(instance: list, bucket_name: str)->list:
    from google.cloud import aiplatform as aip
    from google.cloud import storage
    import base64

    endpoint = aip.Endpoint("projects/580339194016/locations/us-east4/endpoints/5529408791713415168"
                            )
    response = endpoint.predict(instances=instance)
    predictions = response.predictions[0]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for i, pred in enumerate(predictions):
        image_data = base64.b64decode(pred)
        blob = bucket.blob(f'images/image_{i}.png')
        # TODO: change name to be unique
        blob.upload_from_string(image_data, content_type='image/png')
        print(f"Image {i} saved to bucket {bucket_name}")

@dsl.component(base_image="python:3.10", packages_to_install=["google-cloud-storage", "Pillow"])
def create_gifs(bucket_name: str, folder_name: str, gif_filename: str):
    from google.cloud import storage
    from PIL import Image
    from io import BytesIO

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_name+"/")

    # TODO: change to not save locally before uploading to bucket
    images = []
    for blob in blobs:
        image_bytes = blob.download_as_bytes()
        image = Image.open(BytesIO(image_bytes))
        images.append(image)

    with BytesIO() as output:
        images[0].save(
            output,
            format="GIF",
            save_all=True,
            append_images=images[1:],
            duration=1000 // 36,
            loop=0,
        )
        output.seek(0)
        blob = bucket.blob(f"{folder_name}/{gif_filename}")
        blob.upload_from_file(output, content_type="image/gif")


# Pipeline function
@dsl.pipeline
def prediction_pipeline(instance: list=[{"sample_key": ["dog", "cat"]}]):
    predict(instance=instance, bucket_name="saved_predictions")
    create_gifs(bucket_name="saved_predictions", folder_name="images", gif_filename="test.gif")

compiler.Compiler().compile(prediction_pipeline, package_path='pipeline.yaml')

# Run pipeline
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