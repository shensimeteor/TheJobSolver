#!/usr/bin/env python3
import os

with open("mainpage_urls.txt", "r") as f:
    urls=f.readlines()
urls=[x.strip() for x in urls]

print(urls[0:5])

with open("url_log.txt", "w") as f:
    for url in urls:   
        print(url)
        os.system('python3 crawl_indeed_para.py "%s"' %url)
        f.write("done: %s \n"%url)

