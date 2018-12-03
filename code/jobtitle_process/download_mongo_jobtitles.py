#!/usr/bin/env python

import pymongo
import csv


def copy_dict_byfields(post, fields_to_copy):
    dct={}
    for fld in fields_to_copy:
        dct[fld]=post[fld]
    return dct


url="mongodb://user:indeedjob@ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase"
client = pymongo.MongoClient(url)
db=client["appDatabase"]
collection=db["jobs"]
print(12)
posts=collection.find({},{"job_title":1, "query_jobtyp_explvl":1, "query_keywords":1})
list_cleaned_jds=[]
list_jobs=[]  # list of dict, '_id', 'query_keyword', 
vocab=set()
cnt=0
maxcnt=100
fields_to_copy=['_id', 'query_jobtyp_explvl', "job_title", "query_keywords"]
for post in posts:
    cnt+=1
    if(cnt>maxcnt):
        break
    list_jobs.append(copy_dict_byfields(post, fields_to_copy))
    for w in jd_cleaned:
        vocab.add(w)

with open("jobs_infos.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=fields_to_copy)
    writer.writeheader()
    for row in list_jobs:
        writer.writerow(row)
