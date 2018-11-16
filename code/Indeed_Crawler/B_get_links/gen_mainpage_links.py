#!/usr/bin/env python

qword_file="keywords.txt"
cities_file="cities_software_engineer_step2_f100.txt"

jt_explvl_queries=["jt=internship", "jt=fulltime&explvl=entry_level", "jt=fulltime&explvl=mid_level", "jt=fulltime&explvl=senior_level"]

base_url="http://www.indeed.com/"

with open(qword_file, "r") as f:
    qs=f.readlines()
qs=[x.strip() for x in qs]

with open(cities_file, "r") as f:
    cs=f.readlines()
cs=[x.strip() for x in cs]

print(qs[0:5])
print(cs[0:5])

links=[]
for q in qs:
    for c in cs:
        for jt_explvl in jt_explvl_queries:
            link=base_url+"jobs?q=%s&l=%s&%s"%(q, c, jt_explvl)
            links.append(link)

output_links="mainpage_urls.txt"
with open(output_links, "w") as f:
    for link in links:
        f.write(link+"\n")




