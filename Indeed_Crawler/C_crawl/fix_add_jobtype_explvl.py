#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob
import re
jtlvls=["internship", "fulltime+entry_level", "fulltime+mid_level", "fulltime+senior_level"]
filekeywords=["internship", "entry_level", "mid_level", "senior_level"  ]
dirx="htmls/main_pages/"

def get_info_from_main_page(soup):
    start_soup = soup
    data_jks = start_soup.find_all("div", class_=re.compile(".*row.*result"))
    infos=[]  # tuple (jk, job_title, company, location)
    for div in data_jks:
        jk=div["data-jk"]
        a=div.find(name="a", attrs={"data-tn-element":"jobTitle"})
        jobtitle=a["title"]
        span = div.find(name="span", attrs={"class":"company"})
        company=span.text.strip()
        locdiv = div.find(name=re.compile("span|div"), attrs={"class":"location"})
        location=locdiv.text.strip()
        infos.append( (jk, jobtitle, company, location) )
    return infos

for (jtlvl, filekw) in zip(jtlvls, filekeywords):
    files=glob.glob(dirx+"*%s*.html"%filekw)
    print(len(files))
    for filex in files:
        with open(filex, "r") as f:
            print(filex)
            resp = f.read()
            soup = BeautifulSoup(resp, "lxml")
            infos=get_info_from_main_page(soup)
            print(infos)
            exit(0)

