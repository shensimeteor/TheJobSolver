#!/usr/bin/env python
import pandas as pd
import re

def stop_words():
    s = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
    l = s.split()
    l1 = [w.replace("'","") for w in l] #remove apostrophes
    return set(l1)

# lower case, then remove non-(a-z)
def filter_jobtitle(jobtitle):
    y=re.sub(r"[^a-z]"," ",jobtitle.lower())
    xs=y.split()
    return " ".join(xs)

# lower case, remove i, ii, iii, iv, v; remove any inside (); then remove non-(a-z); remove intern, summer # still 160K left
# replace sr by senior; replace jr by junior
# remove stop words
def filter2_jobtitle(jobtitle):
    y=jobtitle.lower()
    y=re.sub(r"\(.*\)", " ", y) # remove (..)
    y=re.sub(r"[^a-z]", " ", y) # remove punctuations, numbers
    y=re.sub(r"\b(i|ii|iii|iv|intern|interns|internship|summer|student|students|contractor|contractors|contract)\b", " ",y)
    y=re.sub(r"\b(sr)\b", "senior", y)
    y=re.sub(r"\b(jr)\b", "junior", y)
    xs=y.split()
    stops = stop_words()
    xs=[x for x in xs if x not in stops]
    return " ".join(xs)

#besides 2, remove "- ." (for the last -). 
def filter3_jobtitle(jobtitle):
    y=jobtitle.lower()
    y=re.sub(r"\(.*\)", " ", y) # remove (..)
    xs = y.split(" - ") 
    if(len(xs) > 1):
        prefix=" ".join(xs[0:-1])
        if (len(prefix.split()) >= 2): 
            y=" - ".join(xs[0:-1])
    y=re.sub(r"r&d", "research develop", y)
    y=re.sub(r"[^a-z]", " ", y) # remove punctuations, numbers
    y=re.sub(r"\b(i|ii|iii|iv|intern|interns|internship|summer|student|students|contractor|contractors|contract)\b", " ",y)
    y=re.sub(r"(entry *level|mid *level|senior *level|part *time|full *time)", " ",y)
    y=re.sub(r"\b(sr|senior|jr|junior)\b", " ", y)
    y=re.sub(r"quality *assurance", "qa", y)
    y=re.sub(r"user *experience", "ux", y)
    y=re.sub(r"(opportunity|opportunities|opening|openings|year|years|remote|required)", " ",y)
    xs=y.split()
    stops = stop_words()
    xs=[x for x in xs if x not in stops]
    return " ".join(xs) 

df = pd.read_csv("jobs_infos.csv")

job_title_ts = df["job_title"]

cleaned1_ts  = df["job_title"].apply(filter3_jobtitle)

print("count_of_unique_job_title=%d"%job_title_ts.nunique())
print("count_of_unique_cleaned_job_title=%d"%cleaned1_ts.nunique())

df["cleaned_job_title"] = cleaned1_ts

df.to_csv("jobs_infos_cleaned3.csv")


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


