import urllib.request
import requests
from bs4 import BeautifulSoup

# Create url for each page
def create_url(page_number):
    return f"https://www.moma.org/collection/?utf8=%E2%9C%93&q=&classifications=any&date_begin=Pre-1850&date_end=2023&with_images=1&on_view=1&page={page_number}&direction=fwd"

# Get contents from response and convert to beautifulsoup object
def get_image_urls(base_url: str) -> list[str]:
    response = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, "html.parser")
    # Get all image tags
    images = soup.find_all("img")
    # Get the src attribute of each image
    image_urls = [image["src"] for image in images]
    return image_urls


if __name__ == "__main__":
    images_url = get_image_urls(create_url(4))
    base_url = 'https://www.moma.org'
    for i in range(5):
        url = base_url + images_url[i]
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            with open(f"./artworks/test2_{i}.jpg", 'wb') as f:
                f.write(response.content)

