#!/usr/bin/env python
import os
import shutil
import csv
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MiniBatchKMeans
from collections import Counter
import numpy as np

def load_pickle(filex):
    with open(filex, "rb") as f:
        return pickle.load(f)

def get_vecmatrix(list_jt_vectors):
    jobid_list=[x[1] for x in list_jt_vectors]
    jobtitle_list=[x[2] for x in list_jt_vectors]
    vec_matrix=np.squeeze(np.array([x[3] for x in list_jt_vectors]))
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
def output_dict_cluster(dir_output, dict_cluster, threshold=0):
    if(os.path.isdir(dir_output)):
        shutil.rmtree(dir_output)
    os.makedirs(dir_output)
    n_cluster = len(dict_cluster)
    for i in range(1,n_cluster+1):
        file_output = dir_output+"/cluster_%0.3d.txt"%i
        list_idjts = dict_cluster[i]
        if(len(list_idjts) >= threshold):
            with open(file_output, "w") as f:
                writer=csv.writer(f)
                writer.writerow(["_id", "cleaned_job_title"])
                writer.writerows(list_idjts)

# summary count of each cluster
def output_summary_clusters(file_summary, csv_file, dict_cluster, threshold=0):
    n_cluster = len(dict_cluster)
    sum_cnt=0
    num_jobs=0 # all jobs
    n_cluster_filter=0
    dict_cluster_size=dict([])  # only for clusters after filtering, cluster_id -> size of cluster
    for i in range(1,n_cluster+1):
        list_idjts = dict_cluster[i]
        if(len(list_idjts) >= threshold):
            sum_cnt+=len(list_idjts)
            n_cluster_filter+=1
            dict_cluster_size[i] = len(list_idjts)
        num_jobs +=  len(list_idjts)
    str_head="total cluster size=%d, threshold=%d, cluster size after filtering=%d\n" %(n_cluster, threshold, n_cluster_filter)
    cluster_sizes=np.array(list(dict_cluster_size.values()), np.float)
    print(type(cluster_sizes))
    print(cluster_sizes.dtype)
    print(cluster_sizes.shape)
    str_head+="average size of each cluster=%f, max=%f, min=%f \n" %(np.average(cluster_sizes), np.max(cluster_sizes), np.min(cluster_sizes))
    str_head+="# of jobs clustered = %d, # of total jobs = %d \n" %(sum_cnt, num_jobs)
    str_body=""
    #sort by cluster size
    cluster_idcnts=sorted(dict_cluster_size.items(), key=lambda x:-x[1])
    rows=[]
    for cid,cnt in cluster_idcnts:
        list_idjts = dict_cluster[cid]
        words = []
        for jid,jt in list_idjts:
            words.extend(jt.split())
        c=Counter(words)
        most_com = c.most_common(10)
        str_most_com = ' '.join(["%s,%0.3f"%(x[0],x[1]/cnt) for x in most_com])
        str_body+="%d (%d): %s\n" %(cid, cnt, str_most_com)
        #prepare csv rows
        row=[cid,cnt]
        for x in most_com:
            row.extend([x[0], "%0.3f"%(x[1]/cnt)])
        rows.append(row)

    #output to file
    with open(file_summary, "w") as f:
        f.write(str_head)
        f.write(str_body)
    #write to csv
    with open(csv_file, "w") as f:
        writer=csv.writer(f)
        header = ["cluster_id", "cluster_size"]
        header.extend(["word", "freq"]*10)
        writer.writerow(header)
        writer.writerows(rows)


file_jt_vector="jt_vector.pkl"
print("to read pkl: "+file_jt_vector)
list_jt_vectors = load_pickle(file_jt_vector) 
list_ids, list_jts, vec_matrix = get_vecmatrix(list_jt_vectors)
jt_dict = get_worddict(list_jts)  # dict: job_title -> index

#cluster_sizes=[200, 500, 1000, 1200, 1500]
cluster_sizes=[200]
for n_clusters in cluster_sizes:
    batch_size=10000
    print("to cluster: MiniBatchKMeans: n_clusters=%d, batch_size=%d." %(n_clusters, batch_size))
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, compute_labels=True, batch_size=batch_size)
    kmeans.fit(vec_matrix[:,:])
    array_clusterids = kmeans.labels_+1

    dict_cluster=get_clusterdict(list_jts, list_ids, array_clusterids)
    dir_cluster="cluster_results/kmeans_cleaned3_filter5_average_full/%d_clusters" %n_clusters
    cluster_size_threshold=0
    print("to output cluster to %s" %dir_cluster)
    output_dict_cluster(dir_cluster, dict_cluster, cluster_size_threshold)
    output_summary_clusters(dir_cluster+"/summary.txt", dir_cluster+"/summary.csv", dict_cluster, cluster_size_threshold)
