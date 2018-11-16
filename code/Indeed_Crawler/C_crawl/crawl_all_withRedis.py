#!/usr/bin/env python

from init_redis import RedisWrapper
import os
rw = RedisWrapper()
print(rw.url_queue_size())
while(rw.url_queue_size()>0):
    url=rw.start_work_url()
    cmd="python3 crawl_indeed_para.py '%s' redis" %url
    print(cmd)
    code=os.system(cmd)
    if(code==0):
        rw.finish_work_url(url)
        print("done")

