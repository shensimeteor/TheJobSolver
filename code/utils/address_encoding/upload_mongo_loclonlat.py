#!/usr/bin/env python
import pymongo
import csv
# upload job_location_cleaned 

# dict:  original -> cleaned
def read_dict_match(match_file):
    dct={}
    with open(match_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            dct[row[0]] = row[1]
    return dct

# dict: location (cleaned) -> [lon, lat]
def read_dict_loclonlat(loclonlat_file):
    dct={}
    with open(loclonlat_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            dct[row[0]] = [float(row[1]), float(row[2])]
    return dct


dict_match = read_dict_match("job_location_match.csv")
dict_loclonlat = read_dict_loclonlat("job_locations_cleaned_lonlat.csv")


url="mongodb://user:indeedjob@localhost:27017/appDatabase"
client = pymongo.MongoClient(url)
db=client["appDatabase"]
collection=db["jobs"]
collection.create_index("job_location_cleaned")
collection.create_index("job_location_lonlat2")

posts=collection.find({}, {"_id":1, "job_location":1})
for post in posts:
    jid = post["_id"]
    loc = post["job_location"].encode("ascii", "ignore")
    cleaned_loc = dict_match[loc]
    lonlat = dict_loclonlat[cleaned_loc]
    print((jid, loc, cleaned_loc, lonlat))
    collection.update({"_id": jid}, {"$set": {"job_location_cleaned":cleaned_loc, "job_location_lonlat2": lonlat}})
