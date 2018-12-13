#!/usr/bin/env python

def read_dicts(filename):
    dict_idx=dict([])
    dict_cat=dict([])
    with open(filename, "r") as f:
        for line in f.readlines():
            stri,cat = line.strip().split(',')
            i=int(stri)
            dict_idx[i] = cat
            dict_cat[cat] = i
    return dict_idx, dict_cat


dict_idx,dict_cat = read_dicts("list_cat_index_classify.txt")
print(dict_idx)
print(dict_cat)
        
