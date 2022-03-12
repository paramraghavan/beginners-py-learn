import traceback
start_key = 'start'

def printStackTrace(message:str) :
    traceback_error_msg = traceback.format_exc()
    print(f'{80*"-"}\n{message}:\n{80*"-"}\n{traceback_error_msg}{80*"-"}')