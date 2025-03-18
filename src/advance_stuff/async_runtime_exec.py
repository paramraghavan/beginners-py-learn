import asyncio
import subprocess
import traceback
import shlex
import time
import os
import signal
from typing import Union, List, Dict, Optional, Any


async def async_runtime_exec(
        command: Union[str, List[str]],
        timeout: Optional[float] = None,
        shell: bool = False,
        check_interval: float = 5.0,
        progress_callback=None,
        fire_and_forget: bool = False,
        log_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a command or script asynchronously.

    Parameters:
    - command: Command to execute (string or list)
    - timeout: Maximum execution time in seconds (None for no limit)
    - shell: Whether to run command in a shell (use with caution)
    - check_interval: How often to check and report progress (seconds)
    - progress_callback: Optional function to call with progress updates
    - fire_and_forget: If True, returns immediately after starting the process
    - log_file: If provided and fire_and_forget=True, redirects output to this file

    Returns:
    - Dictionary with execution results or submission status for fire_and_forget
    """
    msg = {
        "start_time": time.time(),
        "command": command if isinstance(command, str) else " ".join(command),
        "status": "starting"
    }

    try:
        # Prepare the command
        if isinstance(command, str) and not shell:
            command = shlex.split(command)

        # Setup logging for fire and forget mode
        if fire_and_forget and log_file:
            # Open log file for redirection
            log_fd = open(log_file, 'w')
            stdout_dest = log_fd
            stderr_dest = log_fd
            print(f"Process output will be logged to: {log_file}")
        else:
            stdout_dest = asyncio.subprocess.PIPE
            stderr_dest = asyncio.subprocess.PIPE

        # Create subprocess
        print(f"Executing async: {command}")

        if shell:
            process = await asyncio.create_subprocess_shell(
                command if isinstance(command, str) else " ".join(command),
                stdout=stdout_dest,
                stderr=stderr_dest
            )
        else:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=stdout_dest,
                stderr=stderr_dest
            )

        # Store process info
        msg["pid"] = process.pid
        msg["status"] = "running"

        # For fire and forget mode, return immediately
        if fire_and_forget:
            msg["submission_success"] = True
            msg["fire_and_forget"] = True

            if log_file:
                msg["log_file"] = log_file

            print(f"Process started with PID {process.pid} in fire-and-forget mode")

            # Detach process from Python's process group (if on Unix)
            try:
                if hasattr(os, 'setpgrp'):
                    # Only on Unix-like systems
                    os.setpgrp()
            except Exception:
                # Ignore if not possible
                pass

            return msg

        # Set up communication tasks
        stdout_chunks = []
        stderr_chunks = []

        async def read_stream(stream, chunks):
            if stream:
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    line_text = line.decode('utf-8') if isinstance(line, bytes) else line
                    chunks.append(line_text)
                    print(line_text.rstrip())  # Print live output

        # Start reading streams in background tasks
        stdout_task = asyncio.create_task(read_stream(process.stdout, stdout_chunks))
        stderr_task = asyncio.create_task(read_stream(process.stderr, stderr_chunks))

        # Monitor the process
        start_time = time.time()

        # For very long-running processes, we monitor rather than just wait
        while True:
            # Wait for process to complete with a timeout
            try:
                # Check if the process has completed
                process_completed = await asyncio.wait_for(
                    process.wait(),
                    timeout=check_interval
                )
                # Process is done
                break
            except asyncio.TimeoutError:
                # Still running, check progress
                current_time = time.time()
                elapsed = current_time - start_time

                # Create progress update
                update = {
                    "elapsed_time": elapsed,
                    "timestamp": current_time,
                    "still_running": True
                }

                # Get resource usage if available
                try:
                    import psutil
                    if process.pid:
                        proc = psutil.Process(process.pid)
                        update["memory_percent"] = proc.memory_percent()
                        update["cpu_percent"] = proc.cpu_percent(interval=0.1)
                except (ImportError, psutil.NoSuchProcess):
                    pass

                msg.setdefault("progress_updates", []).append(update)

                # Call progress callback if provided
                if progress_callback:
                    progress_callback(update)

                print(f"Process still running after {elapsed:.1f}s")

                # Check for timeout
                if timeout and elapsed > timeout:
                    print(f"Command execution exceeded timeout of {timeout}s")

                    # Try graceful termination first
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), timeout=5.0)
                    except asyncio.TimeoutError:
                        print("Process didn't terminate gracefully, killing...")
                        process.kill()

                    msg["success"] = False
                    msg["error_type"] = "timeout"
                    msg["error_message"] = f"Command execution timed out after {timeout}s"
                    break

        # Wait for stdout/stderr tasks to complete
        await stdout_task
        await stderr_task

        # Collect output
        msg["stdout"] = "".join(stdout_chunks)
        msg["stderr"] = "".join(stderr_chunks)

        # Record final status
        if "error_type" not in msg:  # Not a timeout
            msg["returncode"] = process.returncode
            msg["success"] = (process.returncode == 0)
            msg["status"] = "completed"

            # Log appropriate message based on result
            if process.returncode == 0:
                print(f"Command executed successfully")
            else:
                print(f"Command failed with return code: {process.returncode}")

    except Exception as e:
        print("Unexpected error during execution:")
        print(traceback.format_exc())
        msg["success"] = False
        msg["error_type"] = type(e).__name__
        msg["error_message"] = str(e)
        msg["status"] = "error"

    finally:
        # Always include execution time
        msg["end_time"] = time.time()
        msg["execution_time"] = msg["end_time"] - msg["start_time"]

        # Close log file if opened
        if fire_and_forget and log_file and 'log_fd' in locals():
            log_fd.close()

    return msg


# Helper function for getting PID status
def get_process_status(pid):
    """Check if a process with given PID is still running"""
    try:
        import psutil
        return psutil.Process(pid).status()
    except (ImportError, psutil.NoSuchProcess):
        try:
            # Fallback for Unix systems
            os.kill(pid, 0)  # Signal 0 tests if process exists
            return "running"
        except ProcessLookupError:
            return "not running"
        except PermissionError:
            return "permission denied"


# Example of using fire and forget mode
async def main():
    # Example 1: Normal execution - wait for completion
    print("=== Running with full wait ===")
    result1 = await async_runtime_exec(
        "echo 'Starting' && sleep 2 && echo 'Finished'",
        shell=True
    )
    print(f"Result: {result1['success']}, Time: {result1['execution_time']:.2f}s")

    # Example 2: Fire and forget - return immediately
    print("\n=== Running fire and forget ===")
    result2 = await async_runtime_exec(
        "echo 'Starting long process' && sleep 10 && echo 'Long process finished'",
        shell=True,
        fire_and_forget=True,
        log_file="/tmp/long_process.log"
    )
    print(f"Submission successful: {result2.get('submission_success')}")
    print(f"Process PID: {result2.get('pid')}")
    print(f"Log file: {result2.get('log_file')}")

    # Check status after a few seconds
    if 'pid' in result2:
        await asyncio.sleep(2)
        status = get_process_status(result2['pid'])
        print(f"Process status after 2s: {status}")


# Run the example
if __name__ == "__main__":
    asyncio.run(main())