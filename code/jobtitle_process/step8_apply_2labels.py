#!/usr/bin/env python
# similiar with step6, but after step6, we have done some preliminary labeling for clusters, (i.e. cluster_labels.txt), 
# now we get other unlabeled clusters, do cluster again (to get finer grained clusters) 
import copy
import re
import os
import glob
import shutil
import csv
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MiniBatchKMeans
from collections import Counter
import numpy as np


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
        label=line.strip().split(',')[0]
        dict_label[label]=[int(x)  for x in line.strip().split(',')[1:]]
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

# input: dict_cluster:  cluster_id -> [(_id, job_title)]
#        dict_labels : label -> [ cluster_ids ]
# output: dict_labeled_idjts:  label -> [ (_id, job_title) ]
def get_dict_labeled_idjts(dict_cluster, dict_labels):
    dict_labeled_idjts = {}
    for label in dict_labels.keys():
        idjts=[]
        for cid in dict_labels[label]:
            idjts.extend(dict_cluster[cid])
        dict_labeled_idjts[label]=idjts
    return dict_labeled_idjts

# if key same, merged into 1 list
# else merge key/value
def merge_dict_labeled_idjts(dict_labeled_idjts1, dict_labeled_idjts2):
    dict_labeled_idjts_merged = copy.deepcopy(dict_labeled_idjts1)
    for k in dict_labeled_idjts2.keys():
        if k in dict_labeled_idjts_merged.keys():
            dict_labeled_idjts_merged[k].extend(dict_labeled_idjts2[k])
        else:
            dict_labeled_idjts_merged[k] = dict_labeled_idjts2[k]
    return dict_labeled_idjts_merged

def summarize_dict_labeled_idjts(dict_labeled_idjts):
    n_labels = len(dict_labeled_idjts)
    print("summary: n_labels = %d" %(n_labels))
    total_size = 0
    for label in dict_labeled_idjts.keys():
        label_size = len(dict_labeled_idjts[label])
        total_size += label_size
        print("- %s, size: %d" %(label, label_size))
    print("total size: %d" %total_size) 


def output_dict_labeled_idjts(dir_output, dict_labeled_idjts):
    if(os.path.isdir(dir_output)):
        shutil.rmtree(dir_output)
    os.makedirs(dir_output)
    for label in dict_labeled_idjts.keys():
        file_output=dir_output+re.sub(r"(/| )","+",label)+".txt"
        list_idjts = dict_labeled_idjts[label]
        with open(file_output, "w") as f:
            writer=csv.writer(f)
            writer.writerow(["_id", "cleaned_job_title"])
            writer.writerows(list_idjts)

    

#read 1st level cluster & labels
dir_cluster1="cluster_results_save/new_200_clusters/"
print("to read dict_cluster1 and dict_labels from:  "+dir_cluster1)
dict_cluster1=read_dict_cluster(dir_cluster1)
dict_labels1 = read_dict_label(dir_cluster1+"/labels_1st.txt")
dict_labeled_idjts1 = get_dict_labeled_idjts(dict_cluster1, dict_labels1)
summarize_dict_labeled_idjts(dict_labeled_idjts1)

#read 2nd level cluster & labels
dir_cluster2="cluster_results_save/2nd_500_clusters/"
print("to read dict_cluster2 and dict_labels from:  "+dir_cluster2)
dict_cluster2=read_dict_cluster(dir_cluster2)
dict_labels2 = read_dict_label(dir_cluster2+"/labels_2nd.txt")
dict_labeled_idjts2 = get_dict_labeled_idjts(dict_cluster2, dict_labels2)
summarize_dict_labeled_idjts(dict_labeled_idjts2)

dict_labeled_idjts_all = merge_dict_labeled_idjts(dict_labeled_idjts1, dict_labeled_idjts2)
summarize_dict_labeled_idjts(dict_labeled_idjts_all)

# write labeled_idjts
output_dict_labeled_idjts("labeled_results/", dict_labeled_idjts_all)

