from google.cloud import storage
import os

BUCKET_NAME = "preprocess_data"
BUCKET_FOLDER_NAME = "train"
LOCAL_DIR = "train" 

def download_bucket_folder(bucket_name, bucket_folder_name, local_directory):
    """Downloads all objects within a folder in a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # List objects in the specified "folder"
    blobs = bucket.list_blobs(prefix=bucket_folder_name)

    for blob in blobs:
        # Determine the local file path by removing the folder prefix
        local_path = os.path.join(local_directory, 'train_data', blob.name.replace(bucket_folder_name + '/', ''))
        print(local_path)

        # Create any necessary subdirectories
        os.makedirs('train/train_data', exist_ok=True)

        # Download the object to the local path
        blob.download_to_filename(local_path)
        print(f"Downloaded {blob.name} to {local_path}")
    
    print('finnished fetching data from google buckets')

if __name__ == "__main__":
    download_bucket_folder(BUCKET_NAME, BUCKET_FOLDER_NAME, LOCAL_DIR)
