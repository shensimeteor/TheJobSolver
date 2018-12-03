#!/usr/bin/env python
import pymongo
import pickle
class VecdataMongoGetter:
    def connect(self, url="mongodb://user:indeedjob@ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase", db_name="appDatabase", collection_name="test"):
        self.client = pymongo.MongoClient(url)
        self.db=self.client[db_name]
        self.collection=self.db[collection_name]

    def getVector(self, word):
        doc=self.collection.find_one({"word": word})
        if(doc):
            return doc["vector"]
        else:
            return None


def dump_pickle(data,pkl_file):
    with open(pkl_file, "wb") as f:
        pickle.dump(data, f, 1)

# write a file, each line has a word
def write_word_perline(filename, words):
    with open(filename, "w") as f:
        for w in words:
            f.write("%s\n" %w)

def read_word_perline(filename):
    words=[]
    with open(filename, "r") as f:
        words=f.readlines()
    words=[w.strip() for w in words]
    return words

if __name__ == "__main__":

    list_vocab=read_word_perline("words_list.txt")
    print("total vocab=%d" % len(list_vocab))

    getter=VecdataMongoGetter()
    getter.connect(collection_name="vecdata_wiki_news")

#    x=getter.collection.find_one({"word":"wwweeocgovemployersuploadeeocselfprintposterpdf"})
#    print(x)
#    print(type(x))
#    if(x):
#        print("not none")

    word_vec=[]  # [ [word, vect] ]
    word_miss=[]
    for w in list_vocab:
        vec = getter.getVector(w)
        if(vec):
#            print("get vector: %s" %w)
            word_vec.append([ w, vec] )
        else:
#            print("miss vector: %s" %w)
            word_miss.append(w)

    print("word_vec size=%d"% len(word_vec))
    print("word_miss size=%d"% len(word_miss))
    write_word_perline("missed_word.txt", word_miss)
    dump_pickle(word_vec, "wordvectors.pkl")
        
        
     
