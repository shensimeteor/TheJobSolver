#!/usr/bin/env python

from bs4 import BeautifulSoup
import time
import random
import requests
import re
import sys
import glob
import os
import logging
import datetime

def write_html(filename, soup):
    with open(filename, "w") as f:
        f.write(soup.prettify())

# return jobsearch-JobComponent-description (pure text), from the job page soup
def extract_description(soup):
    div=soup.find(name="div", class_=re.compile(".*jobsearch-JobComponent-description.*"))
    res_content=div.get_text()
    return res_content

# from the base_url and num_jobs, return main page URLs list (append &start=)
def get_main_page_URLs(base_url, num_jobs):
    urls=[]
    num_pages=int(num_jobs/10)
    if(num_pages>100):
        num_pages=100
    urls.append(base_url)
    for ipage in range(1,num_pages+1):
        x=base_url+"&start=%d"%(ipage*10)
        urls.append(x)
    return urls

# get info tuple list [ (jk, jobtitle, company, location) ] from main page
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

# write output into text. query url, then info, then description
def write_output(filename, query_url, info, desc):
    with open(filename, "w") as f:
        f.write("%s\n" %query_url)
        f.write("%s \n %s \n %s \n %s \n" %(info[0], info[1], info[2], info[3]))
        f.write("%s \n"%desc)

# return set_jks
def get_downloaded_jks(output_dir):
    dirs=os.listdir(output_dir)
    jks=set()
    for dirx in dirs:
        txts=glob.glob("output/"+dirx+"/*.txt")
        for txt in txts:
            jks.add(txt.split('.')[0].split('/')[2])
    return jks

# return num_jobs from the mainpage soup
def get_num_jobs(soup):
    num_found = soup.find(id = 'searchCount').string.encode('utf-8').split() #this returns the total number of results
    logging.info("num_found="+str(num_found))
    print(num_found)
    num_jobs = num_found[-2].decode("utf-8").split(',')
    if len(num_jobs)>=2:
        num_jobs = int(num_jobs[0]) * 1000 + int(num_jobs[1])
    else:
        num_jobs = int(num_jobs[0])
    num_pages = int(num_jobs/10) #calculates how many pages needed to do the scraping
    logging.info("num_jobs=%d, num_pages=%d" %(num_jobs, num_pages))
    print(num_jobs)
    print(num_pages)
    return num_jobs

def create_dirs():
    if(not os.path.isdir("htmls/main_pages")):
        os.makedirs("htmls/main_pages")
    if(not os.path.isdir("htmls/job_pages")):
        os.makedirs("htmls/job_pages")
    if(not os.path.isdir("output")):
        os.makedirs("output")
    if(not os.path.isdir("logs")):
        os.makedirs("logs")

def print_help():
    print('''
Usage: python3 crawl_indeed_para.py <URL of mainpage to start crawl> [redis]
Note, if redis is present, make sure you run init_redis.py first
''')
    exit(0)
    

###############################
# main function
## initialize
opt_write_to_mongodb=False
opt_write_to_text=True
opt_write_html=False
if(not (opt_write_to_text or opt_write_to_mongodb)):
    print("Error, opt_write_to_mongodb, opt_write_to_text, must have at least 1 to be true")
    exit(0)

if(opt_write_to_mongodb):
    from mongo_saver import MongoSaver
    saver=MongoSaver("mongodb://user:indeedjob@localhost/appDatabase", "appDatabase", "jobs")
    saver.init_collection()
##
if(len(sys.argv) == 1 or (len(sys.argv)==3 and sys.argv[2] != "redis")):
    print_help()

main_base_url = "https://www.indeed.com/jobs?"
job_base_url = "https://www.indeed.com/viewjob?"
start_url = sys.argv[1]
if(len(sys.argv) == 3):
    opt_with_redis=True
    from init_redis import RedisWrapper
    rw = RedisWrapper()
else:
    opt_with_redis=False

pattern=re.compile("q=([^&]*)&l=([^&]*)&jt=(.*)")
x=re.search(pattern, start_url)
query_word=x.group(1)
query_location=x.group(2)
query_jobtyp_explvl=x.group(3).replace('&explvl=', '+')
print(query_word)

