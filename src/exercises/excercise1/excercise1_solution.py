import pandas as pd

sep:str = '_'
debug:bool = True
student_column_purge_list = [0, 2, 2, 2] # remove id,email,ssn and address

def process(students_file_name:str, teachers_file_name:str) -> str:
    # read csv file into df
    students_df = pd.read_csv(students_file_name)
    print(students_df)
    student_cols = (students_df.columns[0]).split(sep)
    assert len(student_cols) == 7, f"Something wrong with the file {students_file_name}"
    assert 'fname' in student_cols and 'lname' in student_cols and 'cid' in student_cols, f'Something wrong with the file {students_file_name}, columns - fname, lname or cid do not exist.'
    for item in student_column_purge_list:
        student_cols.pop(item)
    rows = []
    for index, col in students_df.iterrows():
        if debug:
            print(index, col)
        row = (col.tolist()[0]).split(sep)
        assert len(row) == 7, f"Something wrong with the file {students_file_name} at index {index} and row data {col}"

        for item in student_column_purge_list:
            row.pop(item)
        if debug:
            print(row)
        rows.append(row)

    formatted_students_df = pd.DataFrame(rows, columns=student_cols)
    if debug:
        print(formatted_students_df)
        print(formatted_students_df.count())

    # read parquet file into df
    teachers_df = pd.read_parquet(teachers_file_name)
    assert len(teachers_df.columns) == 7, f"Something wrong with the file {teachers_file_name}"
    assert 'fname' in teachers_df.columns and 'lname' in teachers_df.columns and 'cid' in teachers_df.columns, f'Something wrong with the file {teachers_file_name}, columns - fname, lname or cid do not exist.'
    for index, col in teachers_df.iterrows():
        if debug:
            print(index, col)

    print(teachers_df)
    print(teachers_df.count())
    teachers_df.rename(columns={'fname': 'teachers_fname', 'lname': 'teachers_lname'}, inplace=True)

    # trim unused columns
    teachers_drop_list = ['id','email', 'ssn', 'address']

    for item in teachers_drop_list:
        #  1 is the axis number (0 for rows and 1 for columns.)
        teachers_df.drop(item,  axis=1, inplace=True)

    # join teacher with formatted students
    join_df = pd.merge(formatted_students_df, teachers_df, on='cid', how='inner')

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