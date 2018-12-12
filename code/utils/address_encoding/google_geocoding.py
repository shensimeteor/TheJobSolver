#!/usr/bin/env python
#by google map geocoding

import requests
import json
import csv
# remove it before submit
key=""


# read dict_location: location, count. 
def read_location_csv(csvfile):
    lst=[]
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            lst.append(line)
    return lst

# location should be pre-processed, i.e. no " " in location
# return (lon,lat)
def request_lonlat(google_apikey, location):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(location, google_apikey)
    response = requests.get(url)
    try:
        dict_res = json.loads(response.text)
        lon = float(dict_res["results"][0]["geometry"]["location"]["lng"])
        lat = float(dict_res["results"][0]["geometry"]["location"]["lat"])
        return (lon,lat)
    except Exception as e:
        print(e)
        return None
        



list_location=read_location_csv("job_locations_cleaned.csv")
with open("job_locations_cleaned_lonlat.csv", "w") as f:
    cnt=0
    writer = csv.writer(f)
    for loc,tmp in list_location:
        cnt+=1
        lonlat = request_lonlat(key, loc)
        if (lonlat):
            lon,lat = lonlat
            print("%d, %s, %s" %(cnt, loc, str(lonlat)))
        else:
            lon=None
            lat=None
            print("%d, %s, %s" %(cnt, loc, "(None,None)"))
        writer.writerow((loc,lon,lat))

