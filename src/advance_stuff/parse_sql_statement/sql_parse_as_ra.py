import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Function, Case
from sqlparse.tokens import Keyword, DML

def extract_case_when(parsed):
    case_when_statements = []
    for token in parsed.tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                if 'CASE' in identifier.value:
                    case_when_statements.append(identifier)
        elif isinstance(token, Identifier):
            if 'CASE' in token.value:
                case_when_statements.append(token)
        elif isinstance(token, Function):
            if 'CASE' in token.value:
                case_when_statements.append(token)
        elif isinstance(token, Case):
            case_when_statements.append(token)
    return case_when_statements

def parse_case_when(case_statement):
    lines = case_statement.value.split('\n')
    case_clauses = []
    for line in lines:
        line = line.strip()
        if line.startswith('WHEN'):
            condition = line[5:line.find('THEN')].strip()
            result = line[line.find('THEN') + 5:].strip()
            case_clauses.append((condition, result))
        elif line.startswith('ELSE'):
            else_result = line[5:].strip()
            case_clauses.append(('ELSE', else_result))
    return case_clauses

def parse_case_alias(case_statement):
    lines = case_statement.value.split('\n')
    case_clauses = []
    for line in lines:
        line = line.strip()
        if line.startswith('END'):
            condition = line[5:line.find('THEN')].strip()
            result = line[line.find('THEN') + 5:].strip()
            case_clauses.append((condition, result))
        elif line.startswith('ELSE'):
            else_result = line[5:].strip()
            case_clauses.append(('ELSE', else_result))
    return case_clauses

def extract_column_alias(parsed):
    # Traverse the tokens to find the alias after the END keyword
    for token in parsed.tokens:
        if token.ttype == Keyword and token.value.upper() == 'END':
            next_token = parsed.token_next(parsed.token_index(token))
            if next_token and isinstance(next_token, Identifier):
                return next_token.value.strip()
            elif next_token and next_token.ttype == Keyword:
                # Handle case where alias follows an "AS" keyword
                alias_token = parsed.token_next(parsed.token_index(next_token))
                if alias_token:
                    return alias_token.value.strip()
    return None

def convert_to_ra(case_clauses, alias):
    ra_statements = []
    for condition, result in case_clauses:
        if condition != 'ELSE':
            ra_statements.append(f"σ[{condition}] -> {result}")
        else:
            ra_statements.append(f"ELSE -> {result}")
    if alias:
        ra_statements.append(f"AS {alias}")
    return ra_statements

# Example SQL statement with CASE WHEN

## TODO this does not work, but works with regex, to be fixed
sql_case_statement = """
SELECT CASE WHEN amount > 100 THEN 'High' WHEN amount > 50 THEN 'Medium' ELSE 'Low' end AS amount_category FROM transactions;
"""

sql = """
SELECT
    CASE
        WHEN amount > 100 THEN 'High'
        WHEN amount > 50 THEN 'Medium'
        ELSE 'Low'
    END as amount_category
FROM transactions;
"""

# Parse the SQL statement
parsed = sqlparse.parse(sql_case_statement)[0]

# Extract CASE WHEN statements
case_when_statements = extract_case_when(parsed)

# Parse and convert each CASE WHEN statement to relational algebra
for case_statement in case_when_statements:
    case_clauses = parse_case_when(case_statement)
    alias = extract_column_alias(parsed)
    ra_statements = convert_to_ra(case_clauses, alias)
    print("Relational Algebra Representation:")
    for ra in ra_statements:
        print(ra)
