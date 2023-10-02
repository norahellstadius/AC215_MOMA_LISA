import urllib.request
import requests
from bs4 import BeautifulSoup

url = "https://www.moma.org/media/W1siZiIsIjQ2MTI1NiJdLFsicCIsImNvbnZlcnQiLCItcXVhbGl0eSA4MCAtcmVzaXplIDE1MzZ4MTUzNlx1MDAzZSJdXQ.jpg?sha=68352f31a84be027"
# Open the URL as Browser, not as python urllib
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


response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(response.status_code)
#urllib.request.urlretrieve(url, "geeksforgeeks.png", headers={'User-Agent': 'Mozilla/5.0'})

# Opening the image and displaying it (to confirm its presence)
# page=urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
#infile=urllib.request.urlopen(page).read()

if response.status_code == 200:
    with open("./artworks/test.jpg", 'wb') as f:
        f.write(response.content)