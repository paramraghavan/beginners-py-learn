import pandas as pd

sep:str = '_'
debug:bool = True
student_column_purge_list = ['id','email','ssn','address'] # remove id,email,ssn and address

def process(students_file_name:str, teachers_file_name:str) -> str:
    # read csv file into df
    students_df = pd.read_csv(students_file_name, delimiter=sep)
    print(students_df)
    assert len(students_df.columns) == 7, f"Something wrong with the file {students_file_name}"
    assert 'fname' in students_df.columns and 'lname' in students_df.columns and 'cid' in students_df.columns, f'Something wrong with the file {students_file_name}, columns - fname, lname or cid do not exist.'
    students_df.drop(['id','email','ssn','address'], axis=1, inplace=True)

    if debug:
        print(students_df)
        print(students_df.count())


    # read parquet file into df
    teachers_df = pd.read_parquet(teachers_file_name)
    assert len(teachers_df.columns) == 7, f"Something wrong with the file {teachers_file_name}"
    assert 'fname' in teachers_df.columns and 'lname' in teachers_df.columns and 'cid' in teachers_df.columns, f'Something wrong with the file {teachers_file_name}, columns - fname, lname or cid do not exist.'
    print(teachers_df)
    print(teachers_df.count())
    teachers_df.rename(columns={'fname': 'teachers_fname', 'lname': 'teachers_lname'}, inplace=True)

    # trim unused columns
    teachers_drop_list = ['id','email', 'ssn', 'address']
    teachers_df.drop(teachers_drop_list,  axis=1, inplace=True)

    # join teacher with formatted students
    join_df = pd.merge(students_df, teachers_df, on='cid', how='inner')

    print(join_df)
    # df1= join_df.query("fname == 'Willie'")
    # print(df1)

    result = join_df.to_json(orient='records')
        # .replace('},{', '} {')
    with open('student_class.json', 'w') as f:
        f.write(result)
    print(result)


if __name__ == "__main__":
    print('start')
    students_file_name = 'students.csv'
    teachers_file_name = 'teachers.parquet'
    process(students_file_name, teachers_file_name)


'''
Notes:
https://www.datasciencemadesimple.com/join-merge-data-frames-pandas-python/
'''