from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from schema import ProductSchema

url_header = "https://www2.hm.com"
apiurl = ""

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
    data["price"] = price
    ProductSchema.model_validate(data, strict=True)
    requests.post(apiurl+"input", json=data)

def all_data(products):
    for product in products:
        grab_data(product)

def hm(numclothes : int, _apiurl : str):
    global apiurl
    apiurl = _apiurl
    # needed to add user agent to access
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
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
