from kfp import dsl, compiler
from google.cloud import aiplatform as aip
from google.cloud import storage
from PIL import Image
import io
import base64

@dsl.component
def predict(instance: list):
    endpoint = aip.Endpoint("projects/580339194016/locations/us-east4/endpoints/5529408791713415168"
                            )
    response = endpoint.predict(instances=instance)
    predictions = response.predictions
    print("Result:", predictions)
    return predictions

@dsl.component
def save_images_to_bucket(predictions: dict, bucket_name: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for i, pred in enumerate(predictions):
        image_data = base64.b64decode(pred)
        blob = bucket.blob(f'image_{i}.png')
        blob.upload_from_string(image_data, content_type='image/png')
        print(f"Image {i} saved to bucket {bucket_name}")

# Pipeline function
@dsl.pipeline
def prediction_pipeline(instance: list=[{"sample_key": ["dog", "cat"]}]):
    prediction_task = predict(instance=instance)
    save_images_task = save_images_to_bucket(predictions=prediction_task.outputs, bucket_name="saved_predictions")

compiler.Compiler().compile(prediction_pipeline, package_path='pipeline.yaml')

# @dsl.component
# def post_process(base64_list: list, bucket_name: str, frames_per_second: int=36):
#     print(type(base64_list))
#     # convert base64 to PIL image
#     images = [0]*8
#
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#
#     for i, base64_string in enumerate(base64_list):
#         # Decode the base64 string
#         decoded_data = base64.b64decode(base64_string.encode('utf-8'))
#
#         # Create a BytesIO stream and open the image using PIL
#         image = Image.open(io.BytesIO(decoded_data))
#         images[i] = image
#         blob = bucket.blob(f'image_{i}.png')
#
#         with io.BytesIO() as output:
#             image.save(output, format='PNG')
#             output.seek(0)
#             blob.upload_from_file(output, content_type='image/png')
#
#     return images

# @dsl.pipeline
# def sample_pipeline(instance: list=[{"sample_key": ["dog", "cat"]}]):
#     predictions = predict(instance=instance)
#     print(predictions.keys())
#     post_process(base64_list=predictions.outputs, bucket_name="saved_predictions")