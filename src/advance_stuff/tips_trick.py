
elem = { 'TableList' : [ \
                 {'Name': 'table1'},  {'Name': 'table2'},  {'Name': 'table3'} \
                ] \
}

'''
see the usage of for loop with the square brackets
'''
tables = []
tables += [
                {
                    "name": table["Name"],
                }
                for table in elem["TableList"]
            ]

print(tables)