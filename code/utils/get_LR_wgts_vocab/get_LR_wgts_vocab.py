#!/usr/bin/env python

import numpy as np
import pickle


def output_lines(lines,filename):
    with open(filename, "w") as f:
        for line in lines:
            f.write(str(line)+"\n")

# read 
wgts=np.load("../../../data/coeff_array.npy")
print(wgts.shape)

with open ("../../../data/vocabfile.pkl", "r") as f:
    vocab = pickle.load(f)

print(len(vocab))
print(type(vocab))


# sort and print highest
ntype = 21
ntop_to_show=2000
indices = np.argsort(wgts, axis = 1)
for i in range(ntype):
    top_idx = indices[i, ::-1]
    top_words = [vocab[k] for k in top_idx[0:ntop_to_show]]
    word_wgts = wgts[i, top_idx]
    out_word_wgt = zip(top_words, word_wgts)
    output_lines(out_word_wgt, "output/cat%d_top%d.txt" %(i, ntop_to_show))
