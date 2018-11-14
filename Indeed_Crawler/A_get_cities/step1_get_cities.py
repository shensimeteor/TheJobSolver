#!/usr/bin/env python

from bs4 import BeautifulSoup
import time
import random
import requests
import re
import sys

def get_locations_from_mainpage(soup):
    div_location_rbo=soup.find("div", {"id":"LOCATION_rbo"})
    lis=div_location_rbo.ul.find_all("li")
    location_count_pair=[]
    for li in lis:
        if("title" in li.a.attrs):
            strx=li.a["title"]
            loc=re.search(r"(.+) \((\d+)\)", strx)
            location_count_pair.append((loc.group(1), loc.group(2)))
    return location_count_pair
        
def read_lines(filename):
    with open(filename, "r") as f:
        lines=f.readlines()
    lines=[line.strip() for line in lines]
    return lines

# each line must be a string
def write_lines(filename, lines):
    with open(filename, "w") as f:
        for line in lines:
            f.write(str(line)+"\n")

# write tuplist = [ () () .. () ], use \tab as separator
def write_tuple_list(filename, tuplist):
    with open(filename, "w") as f:
        for tup in tuplist:
            str_tup = [str(x) for x in tup] 
            line='\t'.join(str_tup)
            f.write(line+"\n")


states=read_lines("states.txt")
#test for write, passed
#write_lines("x.txt", states)
#test_states=[ (s,1) for s in states ]
#write_tuple_list("y.txt", test_states)
#exit(0)

cities=[]

base_url = "http://www.indeed.com"   
qword="software engineer"
count=0
for loc in states:
    location=loc
    count+=1
    print((count, loc))
    start_url = "http://www.indeed.com/jobs?q=%s&l=%s"%(qword, location)
    resp = requests.get(start_url)
    soup=BeautifulSoup(resp.content, "lxml")
    loc_info=get_locations_from_mainpage(soup)
    cities.extend(loc_info)
    j = random.randint(1000,2300)/1000.0
    time.sleep(j)

write_tuple_list("cities_software_engineer.txt", cities)





