#!/usr/bin/env python
# similiar with step6, but after step6, we have done some preliminary labeling for clusters, (i.e. cluster_labels.txt), 
# now we get other unlabeled clusters, do cluster again (to get finer grained clusters) 
import os
import glob
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

# opposite to output_dict_cluster, read dict_cluster from dir_cluster (dict_cluster:  cluster_id -> [(_id, cleaned_job_title)]
def read_dict_cluster(dir_cluster):
    cluster_files=glob.glob(dir_cluster+"/cluster_*.txt") 
    dict_cluster=dict([])
    for cfile in cluster_files:
        cid=int(cfile.split("/")[-1].split("_")[1].split(".")[0])
        with open(cfile, "r") as f:
            lines=f.readlines()
            lst=[]
            for line in lines[1:]:
                lst.append(tuple(line.strip().split(',')))
            dict_cluster[cid]=lst
    return dict_cluster

# summarize dict_cluster to dict_cluster_size, i.e. cluster_id -> size_of_cluster
def get_dict_cluster_size(dict_cluster):
    dict_cluster_size=dict()
    for k in dict_cluster.keys():
        dict_cluster_size[k]=len(dict_cluster[k])
    return dict_cluster_size

# return dict_label: label -> list of cluster_ids, 
def read_dict_label(label_file):
    with open(label_file,"r") as f:
        lines=f.readlines()
    dict_label=dict()
    for line in lines:
        label=line.split(',')[0]
        dict_label[label]=[int(x)  for x in line.split(',')[1:]]
    return dict_label
        
#
def get_jids_by_cids(dict_cluster, cids):
    jids=[]
    for cid in cids:
        jids.extend([x[0] for x in dict_cluster[cid]])
    return jids
# 
def find_jtvector_sublist_byids(list_jt_vectors, set_ids):
    sublist=[]
    for jt_vector in list_jt_vectors:
        if(jt_vector[1] in set_ids):
            sublist.append(jt_vector)
    return sublist

# summary count of each cluster
def output_summary_clusters(file_summary, csv_file, dict_cluster, threshold=0):
#{{{
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
#}}}

# read manual labels & dict_clusters
dir_cluster="cluster_results_save/new_200_clusters/"
print("to read dict_cluster and dict_labels from:  "+dir_cluster)
dict_cluster=read_dict_cluster(dir_cluster)
dict_labels = read_dict_label(dir_cluster+"/labels.txt")


# find unlabeled cluster-Ids
nested_labeled_cids = dict_labels.values()
labeled_cids = set([ cid for cids in nested_labeled_cids for cid in cids])
unlabeled_cids = [ cid for cid in dict_cluster.keys() if cid not in labeled_cids]
print("\nfound labeled /unlabeled clusters")
print("- labeled=%d" %len(labeled_cids))
print("- unlabeled=%d" %len(unlabeled_cids))

# do cluster for unlabeled clusters again to find finer grained clusters
unlabeled_jids = set(get_jids_by_cids(dict_cluster, unlabeled_cids))
print("- unlabeled jobs=%d" %len(unlabeled_jids))

file_jt_vector="jt_vector.pkl"
print("\nto read pkl: "+file_jt_vector)
list_jt_vectors = load_pickle(file_jt_vector) 
print("to find jtvector sublist by unlabeled jids.")
unlabeled_list_jt_vectors = find_jtvector_sublist_byids(list_jt_vectors, unlabeled_jids)
list_ids, list_jts, vec_matrix = get_vecmatrix(unlabeled_list_jt_vectors)
print("unlabeld_list_jt_vectors's vec_matrix shape: "+str(vec_matrix.shape))

print("\n to cluster unlabeled job titles")
cluster_sizes=[500]
for n_clusters in cluster_sizes:
    batch_size=10000
    print("- to cluster: MiniBatchKMeans: n_clusters=%d, batch_size=%d." %(n_clusters, batch_size))
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, compute_labels=True, batch_size=batch_size)
    kmeans.fit(vec_matrix[:,:])
    array_clusterids = kmeans.labels_+1

    dict_cluster=get_clusterdict(list_jts, list_ids, array_clusterids)
    dir_cluster="cluster_results/kmeans_cleaned3_filter5_average_2nd/%d_clusters" %n_clusters
    cluster_size_threshold=200
    print("- to output cluster to %s" %dir_cluster)
    output_dict_cluster(dir_cluster, dict_cluster, cluster_size_threshold)
    output_summary_clusters(dir_cluster+"/summary.txt", dir_cluster+"/summary.csv", dict_cluster, cluster_size_threshold)
