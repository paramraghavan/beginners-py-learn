I have csv file with thousands for rows for 250+ jobs that run at intervals - daily, hourly, half hourly, weekly,
bi-weekly, every 15 minutes, monthly and so on. The columns varialble are : job-name, start-date-time, end-date-time,
s3_location, status. status states for - Start, Running, Failed, Success 
From the above csv data we want to make the job schedule for each of the jobs - by job-name.

We do have scenarios for example we have JobA thats run every 30 minutes,
usuusally it completed in the alloted time, some times it exceeds 30 minutes takes about X hours, maybe 3 hours, when
this happens. the jobA will not run for next X hours when this job A is running, and the next job A will run 30 minutes
after this job A has completed 
Help me with python code that reads the csv data, process the csv to get the  schedule for
each job by job-name, run frequency/per - hour/day/week/month, number of runs per day, average, 
min, max execution time and success rate for each jobs by job-name Also make some sample data

Create csv file with
Header columns :
job_name, schedule, avg_execution_time, min_execution_time, max_execution_time, success_rate, total run,
median_interval_minutes, earliest_run and latest run
