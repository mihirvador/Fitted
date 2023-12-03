from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    title: str
    url: Optional[str]
    image: Optional[str]
    site_name: Optional[str]