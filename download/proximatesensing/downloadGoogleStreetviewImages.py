#!/usr/bin/env python2
## Document information
__author__ = "Adrian Letchford <http://www.dradrian.com>"
__modifiedby__ = "David Swinkels"
__github__ = "davidswinkels"
__purpose__ = "Part of MSc thesis Geo-Information Science at Wageningen University"
__status__ = "Production"

"""
This is a light module for downloading photos from Google street view. The
functions allow you to retrieve current and **old** photos.

The photos on Google street view are panoramas and are refered to as such.
However, you have the option of downloading flat photos, or panoramas.

Retrieving photos is a two step process. First, you must translate GPS
coordinates into panorama ids. The following code retrieves a list of
the closest panoramas giving you their id and date:

>>> import streetview
>>> panoids = streetview.panoids(lat, lon)

You can then use the panorama ids to download photos with the following
function:

>>> streetview.api_download(panoid, heading, flat_dir, key)

"""

## Load modules
import re
from datetime import datetime
import requests
import time
import shutil
import itertools
from PIL import Image
from io import BytesIO
import os
import math
import urllib, urllib2
import pandas as pd

## Store streetview_key as a variable
STREETVIEW_KEY = "" ## Provide YOUR API key HERE!!
STREETVIEW_KEY2 = "" ## Provide YOUR API key HERE!!
STREETVIEW_KEY3 = "" ## Provide YOUR API key HERE!!

## Define variables for downloading streetview images
input_csv = './input/building_points.csv'
result_csv = './data/building_points_1_124818.csv'
iterations = 1
start_iteration = 33974

def _panoids_url(lat, lon):
    """
    Builds the URL of the script on Google's servers that returns the closest
    panoramas (ids) to a give GPS coordinate.
    """
    url = "https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{0:}!4d{1:}!2d50!3m10!2m2!1sen!2sGB!9m1!1e2!11m4!1m3!1e2!2b1!3e2!4m10!1e1!1e2!1e3!1e4!1e8!1e6!5m1!1e2!6m1!1e2&callback=_xdc_._v2mub5"
    return url.format(lat, lon)



def _panoids_data(lat, lon):
    """
    Gets the response of the script on Google's servers that returns the
    closest panoramas (ids) to a given GPS coordinate.
    """
    url = _panoids_url(lat, lon)
    return requests.get(url)

def _panoids(lat, lon):
    """
    Gets the closest panoramas (ids) to the GPS coordinates.

    """

    resp = _panoids_data(lat, lon)

     # Only select google panoramas
    pans = re.findall('\[[0-9]+,"(.+?)"\].+?Google"\]\]\]\].+?\[\[null,null,(-?[0-9]+.[0-9]+),(-?[0-9]+.[0-9]+)', resp.text)
    pans = [{
        "panoid": p[0],
         "lat": float(p[1]),
         "lon": float(p[2])} for p in pans]  # Convert to floats
    if len(pans) > 0:
        for i in range(0, len(pans)):
            url = "https://maps.googleapis.com/maps/api/streetview/metadata?pano=" + pans[i]['panoid'] + "&key=AIzaSyC2mpaxCQ5okgt_DOa4NMgJyLLKHFfqGqI"
            metadata = eval(urllib2.urlopen(url).read())
            pans[i].update({'year': int(metadata['date'][:4]), 'month': int(metadata['date'][-2:])})
      
        # Sort the pans array from newest year to oldest year
        def func(x):
            if 'year'in x:
                return datetime(year=x['year'], month=x['month'], day=1)
            else:
                return datetime(year=1000, month=1, day=1)
        pans.sort(key=func, reverse =True)
   
        # Select recent panorama	
        for i in range(0, len(pans)):
	    if pans[i]['year'] == 2016:
                pan = pans[i]
	        print "Pano: " + str(pans[i])
		return pan
            if pans[i]['year'] == 2015:
		pan = pans[i]
		print "Pano: " + str(pans[i])
		return pan
            if pans[i]['year'] == 2014:
		pan = pans[i]
		print "Pano: " + str(pans[i])
		return pan
            if pans[i]['year'] == 2013:
		pan = pans[i]
		print "Pano: " + str(pans[i])
		return pan
            if pans[i]['year'] == 2012:
		pan = pans[i]
		print "Pano: " + str(pans[i])
		return pan
            if pans[i]['year'] == 2011:
		pan = pans[i]
		print "Pano: " + str(pans[i])
		return pan
            if pans[i]['year'] == 2010:
		pan = pans[i]
		print "Pano: " + str(pans[i])
		return pan
            else:
		print "Pano: No panorama available on this location for 2016-2010"
    else:
        print "Pano: No panorama available on this location"


