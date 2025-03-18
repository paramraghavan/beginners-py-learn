import subprocess
import traceback
import shlex
import time

"""
A good rule of thumb is to use shell=False unless you specifically need shell features.
Use shell=True when:
Shell features are needed: Pipelines (|), redirections (>), wildcards (*)
runtime_exec("find /var/log -name '*.log' | grep 'error' > /tmp/errors.txt", shell=True)
"""

# for python 3.x
def runtime_exec(command, timeout=None, shell=False):
    """
    Execute a command or script and wait for completion.

    Parameters:
    - command: Command to execute (string or list)
    - timeout: Maximum execution time in seconds (None for no limit)
    - shell: Whether to run command in a shell (use with caution)

    Returns:
    - Dictionary with execution results
    """


    msg = {
        "start_time": time.time(),
        "command": command if isinstance(command, str) else " ".join(command)
    }

    try:
        # Prepare the command
        if isinstance(command, str) and not shell:
            # Split the string into a list for safer execution
            command = shlex.split(command)

        # Execute the command and wait for completion
        print(f"Executing: {command}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Get text instead of bytes
            check=False,  # Don't raise exception on non-zero exit
            timeout=timeout,  # Optional timeout
            shell=shell  # Whether to use shell
        )

        # Record execution details
        msg["returncode"] = result.returncode
        msg["stdout"] = result.stdout
        msg["stderr"] = result.stderr
        msg["success"] = (result.returncode == 0)
        msg["execution_time"] = time.time() - msg["start_time"]

        # Log appropriate message based on result
        if result.returncode == 0:
            print(f"Command executed successfully in {msg['execution_time']:.2f}s")
            if result.stdout.strip():
                print(f"Output: {result.stdout[:200]}..." if len(result.stdout) > 200 else f"Output: {result.stdout}")
        else:
            print(f"Command failed with return code: {result.returncode}")
            print(f"Error: {result.stderr[:200]}..." if len(result.stderr) > 200 else f"Error: {result.stderr}")

    except subprocess.TimeoutExpired as e:
        print(f"Command timed out after {timeout} seconds")
        msg["success"] = False
        msg["error_type"] = "timeout"
        msg["error_message"] = str(e)

    except Exception as e:
        print("Unexpected error during execution:")
        print(traceback.format_exc())
        msg["success"] = False
        msg["error_type"] = type(e).__name__
        msg["error_message"] = str(e)

    finally:
        # Always include end time
        msg["end_time"] = time.time()
        if "execution_time" not in msg:
            msg["execution_time"] = msg["end_time"] - msg["start_time"]

    return msg

import os
if __name__ == '__main__':

    curr_dir = os.getcwd()
    command_arr = [curr_dir, 'dir.sh']
    command = f'{os.sep}'.join(command_arr)
    runtime_exec(command)