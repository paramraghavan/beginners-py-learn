API’s used:

fileArrivalAPI - get a list of files available
alertAPI - api to raise alert - email or log or both
GatherObject - manages a list of files with its atttirbutes , also has attribute called parentJobId
parentJobId - is uuid assiged when a new instance of Gatherobject is created
fileStatusAPI - given file name , returns the status of the file - PENDING, WORKING, COMPLETE , FAIL
FileObject - jobQueue has FileObjects Using worker, workermanager pattern

The worker manager collects the ariving files with fileArrivalAPI call. The files are added to GatherObject object Once
the gather is complete, files in GatherObject are added to the queue, called jobQueue. WorkerManger runs on Gather mode,
in gather mode we manage the file arrival

The worker, child thread, is a pool of threads. These threads run in monitor mode. Monitor mode check the the file
completion or failure status using fileStatusAPI

When a file is available in jobQueue, the worker/child thread which is free picks up this fileObject from the jobQueue
and starts processing it.

If no worker is available the fileObject(s) stays in the queue.

Add a option to shutdown FileMonitor gracefully - a separate threads monitors a specified folder for file shutdown.now.
When this file is seen it picks it , renames it as shutdown.now.started. Then grecefully shouts down the WorkerManegr
and Worker threads Implementation mode details:
Use schedule.ready, to schedule jobs if thats a good option The workermanager wakes up every 5 minutes, first it creates
a GatherObject and assigns a parent-jobid to it, which is a uuid, and continuously monitors for file arrival via
fileArrivalAPI every fixed interval , x, let say 1 minute for the next y times, let says y is 5 times.

As it finds files it adds to this GatherObject
Once this gather period is complete it adds the all FileObjects from GatherObejct to the jobQueue. Uses API call
createManifest - creates manifest file using the name in FileObject as {gatherObject_uuid)_arrival_file_name.manifest

The workermanager wakes up again after 5 minutes later and continutes monitoring via the fileArrivalAPI When a worker is
available in the worker pool it is reads a FileObject object from the queue. The worker picks up FileObject
The worker use the fileStatusAPI to monitor the status of the FileObject
And as the file status changes it udpates the FileObject status

Worker continuously monitors the FileObject every X1 minutes, 2 minutes lets say, for X2 times, let say 15 times (so
monitors for 20 minutes).

- It keep making call to fileStatusAPI to cehck file status
- FileObject is status is complete, it exits monitoring and waits for the next item in the Queue
- If error occurs call the alertAPI, it exits monitoring and waits for the next item in the Queue
- If the monitor time is completed for this FileObject, again its call alerAPI and waits for the next item in the queue 


## Solution
"""
File Monitoring System
=====================

A multi-threaded system for monitoring file processing with the following features:
- Periodic file gathering and monitoring
- Worker pool for parallel processing
- Graceful shutdown capability
- Configurable monitoring intervals and retry attempts

Architecture:
------------
1. WorkerManager: Gathers files periodically and adds them to a processing queue
2. Worker Pool: Multiple workers monitor file status and handle processing
3. ShutdownMonitor: Enables graceful system shutdown

Key Components:
-------------
- FileObject: Represents individual files with their processing status
- GatherObject: Groups related files under a single parent job ID
- Thread-safe job queue for managing file processing tasks

APIs Used:
---------
- fileArrivalAPI: Retrieves list of available files
- fileStatusAPI: Checks processing status of files
- alertAPI: Raises alerts via email or logs
- createManifest: Creates manifest files for gathered files

Usage:
-----
monitor = FileMonitor(
    shutdown_folder="/path/to/shutdown",
    gather_interval=5,
    num_workers=3
)
monitor.start()

Shutdown:
--------
Place a file named 'shutdown.now' in the specified shutdown folder to initiate
graceful shutdown. The file will be renamed to 'shutdown.now.started' during
the shutdown process.