def _calc_degrees(opposite, adjacent):
    """
    Calculates angle in degrees with inverse tangens based on length of opposite and adjacent sides
    """
    return math.degrees(math.atan(abs(opposite) / abs(adjacent)))


def _calc_heading(lat_street, lon_street, lat_object, lon_object):
    """
    Calculate heading based on streetview location and object location
    
    :param lat_street, lon_street: location of streetview image in double format
    :param lat_object, lon_object: location of object in double format
    :param direction: text that describes direction (e.g. "North", "Northeast")
    :param heading: heading indicates the compass heading of the camera. Accepted values are from 0 to 360 (both values indicating North, with 90 indicating East, and 180 South)
    """
 
    heading_lat = round(float(lat_object) - float(lat_street), 7)
    heading_lon = round(float(lon_object) - float(lon_street), 7)
    if (abs(heading_lat) > abs(heading_lon)):
        if heading_lat > 0.0:
            if heading_lon > 0.0:
                heading = _calc_degrees(heading_lon, heading_lat)
                direction = "Northeast"
            if heading_lon < 0.0:
                heading = 360.0 - _calc_degrees(heading_lon, heading_lat)
                direction = "Northwest"
        if heading_lat < 0.0:
            if heading_lon > 0.0:
                heading = 180.0 - (_calc_degrees(heading_lon, heading_lat))
                direction = "Southeast"
            if heading_lon < 0.0:
                heading = 180.0 + _calc_degrees(heading_lon, heading_lat)
                direction = "Southwest"
    if (abs(heading_lat) < abs(heading_lon)):
        if heading_lat > 0.0:
            if heading_lon > 0.0:
                heading = 90.0 - _calc_degrees(heading_lat,heading_lon)
                direction = "Northeast"
            if heading_lon < 0.0:
                heading = 270.0 + _calc_degrees(heading_lat,heading_lon)
                direction = "Northwest"
        if heading_lat < 0.0:
            if heading_lon > 0.0:
                heading = 90.0 + _calc_degrees(heading_lat,heading_lon)
                direction = "Southeast"
            if heading_lon < 0.0:
                heading = 270.0 - _calc_degrees(heading_lat,heading_lon)
                direction = "Southwest"
    if (abs(heading_lat) == abs(heading_lon)):
        if heading_lat > 0.0:
            if heading_lon > 0.0:
                heading = 45.0
                direction = "Northeast"
            if heading_lon < 0.0:
                heading = 315.0
                direction = "Northwest"
        if heading_lat < 0.0:
            if heading_lon > 0.0:
                heading = 135.0
                direction = "Southeast"
            if heading_lon < 0.0:
                heading = 225.0
                direction = "Southwest"
    if (heading_lat == 0.0):
        if heading_lon > 0.0:
            direction = "East"
            heading = 90.0
        if heading_lon < 0.0:
            direction = "West"
            heading = 270.0
        if heading_lon == 0.0:
            direction = "No direction to object; object is at viewing location"
            heading = "NA"
    if (heading_lon == 0.0):
        if heading_lat < 0.0:
            direction = "South"
            heading = 180.0
        if heading_lat > 0.0:
            direction = "North"
            heading = 0.0
    return direction, heading

def _calc_distance(lon1, lat1, lon2, lat2): 
    """ 
    Calculate the great circle distance between two points on the earth (specified in decimal degrees) 
    """ 
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2]) 

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2 
    c = 2 * math.asin(math.sqrt(a)) 
    radius = 6371000 
    # Radius of earth in meters. Use 3956 for miles 
    return c * radius

