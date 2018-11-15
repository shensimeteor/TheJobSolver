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


#### Literature Review:
https://arxiv.org/pdf/1707.09751.pdf
https://www.kdnuggets.com/2017/05/deep-learning-extract-knowledge-job-descriptions.html
