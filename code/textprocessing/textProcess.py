#!/usr/bin/env python

import pymongo
import pprint
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class textProcess:

    def __init__(self, url_mongod, name_database, name_collection):
        self.name_collection = name_collection
        self.client = pymongo.MongoClient(url_mongod)
        self.name_database = name_database

    def preprocess(self):
        c = 1
        l = []
        collection = self.client[self.name_database][self.name_collection]
        #pprint.pprint(self.client[self.name_database][self.name_collection].find_one())
        for post in collection.find({'query_jobtyp_explvl':'fulltime+senior_level'}): #iterate through each document
            #pprint.pprint(post['query_jobtyp_explvl'])
            print(c,"\n")
            jd = post['job_description']
            removed = self.removeStopWords(jd)
            l.extend(removed)
            #print(removed)
            c = c+1
        #print(l)
        self.generate_word_cloud(l)
    def stop_words(self):
            s = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
            l = s.split()
            l1 = [w.replace("'","") for w in l] #remove apostrophes
            return l1


    def removeStopWords(self,line):
            wordsList = line.split()
            wordsList = [re.sub(r'\W+', '', word) for word in wordsList] #remove alphanumeric character
            filtered = filter(lambda word: re.match(r'\w+', word), wordsList) #atleast of length 1
            words_lower = [word.lower() for word in filtered] #convert to lower case
            clean_words_any = [re.sub("[^a-z]", "",word) for word in words_lower] #remove special characters
            clean_words = filter(lambda word: re.match(r'\w+', word), clean_words_any) #atleast of length 1 after removing the special characters
            stop_words_list = self.stop_words() #get the stop words
            filtered_words = list(filter(lambda word: word not in stop_words_list, clean_words)) #check for stop words
            #s = ''.join(filtered_words) #convert list to string
            return filtered_words

    def generate_word_cloud(self,l):
           #convert list to string and generate
           unique_string=(" ").join(l)
           wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
           plt.figure(figsize=(15,8))
           plt.imshow(wordcloud)
           plt.axis("off")
           plt.savefig("job_wordcloud"+".png", bbox_inches='tight')
           plt.show()
           plt.close()

if __name__ == "__main__":
            w = textProcess("mongodb://user:indeedjob@ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase", "appDatabase", "jobs")
            w.preprocess()