def download_streetview(lat_object, lon_object, neighbourhood_id, building_id, width = 640, height = 640):
    """
    Downloads streetview image for location at fov levels: 90, 60 and 30

    :param width: the width of the image in pixels
    :param height: the height of the image in pixels
    """
    pan = _panoids(lat = lat_object, lon = lon_object)
    if width > 640:
        width = 640
    if height > 640:
        height = 640
    size = str(width) + "x" + str(height)
    if type(pan) is dict:
        direction, heading = _calc_heading(lat_street = pan['lat'], lon_street = pan['lon'], lat_object = lat_object, lon_object = lon_object)
        for fov in [90, 60, 30]:
            url = "https://maps.googleapis.com/maps/api/streetview?size=" + size + "&pano=" + pan['panoid'] + "&heading=" + str(heading) + "&pitch=0&fov=" + str(fov) + "&key=" + STREETVIEW_KEY2
            filename = "N" + neighbourhood_id + "_B" + str(building_id) + "_P" + pan['panoid'] + "_F" + str(fov) + "_A00"
            savedir = "./data/" + neighbourhood_id[-4:] + "/"
            saveloc = savedir + filename + ".jpg"
            urllib.urlretrieve(url, saveloc)
            date = str(pan['year']) + "y" + "%02d" % pan['month'] + "m"	
        return pan['panoid'], pan['lat'], pan['lon'], date, heading
    else:
        return "N/A", "N/A", "N/A", "N/A", "N/A"


def download_streetview_loop(input_csv, result_csv, iterations, start_iteration):
    """
    Downloads streetview images by looping over observations from csv file

    :param input_csv: specifies the location of the input csv (e.g. './input/building_points.csv')
    :param result_csv: specifies the location of the result csv (e.g. './data/building_points_error.csv')
    :param iterations: specifies the amount of iterations performed in this loop
    :param start_iteration: specifies the starting iteration 
    """
    df = pd.read_csv(input_csv, sep = ',', header = 0)
    # Check if neighbourhood directories exist in data repository
    listBUCODES = df.BU_CODE.unique()
    for i in range(0, len(listBUCODES)):
        savedir = "./data/" + listBUCODES[i][-4:] + "/"
        if not os.path.exists(savedir):
	    os.makedirs(savedir)
    # Iterate over observations to download images, create metadata and multilabel, and save metadata and multilabel
    for i in range(start_iteration,(start_iteration + iterations)):
        print "---- Row number (" + str(i) + ") ---- Iteration " + str(i - start_iteration) + " out of " + str(iterations) + " iterations (" + str(round(100.0*(i - start_iteration)/float(iterations),2)) + "%) ----"
        print "BU_CODE: " + str(df['BU_CODE'][i]) + ", Building ID: " + str(df['BuildingID'][i]) + ", Latitude: " + str(df['POINT_Y'][i]) + ", Longitude: " + str(df['POINT_X'][i])
        pano_id, pano_lat, pano_lon, pano_date, heading = download_streetview(lat_object = df['POINT_Y'][i], lon_object = df['POINT_X'][i], neighbourhood_id = df['BU_CODE'][i], building_id = df['BuildingID'][i])
        df_result = pd.read_csv(result_csv, sep = ',', header = 0) 
        if pano_id == "N/A":
            df_result.set_value(index = i, col = ['state_download'], value = "Download tried")
            df_result.set_value(index = i, col = ['state_error'], value = "Download fail")
            download_text = "Unsuccessful download"
        else:
            filename = "N" + df['BU_CODE'][i] + "_B" + str(df['BuildingID'][i]) + "_P" + pano_id
            distance = str(round(_calc_distance(lon1 = df['POINT_X'][i], lat1 = df['POINT_Y'][i], lon2 = pano_lon, lat2 = pano_lat), 2)) + ' m'
            metadata = {}
            metadata['neighbourhood_id'] = df['BU_CODE'][i]
            metadata['building_id'] = df['BuildingID'][i]
            metadata['building_year'] = df['Bouwjaar'][i]
            metadata['building_update'] = df['BeginDatum'][i]
            metadata['building_lat'] = df['POINT_Y'][i]
            metadata['building_lon'] = df['POINT_X'][i]
            metadata['pano_id'] = pano_id
            metadata['pano_date'] = pano_date
            metadata['pano_lat'] = pano_lat
            metadata['pano_lon'] = pano_lon   
            metadata['distance'] = distance
            metadata['heading'] = round(heading,2)
            metadata['coordinate_system'] = "WGS84 EPSG:4326"
            savedir = "./data/" + df['BU_CODE'][i][-4:] + "/"
            metadata_saveloc = savedir + filename + "_metadata.txt"
            with open(metadata_saveloc, "w") as metadata_file:
                metadata_file.write(str(metadata))
            label_saveloc = savedir + filename + "_label.txt"
            label = str(df['Residentia'][i]) + "\n" + str(df['Meeting'][i]) + "\n" + str(df['Healthcare'][i]) + "\n" + str(df['Industry'][i]) + "\n" + str(df['Office'][i]) + "\n" + str(df['Accommodat'][i])+ "\n" + str(df['Education'][i]) + "\n" + str(df['Sport'][i])   + "\n" + str(df['Shop'][i]) + "\n" + str(df['Other'][i])
            with open(label_saveloc, "w") as label_file:
                label_file.write(label)
            df_result.set_value(index = i, col = ['state_download'], value = "Download tried")
            df_result.set_value(index = i, col = ['state_error'], value = "Download success")
            df_result.set_value(index = i, col = ['pano_id'], value = pano_id)
            df_result.set_value(index = i, col = ['pano_date'], value = pano_date)
            df_result.set_value(index = i, col = ['pano_lat'], value = pano_lat)
            df_result.set_value(index = i, col = ['pano_lon'], value = pano_lon)
            df_result.set_value(index = i, col = ['distance'], value = distance)
            df_result.set_value(index = i, col = ['heading'], value = round(heading,2))
            download_text = "Successful download"
        df_result.to_csv(path_or_buf = result_csv, sep = ',', index = False)
        print download_text

