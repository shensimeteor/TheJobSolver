#!/usr/bin/env python


import pandas as pd
import numpy as np

def cnt_nword(job_title):
    return len(str(job_title).split())
    
df=pd.read_csv("jobs_infos_cleaned3.csv")
df["word_cnt_cjt"]=df["cleaned_job_title"].apply(cnt_nword)

df_new = df[df.word_cnt_cjt<=5]

df_new.to_csv("jobs_infos_cleaned3_filter5.csv")

df_long = df[df.word_cnt_cjt>5]
print(df_long)

