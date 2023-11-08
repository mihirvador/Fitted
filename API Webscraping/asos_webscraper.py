from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import json
import time

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

numclothes = 10
MAX_THREADS = 30

allclothes = dict()

def grab_data(url, rprice):
    tags = ["title", "url", "image", "site_name"]
    url = "https://www.asos.com" + url
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    data = dict()
    for tag in tags:
        data[tag] = soup.find("meta", property="og:"+tag)["content"]
    data["price"] = rprice
    allclothes[data["title"]] = data

def all_data(allurls):
    threads = min(MAX_THREADS, len(allurls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for link in allurls:
            price = link.find("span", {"class" : "price__B9LP"}).text
            executor.submit(grab_data, link.get("href"), price)

def main():
    alldata = []
    url = "https://www.asos.com/us/men/a-to-z-of-brands/cat/?cid=1361"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    elements = soup.findAll("a", {"class" : "brandTitle_k7acW"})
    i = 0
    for brand in elements:
        currurl = "https://www.asos.com" + brand.get("href")
        page = requests.get(currurl, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        elements = soup.findAll("a", {"class" : "productLink_P97ZK"})
        for ele in elements:
            if(i == numclothes):
                break
            alldata.append(ele)
            i += 1
        else:
            continue
        break
    start_time = time.time()
    all_data(alldata)
    duration = time.time() - start_time
    print(f"The program run for {duration} seconds")
    with open('asos.json', 'w') as convert_file: 
        convert_file.write(json.dumps(allclothes))

main()
