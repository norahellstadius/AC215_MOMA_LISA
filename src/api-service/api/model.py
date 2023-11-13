import os
import json
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from google.cloud import aiplatform
from google.cloud import storage


def create_gifs(bucket_name: str, folder_name: str, gif_filename: str):

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


def make_prediction_vertexai(instance, bucket_name = "saved_predictions"):
    print("Predict using Vertex AI endpoint")

    # Get the endpoint
    # Endpoint format: endpoint_name="projects/{PROJECT_NUMBER}/locations/us-central1/endpoints/{ENDPOINT_ID}"
    endpoint = aiplatform.Endpoint(
        "projects/580339194016/locations/us-central1/endpoints/7732031848334753792"
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

    create_gifs(bucket_name, folder_name="images", gif_filename="test.gif")


    


    