import os
import numpy as np
import tensorflow as tf
from google.cloud import storage
from PIL import Image
from io import BytesIO
from transformers import pipeline
import json

class PreprocessData:
    def __init__(self):
        self.client = storage.Client()
        self.source_bucket_name = 'moma_scrape'
        self.destination_bucket_name = 'preprocess_data'
        self.folder_name = folder_name = 'imgs'
        self.meta_data = []
        self.captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        self.dest_jsonl = 'metadata.jsonl'

    def fetch_images_data(self, num_images = 100):
        """Fetch image data from Google Cloud Storage."""
        bucket = self.client.bucket(self.source_bucket_name)
        blobs = bucket.list_blobs(prefix=self.folder_name)

        for i, blob in enumerate(blobs):
            print(i)
            if i >= num_images:
                break
            
            image_data = BytesIO(blob.download_as_bytes())
            image = Image.open(image_data)
            # Ensure the image has 3 channels
            if image.mode != "RGB":
                image = image.convert("RGB")  
            image_name = f"{(blob.name).split('imgs/')[1].split('.jpeg')[0]}.png"
            image.save(image_name, 'PNG')

            self.upload_data_to_google_bucket(image_name)
            os.remove(image_name)
            image_label = self.get_text_label(image)
            image_data = {'file_name': image_name, "text": image_label}
            self.meta_data.append(image_data)
            print(f'preprocessed: {image_name}')
            
        return 

    def create_jsonl_file(self):
        output_file = open(self.dest_jsonl, 'w', encoding='utf-8')
        for dic in self.meta_data:
            json.dump(dic, output_file) 
            output_file.write("\n")

        self.upload_data_to_google_bucket(self.dest_jsonl)
        os.remove(self.dest_jsonl)

    def get_text_label(self, image):
        """Generate text labels for images using a captioning model."""
        
        generated_text = self.captioner(image)[0]['generated_text']
        return "MoMA artwork of: " + generated_text


    def upload_data_to_google_bucket(self, name):
        bucket = self.client.get_bucket(self.destination_bucket_name)
        blob = bucket.blob(f'train/{name}')
        blob.upload_from_filename(f"{name}")
        print(f"uploaded to gs://{self.destination_bucket_name}/train/{name}")

if __name__ == "__main__":
    n = 200
    process = PreprocessData()
    process.fetch_images_data(num_images=n)
    process.create_jsonl_file()
    print("Done")