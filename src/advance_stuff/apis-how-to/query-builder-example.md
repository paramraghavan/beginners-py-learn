## QueryBuilder - Complete Implementation

### Version 1: Without Encapsulation

```python
class QueryBuilder:
    """Basic query builder - exposes internal state"""
    
    def __init__(self, table):
        self.table = table
        self.wheres = []      # Public - anyone can modify
        self.orders = []      # Public - anyone can modify
        self.limit_value = None
        self.offset_value = None
    
    def where(self, field, operator, value):
        """Add WHERE condition"""
        self.wheres.append((field, operator, value))
        # No return statement - can't chain
    
    def order_by(self, field, direction='ASC'):
        """Add ORDER BY clause"""
        self.orders.append((field, direction))
    
    def limit(self, n):
        """Set LIMIT"""
        self.limit_value = n
    
    def offset(self, n):
        """Set OFFSET"""
        self.offset_value = n
    
    def build(self):
        """Build the SQL query string"""
        query = f"SELECT * FROM {self.table}"
        
        # Build WHERE clause
        if self.wheres:
            conditions = []
            for field, operator, value in self.wheres:
                if isinstance(value, str):
                    conditions.append(f"{field} {operator} '{value}'")
                else:
                    conditions.append(f"{field} {operator} {value}")
            query += " WHERE " + " AND ".join(conditions)
        
        # Build ORDER BY clause
        if self.orders:
            order_parts = [f"{field} {direction}" for field, direction in self.orders]
            query += " ORDER BY " + ", ".join(order_parts)
        
        # Add LIMIT
        if self.limit_value:
            query += f" LIMIT {self.limit_value}"
        
        # Add OFFSET
        if self.offset_value:
            query += f" OFFSET {self.offset_value}"
        
        return query


# Usage - verbose and non-chainable
builder = QueryBuilder('users')
builder.where('age', '>', 18)
builder.where('status', '=', 'active')
builder.order_by('created_at', 'DESC')
builder.limit(10)
sql = builder.build()
print(sql)
# SELECT * FROM users WHERE age > 18 AND status = 'active' ORDER BY created_at DESC LIMIT 10
```

**Problems:**
- Can't chain methods - must call each one separately
- Internal state (`wheres`, `orders`) is public - can be accidentally modified
- No validation of inputs

***

### Version 2: With Encapsulation (Production-Ready)

