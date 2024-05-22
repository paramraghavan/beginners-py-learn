'''
Notes:
  The re.DOTALL flag makes the dot (.) in the regular expression match any character, including newline characters.
  This is useful when you want your pattern to match across multiple lines. By default, the dot (.) matches any
 character except a newline.

 The re.VERBOSE flag (also known as re.X) allows you to write regular expressions that are more readable by allowing
  you to include whitespace and comments within the pattern. This can be very helpful for complex patterns.
'''



import re

sql_case_statement = """
SELECT CASE WHEN amount > 100 THEN 'High' WHEN amount > 50 THEN 'Medium' ELSE 'Low' end AS amount_category FROM transactions;
"""

sql_case_statement_1 = """
SELECT
CASE WHEN amount > 100 THEN 'High' WHEN amount > 50 THEN 'Medium' ELSE 'Low' end AS amount_category
FROM transactions;
"""

sql_case_statement_3 = """
SELECT
    CASE
        WHEN amount > 100 THEN 'High'
        WHEN amount > 50 THEN 'Medium'
        ELSE 'Low'
    END as amount_category
FROM transactions;
"""

# Regular expression pattern to match CASE WHEN statements
pattern = re.compile(r"""
    CASE\s+
    (?P<cases>(
        WHEN\s+(?P<condition>.*?)\s+THEN\s+(?P<result>.*?)\s+
    )+)
    ELSE\s+(?P<else_result>.*?)\s+
    END\s+as\s+(?P<alias>.*?)\s+
""", re.VERBOSE | re.DOTALL | re.IGNORECASE)

match = pattern.search(sql_case_statement, re.IGNORECASE)
alias= ''
if match:
    cases = match.group('cases')
    else_result = match.group('else_result')
    alias = match.group('alias')
    # Find all WHEN-THEN pairs
    when_then_pattern = re.compile(r'WHEN\s+(.*?)\s+THEN\s+(.*?)\s+', re.DOTALL)
    when_then_pairs = when_then_pattern.findall(cases)

    # Print the extracted components
    print("WHEN-THEN pairs:")
    for condition, result in when_then_pairs:
        print(f"Condition: {condition.strip()}, Result: {result.strip()}")

    print(f"ELSE Result: {else_result.strip()}")
    print(f'alias {alias}')
else:
    print("No CASE WHEN statement found")


