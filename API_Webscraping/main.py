from fastapi import FastAPI
from . import config, db, models, crud
from cassandra.cqlengine.management import sync_table

settings = config.get_settings()
Product = models.Product
app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(Product)

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
    product = crud.create_entry(data.dict())
    return product