```python
class QueryBuilder:
    """
    Fluent query builder with encapsulation.
    Supports method chaining and safe SQL generation.
    """
    
    def __init__(self, table):
        if not table:
            raise ValueError("Table name cannot be empty")
        
        self._table = table           # Private - implementation detail
        self._wheres = []             # Private - protected from direct access
        self._orders = []             # Private
        self._limit_value = None      # Private
        self._offset_value = None     # Private
        self._select_fields = ['*']   # Private - what columns to select
    
    def select(self, *fields):
        """
        Specify which fields to select.
        Example: .select('id', 'name', 'email')
        """
        if not fields:
            raise ValueError("Must specify at least one field")
        self._select_fields = list(fields)
        return self  # Enable chaining
    
    def where(self, field, operator, value):
        """
        Add WHERE condition with validation.
        
        Args:
            field: Column name
            operator: SQL operator (=, !=, >, <, >=, <=, LIKE, IN)
            value: Value to compare
        
        Returns:
            self (for chaining)
        """
        valid_operators = ['=', '!=', '>', '<', '>=', '<=', 'LIKE', 'IN', 'NOT IN']
        if operator not in valid_operators:
            raise ValueError(f"Invalid operator: {operator}. Must be one of {valid_operators}")
        
        self._wheres.append({
            'field': field,
            'operator': operator,
            'value': value
        })
        return self  # Enables chaining
    
    def where_in(self, field, values):
        """
        Convenience method for WHERE field IN (values).
        Example: .where_in('status', ['active', 'pending'])
        """
        if not isinstance(values, (list, tuple)):
            raise ValueError("Values must be a list or tuple")
        return self.where(field, 'IN', values)
    
    def order_by(self, field, direction='ASC'):
        """
        Add ORDER BY clause.
        
        Args:
            field: Column to sort by
            direction: 'ASC' or 'DESC'
        
        Returns:
            self (for chaining)
        """
        direction = direction.upper()
        if direction not in ['ASC', 'DESC']:
            raise ValueError("Direction must be 'ASC' or 'DESC'")
        
        self._orders.append({'field': field, 'direction': direction})
        return self  # Enables chaining
    
    def limit(self, n):
        """
        Set LIMIT with validation.
        
        Args:
            n: Number of rows to return (must be positive integer)
        
        Returns:
            self (for chaining)
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Limit must be a positive integer")
        self._limit_value = n
        return self  # Enables chaining
    
    def offset(self, n):
        """
        Set OFFSET with validation.
        
        Args:
            n: Number of rows to skip (must be non-negative integer)
        
        Returns:
            self (for chaining)
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("Offset must be a non-negative integer")
        self._offset_value = n
        return self  # Enables chaining
    
    def _escape_value(self, value):
        """
        Private helper to safely escape SQL values.
        Prevents SQL injection by properly formatting values.
        """
        if value is None:
            return 'NULL'
        elif isinstance(value, str):
            # Escape single quotes to prevent SQL injection
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        elif isinstance(value, bool):
            return '1' if value else '0'
        elif isinstance(value, (list, tuple)):
            # For IN clauses
            escaped_items = [self._escape_value(item) for item in value]
            return f"({', '.join(escaped_items)})"
        else:
            return str(value)
    
    def _build_where_clause(self):
        """Private helper to build WHERE clause."""
        if not self._wheres:
            return ""
        
        conditions = []
        for condition in self._wheres:
            field = condition['field']
            operator = condition['operator']
            value = condition['value']
            
            escaped_value = self._escape_value(value)
            conditions.append(f"{field} {operator} {escaped_value}")
        
        return " WHERE " + " AND ".join(conditions)
    
    def _build_order_clause(self):
        """Private helper to build ORDER BY clause."""
        if not self._orders:
            return ""
        
        order_parts = [
            f"{order['field']} {order['direction']}" 
            for order in self._orders
        ]
        return " ORDER BY " + ", ".join(order_parts)
    
    def build(self):
        """
        Build and return the final SQL query string.
        
        Returns:
            str: Complete SQL query
        """
        # SELECT clause
        fields = ', '.join(self._select_fields)
        query = f"SELECT {fields} FROM {self._table}"
        
        # WHERE clause
        query += self._build_where_clause()
        
        # ORDER BY clause
        query += self._build_order_clause()
        
        # LIMIT clause
        if self._limit_value is not None:
            query += f" LIMIT {self._limit_value}"
        
        # OFFSET clause
        if self._offset_value is not None:
            query += f" OFFSET {self._offset_value}"
        
        return query
    
    def __str__(self):
        """String representation - calls build()."""
        return self.build()
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"QueryBuilder(table='{self._table}', conditions={len(self._wheres)})"


# Example Usage - Beautiful Fluent API
print("=== Example 1: Simple Query ===")
query1 = (QueryBuilder('users')
          .where('age', '>', 18)
          .where('status', '=', 'active')
          .order_by('created_at', 'DESC')
          .limit(10)
          .build())
print(query1)
# SELECT * FROM users WHERE age > 18 AND status = 'active' ORDER BY created_at DESC LIMIT 10

print("\n=== Example 2: Select Specific Fields ===")
query2 = (QueryBuilder('products')
          .select('id', 'name', 'price')
          .where('price', '<', 100)
          .where('in_stock', '=', True)
          .order_by('price', 'ASC')
          .limit(5)
          .build())
print(query2)
# SELECT id, name, price FROM products WHERE price < 100 AND in_stock = 1 ORDER BY price ASC LIMIT 5

print("\n=== Example 3: Using WHERE IN ===")
query3 = (QueryBuilder('orders')
          .where_in('status', ['pending', 'processing', 'shipped'])
          .order_by('created_at', 'DESC')
          .limit(20)
          .offset(10)
          .build())
print(query3)
# SELECT * FROM orders WHERE status IN ('pending', 'processing', 'shipped') ORDER BY created_at DESC LIMIT 20 OFFSET 10

print("\n=== Example 4: Complex Query ===")
query4 = (QueryBuilder('employees')
          .select('first_name', 'last_name', 'salary', 'department')
          .where('salary', '>=', 50000)
          .where('department', '=', 'Engineering')
          .where('status', '=', 'active')
          .order_by('salary', 'DESC')
          .order_by('last_name', 'ASC')
          .limit(25)
          .build())
print(query4)

print("\n=== Example 5: SQL Injection Protection ===")
# Notice how single quotes are properly escaped
dangerous_input = "admin' OR '1'='1"
query5 = (QueryBuilder('users')
          .where('username', '=', dangerous_input)
          .build())
print(query5)
# SELECT * FROM users WHERE username = 'admin'' OR ''1''=''1'
# The single quotes are escaped, preventing SQL injection

print("\n=== Example 6: Validation Examples ===")
try:
    QueryBuilder('users').limit(-5)  # Should raise error
except ValueError as e:
    print(f"Error caught: {e}")

try:
    QueryBuilder('users').where('age', 'INVALID_OP', 18)  # Should raise error
except ValueError as e:
    print(f"Error caught: {e}")
```

**Output:**
```
=== Example 1: Simple Query ===
SELECT * FROM users WHERE age > 18 AND status = 'active' ORDER BY created_at DESC LIMIT 10

=== Example 2: Select Specific Fields ===
SELECT id, name, price FROM products WHERE price < 100 AND in_stock = 1 ORDER BY price ASC LIMIT 5

=== Example 3: Using WHERE IN ===
SELECT * FROM orders WHERE status IN ('pending', 'processing', 'shipped') ORDER BY created_at DESC LIMIT 20 OFFSET 10

=== Example 4: Complex Query ===
SELECT first_name, last_name, salary, department FROM employees WHERE salary >= 50000 AND department = 'Engineering' AND status = 'active' ORDER BY salary DESC, last_name ASC LIMIT 25

=== Example 5: SQL Injection Protection ===
SELECT * FROM users WHERE username = 'admin'' OR ''1''=''1'

=== Example 6: Validation Examples ===
Error caught: Limit must be a positive integer
Error caught: Invalid operator: INVALID_OP. Must be one of ['=', '!=', '>', '<', '>=', '<=', 'LIKE', 'IN', 'NOT IN']
```

***

## Key Implementation Details

| Feature | How It's Implemented | Why It Matters |
|---------|---------------------|----------------|
| **Method Chaining** | Every method returns `self` | Enables fluent, readable API |
| **Private State** | `_wheres`, `_orders`, etc. | Hides implementation, prevents tampering |
| **Input Validation** | Check types and values in each method | Fail fast with clear errors |
| **SQL Injection Protection** | `_escape_value()` helper method | Security - escapes dangerous characters |
| **Helper Methods** | `_build_where_clause()`, etc. | Keeps public API clean, logic organized |
| **Convenience Methods** | `where_in()` wraps common pattern | Makes common tasks simple |
| **Magic Methods** | `__str__()` and `__repr__()` | Natural string conversion |

