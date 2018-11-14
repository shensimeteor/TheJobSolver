#!/usr/bin/env python

# filter cities that has jobs < count
# reformat cities to ",| " -> "+"

import re

# read
input_file="cities_software_engineer.txt"
loc_tuplist=[]
with open(input_file,"r") as f:
    for line in f.readlines():
        tup=line.split('\t')
        loc_tuplist.append( (tup[0], int(tup[1].strip())) )

# filter
cnt_filter=100
loc_tuplist=sorted(loc_tuplist, key=lambda x: -x[1])
loc_tuplist_f=[x  for x in loc_tuplist if x[1]>=cnt_filter]
print(len(loc_tuplist_f))
print(loc_tuplist_f[0:5])


# reformat

loc_tuplist_fr = [ (re.sub("(, | )", "+", x[0]),x[1]) for x in loc_tuplist_f]
print(loc_tuplist_fr[0:5])

# remove duplicated 
cities=[]
set_cities=set()
for loc in loc_tuplist_fr:
    if (loc[0] not in set_cities):
        set_cities.add(loc[0])
        cities.append(loc[0])


output_file="cities_software_engineer_step2_f100.txt"
with open(output_file, "w") as f:
#    for tup in loc_tuplist_fr:
#        f.write(tup[0]+"\n")
    for c in cities:
        f.write(c + "\n")

