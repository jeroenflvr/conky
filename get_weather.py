#!/usr/bin/python
# -*- coding: utf-8 -*-
###### using https://openweathermap.org/api for free #########

from __future__ import division
import requests
from pprint import pprint
import json
import sys,getopt
import time
from calendar import timegm
import os

sentinel_file = "sentinel_file"
openweathermap_api_key = '4c972b1ae53fd6c982664615b3d69f8d'
sentinel_valid_time = 3600

#https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    #ix = int((d + 11.25)/22.5)
    ix = int((d + 11.25)/22.5 - 0.02)
    return dirs[ix % 16]

def store_sentinel(s):
  f = open(sentinel_file, "w")
  json.dump(s,f)
  f.close

def get_sentinel():
  f = open(sentinel_file, "r")
  return json.load(f)

def sentinel_exists():
  return os.path.isfile(sentinel_file)

def sentinel_changetime():
  return os.path.getmtime(sentinel_file)

def fetch_weather_from_api():
    url = "https://api.openweathermap.org/data/2.5/find?q=brussels,be&units=metric&appid=" + openweathermap_api_key

    headers = {
     'accept': "application/json",
     'authorization': "Bearer " + openweathermap_api_key,
     'cache-control': "no-cache",
    }
    querystring = ""
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data


def main(argv):
    data = ""
    if sentinel_exists():
      if time.time() - sentinel_changetime() > sentinel_valid_time:
        data = fetch_weather_from_api()
        store_sentinel(data)
      else:
        data = get_sentinel()
    else:
      data = fetch_weather_from_api()
      store_sentinel(data)
#    print(data)
    if "desc" in sys.argv:
      print (str(data["list"][0]["weather"][0]["description"]) )
    if "id" in sys.argv:
      print (str(data["list"][0]["weather"][0]["id"]) )
    if "wind" in sys.argv:
      print (str(data["list"][0]["wind"]["speed"]*3.6) + "km/h " + str(degrees_to_cardinal(data["list"][0]["wind"]["deg"])))
    if "temp" in sys.argv:
      print (str(data["list"][0]["main"]["temp"]) + '°C')
    if "temp_min_max" in sys.argv:
      print ("Min: " + str(data["list"][0]["main"]["temp_min"]) + '°C' + "\tMax: " + str(data["list"][0]["main"]["temp_max"]) + '°C')

    exit()

if __name__ == "__main__":
   main(sys.argv[1:])
