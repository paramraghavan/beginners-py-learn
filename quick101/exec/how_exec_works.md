# Exec
You need to run user-provided Python code that you don't know in advance.

## 🎯 What This Code Does

It **runs user-provided code as a string** and gives that code access to specific variables.

---

## 📚 Simple Examples (Building Up)

### **Example 1: Basic exec()**

```python
# Simple code as a string
code = "result = 5 + 3"

# Execute the string as Python code
exec(code)

# Now 'result' exists as a variable
print(result)  # Output: 8
```

**What happened?**

- `exec()` ran the string `"result = 5 + 3"` as if you typed it
- Created a variable `result` with value 8

---

### **Example 2: Using Variables in exec()**

```python
# We have a variable
x = 10

# Code that uses 'x'
code = "y = x * 2"

# Execute - it can see 'x'
exec(code)

print(y)  # Output: 20
```

**Problem:** Code can access ALL variables in scope! ⚠️

---

### **Example 3: Controlled Variables (Safe)**

```python
# We have variables
x = 10
secret = "don't touch me!"

# Create a namespace with ONLY what code should see
namespace = {'x': x}

# Execute code with controlled namespace
code = "y = x * 2"
exec(code, {}, namespace)

# Get result from namespace
y = namespace['y']

print(y)  # Output: 20
print('secret' in namespace)  # Output: False (code couldn't see 'secret')
```

**Key point:** Code only sees what's in `namespace`! ✅

---

## 🔍 Your Transform Example (Step by Step)

### **Setup:**

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Your DataFrame (imagine a table with loan data)
df = spark.createDataFrame([
    (1, 30000, "2026-01-01"),
    (2, 60000, "2026-01-02"),
    (3, 45000, "2026-01-03")
], ["loan_id", "loan_amount", "effective_date"])

print("BEFORE TRANSFORM:")
df.show()
# Output:
# +-------+-----------+--------------+
# |loan_id|loan_amount|effective_date|
# +-------+-----------+--------------+
# |      1|      30000|    2026-01-01|
# |      2|      60000|    2026-01-02|
# |      3|      45000|    2026-01-03|
# +-------+-----------+--------------+
```

---

### **User Provides Transform Code (as string):**

```python
# This is what the user types in the web UI
transform_code = """
# Filter high-value loans
df = df.filter(df['loan_amount'] > 40000)

# Add a new column
df = df.withColumn('amount_thousands', F.col('loan_amount') / 1000)
"""

# This is just a STRING, not executed yet!
print(type(transform_code))  # Output: <class 'str'>
```

---

### **Execute Transform (Your Code):**

```python
# Step 1: Create namespace with tools the user needs
local_vars = {
    'df': df,  # The DataFrame
    'F': F,  # PySpark functions
    'Window': Window  # Window functions
}

print("BEFORE exec():")
print("local_vars keys:", local_vars.keys())
# Output: dict_keys(['df', 'F', 'Window'])

# Step 2: Execute user's code
# exec(code, globals, locals)
#      - code: the string to execute
#      - globals: {} means no global variables
#      - locals: local_vars means use this dictionary for variables
exec(transform_code, {}, local_vars)

print("\nAFTER exec():")
print("local_vars keys:", local_vars.keys())
# Output: dict_keys(['df', 'F', 'Window'])
# Note: 'df' was MODIFIED by the code!

# Step 3: Get the transformed DataFrame back
transformed_df = local_vars['df']

print("\nAFTER TRANSFORM:")
transformed_df.show()
# Output:
# +-------+-----------+--------------+-----------------+
# |loan_id|loan_amount|effective_date|amount_thousands |
# +-------+-----------+--------------+-----------------+
# |      2|      60000|    2026-01-02|             60.0|
# |      3|      45000|    2026-01-03|             45.0|
# +-------+-----------+--------------+-----------------+
```

---

## 🔬 What Happened Inside exec()?

### **Visualization:**

```python
# BEFORE exec():
local_vars = {
                 'df': DataFrame[loan_id, loan_amount, effective_date],  # 3 rows
                 'F': < pyspark.sql.functions >,
'Window': < pyspark.sql.window.Window >
}

# USER'S CODE EXECUTES:
# df = df.filter(df['loan_amount'] > 40000)
# df = df.withColumn('amount_thousands', F.col('loan_amount') / 1000)

# AFTER exec():
local_vars = {
                 'df': DataFrame[loan_id, loan_amount, effective_date, amount_thousands],  # 2 rows now!
                 'F': < pyspark.sql.functions >,
'Window': < pyspark.sql.window.Window >
}
```

**Key:** The `df` inside `local_vars` was **replaced** by the transformed DataFrame!

---

## 🎓 Complete Working Example

```python
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window

# Initialize Spark
spark = SparkSession.builder.appName("exec_example").getOrCreate()

# Create sample data
df = spark.createDataFrame([
    (1, 30000), (2, 60000), (3, 45000), (4, 80000)
], ["id", "amount"])

print("=" * 60)
print("ORIGINAL DATA:")
print("=" * 60)
df.show()

