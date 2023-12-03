from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

numclothes = 10

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
    for link in allurls:
        price = link.find("span", {"class" : "price_CMH3V"}).text
        grab_data(link.get("href"), price)

def main():
    alldata = []
    # men
    url = "https://www.asos.com/us/men/a-to-z-of-brands/cat/?cid=1361"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    elements = soup.findAll("a", {"class" : "brandTitle_k7acW"})
    i = 0
    for brand in elements:
        currurl = "https://www.asos.com" + brand.get("href")
        page = requests.get(currurl, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        elements = soup.findAll("a", {"class" : "productLink_KM4PI"})
        for ele in elements:
            if(i == numclothes):
                break
            alldata.append(ele)
            i += 1
        else:
            continue
        break
    all_data(alldata)
    #women
    url = "https://www.asos.com/us/women/a-to-z-of-brands/cat/?cid=1340"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    elements = soup.findAll("a", {"class" : "brandTitle_k7acW"})
    i = 0
    for brand in elements:
        currurl = "https://www.asos.com" + brand.get("href")
        page = requests.get(currurl, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        elements = soup.findAll("a", {"class" : "productLink_KM4PI"})
        for ele in elements:
            if(i == numclothes):
                break
            alldata.append(ele)
            i += 1
        else:
            continue
        break
    all_data(alldata)
    with open('asos.json', 'w') as convert_file: 
        convert_file.write(json.dumps(allclothes))

main()
