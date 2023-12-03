from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from schema import ProductSchema

apiurl = ""

def grab_data(url):
    tags = ["title", "url", "image", "site_name"]
    webpage = urlopen(url).read()
    soup = BeautifulSoup(webpage, "lxml")
    data = dict()
    for tag in tags:
        data[tag] = soup.find("meta", property="og:"+tag)["content"]
    data["price"] = soup.find("meta", property="og:price:amount")["content"]
    ProductSchema.model_validate(data, strict=True)
    requests.post(apiurl+"input", json=data)
    #allclothes[data["title"]] = data

def all_data(allurls):
    for link in allurls:
        grab_data(link.get("href"))

def arizia(numclothes : int, _apiurl : str):
    global apiurl
    apiurl = _apiurl
    response = requests.get('https://www.aritzia.com/us/en/clothing?lastViewed=' + str(numclothes))
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("div", {"class" : "ar-product-grid js-product-grid center mw-100"})
    tdTags = elements.find_all('a', {"class" : "relative db js-plp-hash"})
    all_data(tdTags)
