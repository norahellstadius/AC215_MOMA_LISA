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
def get_text_data_from_bucket(bucket, object_name):
    # Access the specific object (text file) in the bucket
    blob = bucket.blob(object_name)
    # Download the text data
    text_data = blob.download_as_text()
    return text_data

# Example usage
bucket_name = 'your-bucket-name'
object_name = 'your-text-file.txt'
text_data = get_text_data_from_bucket(bucket_name, object_name)
print(text_data)

# Change data

# ----- upload data to Google buckets -------
for dish in data_for_dishes:
    try:
        response = requests.get(dish["url_img"])
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            object_name_image = "images/" + dish["name"]

            blob_image = bucket.blob(object_name_image)
            blob_image.upload_from_string(response.content)
        else:
            print("failed to download image")

    except Exception as e:
        print(f"An error occured with image upload: {str(e)}")

    try:
        yaml_content = yaml.dump(dish)
        object_name_text = "text/" + dish["name"]
        blob_text = bucket.blob(object_name_text)
        blob_text.upload_from_string(yaml_content)
    except Exception as e:
        print(f"An error occured with text upload: {str(e)}")


if __name__ == "__main__":
    print(get_text_data_from_bucket(BUCKET_SRC, ))