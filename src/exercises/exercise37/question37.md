i have job1 which is a prodcuer jobs, it creates a json file, data-mmddyyy.json.
I have job2 consumer job which runs15 -20 minutes after the producer jobs. These 2 jobs run daily. When the cosumer job
starts it has to wait or the json file producesd by job1,data-mmddyyy.json, only then it can proceed. I will wait for 2
hours before it times out and raise an exception. If the file is ready with 2 hours it the job2 will process the json
file.
Can you write a python implemenation for job1 and job 2 . Both these jobs runs as separate python scripts. these job
sahre file system