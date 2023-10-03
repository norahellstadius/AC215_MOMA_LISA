import requests
import yaml
from google.cloud import storage
import urllib.request
import requests
import os 
import zipfile

CLINT = storage.Client()
BUCKET_NAME = "imagenet_scrape"
BUCKET = CLINT.bucket(BUCKET_NAME)

ZIP_FILE_PATH = 'scrape/imagenet_data.zip'
EXTRACT_PATH = 'scrape/'
BASE_PATH = 'scrape/imagenet-mini'

def unzip_file(zip_file_path, extract_to_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
        print(f'Successfully unzipped {zip_file_path} to {extract_to_path}')
    except Exception as e:
        print(f'Error unzipping {zip_file_path}: {str(e)}')

def upload_imagenet_images(bucket, base_path):

    folder_names = ['train', 'val']
    for folder in folder_names: 
        sub_folders = os.listdir(os.path.join(base_path, folder)) #add whole paths 
        for sub_folder in sub_folders:
            img_names = os.listdir(os.path.join(base_path, folder,sub_folder))
            for img in img_names:
                img_path = os.path.join(base_path, folder, sub_folder, img)
                destination_blob_name =  "images/" + f'{img}'
                blob = bucket.blob(destination_blob_name)
                blob.upload_from_filename(img_path)
                print(f'Successfully uploaded {img_path} to {destination_blob_name}')

if __name__ == "__main__":
    unzip_file(ZIP_FILE_PATH, EXTRACT_PATH)
    upload_imagenet_images(BUCKET, BASE_PATH)

