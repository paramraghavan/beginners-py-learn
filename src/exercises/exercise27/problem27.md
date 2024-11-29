I have csv file with thousands for rows for 250+ jobs that run at intervals - daily, hourly, half hourly, weekly,
bi-weekly, every 15 minutes, monthly and so on. The columns vaialble are : job-name, start-date-time, end-date-time,
ingest-location, status. status states for - Start, Running, Failed, Success From the data I want to get the job
schedule for each of the jobs - by job-name.

We do have sceanrios for example we have JobA thats run every 30 minutes,
ususally it completed in the alloted time, some times it exceeds 30 minutes takes about X hours, maybe 3 hours, when
this happens. the jobA will not run for next X hours when this job A is running, and the next job A will run 30 minutes
after this job A has completed Help me with python code that reads the csv data, munges it gets me the job schedules for
each job by job-name, average, min and max execution time for each jobs by job-name Also make some sample data