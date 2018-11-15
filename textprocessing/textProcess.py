#!/usr/bin/env python

import pymongo
import pprint
'''
fields: query_keywords, query_location, query_jobtyp_explvl, job_title, jk(_id), job_location, company, job_description
'''

class textProcess:

    def __init__(self, url_mongod, name_database, name_collection):
        self.name_collection = name_collection
        self.client = pymongo.MongoClient(url_mongod)
        self.name_database = name_database

    def print_one(self):
        collection = self.client[self.name_database][self.name_collection]
        #pprint.pprint(self.client[self.name_database][self.name_collection].find_one())
        for post in collection.find().limit(5): #iterate through each document
            pprint.pprint(post)

if __name__ == "__main__":
    w = textProcess("mongodb://user:indeedjob@ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase", "appDatabase", "jobs")
    w.print_one()
    #w.init_collection()
