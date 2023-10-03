import requests
import yaml
from google.cloud import storage
from io import BytesIO

# Preprocessing file
print("We are processing your data. Please wait patiently...")

client = storage.Client()
BUCKET_SRC_NAME_MOMA = "moma_scrape"
BUCKET_SRC_NAME_IMAGENET = "imagenet_scrape"
FOLDER_NAME_MOMA = "imgs"
FOLDER_NAME_IMAGENET = "images"
BUCKET_DEST_NAME = "preprocess_data"
BUCKET_SRC_IMAGENET = client.bucket(BUCKET_SRC_NAME_IMAGENET)
BUCKET_SRC_MOMA =  client.bucket(BUCKET_SRC_NAME_MOMA)
BUCKET_DEST = client.bucket(BUCKET_DEST_NAME)

# Get data
def get_images(bucket, folder_name):
    img_data = []
    blobs = bucket.list_blobs(prefix = folder_name)
    for blob in blobs:
        img_data.append(BytesIO(blob.download_as_bytes()))
    # # Load the image data using Pillow
    # image = Image.open(BytesIO(image_data))

    # image.show()  # Show the image using the default image viewer
    # image.save('downloaded_image.jpg')  # Save the image to a local file
    return img_data

# def transform_and_upload(bucket, text):
#     transformed_text = text[::-1]
#     try:
#         yaml_content = yaml.dump(transformed_text)
#         object_name_text = "texts/" + "banana_bread_test"
#         blob_text = bucket.blob(object_name_text)
#         blob_text.upload_from_string(yaml_content)
#     except Exception as e:
#         print(f"An error occured with text upload: {str(e)}")


if __name__ == "__main__":
   print(get_images(BUCKET_SRC_MOMA, 'imgs')[0].shape)
