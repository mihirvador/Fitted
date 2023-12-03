from aritzia_webscraper import arizia
from asos_webscraper import asos
from hm_webscraper import hm

url = "https://fitted-api-9e3i.onrender.com/"
num_clothes = 10
arizia(num_clothes, url)
asos(num_clothes, url)
hm(num_clothes, url)

