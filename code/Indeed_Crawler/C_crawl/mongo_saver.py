#!/usr/bin/env python

import pymongo
'''
fields: query_keywords, query_location, query_jobtyp_explvl, job_title, jk(_id), job_location, company, job_description
'''

class MongoSaver:
    
    def __init__(self, url_mongod, name_database, name_collection):
        self.name_collection = name_collection
        self.client = pymongo.MongoClient(url_mongod)
        self.name_database = name_database

    def init_collection(self):
        self.db=self.client[self.name_database]
        self.collection=self.db[self.name_collection]
        self.collection.create_index("query_keywords")
        self.collection.create_index("query_jobtyp_explvl")
        self.collection.create_index("job_title")
        self.collection.create_index("job_location")
        self.collection.create_index("company")

    def insert(self, dct):
        self.collection.save(dct)


if __name__ == "__main__":
    saver=MongoSaver("mongodb://user:indeedjob@localhost/appDatabase", "appDatabase", "jobs")
    saver.init_collection()
    import glob
    import re
    pattern=re.compile("q=([^&]*)&l=([^&]*)&jt=(.*)")
    # done uploading: software+engineer, data+scientist
    # dirs_to_upload=["output/data+engineer/", "output/autonomous+vehicle/", "output/business+analyst/", "output/data+analyst/", 
    # "output/devops+engineer/", "output/machine+learning/", "output/product+manager/", "output/quality+assurance/", "output/ui+ux+designer/"]
    # todo: output/system+administrator
    dirs_to_upload=["output/system+administrator/", "output/database+administrator/", "output/game+software+engineer/", "output/embedded+software+engineer/", "output/robotics+software+engineer/", "output/network+engineer/"] 
    for dirx in dirs_to_upload:
        txtfiles=glob.glob(dirx+"*.txt")
        for txtf in txtfiles:
            print(txtf)
            with open(txtf,"r") as f:
                content=f.readlines()
            url = content[0]
            print(url)
            x=pattern.search(url)
            query_word=x.group(1)
            query_location=x.group(2)
            query_jobtyp_explvl=x.group(3).replace('&explvl=', '+')
            jk = content[1]
            job_title=content[2]
            company=content[3]
            job_location=content[4]
            dct={}
            dct["query_keywords"]=query_word.replace("+", " ")
            dct["query_location"]=query_location.replace("+", " ")
            dct["query_jobtyp_explvl"]=query_jobtyp_explvl
            dct["job_title"]=job_title.strip()
            dct["_id"]=jk.strip()
            dct["company"]=company.strip()
            dct["job_location"]=job_location.strip()
            dct["job_description"]="".join(content[5:])
            #print(dct)
            saver.insert(dct)
    

        
         
