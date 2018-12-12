#!/usr/bin/env python

import re
from collections import defaultdict
import pickle
import csv

# read dict_location: location, count. 
def read_location_csv(csvfile):
    dct={}
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            dct[row[0]] = int(row[1])
    return dct

# replace " " by "+";  remove (); remove zip (to make it coarse)
# return dict_cleaned (location -> count); list_match = [ (location, cleaned_location) ]
def clean_dict_location(dict_location):
    dict_new=defaultdict(lambda:0)
    list_match = []
    for key in dict_location.keys():
        cleaned = re.sub(r"\(.*\)", "", key).strip()
        cleaned = re.sub(r"\d", "", cleaned).strip()
        cleaned = re.sub(r" +", "+", cleaned)
#        if("(" in key):
#           print((key, cleaned))
        dict_new[cleaned] += dict_location[key]
        list_match.append((key, cleaned))
    return dict_new, list_match

def output_dict_location(csvfile, dict_location):
    list_word_cnt = sorted(dict_location.items(), key=lambda x:-x[1])
    with open(csvfile,"w") as f:
        writer = csv.writer(f)
        for wc in list_word_cnt:
            writer.writerow(wc)

def output_list_match(csvfile, list_match):
    with open(csvfile,"w") as f:
        writer = csv.writer(f)
        for ab in list_match:
            writer.writerow(ab)

dct=read_location_csv("job_locations.csv")
dct_cleaned, list_match = clean_dict_location(dct) 
print(len(dct))
print(len(dct_cleaned))
print(len(list_match))
print(list_match[0:2])
output_dict_location("job_locations_cleaned.csv", dct_cleaned)  # for google geocoding api
output_list_match("job_location_match.csv", list_match)
