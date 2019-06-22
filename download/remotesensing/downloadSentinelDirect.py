from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import json
import requests
import geopandas as gpd
import matplotlib.pyplot as plt

username = ''
password = ''
product_id = '8df46c9e-a20c-43db-a19a-4240c2ed3b8b'
temporary_dir = "C:/Users/David/Downloads/"
output_filepath = temporary_dir + product_id + ".tif"
boundsdata = "./files/groningen.geojson"


# connect to the API
api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')
footprint = geojson_to_wkt(read_geojson(boundsdata))

products = api.query(footprint,
                     date=('20190220', '20190225'),
                     producttype='SLC',
                     polarisationmode='VV',
                     sensoroperationalmode='IW')

print(str(len(products)), "sentinel-1 images ready for download")
for product in products:
    api.download(product, directory_path=temporary_dir)
