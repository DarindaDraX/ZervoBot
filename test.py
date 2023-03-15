import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlencode, urlunparse
import urllib.request, urllib.error, urllib.parse

query = "porn"
filter = 'photo-animatedgif'
url = f"https://www.bing.com/images/search?q=cat&safesearch=off"
custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
print(url)
res = requests.get(url, headers={
    "User-Agent": custom_user_agent,
})
with open("response.html", "w") as f:
    f.write(res.text)
soup = BeautifulSoup(res.content, 'lxml')

links = []
for a in soup.find_all("a", {"class": "iusc"}):
    m = json.loads(a["m"])
    murl = m["murl"]
    links.append(murl)

print(links)
