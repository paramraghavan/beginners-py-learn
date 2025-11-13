
# ✅ **1. Sort list of dicts by a specific key**

```python
data = [
    {"name": "Krishna", "age": 20},
    {"name": "Arjun", "age": 18},
    {"name": "Bheem", "age": 25}
]

sorted_data = sorted(data, key=lambda x: x["age"])
print(sorted_data)
```

**Output:**

```python
[
    {'name': 'Arjun', 'age': 18},
    {'name': 'Krishna', 'age': 20},
    {'name': 'Bheem', 'age': 25}
]
```

---

# ✅ **2. Sort in descending order**

```python
sorted_data = sorted(data, key=lambda x: x['age'], reverse=True)
```

---

# ✅ **3. Sort by multiple keys**

For example, primary sort by `age`, secondary by `name`:

```python
sorted_data = sorted(data, key=lambda x: (x["age"], x["name"]))
```

---

# ✅ **4. Sort ignoring upper/lowercase**

```python
sorted_data = sorted(data, key=lambda x: x["name"].lower())
```

---

# ✅ **5. Sort safely when some keys may be missing**

```python
sorted_data = sorted(data, key=lambda x: x.get("age", 0))
```