# User provides this as a string (from web UI)
transform_code = """
# Filter
df = df.filter(df['amount'] > 40000)

# Add column
df = df.withColumn('amount_k', F.col('amount') / 1000)

# Sort
df = df.orderBy(F.desc('amount'))
"""

print("=" * 60)
print("USER'S TRANSFORM CODE:")
print("=" * 60)
print(transform_code)

# Execute transform
print("=" * 60)
print("EXECUTING TRANSFORM...")
print("=" * 60)

# Step 1: Setup namespace
local_vars = {'df': df, 'F': F, 'Window': Window}

# Step 2: Execute
exec(transform_code, {}, local_vars)

# Step 3: Get result
transformed_df = local_vars['df']

print("=" * 60)
print("TRANSFORMED DATA:")
print("=" * 60)
transformed_df.show()

# Output:
# ============================================================
# ORIGINAL DATA:
# ============================================================
# +---+------+
# | id|amount|
# +---+------+
# |  1| 30000|
# |  2| 60000|
# |  3| 45000|
# |  4| 80000|
# +---+------+
#
# ============================================================
# USER'S TRANSFORM CODE:
# ============================================================
# # Filter
# df = df.filter(df['amount'] > 40000)
# 
# # Add column
# df = df.withColumn('amount_k', F.col('amount') / 1000)
# 
# # Sort
# df = df.orderBy(F.desc('amount'))
#
# ============================================================
# EXECUTING TRANSFORM...
# ============================================================
# ============================================================
# TRANSFORMED DATA:
# ============================================================
# +---+------+--------+
# | id|amount|amount_k|
# +---+------+--------+
# |  4| 80000|    80.0|
# |  2| 60000|    60.0|
# |  3| 45000|    45.0|
# +---+------+--------+
```

---

## 💡 Why This Pattern?

### **Without Controlled Namespace (UNSAFE):**

```python
# BAD - User code can access EVERYTHING
admin_password = "secret123"
df = ...

exec(transform_code)  # User could access admin_password!

# User could write:
# transform_code = "print(admin_password)"  # Security risk!
```

### **With Controlled Namespace (SAFE):**

```python
# GOOD - User code only sees what we give
admin_password = "secret123"
df = ...

local_vars = {'df': df, 'F': F, 'Window': Window}
exec(transform_code, {}, local_vars)  # User CANNOT see admin_password

# User writes:
# transform_code = "print(admin_password)"  # NameError! Not in namespace
```

---

## 📊 Diagram: How It Works

```
┌─────────────────────────────────────────────────────────┐
│                  BEFORE exec()                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  local_vars = {                                         │
│      'df': DataFrame(3 rows),                           │
│      'F': pyspark.sql.functions,                        │
│      'Window': pyspark.sql.window.Window                │
│  }                                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         ↓
                         ↓ exec(transform_code, {}, local_vars)
                         ↓
┌─────────────────────────────────────────────────────────┐
│              INSIDE exec() - Code Runs                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Line 1: df = df.filter(df['amount'] > 40000)          │
│          → local_vars['df'] is now filtered            │
│                                                         │
│  Line 2: df = df.withColumn('amount_k', ...)           │
│          → local_vars['df'] now has new column         │
│                                                         │
│  Line 3: df = df.orderBy(...)                          │
│          → local_vars['df'] is now sorted              │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         ↓
                         ↓ exec() completes
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   AFTER exec()                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  local_vars = {                                         │
│      'df': DataFrame(2 rows, 3 columns),  ← CHANGED!   │
│      'F': pyspark.sql.functions,                        │
│      'Window': pyspark.sql.window.Window                │
│  }                                                      │
│                                                         │
│  transformed_df = local_vars['df']  ← Extract result   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Points

1. **exec() runs strings as code:**
   ```python
   code = "x = 5"
   exec(code)  # Same as typing: x = 5
   ```

2. **Controlled namespace = security:**
   ```python
   local_vars = {'df': df}
   exec(code, {}, local_vars)  # Code only sees 'df'
   ```

3. **Variables modified in exec() stay in namespace:**
   ```python
   local_vars = {'df': original_df}
   exec("df = df.filter(...)", {}, local_vars)
   # local_vars['df'] is now the filtered df
   ```

4. **Why 3 arguments to exec()?**
   ```python
   exec(code, globals, locals)
   #    ^^^^  ^^^^^^^  ^^^^^^
   #    │     │        └─ Local variables dict
   #    │     └─ Global variables dict (we use {})
   #    └─ Code to execute (string)
   ```

---

## 🎯 Summary

**Your snippet:**

```python
local_vars = {'df': df, 'F': F, 'Window': Window}
exec(transform_code, {}, local_vars)
transformed_df = local_vars['df']
```

**Means:**

1. Put `df`, `F`, `Window` in a dictionary
2. Run user's code (string) with access ONLY to that dictionary
3. Get back the modified `df` from the dictionary

**It's like:**

- Giving someone a toolbox (local_vars)
- Letting them work with the tools (exec)
- Taking back the finished product (transformed_df)
