'''
Function parses a large list of CSV files, and returns each line to be processed in
another function. We do not want to read all the files into memory, in our case these files are small
but the file could be  mb's, this could consume lots of space all at once,
so we yield each line in a python data structure.
'''
def get_lines(files):
    for file in files:
        print(f'printing file {file}')
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                #print('before yield')
                yield line
                #print('after yield')


def reads_line_by_line_from_all_csv_files_in_current_folder():
    count =1;
    files = list_all_file_in_directory(".", 'csv')
    # print(files)

    for line in get_lines(files):
        print(f'read line {count}. {line}')# process line
        count +=1

from os import listdir
from os.path import isfile, join

def list_all_file_in_directory(mypath, extension):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(extension)]
    return onlyfiles

if __name__ == '__main__':
    reads_line_by_line_from_all_csv_files_in_current_folder()