#!/usr/bin/env python

import pandas as pd
import numpy as np

df=pd.read_csv("jobs_infos_cleaned3.csv")
list_cjts = df["cleaned_job_title"].tolist()
cjt_nwords = np.array([len(str(cjt).split()) for cjt in list_cjts])

min_nwords=1
max_nwords=np.max(cjt_nwords)
acc=0
for nw in range(min_nwords, max_nwords+1):
    cnt=np.count_nonzero(cjt_nwords == nw)
    acc+=cnt
    print("%d words, cnt=%d, acc=%d" %(nw, cnt,acc))

