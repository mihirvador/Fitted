from fastapi import FastAPI
from API_Webscraping.dbs import get_session
from API_Webscraping.models import Product
from API_Webscraping.crud import create_entry
from cassandra.cqlengine.management import sync_table

currProduct = Product
app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    global session
    session = get_session()
    sync_table(currProduct)

@app.get("/")
def read_index():
    return "Uh Oh! Why are You here!"

@app.get("/title")
def tile_list_view():
    return list(Product.objects.all())

@app.get("/site_name/{site_name}")
def site_name_list_view(site_name):
    return list(Product.objects.filter(site_name=site_name))

@app.get("/title/{title}")
def products_detail_view(title):
    try:
        return dict(Product.objects.get(title=title))
    except Exception as e:
        return "Not Found"
    
@app.post("/input")
def site_name_list_view(data):
    product = create_entry(data.dict())
    return product