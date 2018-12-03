#!/usr/bin/env python
import pandas as pd
import re

# lower case, then remove non-(a-z)
def filter_jobtitle(jobtitle):
    y=re.sub(r"[^a-z]"," ",jobtitle.lower())
    xs=y.split()
    return " ".join(xs)



df = pd.read_csv("jobs_infos.csv")

job_title_ts = df["job_title"]

df["cleaned_job_title"] = df["job_title"].apply(filter_jobtitle)

df.to_csv("jobs_infos_cleaned.csv")


# get uniq words set
list_cleaned_jobtitle = df["cleaned_job_title"].tolist()
words_set=set([])
for jobtitle in list_cleaned_jobtitle:
    for w in jobtitle.split():
        words_set.add(w)
print("size of words_set=%d" %len(words_set))
sorted_words = sorted(list(words_set))
with open("words_list.txt", "w") as f:
    for w in sorted_words:
        f.write(w+"\n")


