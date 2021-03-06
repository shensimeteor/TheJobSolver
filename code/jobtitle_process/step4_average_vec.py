#!/usr/bin/env python
from collections import defaultdict
import pickle
import pandas as pd
import numpy as np
import math

# dict: word -> vector
def load_pickle_to_dict(filename):
    with open(filename, "rb") as f:
        lst=pickle.load(f)
    dct=dict([])
    for word, vec in lst:
        dct[word] = vec
    return dct


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


# input: jts (job_titles, list of n str), dict_wordvec (the dictionary to get word-vectors), method: average
# return: list_jt_vec (list of [indx, jobid, job_title, vec_nparray]), list_missed_jt [indx, jobid, job_title])
# Special: if no word in a job-title can't be found in dict_wordvec, then the embedding is all NaN
def calc_jts_wordvec_matrix(jobids, jts, dict_wordvec, method, word_idf=None, manual_wgt=None):
    list_jt_vector = []  # [indx, jobid, job_title, vector (array) ]
    list_jt_missed = []  # [indx, jobid, job_title ]
    jt_vectors_allmean = np.zeros((300,),np.float)
    for i, jt in enumerate(jts):
        job_id = str(jobids[i])
        jt=str(jt)
        if(not jt.strip()):
            list_jt_missed.append( (i, job_id, jt) )
            continue
        vecs = []
        words_in_jt=[]
        for w in jt.split():
            if w in dict_wordvec:
                vec = dict_wordvec[w]
                vecs.append(vec)
                words_in_jt.append(w)
        if(len(vecs) > 0): # at least 1 word in the job title, has vector
            array_vecs = np.array(vecs)
            if(method == "average"):
                jt_vec = np.average(array_vecs, axis=0)
            elif(method == "idf_wgt_avg"):
                if(not word_idf):
                    print("Error, must provide word_idf if use idf_wgt_avg")
                    exit(0)
                wgts = [math.sqrt(word_idf[w]) for w in words_in_jt]
                jt_vec = np.average(array_vecs, axis=0, weights=wgts)
            elif(method == "manual_wgt_avg"):
                if(not manual_wgt):
                    print("Error, must provide manual_wgt if use manual_wgt")
                    exit(0)
                wgts = [manual_wgt[w] for w in words_in_jt]
                jt_vec = np.average(array_vecs, axis=0, weights=wgts)
            list_jt_vector.append( (i, job_id, jt, jt_vec) )
        else:
            jt_vec = None
            list_jt_missed.append( (i, job_id, jt) )
    return (list_jt_vector, list_jt_missed)
    

def output_csv_jt_vectorized(list_jt_vector, outfile):
    df=pd.DataFrame()
    df["_id"] = [x[1] for x in list_jt_vector]
    df["idx"] = [x[0] for x in list_jt_vector]
    df["job_title"] = [x[2] for x in list_jt_vector]
    df["vector"] = [x[3] for x in list_jt_vector]
    df.to_csv(outfile)

def output_csv_jt_missed(list_jt_vector, outfile):
    df=pd.DataFrame()
    df["_id"] = [x[1] for x in list_jt_vector]
    df["idx"] = [x[0] for x in list_jt_vector]
    df["job_title"] = [x[2] for x in list_jt_vector]
    df.to_csv(outfile)

def dump_pickle_jt_vectorized(list_jt_vector, outfile):
    with open(outfile, "wb") as f:
        pickle.dump(list_jt_vector, f, 1)


#dict: word -> idf
def get_word_idf_dict(jts):
    word_doc_count=dict([])  # word -> doc word 
    for jt in jts:
        words_added_in_this_doc=set([])
        for w in str(jt).split():
            if(w in words_added_in_this_doc):
                continue
            if w in word_doc_count:
                word_doc_count[w] += 1
            else:
                word_doc_count[w] = 1
            words_added_in_this_doc.add(w)
    n_collection=len(jts)
    word_idf=dict([])
    for k in word_doc_count.keys():
        word_idf[k] = math.log( n_collection *1.0 / word_doc_count[k])
    return word_idf
        
                

    
# read job titles --> jts (cleaned)
df = pd.read_csv("jobs_infos_cleaned3_filter5.csv")
jts = df["cleaned_job_title"].tolist()
jobids = df["_id"].tolist()
print(jts[0:5])
print(jobids[0:5])

# read word-vec dict
dict_wordvec = load_pickle_to_dict("wordvectors.pkl")

# tf-df weightavg is bad
#word_idf=get_word_idf_dict(jts)

# calculate job title vectors by averaging vectors of each word in this job title
#list_jt_vector, list_jt_missed = calc_jts_wordvec_matrix(jobids, jts, dict_wordvec, "idf_wgt_avg", word_idf=word_idf)
list_jt_vector, list_jt_missed = calc_jts_wordvec_matrix(jobids, jts, dict_wordvec, "average")
#manual_wgt=defaultdict(lambda: 1.0)
#manual_wgt["consultant"] = 0.5
#manual_wgt["associate"] = 0.5
#manual_wgt["specialist"] = 0.5
#manual_wgt["assistant"] = 0.5
#manual_wgt["director"] = 0.5
#list_jt_vector, list_jt_missed = calc_jts_wordvec_matrix(jobids, jts, dict_wordvec, "manual_wgt_avg", manual_wgt=manual_wgt)




print("total jobs=%d" %len(jts))
print("vectorized jobs=%d" %len(list_jt_vector))
print("missed jobs=%d" %len(list_jt_missed))


#dump_pickle_jt_vectorized(list_jt_vector, "jt_idfwgtavg_vector.pkl")
dump_pickle_jt_vectorized(list_jt_vector, "jt_vector.pkl")
#dump_pickle_jt_vectorized(list_jt_vector, "jt_manualwgt_vector.pkl")
output_csv_jt_missed(list_jt_missed, "jt_missed.csv")


