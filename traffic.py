#!/usr/bin/python2.7

""" Collection of traffic data for trafeo """
import urllib
import urllib2
import time
import datetime
import sys

# Set the request headers
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d %H:%M:%S')
request_headers = {
	"Connection": "keep-alive",
	"Transfer-Encoding": "chunked",
	"Cache-Control": "private, no-cache, no-store, max-age=0, must-revalidate",
	"Content-Language": "en-US",
	"Content-Type": "application/json;charset=utf-8",
	"API-Key": "x4w2zaauuqg5mmrxtpe22njp",
	"Application-Key": "Trafeo",
    "Date": timestamp
}

# API Key (@TODO: get it from secure repo, or inject it on the fly)
key = 'x4w2zaauuqg5mmrxtpe22njp';
# Style to be used in subsequent traffic tile calls
style = {'traffic tubes with chevrons': 's1', 'plain lines': 's2', 'plain lines with slightly less glow': 's3'}	
# Minimum Y value/latitude for the bounding box (currectly for NL only)
minY = 50.75
# Minimum X value/longitude for the bounding box (currectly for NL only)
minX = 3.3
# Maximum Y value/latitude for the bounding box (currectly for NL only)
maxY = 53.58
# Maximum X value/longitude for the bounding box (currectly for NL only)
maxX = 7.23
# Zoom level (0 - 18)
zoom = 10
# Reference value for the state of traffic at a particular time, obtained from the Viewport API call. Use -1 to get the most recent traffic information.
traffic_model_id = -1
# Response content type
content_type = 'json'	
# Language of cause and description fields for traffic incidents returned. Default: English.
language = 'en'
# Projection for input and output coordinates. Default: EPSG900913.
projection = 'EPSG4326'	

# Traffic api provider url
url = "https://api.tomtom.com/lbs/services/trafficIcons/3/%s/%2.2f,%2.2f,%2.2f,%2.2f/%d/%d/%s" % (style['plain lines'], minY, minX, maxY, maxX, zoom, traffic_model_id, content_type)

values = {
    'key' : key,
    'projection' : projection,
    'language' : language
}

data = urllib.urlencode(values)

# Send the GET request
req = urllib2.Request(url + '?' + data)

# Read the response
try: 
	response = urllib2.urlopen(req).read()
except urllib2.URLError as e:
    print e.code
    print e.read()

#resp = urllib2.urlopen(req).read()
print response
