import subprocess
import traceback

# for python 3.x
def runtime_exec(command):
    msg = {}
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if int(result.returncode) != 0:
            print('script output: {0}'.format(result.stdout))
            print('script error: {0}'.format(result.stderr))
            msg["stderr"] = str(result.stderr)
        msg["stdout"] = result.stdout
        print('script executed successfully {0}'.format(result.stdout))
        return msg
    except subprocess.CalledProcessError as e:
        print("Calledprocerr")
        print(traceback.format_exc())
        msg["Error"] = "Error performing get_application_log " + str(e)
    return msg

import os
if __name__ == '__main__':

    curr_dir = os.getcwd()
    command_arr = [curr_dir, 'dir.bat']
    command = '\\'.join(command_arr)
    runtime_exec(command)