#start_url = "http://www.indeed.com/jobs?q=software+engineer&l=New+York+NY"
# create dirs
create_dirs()
# config logging
logfile=datetime.datetime.now().strftime("info_%Y-%m-%d_%H-%M-%S.log")
logging.basicConfig(level=logging.INFO, filename="logs/"+logfile, filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("initialized, start_url=%s"%start_url)

# load downloaded jks
if(not opt_with_redis):
    downloaded_jks=get_downloaded_jks("output/")  
    n_downloaded_jks=len(downloaded_jks)
else:
    n_downloaded_jks=rw.jks_set_size()
logging.info("initial jks size=%d" %n_downloaded_jks)

# start crawl
try:
    resp = requests.get(start_url)
except:
    logging.warning("start_page_fail_load, url=%s"%start_url, exc_info=True)
    exit(0)

## 1. get number of jobs
try:
    start_soup = BeautifulSoup(resp.content, "lxml")
    num_jobs = get_num_jobs(start_soup)
except:
    logging.warning("start_page_fail_parse, url=%s"%start_url, exc_info=True)
    exit(0)

## 2. get main page URLs
main_urls=get_main_page_URLs(start_url, num_jobs)
print(len(main_urls))
logging.info("find mainpage urls = %d" %len(main_urls))

## 3. for every main page, crawl the infos and download job descriptions 
ipage=0
for mainurl in main_urls:
    ipage+=1
    j = random.randint(1000,2100)/1000.0
    print(mainurl)
    logging.info("start main page %s"%mainurl)
    time.sleep(j) #waits for a random time so that the website don't consider you as a bot
    try:
        resp = requests.get(mainurl)
    except:
        logging.warning("main_page_fail_load, url=%s"%mainurl, exc_info=True)
    try: 
        soup = BeautifulSoup(resp.content, "lxml")
        if(opt_write_html):
            html_name="htmls/main_pages/%s"%(mainurl.split('?')[1]+".html")
            write_html(html_name, soup)
        infos=get_info_from_main_page(soup)
        print(len(infos))
    except:
        logging.warning("main_page_fail_parse, url=%s"%mainurl, exc_info=True)
        continue

    get_info = True
    for i in range(len(infos)):
        jk=infos[i][0]

        if(((not opt_with_redis) and (jk in downloaded_jks)) or (opt_with_redis) and rw.check_jk_exist(jk)):
            continue
        try:
            xurl = job_base_url+"jk=%s"%jk
            j = random.randint(1000,2100)/1000.0
            time.sleep(j) #waits for a random time so that the website don't consider you as a bot
            resp2 = requests.get(xurl)
        except TimeoutException:
            print("crawl fail "+xurl)
            logging.warning("job_page_fail_load, url=%s"%xurl, exc_info=True)
            get_info = False
            continue

        if get_info:
            #soup=BeautifulSoup(driver.page_source)
            soup2 = BeautifulSoup(resp2.content,"lxml")
            if(opt_write_html):
                html_name="htmls/job_pages/%s.html" %jk
                write_html(html_name, soup2)
                
            try:
                res=extract_description(soup2)
                print("done "+xurl)
            except:
                print("extract fail "+xurl)
                logging.warning("job_page_fail_parse, url=%s"%xurl, exc_info=True)
                continue
            
            if(opt_write_to_text):
                try:
                    dirname="output/%s"%query_word
                    if(not os.path.isdir(dirname)):
                        os.mkdir(dirname)
                    output_name="output/%s/%s.txt"%(query_word,jk)
                    write_output(output_name, start_url, infos[i], res)
                except:
                    print("write to output txt fail "+xurl)
                    logging.warning("job_page_fail_text, url=%s"%xurl, exc_info=True)

            ##mongodb
            if(opt_write_to_mongodb):
                try:
                    dct={}
                    dct["query_keywords"]=query_word.replace("+", " ")
                    dct["query_location"]=query_location.replace("+", " ")
                    dct["query_jobtyp_explvl"]=query_jobtyp_explvl
                    job_title=infos[i][1]
                    company=infos[i][2]
                    job_location=infos[i][3]
                    dct["job_title"]=job_title.strip()
                    dct["_id"]=jk.strip()
                    dct["company"]=company.strip()
                    dct["job_location"]=job_location.strip()
                    dct["job_description"]=res
                    saver.insert(dct)
                except:
                    print("write to mongodb fail "+xurl)
                    logging.warning("job_page_fail_mongo, url=%s"%xurl, exc_info=True)
            
            if(not opt_with_redis):
                downloaded_jks.add(jk)
            else:
                rw.add_jks([jk])
            logging.info("done job_page, url=%s"%xurl)

        
    

