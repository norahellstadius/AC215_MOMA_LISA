import requests
import yaml
from bs4 import BeautifulSoup
from google.cloud import storage
from typing import List

import urllib.request
import requests
from bs4 import BeautifulSoup

# Create url for each page
def create_url(page_number):
    return f"https://www.moma.org/collection/?utf8=%E2%9C%93&q=&classifications=any&date_begin=Pre-1850&date_end=2023&with_images=1&on_view=1&page={page_number}&direction=fwd"

# Get contents from response and convert to beautifulsoup object
def get_image_urls(base_url: str) -> List[str]:
    response = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, "html.parser")
    # Get all image tags
    images = soup.find_all("img")
    # Get the src attribute of each image
    image_urls = [image["src"] for image in images]
    return image_urls

def scrape_img_url(image_url: str, id: int) -> None:
    # base_url = 'https://www.moma.org'
    # image_url = base_url + url
    response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    print(response.status_code)

    if response.status_code == 200:
        object_name_image = "images/" + f'moma_{id}.jpeg'
        blob_image = bucket.blob(object_name_image)
        blob_image.upload_from_string(response.content)
    else:
        print("failed to download image")
    
    return None

if __name__ == "__main__":
    client = storage.Client()
    bucket_name = "moma_scrape"
    bucket = client.bucket(bucket_name)

    base_url = 'https://www.moma.org'
    j = 0

    for i in range(1, 25):
        try:
            site_url = create_url(i)
            print(site_url)
            img_urls = get_image_urls(site_url)
            for x in img_urls:
                scrape_img_url(base_url + x, j)
                j += 1
        except Exception:
            print(f"{i} failed")

    print("Done")