#Write CSV file
#df_result = pd.read_csv('./input/building_points.csv', sep = ',', header = 0)
#df_result['state_download'] = "Not downloaded"
#df_result['state_error'] = "Not downloaded"
#df_result['pano_id'] = "Not available"
#df_result['pano_date'] = "Not available"
#df_result['pano_lat'] = 0.00
#df_result['pano_lon'] = 0.00   
#df_result['distance'] = "Not available"
#df_result['heading'] = 0.00
#df_result.to_csv(path_or_buf = './data/building_points_error35257.csv', sep = ',')

download_streetview_loop(input_csv = input_csv, result_csv = result_csv, iterations = iterations, start_iteration = start_iteration)

## Test:read dataframe building points
#import pandas as pd
#pd.read_csv('./input/building_points.csv', sep = ',', header = 0)

## Test:read dataframe building_points_error
#import pandas as pd
#pd.read_csv('./data/building_points_error.csv', sep = ',', header = 0)

## Test: _panoids
#df = pd.read_csv('./input/building_points.csv', sep = ',', header = 0)
#for i in range(0,10):
#    _panoids(df['POINT_Y'][i], df['POINT_X'][i])

## Test: Panoids supplied with one object
#lat_object = 48.853566
#lon_object = 2.349098
#pan = _panoids(lat_object, lon_object)
#lat_street = pan['lat']
#lon_street = pan['lon']
#heading, direction = _calc_heading(lat_street, lon_street, lat_object = lat_object, lon_object = lon_object)
#url = "https://maps.googl#eapis.com/maps/api/streetview?size=600x600&pano=" + pan['panoid'] + "&heading=" + str(heading) + "&pitch=0&fov=90" + "&key=" + STREETVIEW_KEY
#urllib.urlretrieve(url, "/home/david/Temp/temp.jpg")


