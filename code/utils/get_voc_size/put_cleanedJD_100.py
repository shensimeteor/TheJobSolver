#!/usr/bin/env python
import pymongo

field="job_description_cleaned2"
# update
#for label in dict_labeled_idjts.keys():
#    print("uploading label= %s" %label)
#    for jid, jt in dict_labeled_idjts[label]:
#        collection.update({"_id": jid}, {"$set": {"job_title_label": label}})

limit=100
words=set()
with open("vocab_cleanedJD.csv", "r") as f:
    for line in f.readlines():
        w,c=line.strip().split(',')
        if(int(c) >= limit):
            words.add(w)
print(len(words))
            

url="mongodb://user:indeedjob@localhost:27017/appDatabase"
client = pymongo.MongoClient(url)
db=client["appDatabase"]
collection=db["jobs"]
posts=collection.find({"job_title_label": {"$ne": "unknown"}})

for post in posts:
    jid = post["_id"]
    jd_cleaned = post["job_description_cleaned"]
    jd_cleaned2 = [x for x in jd_cleaned if x in words]
    print("%s, cleanedout: %d" %(jid, len(jd_cleaned) - len(jd_cleaned2)))
    collection.update({"_id": jid}, {"$set": {field: jd_cleaned2}})
