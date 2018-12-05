#!/usr/bin/env python
import os
import csv
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from collections import Counter
import numpy as np

def load_pickle(filex):
    with open(filex, "rb") as f:
        return pickle.load(f)

def get_vecmatrix(list_jt_vectors):
    jobid_list=[x[1] for x in list_jt_vectors]
    jobtitle_list=[x[2] for x in list_jt_vectors]
    vec_matrix=np.squeeze(np.array([x[3] for x in list_jt_vectors]))
    print(vec_matrix.shape)
    return (jobid_list, jobtitle_list, vec_matrix)

def get_worddict(word_list):
    word_dict={}
    for (i,w) in enumerate(word_list):
        word_dict[w] = i
    return word_dict

# cluster dict:  cluster_id -> [(jid1,jt1), (jid2,jt2), ..]
def get_clusterdict(list_jts, list_ids, array_clusterids):
    n_cluster = np.max(array_clusterids)
    dict_cluster = dict([])
    for i in range(1,n_cluster+1):
        idx = np.nonzero(array_clusterids == i)[0]
        dict_cluster[i] = [ (list_ids[j], list_jts[j]) for j in idx]
    return dict_cluster


# will output each cluster as a file in the dir
def output_dict_cluster(dir_output, dict_cluster, threshold=None):
    if(not os.path.isdir(dir_output)):
        os.makedirs(dir_output)
    n_cluster = len(dict_cluster)
    for i in range(1,n_cluster+1):
        file_output = dir_output+"/cluster_%0.3d.txt"%i
        list_idjts = dict_cluster[i]
        if(threshold and len(list_idjts) >= threshold):
            with open(file_output, "w") as f:
                writer=csv.writer(f)
                writer.writerow(["_id", "cleaned_job_title"])
                writer.writerows(list_idjts)

def print_cluster_highfreq_words(dict_cluster, threshold=None):
    n_cluster = len(dict_cluster)
    for i in range(1,n_cluster+1):
        list_idjts = dict_cluster[i]
        if(threshold and len(list_idjts) >= threshold):
            words = []
            for jid,jt in list_idjts:
                words.extend(jt.split())
            c=Counter(words)
            most_com = c.most_common(10)
            str_most_com = ' '.join([x[0] for x in most_com])
            print("%d(%d): %s" %(i, len(list_idjts),str_most_com))


    

    

list_jt_vectors = load_pickle("jt_vector_sampled.pkl")
list_ids, list_jts, vec_matrix = get_vecmatrix(list_jt_vectors)
cos_sim=cosine_similarity(vec_matrix)
jt_dict = get_worddict(list_jts)  # dict: job_title -> index

Z=linkage(vec_matrix, method='average', metric='cosine')
cluster_sizes = [300, 400, 500, 600, 700, 800]
for sz in cluster_sizes:
    array_clusterids = fcluster(Z, sz, criterion='maxclust')
    dict_cluster=get_clusterdict(list_jts, list_ids, array_clusterids)
    dir_cluster="cluster_results/cleaned3_filter5_sample0.05/%d_clusters" %sz
    print(dir_cluster)
    output_dict_cluster(dir_cluster, dict_cluster,40)
    print_cluster_highfreq_words(dict_cluster, 40)
