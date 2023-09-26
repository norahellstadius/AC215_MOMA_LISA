import requests
import yaml
from google.cloud import storage


# Preprocessing file
print("We are processing your data. Please wait patiently...")

client = storage.Client()
BUCKET_SRC_NAME = "cook_this_scrape"
BUCKET_DEST_NAME = "cook_this_preprocess"
BUCKET_SRC, BUCKET_DEST = client.bucket(BUCKET_SRC_NAME), client.bucket(
    BUCKET_DEST_NAME
)

# Get data
def get_text_data_from_bucket(bucket):
    # Access the specific object (text file) in the bucket
    blobs = bucket.blob('text/Banana bread')
    return blobs.download_as_text()

def transform_and_upload(bucket, text):
    transformed_text = text[::-1]
    try:
        yaml_content = yaml.dump(transformed_text)
        object_name_text = "texts/" + "banana_bread_test"
        blob_text = bucket.blob(object_name_text)
        blob_text.upload_from_string(yaml_content)
    except Exception as e:
        print(f"An error occured with text upload: {str(e)}")


if __name__ == "__main__":
    text = get_text_data_from_bucket(BUCKET_SRC)
    transform_and_upload(BUCKET_DEST,text)
    print("Done")