from models import Product

def create_entry(data:dict):
    return Product.create(**data)