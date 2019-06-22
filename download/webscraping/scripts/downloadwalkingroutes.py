import fiona
import requests
from shapely.geometry import shape
import geopandas as gpd
import matplotlib.pyplot as plt


def store_bytes_to_filepath(content, filepath):
    with open(filepath, 'wb') as file:
        file.write(content)


def download_to_file(url, headers, filepath):
    content = download_content(url, headers)
    store_bytes_to_filepath(content, filepath)


def download_content(url, headers):
    response = requests.get(url, headers=headers)
    return response.content


def read_gpx_to_geodataframe(input_filepath):
    input_gdf = gpd.read_file(input_filepath)
    return input_gdf


# Constant variables
temp_filepath = "C:/Users/David/Downloads/Wandelroutes/5653357.gpx"
output_filepath = "C:/Users/David/Downloads/Wandelroutes/5653357.json"
route_search_url = ""
route_url = ""
route_search_headers = {"Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
                        "Connection": "keep-alive",
                        "Content-Length": "331",
                        "Content-Type": "text/plain;charset=UTF-8",
                        "DNT": "1",
                        "Host": "",
                        "Origin": "",
                        "Referer": "",
                        "TE": "Trailers",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}

route_search_params = {"jsonrpc": "2.0",
                       "id": "3",
                       "method": "searchAdvanced",
                       "params": [{"bounds": {"min": {"lat": 50.400370273479346,
                                                      "lon": 4.974064280094581},
                                              "max": {"lat": 52.118895633404020,
                                                      "lon": 6.819767405094581}},
                                   "type.id": 2,
                                   "score.min": 0.5,
                                   "bounds.comparator": "geometry"},
                                  "null",
                                  20,
                                  0,
                                  {"clusters": "false",
                                   "addLanguage":"en",
                                   "media": "true",
                                   "description": "true"}]}
route_search_data = {"mimeType": "text/plain;charset=UTF-8",
                     "params": [],
                     "text": "{\"jsonrpc\":\"2.0\",\"id\":\"4942\",\"method\":\"searchAdvanced\",\"params\":[{\"bounds\":{\"min\":{\"lat\":50.400370273479346,\"lon\":4.974064280094581},\"max\":{\"lat\":52.11889563340402,\"lon\":6.819767405094581}},\"type.id\":2,\"score.min\":0.5,\"bounds.comparator\":\"geometry\"},null,20,0,{\"clusters\":false,\"addLanguage\":\"en\",\"media\":true,\"description\":true}]}"}
default_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
                   "Connection": "test",
                   "Cookie": "rtysid=5gf59rik6gf8o7b5an7nalcsh0; "
                             "_ga=GA1.2.1811204879.1553438381; _"
                             "gid=GA1.2.1815573989.1553438381; __"
                             "gads=ID=fab95f7aaf65227e:T=1553438384:S=ALNI_MaIjkdo1dKpYiyQKfWZEymqT7HgUQ",
                   "Host": "",
                   "Referer": "",
                   "TE": "Trailers",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"}


# Setup script
response = requests.post(url=route_search_url, headers=route_search_headers,
                         data=route_search_data)


rows_list = []
input_rows = [1, 2, 3]
download_to_file(route_url, default_headers, filepath)
for row in input_rows:

    layer = fiona.open(filepath, layer='tracks')
    geom = layer[0]
    route_name = geom['properties']['name']
    route_geodata = {'type': 'MultiLineString',
                     'coordinates': geom['geometry']['coordinates']}
    print(route_geodata)
    route_geometry = shape(route_geodata)
    route_dict = {'name': route_name,
                  'geometry': route_geometry}
    rows_list.append(route_dict)


routes_gdf = gpd.GeoDataFrame(rows_list)
routes_gdf.crs = {'init': 'epsg:4326', 'no_defs': True}
routes_gdf.to_file(filename=output_filepath, driver="GeoJSON")

routes_gdf.plot()
plt.show()




