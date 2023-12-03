from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import json
import time



numclothes = 10
MAX_THREADS = 30
url_header = "https://www2.hm.com"

allclothes = dict()

def grab_data(product):
    title = product.find("a", attrs={"class" : "link"}).contents[0]
    url = url_header + product.find("a", {"class" : "link"}).get("href")
    image = product.find("img").get("src")
    if image == None: # this site has inconsistant tags >:(
        image = product.find("img").get("data-src")
    site_name = "H&M"
    price = product.find("span", {"class" : "price regular"}).contents[0]

    data = dict()
    data["title"] = title
    data["url"] = url
    data["image"] = "https:" + image
    data["site_name"] = site_name
    data["price:amount"] = price
    allclothes[data["title"]] = data
    # print(data, "\n\n")

# def grab_data(url):
#     url = "https://www2.hm.com" + url
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
#         response = requests.get(url, headers=headers)
#         print("Response code: ", response.status_code)
#         webpage = response.text
#         soup = BeautifulSoup(webpage, "lxml")
#         # opened = urlopen(response)
#         # print("Response code: ", opened.getcode())
#         # webpage = opened.read()
#     except Exception as error: # 404, 500, etc..
#         print("ERROR: ", error)
#         pass

#     # print("\n\nwebpage: \n\n", webpage)
#     # soup = BeautifulSoup(webpage, "lxml")
#     # print("soup: \n" + str(soup))
#     data = dict()
#     for tag in property_tags:
#         # print("\n", tag)
#         data[tag] = soup.find("meta", property="og:"+tag)["content"]
#         print("\nTag ", tag, data[tag])
#     data[image_tag] = soup.find("meta", name="og:"+image_tag)["content"]
#     data[price_tag] = soup.find("span", {"class" : "edbe20 ac3d9e"})
#     print("data : " + str(data))
#     allclothes[data["title"]] = data

def all_data(products):
    threads = min(MAX_THREADS, len(products))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for product in products:
            executor.submit(grab_data, product)

def main():
    # needed to add user agent to access
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    start_time = time.time()
    # women
    response = requests.get('https://www2.hm.com/en_us/women/products/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=' + str(numclothes/2), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("ul", {"class" : "products-listing small"})
    products = elements.find_all("article", {"class" : "hm-product-item"})
    all_data(products)
    # men
    response = requests.get('https://www2.hm.com/en_us/men/products/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=' + str(numclothes/2), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("ul", {"class" : "products-listing small"})
    products = elements.find_all("article", {"class" : "hm-product-item"})
    all_data(products)

    duration = time.time() - start_time

    with open("hm.json", "w") as outfile: 
        json.dump(allclothes, outfile)

    print(f"The program run for {duration} seconds")

main()
