#!/usr/bin/env python
import glob
import os
keywords=["software+engineer","data+scientist","data+engineer"]
for words in keywords:
    if(not os.path.isdir("output/"+words)):
        os.mkdir("output/"+words)

for fn in glob.iglob("output/*.txt"):
    with open(fn, "r") as f:
        head=f.readline()
    jk=fn.split("/")[1]
    for words in keywords:
        if( words in head ):
            print((words, head))
            print((fn, "output/"+words+"/"+jk))
            os.rename(fn, "output/"+words+"/"+jk)
