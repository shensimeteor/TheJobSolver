Used to host job-detail page server (when user click an job_id in Kibana, it will redirect user to a job-detail page, to see the highlight words)
- need to be hosted on same server (as it will access mongoDB/appDatabase/jobs in local)
- need to open 8000 port in EC2 setting
- need to set _id format to be URL (Link) with proper URL/label template in Kibana/management/index pattern
- to start server: python manage.py runserver 0.0.0.0:8000

