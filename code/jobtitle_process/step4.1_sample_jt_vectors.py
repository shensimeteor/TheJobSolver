#!/usr/bin/env python

import pickle
import random 
sample_rate=0.05


def load_pickle(filex):
    with open(filex, "rb") as f:
        return pickle.load(f)

def dump_pickle(filex, data):
    with open(filex, "wb") as f:
        pickle.dump(data, f, 1)

list_jt_vec = load_pickle("jt_vector.pkl")
idx=list(range(len(list_jt_vec)))
random.shuffle(idx)

n_sample = int(sample_rate * len(list_jt_vec))
sample_idx = idx[0:n_sample]

list_sampled_jt_vec = [list_jt_vec[i] for i in sample_idx]

dump_pickle("jt_vector_sampled.pkl", list_sampled_jt_vec)
