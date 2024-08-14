from lark import Lark, Transformer

# Define the grammar
sql_grammar = """
    ?start: case_when
    ?case_when: "CASE" when_clauses "END" "AS" column_name
    ?when_clauses: when_clause+
    ?when_clause: "WHEN" condition "THEN" result
    ?condition: column comparator value
    ?comparator: ">" | "=" | "<"
    ?result: ESCAPED_STRING
    ?column: CNAME
    ?value: SIGNED_NUMBER
    ?column_name: CNAME

    %import common.CNAME
    %import common.SIGNED_NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""


# Define the transformer to process the parsed tree
class SQLTransformer(Transformer):
    def case_when(self, items):
        return {"case_when": items}

    def when_clauses(self, items):
        return {"when_clauses": items}

    def when_clause(self, items):
        return {"when_clause": items}

    def condition(self, items):
        return {"condition": items}

    def comparator(self, items):
        return {"comparator": items[0]}

    def result(self, items):
        return {"result": items[0]}

    def column(self, items):
        return {"column": items[0]}

    def value(self, items):
        return {"value": items[0]}

    def column_name(self, items):
        return {"column_name": items[0]}


# Create the parser
parser = Lark(sql_grammar, parser='lalr', transformer=SQLTransformer())

# Parse the SQL statement
sql_statement = """
CASE
    WHEN Quantity > 30 THEN 'The quantity is greater than 30'
    WHEN Quantity = 30 THEN 'The quantity is 30'
    ELSE 'The quantity is under 30'
END AS QuantityText
"""

parsed_tree = parser.parse(sql_statement)
print(parsed_tree)
