#!/usr/bin/env python

import redis
import os
import glob

class RedisWrapper:
    def __init__(self, host="172.31.86.202", pwd="Indeed300K"):
        self.host=host
        self.pwd=pwd
        self.key_urls="urls_queue"
        self.key_jks="jks_set"
        self.key_job_list="job_list" #when work on a url, add it into job_list, when finish it, remove it
        self.r = redis.Redis(host, password=pwd)
    
    def flush_db(self):
        self.r.flushdb()
    
    # enqueue from tail
    def offer_urls(self, urls):
        self.r.lpush(self.key_urls,  *urls)

    # enqueue from head ~ push into stack
    def push_url(self, url):
        self.r.rpush(self.key_urls, url)

    def poll_url(self):
        return self.r.brpop(self.key_urls, 5)[1].decode('ascii')

    def url_queue_size(self):
        return self.r.llen(self.key_urls)

    def add_jks(self,jks):
        self.r.sadd(self.key_jks, *jks)

    def jks_set_size(self):
        return self.r.scard(self.key_jks)

    def check_jk_exist(self,jk):
        return self.r.sismember(self.key_jks, jk)

    #high level API, pull a url, and insert it into a job list, return the url
    def start_work_url(self):
        with self.r.pipeline() as pipe:
            while 1:
                try:
                    pipe.watch(self.key_urls)
                    url=pipe.lrange(self.key_urls, -1, -1)[0].decode('ascii')
#                    url=pipe.brpop(self.key_urls,5)[1].decode("ascii")
                    pipe.multi()
                    pipe.lpush(self.key_job_list, url)
                    pipe.brpop(self.key_urls,5)
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue
        return url

    #high level API, i.e. remove it from job list
    def finish_work_url(self,url):
        self.r.lrem(self.key_job_list, url)

    def recover_failed_joblist(self):
        urls=self.r.lrange(self.key_job_list, 0, -1)
        self.r.rpush(self.key_urls, *urls)
        self.r.delete(self.key_job_list)
    
    def job_list_size(self):
        return self.r.llen(self.key_job_list)
        
# return set_jks
def get_downloaded_jks(output_dir):
    dirs=os.listdir(output_dir)
    jks=set()
    for dirx in dirs:
        txts=glob.glob(output_dir+"/"+dirx+"/*.txt")
        for txt in txts:
            jk_file=os.path.basename(txt)
            jks.add(jk_file.split(".")[0])
    return jks

##init the redis
if __name__ == "__main__":
    import sys

    if(len(sys.argv)==2 and sys.argv[1]=="start"):
        opt_start=True
    else:
        opt_start=False

    # read urls, i.e. the url to crawl
    if(opt_start):
        with open("mainpage_urls.txt", "r") as f:
            urls=f.readlines()
        urls=[x.strip() for x in urls]
    # read jks, i.e. all jobs already download
    downloaded_jks=get_downloaded_jks("output")
    
    # put to redis
    rw = RedisWrapper()
    if(opt_start):
        rw.flush_db()
        print("init_redis: db cleaned")
        rw.offer_urls(urls)
        print("init_redis: urls enqueued")
    print("-- urls_queue size=%d" %rw.url_queue_size())

    rw.add_jks(downloaded_jks)
    print("init_redis: downloaded_jks inserted")
    print("-- jks_set size=%d" %rw.jks_set_size())
    failed_jobs=rw.job_list_size()
    print("redis job_list size=%d" %failed_jobs)
    if(failed_jobs>0):
        rw.recover_failed_joblist()
        print("init_redis: failed job enqueued, urls_queue size=%d" %rw.url_queue_size())
    

