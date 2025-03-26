#!/bin/bash

# Path to the job_monitor executable - replace with actual path
JOB_MONITOR_PATH="/path/to/job_monitor"

# Log file
LOG_FILE="/path/to/job_monitor_check.log"

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Check if job_monitor is running
if pgrep -f "job_monitor" > /dev/null
then
    echo "$TIMESTAMP: job_monitor is running." >> $LOG_FILE
    exit 0
else
    echo "$TIMESTAMP: job_monitor is not running. Attempting to start..." >> $LOG_FILE

    # Start the job_monitor process with nohup to keep it running after session ends
    nohup $JOB_MONITOR_PATH >> $LOG_FILE 2>&1 &

    # Verify it started
    sleep 2
    if pgrep -f "job_monitor" > /dev/null
    then
        echo "$TIMESTAMP: job_monitor started successfully." >> $LOG_FILE
        exit 0
    else
        echo "$TIMESTAMP: Failed to start job_monitor." >> $LOG_FILE
        exit 1
    fi
fi