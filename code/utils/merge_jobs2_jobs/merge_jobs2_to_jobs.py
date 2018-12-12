#!/usr/bin/env python
import pymongo

url="mongodb://user:indeedjob@localhost:27017/appDatabase"

client = pymongo.MongoClient(url)
db=client["appDatabase"]
jobs2=db["jobs2"]
jobs=db["jobs"]
posts=jobs2.find()

for post in posts:
    jid = post["_id"]
    imp_words = post["imp_words"]
    print((jid,imp_words))
    jobs.update({"_id": jid}, {"$set": {"tfidf_imp_words": imp_words}})
