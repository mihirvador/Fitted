from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import json


numclothes = 10

allclothes = dict()

def grab_data(url):
    tags = ["title", "url", "image", "site_name", "price:amount"]
    webpage = urlopen(url).read()
    soup = BeautifulSoup(webpage, "lxml")
    data = dict()
    for tag in tags:
        data[tag] = soup.find("meta", property="og:"+tag)["content"]
    allclothes[data["title"]] = data

def all_data(allurls):
    for link in allurls:
        grab_data(link.get("href"))

def main():
    response = requests.get('https://www.aritzia.com/us/en/clothing?lastViewed=' + str(numclothes))
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("div", {"class" : "ar-product-grid js-product-grid center mw-100"})
    tdTags = elements.find_all('a', {"class" : "relative db js-plp-hash"})
    all_data(tdTags)
    with open('aritzia.json', 'w') as convert_file: 
        convert_file.write(json.dumps(allclothes))

main()
