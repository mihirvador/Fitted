from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
# data = {
#     "title": "TITLE",
#     "url": "URL",
#     "image": "IMAGEURL",
#     "site_name": "SITENAME"
# }

class Product(Model):
    __keyspace__ = "fitted"
    title = columns.Text(partition_key = True, primary_key=True, required=True)
    url = columns.Text()
    image = columns.Text()
    site_name = columns.Text(index=True, required=True)