# final-project-project-final-chowdhury-satish-shen
final-project-project-final-chowdhury-satish-shen created by GitHub Classroom


#### Shell Command to connect to the MongoDB instance contatining the Indeed.com crawled dataset:
mongo -u user -p indeedjob ec2-184-73-64-187.compute-1.amazonaws.com/appDatabase

#### Several query examples of MongoDB: 
1. db.jobs.find().limit(1)    #  to see an example of document.
2. db.jobs.find().count()     # count the documents
3. db.jobs.distinct("company")    # show all company list, 
4. db.jobs.distinct("company").length    # number of all companies
5. db.jobs.find({"company": /.*Google.*/}).limit(5)  # show 5 jobs from google,  /.*Google.*/ means the "company" field contains substring "Google"



#### Schema of each document:

1. "_id": job id, internal job id of Indeed.com
2. "query_keywords": this is the keyword I use to query this job. 
3. "query_location": this is the location I used to query this job.  # use the "job_location" as real job location. This field is just what I use to query the job list in Indeed
4. "query_jobtyp_explvl":  I selected 4 [" internship", "fulltime+entry_level", "fulltime+mid_level", "fulltime+senior_level"]. They are combinations of job type (intern or fulltime) and experience level. I feel it's interesting to see how the keywords of job description might be different among different experience levels.
5. "job_title": the job_title shown in Indeed.com job list
6. "company": company, shown in Indeed.com job list
7. "job_location":  location of the job, shown in Indeed.com job list
8. "job_description":  the long description. 



#### Literature Review:
1. https://arxiv.org/pdf/1707.09751.pdf
2. https://www.kdnuggets.com/2017/05/deep-learning-extract-knowledge-job-descriptions.html
