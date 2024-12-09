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
"""

import uuid
import time
import queue
import threading
import schedule
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, NamedTuple
import pandas as pd


class FileStatus(Enum):
    """Represents the possible states of a file in the processing pipeline."""
    PENDING = "PENDING"  # File is queued for processing
    WORKING = "WORKING"  # File is currently being processed
    COMPLETE = "COMPLETE"  # File processing completed successfully
    FAIL = "FAIL"  # File processing failed


class FileMetadata(NamedTuple):
    """Represents the metadata of a file used for duplicate detection."""
    name: str
    size: int
    modified_time: datetime


@dataclass
class FileObject:
    """
    Represents a file in the processing system with its metadata and status.

    Attributes:
        file_name: Name of the file being processed
        file_size: Size of the file in bytes
        in_time: Create time of the file
        status: Current processing status of the file
        attempts: Number of monitoring attempts made
        alert: Alert sent True/False
    """
    file_name: str
    file_size: int
    in_time: datetime
    status: FileStatus = FileStatus.PENDING
    attempts: int = 0
    alert:bool = False

    def matches(self, other_metadata: FileMetadata) -> bool:
        """
        Check if this file matches the given metadata.

        Args:
            other_metadata: FileMetadata to compare against

        Returns:
            True if the files match in name, size, and modified time
        """
        return (self.file_name == other_metadata.name and
                self.file_size == other_metadata.size and
                self.in_time == other_metadata.modified_time)

class FileStateTracker:
    """
    Tracks file states in a thread-safe manner using a DataFrame.
    """

    def __init__(self):
        self.df = pd.DataFrame(columns=[
            'file_name', 'file_size', 'in_time', 'status',
            'attempts', 'alert'
        ])
        self.lock = threading.Lock()

    def update_file_state(self, file_obj: FileObject):
        """
        Updates or adds a file's state in the DataFrame.
        Uses composite key of file_name + file_size for uniqueness.
        """
        with self.lock:
            row = {
                'file_name': file_obj.file_name,
                'file_size': file_obj.file_size,
                'in_time': file_obj.in_time,
                'status': file_obj.status.value,
                'attempts': file_obj.attempts,
                'alert': file_obj.alert
            }

            # Create composite mask using both file_name and file_size
            mask = (self.df['file_name'] == file_obj.file_name) & \
                   (self.df['file_size'] == file_obj.file_size)

            if mask.any():
                self.df.loc[mask] = pd.Series(row)
            else:
                self.df.loc[len(self.df)] = row

    def get_dataframe(self) -> pd.DataFrame:
        """Returns a copy of the current DataFrame"""
        with self.lock:
            return self.df.copy()

    def clear_data(self):
        """Clears all data from the DataFrame"""
        with self.lock:
            self.df = pd.DataFrame(columns=[
                'file_name', 'file_size', 'in_time', 'status',
                'attempts', 'alert'
            ])

class GatherObject:
    """
    Groups related files under a single parent job ID for batch processing.

    Tracks files gathered within a specific time window and prevents duplicates.
    """

    def __init__(self):
        self.parent_job_id = str(uuid.uuid4())
        self.files: List[FileObject] = []
        self.gather_start_time = datetime.now()

    def has_duplicate(self, file_metadata: FileMetadata) -> bool:
        """
        Check if a file with matching metadata exists in this gather.

        Args:
            file_metadata: Metadata of the file to check

        Returns:
            True if a matching file exists, False otherwise
        """
        return any(existing_file.matches(file_metadata)
                   for existing_file in self.files)

    def add_file(self, file_metadata: FileMetadata) -> None:
        """
        Add a new file to this gather group if it's not a duplicate.

        Args:
            file_metadata: Metadata of the file to add
        """
        if not self.has_duplicate(file_metadata):
            file_obj = FileObject(
                file_name=file_metadata.name,
                file_size=file_metadata.size,
                in_time=file_metadata.modified_time
            )
            self.files.append(file_obj)
            # Update state tracker
            self.file_monitor.state_tracker.update_file_state(file_obj)

class FileMonitor:
    """
    Main orchestrator for the file monitoring system.

    Manages the lifecycle of file gathering, monitoring, and processing through
    a combination of WorkerManager and Worker threads. Provides graceful shutdown
    capability through a dedicated ShutdownMonitor.

    Args:
        shutdown_folder: Directory to monitor for shutdown signal file
        gather_interval: Minutes between gathering cycles
        gather_check_interval: Minutes between checks during gathering
        gather_check_times: Number of checks per gathering cycle
        monitor_interval: Minutes between status checks for each file
        monitor_check_times: Maximum number of status checks per file
        num_workers: Number of worker threads to spawn
    """

    def __init__(self,
                 shutdown_folder: str,
                 gather_interval: int = 5,
                 gather_check_interval: int = 1,
                 gather_check_times: int = 5,
                 monitor_interval: int = 2,
                 monitor_check_times: int = 15,
                 num_workers: int = 3):
        self.job_queue: queue.Queue = queue.Queue()
        self.shutdown_event = threading.Event()
        self.shutdown_folder = shutdown_folder

        # Configuration parameters
        self.gather_interval = gather_interval
        self.gather_check_interval = gather_check_interval
        self.gather_check_times = gather_check_times
        self.monitor_interval = monitor_interval
        self.monitor_check_times = monitor_check_times

        # Thread management
        self.worker_manager = None
        self.workers: List[threading.Thread] = []
        self.num_workers = num_workers
        self.shutdown_monitor = None
        # manages state of filemonitor in dataframe
        self.state_tracker = FileStateTracker()


    def file_arrival_api(self) -> List[FileMetadata]:
        """
        Check for new files that have arrived within the gather window.

        The function looks for files modified within the last gather_check_times
        minutes and returns their metadata. It's designed to be replaced with
        actual API implementation while maintaining the same interface.

        Returns:
            List of FileMetadata for newly arrived files
        """
        # Mock implementation - replace with actual API call
        # This shows the expected structure
        watch_dir = "/path/to/watch"
        lookback_minutes = self.gather_check_times
        cutoff_time = datetime.now() - timedelta(minutes=lookback_minutes)

        arrived_files = []

        # In real implementation, this would be replaced with actual API call
        # This is just to demonstrate the logic
        try:
            for filename in os.listdir(watch_dir):
                filepath = os.path.join(watch_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    modified_time = datetime.fromtimestamp(stat.st_mtime)

                    # Only include files modified within the lookback window
                    if modified_time >= cutoff_time:
                        arrived_files.append(FileMetadata(
                            name=filename,
                            size=stat.st_size,
                            modified_time=modified_time
                        ))
        except Exception as e:
            self.alert_api(
                f"Error checking for new files: {str(e)}",
                "error"
            )

        return arrived_files

    def file_status_api(self, file_name: str) -> FileStatus:
        """
        Mock implementation of fileStatusAPI.

        Args:
            file_name: Name of the file to check status for

        Returns:
            Current status of the specified file
        """
        # Implementation would go here
        return FileStatus.PENDING

    def alert_api(self, message: str, alert_type: str) -> None:
        """
        Mock implementation of alertAPI.

        Args:
            message: Alert message to send
            alert_type: Type of alert (e.g., "error", "warning")
        """
        # Implementation would go here
        print(f"Alert ({alert_type}): {message}")

    def create_manifest(self, gather_object: GatherObject) -> None:
        """
        Creates manifest files for all files in a gather group.

        Args:
            gather_object: GatherObject containing files needing manifests
        """
        for file_obj in gather_object.files:
            manifest_name = f"{gather_object.parent_job_id}_{file_obj.file_name}.manifest"
            # Implementation would go here
            print(f"Created manifest: {manifest_name}")

    class WorkerManager(threading.Thread):
        """
        Manages the file gathering process on a periodic basis.

        The WorkerManager wakes up at configured intervals to gather new files,
        create GatherObjects, and add files to the processing queue.
        """

        def __init__(self, file_monitor):
            """
            Initialize the WorkerManager.

            Args:
                file_monitor: Parent FileMonitor instance
            """
            super().__init__()
            self.file_monitor = file_monitor
            self.current_gather: Optional[GatherObject] = None

        def run(self) -> None:
            """Main execution loop for the WorkerManager."""
            schedule.every(self.file_monitor.gather_interval).minutes.do(self.gather_files)

            while not self.file_monitor.shutdown_event.is_set():
                schedule.run_pending()
                time.sleep(1)

    def gather_files(self) -> None:
        """
        Performs a complete gathering cycle for new files, stopping when no new files
        are detected for 5 minutes or when the gather window completes.
        """
        self.current_gather = GatherObject()
        last_file_time = time.time()
        files_seen = set()

        while True:
            if self.file_monitor.shutdown_event.is_set():
                break

            new_files = self.file_monitor.file_arrival_api()
            found_new = False

            for file_metadata in new_files:
                if file_metadata not in files_seen:
                    self.current_gather.add_file(file_metadata)
                    files_seen.add(file_metadata)
                    last_file_time = time.time()
                    found_new = True

            # Break if no new files for 5 minutes
            if time.time() - last_file_time > 300:  # 5 minutes in seconds
                break

            time.sleep(self.file_monitor.gather_check_interval * 60)

        # Add gathered files to queue
        for file_obj in self.current_gather.files:
            self.file_monitor.job_queue.put(file_obj)

        # Create manifest
        self.file_monitor.create_manifest(self.current_gather)


    class Worker(threading.Thread):
        """
        Worker thread that monitors and processes individual files.

        Workers pick up FileObjects from the job queue and monitor their status
        until completion, failure, or timeout.
        """

        def __init__(self, file_monitor, worker_id: int):
            """
            Initialize a Worker thread.

            Args:
                file_monitor: Parent FileMonitor instance
                worker_id: Unique identifier for this worker
            """
            super().__init__()
            self.file_monitor = file_monitor
            self.worker_id = worker_id

        def run(self) -> None:
            """Main execution loop for the Worker."""
            while not self.file_monitor.shutdown_event.is_set():
                try:
                    file_obj = self.file_monitor.job_queue.get(timeout=1)
                    self.monitor_file(file_obj)
                    self.file_monitor.job_queue.task_done()
                except queue.Empty:
                    continue

        def monitor_file(self, file_obj: FileObject) -> None:
            """
            Monitor a single file's status until completion or timeout.

            Args:
                file_obj: FileObject to monitor
            """
            file_obj.start_time = datetime.now()

            for _ in range(self.file_monitor.monitor_check_times):
                if self.file_monitor.shutdown_event.is_set():
                    break

                status = self.file_monitor.file_status_api(file_obj.file_name)
                file_obj.status = status

                # Update state tracker after each status change
                self.file_monitor.state_tracker.update_file_state(file_obj)

                if status == FileStatus.COMPLETE:
                    break
                elif status == FileStatus.FAIL:
                    self.file_monitor.alert_api(
                        f"File {file_obj.file_name} failed processing",
                        "error"
                    )
                    break

                time.sleep(self.file_monitor.monitor_interval * 60)

            if file_obj.status not in [FileStatus.COMPLETE, FileStatus.FAIL]:
                self.file_monitor.alert_api(
                    f"Monitoring timeout for file {file_obj.file_name}",
                    "warning"
                )

            file_obj.end_time = datetime.now()

    class ShutdownMonitor(threading.Thread):
        """
        Monitors for shutdown signals and initiates graceful shutdown.

        Watches a specified folder for a 'shutdown.now' file. When found,
        renames it and triggers system shutdown.
        """

        def __init__(self, file_monitor):
            """
            Initialize the ShutdownMonitor.

            Args:
                file_monitor: Parent FileMonitor instance
            """
            super().__init__()
            self.file_monitor = file_monitor

        def run(self) -> None:
            """Main execution loop for the ShutdownMonitor."""
            while not self.file_monitor.shutdown_event.is_set():
                shutdown_file = Path(self.file_monitor.shutdown_folder) / "shutdown.now"
                if shutdown_file.exists():
                    # Rename the file to indicate shutdown has begun
                    shutdown_file.rename(shutdown_file.parent / "shutdown.now.started")
                    self.file_monitor.shutdown()
                time.sleep(5)

    def start(self) -> None:
        """
        Start all system components.

        Launches the WorkerManager, Worker pool, and ShutdownMonitor threads.
        """
        # Start WorkerManager
        self.worker_manager = self.WorkerManager(self)
        self.worker_manager.start()

        # Start Workers
        for i in range(self.num_workers):
            worker = self.Worker(self, i)
            worker.start()
            self.workers.append(worker)

        # Start Shutdown Monitor
        self.shutdown_monitor = self.ShutdownMonitor(self)
        self.shutdown_monitor.start()

    def shutdown(self) -> None:
        """
        Perform graceful system shutdown.

        Sets the shutdown event and waits for all threads to complete.
        """
        print("Initiating graceful shutdown...")
        self.shutdown_event.set()

        # Wait for WorkerManager to complete
        if self.worker_manager:
            self.worker_manager.join()

        # Wait for all workers to complete
        for worker in self.workers:
            worker.join()

        # Wait for shutdown monitor
        if self.shutdown_monitor:
            self.shutdown_monitor.join()

        print("Shutdown complete")


def main():
    """
    Entry point for the File Monitoring System.

    Creates and starts a FileMonitor instance with default configuration.
    Handles keyboard interrupts for manual shutdown.
    """
    monitor = FileMonitor(
        shutdown_folder="/path/to/shutdown/folder",
        gather_interval=5,
        gather_check_interval=1,
        gather_check_times=5,
        monitor_interval=2,
        monitor_check_times=15,
        num_workers=3
    )

    try:
        monitor.start()
        # Keep main thread alive until shutdown
        while not monitor.shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.shutdown()


if __name__ == "__main__":
    main()
