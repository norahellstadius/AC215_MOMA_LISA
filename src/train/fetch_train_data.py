from google.cloud import storage
import os

BUCKET_NAME = "preprocess_data"
FOLDER_NAME = "train"  
LOCAL_DIR = "train" 

def download_bucket_folder(bucket_name, folder_name, local_directory):
    """Downloads all objects within a folder in a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # List objects in the specified "folder"
    blobs = bucket.list_blobs(prefix=folder_name)

    for blob in blobs:
        # Determine the local file path by removing the folder prefix
        local_path = os.path.join(local_directory, blob.name.replace(folder_name + '/', ''))

        # Create any necessary subdirectories
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Download the object to the local path
        blob.download_to_filename(local_path)
        print(f"Downloaded {blob.name} to {local_path}")
    
    print('finnished fetching data from google buckets')

if __name__ == "__main__":
    
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

    download_bucket_folder(BUCKET_NAME, FOLDER_NAME, LOCAL_DIR)
