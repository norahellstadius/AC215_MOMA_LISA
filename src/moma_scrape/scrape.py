import urllib.request
import requests

url = "https://www.moma.org/media/W1siZiIsIjQ2MTI1NiJdLFsicCIsImNvbnZlcnQiLCItcXVhbGl0eSA4MCAtcmVzaXplIDE1MzZ4MTUzNlx1MDAzZSJdXQ.jpg?sha=68352f31a84be027"
# Open the URL as Browser, not as python urllib

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(response.status_code)
#urllib.request.urlretrieve(url, "geeksforgeeks.png", headers={'User-Agent': 'Mozilla/5.0'})

# Opening the image and displaying it (to confirm its presence)
# page=urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
#infile=urllib.request.urlopen(page).read()

if response.status_code == 200:
    with open("./artworks/test.jpg", 'wb') as f:
        f.write(response.content)