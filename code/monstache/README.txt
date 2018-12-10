use monstache to connect MongoDB and ElasticSearch
1. install monstache
2. run: monstache -f monstache.conf
  # note. if you want to do initial copy from mongodb to elasticsearch, uncomment:
    direct-read-namespaces = ["appDatabase.jobs", "appDatabase.jobs2"]. Then run
   Otherwise, (you just want to sync in running time), comment this line, then run:
     nohup monstache -f monstache.conf &>nohup.out &


Reference: 
https://rwynn.github.io/monstache-site/start/
