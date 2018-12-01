#!/usr/bin/env python

import pymongo
import io


# field: "word" (string),  "vector" (array)
#  metadata collection, <collection_name>.meta (field: "note", to save some comments)
class VecdataMongoSaver:
    
    def __init__(self, url_mongod="mongodb://user:indeedjob@localhost/appDatabase", name_database="appDatabase", name_collection="test"):
        self.name_collection = name_collection
        self.client = pymongo.MongoClient(url_mongod)
        self.name_database = name_database

    def init_collection(self, note=None):
        print(self.name_database)
        print(self.name_collection)
        self.db=self.client[self.name_database]
        self.collection=self.db[self.name_collection]
        self.collection.drop()
        self.collection.create_index("word")
        if ( note):
            name_collection_meta=self.name_collection+"_meta"
            collection_meta=self.db[name_collection_meta]
            collection_meta.remove({})
            dct={}
            dct["note"] = note
            collection_meta.save(dct)

    def insert(self, dct):
        self.collection.save(dct)


if __name__ == "__main__":
    # read vecdata_file and save to collection_name under appDatabase
    vecdata_file="../vecdata/wiki-news-300d-1M.vec"
    collection_name="vecdata_wiki_news"

    saver=VecdataMongoSaver(name_collection=collection_name)
    saver.init_collection(vecdata_file)
    
    fin = io.open(vecdata_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    cnt=0
    for line in fin:
        tokens = line.rstrip().split(' ')
        word = tokens[0]
        vector = list(map(float, tokens[1:]))
        dct={}
        dct["word"] = word
        dct["vector"] = vector
        saver.insert(dct)
        cnt+=1
        if(cnt % 100 == 0):
            print("%d of %d"%(cnt, n))

