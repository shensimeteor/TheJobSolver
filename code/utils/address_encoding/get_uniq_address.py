#!/usr/bin/env python

import pymongo
import csv
from collections import defaultdict

def copy_dict_byfields(post, fields_to_copy):
    dct={}
    for fld in fields_to_copy:
        dct[fld]=post[fld]
    return dct


url="mongodb://user:indeedjob@ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase"
client = pymongo.MongoClient(url)
db=client["appDatabase"]
collection=db["jobs"]
posts=collection.find({},{"job_location":1})
set_words=defaultdict(lambda:0)
cnt=0
for post in posts:
    cnt+=1
    w = post["job_location"].encode("ascii", "ignore")
    if(cnt%100==0):
        print(cnt)
    set_words[w]+=1
list_word_cnt = sorted(set_words.items(), key=lambda x:-x[1])
print(cnt)
print(len(list_word_cnt))
with open("job_locations.csv","w") as f:
    writer=csv.writer(f)
    for wc in list_word_cnt:
        writer.writerow(wc)
