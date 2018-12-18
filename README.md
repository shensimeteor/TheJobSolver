# final-project-project-final-chowdhury-satish-shen
final-project-project-final-chowdhury-satish-shen created by GitHub Classroom

#### Note: EC2 is stopped to save money, so database/Kibana/web is all disconnected. 
#BUT is not terminated, volume is also saved
## some basic steps to restart the server
#1. go to AWS/EC2, restart the Big Mongo Server (EC2 instance), and make sure the disk is mounted to /dev/sda1
    -- close 27017 port (mongodb) in EC2 security;  make sure 5601 (or 80, if nginx) is open  
#2. ssh to EC2, start mongod: sudo service mongod start. Use mongo ... command to check service availablity  
#3. start ElasticSearch/Kibana: sudo service elasticsearch start;  sudo service kibana start;  and use curl .. command to check     elasticsearch availability.  Use browser to test availability of Kibana
#4. start monstache,  nohup monstache monstache.conf (in code/monstache) to keep dynamic data sync  
#5. start django, cd code/django/hello_django/, nohup python manage.py runserver 0.0.0.0:8000   
#6. start nginx, sudo htpasswd -c /etc/nginx/htpasswd.users datacenter


#### Shell Command to connect to the MongoDB instance contatining the Indeed.com crawled dataset:
mongo -u user -p indeedjob ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase
##### Login as root user
mongo -u root -p datacenter --authenticationDatabase admin localhost:27017
##### Get the mongodb replications sets
ps aux | grep mongo

#### Several query examples of MongoDB: 
1. db.jobs.find().limit(1)    #  to see an example of document.
2. db.jobs.find().count()     # count the documents
3. db.jobs.distinct("company")    # show all company list, 
4. db.jobs.distinct("company").length    # number of all companies
5. db.jobs.find({"company": /.*Google.*/}).limit(5)  # show 5 jobs from google,  /.*Google.*/ means the "company" field contains substring "Google"



#### Schema of each document:

1. "_id": job id, internal job id of Indeed.com
2. "query_keywords": this is the keyword used to query this job. 
3. "query_location": this is the location used to query this job.  # use the "job_location" as real job location. This field is just what is used to query the job list in Indeed
4. "query_jobtyp_explvl":  From the selected 4 [" internship", "fulltime+entry_level", "fulltime+mid_level", "fulltime+senior_level"]. They are combinations of job type (intern or fulltime) and experience level.
5. "job_title": the job_title shown in Indeed.com job list
6. "company": company, shown in Indeed.com job list
7. "job_location":  location of the job, shown in Indeed.com job list
8. "job_description":  the long description. 
9. "job_description_cleaned": JD in a list containing words sans stop words and other special characters.


### test ElasticSearch accessibility (local)
curl -X GET "localhost:9200/_cat/indices?v"
 should have index: appdatabase.jobs

#### Access Kibana on EC2
 http://ec2-52-55-205-188.compute-1.amazonaws.com
 Username: datacenter
 Password: indeedjob

#### Accuracy
Using Logistic regression with count vectoriser and idf the accuracy came upto 72.7%
Using Logistic regression with only count vectoriser the accuracy came upto 72.89%
Using Logistic regression with cross validation increased the accuracy to 79.20%

#### Literature Review:
1. https://arxiv.org/pdf/1707.09751.pdf
2. https://www.kdnuggets.com/2017/05/deep-learning-extract-knowledge-job-descriptions.html

Scores :
Proposal : 10/10
Checkpoint1: 10/10
Checkpoint2 : 10/10
Final : 30/30
