#!/usr/bin/env python

import pymongo
import csv
import glob

def copy_dict_byfields(post, fields_to_copy):
    dct={}
    for fld in fields_to_copy:
        dct[fld]=post[fld]
    return dct

def read_dict_labeled_idjts(dir_labeled_idjts):
    labeled_idjts_files = glob.glob(dir_labeled_idjts + "/*.txt")
    dict_labeled_idjts = dict([])
    for lfile in labeled_idjts_files:
        label=lfile.split("/")[-1].split(".")[0]
        with open(lfile, "r") as f:
            lines=f.readlines()
            lst=[]
            for line in lines[1:]:
                lst.append(tuple(line.strip().split(',')))
            dict_labeled_idjts[label]=lst
    return dict_labeled_idjts

#read labeled files
dict_labeled_idjts = read_dict_labeled_idjts("labeled_results/")

url="mongodb://user:indeedjob@ec2-52-55-205-188.compute-1.amazonaws.com/appDatabase"
client = pymongo.MongoClient(url)
db=client["appDatabase"]
collection=db["jobs"]
collection.create_index("job_title_label")
# update
for label in dict_labeled_idjts.keys():
    print("uploading label= %s" %label)
    for jid, jt in dict_labeled_idjts[label]:
        collection.update({"_id": jid}, {"$set": {"job_title_label": label}})


