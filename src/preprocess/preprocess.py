from google.cloud import storage
from io import BytesIO
from PIL import Image
import numpy as np
from diffusers import DiffusionPipeline
from torchvision import transforms
import os
import torch 
import yaml


# Preprocessing file
print("We are processing your data. Please wait patiently...")

client = storage.Client()
BUCKET_SRC_NAME_MOMA = "moma_scrape"
BUCKET_SRC_NAME_IMAGENET = "imagenet_scrape"
FOLDER_NAME_MOMA = "imgs"
FOLDER_NAME_IMAGENET = "images"
BUCKET_DEST_NAME = "preprocess_data"

def get_model():
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, use_safetensors=True)
    pipe = pipe.to("cuda")
    return pipe

def get_images(bucket_name, folder_name):
    img_data_dict = {}
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix = folder_name)
    for blob in blobs:
        image_data = BytesIO(blob.download_as_bytes())        
        image = Image.open(image_data)
        
        #check that image does not only have 1 channel
        if image.mode != "RGB":
             image = image.convert("RGB")

        transform = transforms.Compose([
            transforms.Resize((512, 512)),  # Resize the image to 512x512 pixels
            transforms.ToTensor()  # Convert the image to a PyTorch tensor
        ])
        tensor = transform(image)
        tensor = tensor.half().to('cuda').unsqueeze(0)
        img_data_dict[os.path.join(bucket_name, blob.name)] = np.array(tensor)
    return img_data_dict

def get_image_embedding(img_data_dict):
    img_embed_dict = {}
    pipe = get_model()
    for img_dir, img_data_tensor in img_data_dict.items():
        img_latent_sample = pipe.vae.encode(img_data_tensor).to('cuda').latent_dist.sample()
        img_embed_dict[img_dir] = img_latent_sample
    return img_embed_dict

def upload_images_to_google_cloud(bucket_name, data_dict, data_dict_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f'{data_dict_name}.yaml')
    yaml_data = yaml.dump(data_dict, default_flow_style=False)
    blob.upload_from_string(yaml_data)


if __name__ == "__main__":
    img_data_imagenet_dict = get_images(BUCKET_SRC_NAME_IMAGENET, FOLDER_NAME_IMAGENET)
    img_embed_imagenet_dict = get_image_embedding(img_data_imagenet_dict)

    img_data_moma_dict = get_images(BUCKET_SRC_NAME_MOMA, FOLDER_NAME_MOMA)
    img_embed_moma_dict = get_image_embedding(img_data_moma_dict)

    upload_images_to_google_cloud(BUCKET_DEST_NAME, img_embed_imagenet_dict, 'imagenet_embeding')
    upload_images_to_google_cloud(BUCKET_DEST_NAME, img_embed_moma_dict, 'moma_embeding')

