import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

def extract_column_names(sql):
    # Parse the SQL statement
    parsed = sqlparse.parse(sql)
    stmt = parsed[0]  # Assuming the SQL query is the first statement

    column_names = []
    for token in stmt.tokens:
        print(f'type: {token.ttype} token.value: {token.value}')
        #if token.ttype is DML and token.value.upper() == 'SELECT':
        continue
            # Next token should be the columns part
            # columns = next(stmt.tokens)
            # if isinstance(columns, IdentifierList):
            #     for identifier in columns.get_identifiers():
            #         column_names.append(identifier.get_real_name())
            # elif isinstance(columns, Identifier):
            #     column_names.append(columns.get_real_name())
            # break

    return column_names

# Example usage
sql = """
SELECT
CASE WHEN amount > 100 THEN 'High' WHEN amount > 50 THEN 'Medium' ELSE 'Low' end AS amount_category
FROM transactions;
"""
columns = extract_column_names(sql)
print(columns)  # Output: ['name', 'age', 'address']
