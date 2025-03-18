import subprocess
import traceback

# for python 3.x
def runtime_exec(command):
    msg = {}
    try:
        # If command is a string, convert it to a list for subprocess
        if isinstance(command, str):
            # This splits the command properly respecting quotes
            import shlex
            command = shlex.split(command)

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, check=True)

        msg["stdout"] = result.stdout
        print(f'Script executed successfully: {result.stdout}')
        return msg

    except subprocess.CalledProcessError as e:
        print("Command failed with return code:", e.returncode)
        print(f'Script output: {e.stdout}')
        print(f'Script error: {e.stderr}')
        msg["stderr"] = e.stderr
        msg["stdout"] = e.stdout

    except Exception as e:
        print("Unexpected error:")
        print(traceback.format_exc())
        msg["Error"] = f"Error performing command execution: {str(e)}"

    return msg


import os
if __name__ == '__main__':

    curr_dir = os.getcwd()
    command_arr = [curr_dir, 'dir.sh']
    command = f'{os.sep}'.join(command_arr)
    runtime_exec(command)