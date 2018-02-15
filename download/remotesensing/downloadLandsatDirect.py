## Load Libraries
import pycurl
import sys
import os.path
import re

## Urls to public google earth engine repositories of Landsat
urls = 
[
'http://storage.googleapis.com/earthengine-public/landsat/L8/233/073/LC82330732013310LGN00.tar.bz',
'http://storage.googleapis.com/earthengine-public/landsat/L8/233/073/LC82330732015284LGN00.tar.bz'
]

## Download from URL to data repository
def download(url):
    filename = url.rsplit('/', 1)[-1] # split string based on slash and get tail
    filepath = "./data/" + filename
    if os.path.exists(filepath)==True: # if file exists, no download
        print("File already exists at:\n", filepath)
    else: # if file does NOT exist, do download
        print("Downloading data from:\n", url)
        fp = open(filepath, "wb")
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, fp)
        c.perform()
        c.close()
        fp.close()
        print("Extracted to location:\n", filepath)


skip = True
## Download data per url
for url in urls:
    if skip == True: # Skip first argument, because it has Python script location
        skip = False
        continue
    if type(url) != type("str"):
        raise ValueError("Oops! That was no valid string format. Did you provide the URL to download as a string?")
    download(url) 
