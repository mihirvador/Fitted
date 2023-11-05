from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import json
import time


numclothes = 10
MAX_THREADS = 30

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
    threads = min(MAX_THREADS, len(allurls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for link in allurls:
            executor.submit(grab_data, link.get("href"))

def main():
    response = requests.get('https://www.aritzia.com/us/en/clothing?lastViewed=' + str(numclothes))
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("div", {"class" : "ar-product-grid js-product-grid center mw-100"})
    tdTags = elements.find_all('a', {"class" : "relative db js-plp-hash"})
    start_time = time.time()
    all_data(tdTags)
    duration = time.time() - start_time
    print(f"The program run for {duration} seconds")
    with open('artiza.json', 'w') as convert_file: 
        convert_file.write(json.dumps(allclothes))

main()
