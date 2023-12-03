import requests
from schema import ProductSchema

url = "https://fitted-api-9e3i.onrender.com/"

data = {
    'title': 'TITLE',
    'url': 'URL',
    'image': 'IMAGEURL',
    'site_name': 'SITENAME'
}
out = requests.post(url+"input", data=data)
print(out.json())