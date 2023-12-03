from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import json



numclothes = 10
url_header = "https://www.urbanoutfitters.com/"

allclothes = dict()

def grab_data(product):
    title = product.find("a", attrs={"class" : "link"}).contents[0]
    url = url_header + product.find("a", {"class" : "link"}).get("href")
    image = product.find("img").get("srcset")
    if image == None: # this site has inconsistant tags >:(
        image = product.find("img").get("data-src")
    site_name = "Urban Outfitters"
    price = product.find("span", {"class" : "c-pwa-product-price__current s-pwa-product-price__current"}).contents[0]

    data = dict()
    data["title"] = title
    data["url"] = url
    data["image"] = "https:" + image
    data["site_name"] = site_name
    data["price:amount"] = price
    allclothes[data["title"]] = data
    # print(data, "\n\n") #

def all_data(products):
    for product in products:
        grab_data(product)

def main():
    # needed to add user agent to access
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    # women
    response = requests.get('https://www.urbanoutfitters.com/womens-clothing#u-skip-anchor' + str(numclothes/2), headers=headers)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("ul", {"class" : "c-pwa-radio-boxes__list c-pwa-radio-boxes__list--default"})
    products = elements.find_all("article", {"class" : "c-pwa-tile-grid-tile"})
    all_data(products)
    # men
    response = requests.get('https://www.urbanoutfitters.com/mens-clothing#u-skip-anchor' + str(numclothes/2), headers=headers)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find("ul", {"class" : "c-pwa-radio-boxes__list c-pwa-radio-boxes__list--default"})
    products = elements.find_all("article", {"class" : "c-pwa-tile-grid-tile"})
    all_data(products)

    with open("urban_outfitters.json", "w") as outfile: 
        json.dump(allclothes, outfile)

main()
