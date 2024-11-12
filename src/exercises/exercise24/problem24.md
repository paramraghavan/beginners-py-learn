Read from job_run.csv file
jobname, checktime, alert *time, poll*every_x_minutes, emails

* i have python job which runs continuously, wakes up every 5/X mins and check the job_run table
* job_run.csv is a csv file
* REad the job_run into memory, if the file changes, reload job_run to memeory again
* Job status check - use python rest api to check job status by job name and time window
* we can have place holder function to get job status, pass in job_name, time windows and returns job status- Success,
  Failled, Running or NotFound, not found means the job has not run
* Read one job at a time from jon_run and do the following:
* if the check time falls within the 5/X min window, check for the job status for this job, if job fails alert by email
* if the alert time exists, then check the job status for completion- send email alert on error or running status, if
  job run record does not exist for today Not Found , send email alert
* if check time and alert time are not set , then check for poll time, poll this job and send email alert of failure
  with the 5/X interval window