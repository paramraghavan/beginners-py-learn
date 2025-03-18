import asyncio
import subprocess
import traceback
import shlex
import time
import os
from typing import Union, List, Dict, Optional, Any


async def async_runtime_exec(
        command: Union[str, List[str]],
        match_string: Optional[str] = None,
        match_timeout: float = 30.0,
        shell: bool = False,
        log_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a command asynchronously in fire-and-forget mode with optional string matching.

    Parameters:
    - command: Command to execute (string or list)
    - match_string: If provided, will wait for this string in stdout before returning
    - match_timeout: Maximum time to wait for the match_string (seconds)
    - shell: Whether to run command in a shell (use with caution)
    - log_file: If provided, redirects output to this file

    Returns:
    - Dictionary with submission status and matched string if requested
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

        # Determine output handling
        if log_file and not match_string:
            # Just log to file, no need to capture output
            log_fd = open(log_file, 'w')
            stdout_dest = log_fd
            stderr_dest = log_fd
            print(f"Process output will be logged to: {log_file}")
        else:
            # Need to capture output for string matching
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
        msg["submission_success"] = True

        # Wait for matching string if requested
        if match_string:
            match_found = False
            start_matching_time = time.time()

            # Function to read output and look for the matching string
            async def read_until_match():
                matched_line = None
                if process.stdout:
                    while True:
                        line = await process.stdout.readline()
                        if not line:
                            break

                        line_text = line.decode('utf-8')
                        print(line_text.rstrip())  # Echo output

                        # Write to log file if specified
                        if log_file and 'log_fd' in locals():
                            log_fd.write(line_text)
                            log_fd.flush()

                        # Check for match
                        if match_string in line_text:
                            return line_text.strip()
                return None

            try:
                # Wait for match with timeout
                matched_line = await asyncio.wait_for(
                    read_until_match(),
                    timeout=match_timeout
                )

                if matched_line:
                    msg["matched_string"] = matched_line
                    msg["match_found"] = True
                    print(f"Match found: {matched_line}")
                else:
                    msg["match_found"] = False
                    print(f"No match found within timeout")

            except asyncio.TimeoutError:
                msg["match_found"] = False
                msg["match_timeout"] = True
                print(f"Timeout waiting for match after {match_timeout}s")

        # Always in fire-and-forget mode
        print(f"Process running with PID {process.pid}")

        # Try to detach process (Unix systems)
        try:
            if hasattr(os, 'setpgrp'):
                os.setpgrp()
        except Exception:
            pass

    except Exception as e:
        print("Error during execution:")
        print(traceback.format_exc())
        msg["success"] = False
        msg["error_type"] = type(e).__name__
        msg["error_message"] = str(e)
        msg["status"] = "error"

    finally:
        # Close log file if we opened it
        if log_file and 'log_fd' in locals():
            log_fd.close()

        # Include execution time until this point
        msg["end_time"] = time.time()
        msg["setup_time"] = msg["end_time"] - msg["start_time"]

    return msg


# Example usage
async def main():
    # Example 1: Simple fire and forget
    print("=== Running fire and forget ===")
    result1 = await async_runtime_exec(
        "echo 'Starting process' && sleep 10 && echo 'Process finished'",
        shell=True,
        log_file="/tmp/process.log"
    )
    print(f"Submission successful: {result1.get('submission_success')}")
    print(f"Process PID: {result1.get('pid')}")

    # Example 2: Wait for matching string
    print("\n=== Running with string matching ===")
    result2 = await async_runtime_exec(
        "echo 'Initializing' && sleep 2 && echo 'Server started on port 8080' && sleep 10",
        shell=True,
        match_string="Server started on port",
        match_timeout=5.0
    )
    print(f"Matched: {result2.get('match_found', False)}")
    if result2.get('match_found'):
        print(f"Matched string: {result2.get('matched_string')}")
    print(f"Setup time: {result2.get('setup_time'):.2f}s")


# Run the example
if __name__ == "__main__":
    asyncio.run(main())