# file lock
## Use Case
- I have 6 vms running a program, all sharing the file system
- the program on start creates a file with file_id prefix and process name suffix and ends with .read pid_processA.ready
- All the vm rm the same process - processA processing  related to processA
- WE only only have 2 instance of processes across vm's running for processA, any more than that have to wait until the process count readuces to leass than or equal to 2
- When the processes are running we create a file pid_processA.running

### Implementation
- Lock File: Use a lock file to synchronize access to the counter file.
- Counter File: Use a counter file to keep track of how many instances of processA are currently running.
- Start Process: Before starting processA, check the counter file and wait if there are already two instances running.
- Running Process: When processA is running, update the counter file and create a .running file.
- End Process: When processA finishes, decrement the counter and remove the .running file.

In this code, we use file-based locking (fcntl.flock) to ensure that only one VM can modify the counter file at a time.
We use a while loop to wait until the number of running instances is less than the maximum allowed. Once the process
starts, we increment the counter and create a .running file. When the process finishes, we decrement the counter, release
the lock and remove the .running file.

Note:
the lockfile.lock file is not deleted automatically. It is used as a mechanism for acquiring a lock and is not meant to
be deleted after each use. The file itself does not contain any data; it merely acts as a marker for the locking
mechanism.

When a process acquires the lock, it holds onto it until it explicitly releases it. Other processes attempting to
acquire the lock will have to wait until the lock is released. **The file remains on the filesystem to facilitate this
locking mechanism across multiple processes or VMs.**

If you need to clean up the lock file for some reason (e.g., when you're sure no processes are using it anymore), you
can delete it manually. However, in normal operation, the lock file is not deleted and is reused each time a lock is
acquired or released.


### NFS and file lock

The file locking mechanism using fcntl.flock in Python,may not work reliably
across multiple VMs sharing a filesystem via NFS (Network File System). This is because NFS has its own locking
mechanisms, and the behavior of fcntl.flock can be inconsistent when used with NFS.

For file locking to work correctly across VMs sharing an NFS, you can use the fcntl.lockf function instead, which is
designed to be more compatible with NFS. Here's an updated version of the acquire and release lock functions using
lockf:

```python
def acquire_lock():
    while True:
        try:
            lock = open(lock_file, 'w')
            fcntl.lockf(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock
        except IOError:
            time.sleep(1)

def release_lock(lock):
    fcntl.lockf(lock, fcntl.LOCK_UN)
    lock.close()
```

### EFS and file lock

Amazon Elastic File System (EFS) provides a shared file system that can be used across multiple EC2 instances or VMs.
When using EFS, the standard file locking mechanisms like fcntl.flock or fcntl.lockf in Python should work across VMs
sharing the EFS volume. This is because EFS supports NFSv4 locking semantics, which include both advisory and mandatory
locking.

However, it's important to be aware of the potential for increased latency and the eventual consistency model of EFS,
which might affect the timing and reliability of locks in a distributed environment. While file locks should generally
work, the behavior might be different from what you would expect in a local file system or a traditional NFS setup.

To ensure reliable operation, you should test your locking mechanism thoroughly in the specific environment where it
will be deployed. Additionally, consider using more robust distributed locking mechanisms or coordination services if
your application requires strong consistency guarantees or if you encounter issues with file locking on EFS.

### Lock/Unlock

**Acquiring an Exclusive Lock:** To acquire an exclusive lock, you use the flock function with the LOCK_EX flag. T*he call to
flock will block (wait) until the lock can be acquired if the file is already locked by another process. You can also
use the LOCK_NB flag in combination with LOCK_EX to make the call non-blocking (i.e., it will return an error if the
lock cannot be immediately acquired).*

**Releasing the Lock**: The lock is automatically released when the file is closed (e.g., using the close method of the file
object) or when the process holding the lock terminates. You can also explicitly release the lock by calling flock with
the LOCK_UN flag.

## Cross platform file lock - Windows and Mac amd Unix

To achieve file locking in a way that works on both Windows and macOS (as well as other Unix-like systems), you can use
the portalocker library, which provides a cross-platform interface for file locking.

```shell
pip install portalocker
```

Then, you can use portalocker to acquire an exclusive lock (similar to fcntl.LOCK_EX) in a cross-platform manner:
In this rewritten version, portalocker.lock is used to acquire an exclusive, non-blocking lock on the file, and
portalocker.unlock is used to release the lock. If the lock cannot be acquired immediately, a LockException is raised,
and the code retries after a brief delay.

```python
import portalocker
import time

lock_file = "path/to/lockfile.lock"

def acquire_lock():
    while True:
        try:
            lock = open(lock_file, 'w')
            portalocker.lock(lock, portalocker.LOCK_EX | portalocker.LOCK_NB)
            return lock
        except portalocker.exceptions.LockException:
            time.sleep(1)

def release_lock(lock):
    portalocker.unlock(lock)
    lock.close()

```

## File lock acquired via fcntl or portalocker when the process dies

When a process that creates a lock dies, the lock is automatically released. All fcntl locks associated with a file are
removed when that process closes any file descriptor for that file, even if a lock was never requested for that file
descriptor. Fcntl locks are also not inherited by a child process