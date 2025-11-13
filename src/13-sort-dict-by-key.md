# ✅ **1. Sort by key (item name) and get a new dict**

```python
d = {"banana": 3, "apple": 5, "cherry": 2}

sorted_d = dict(sorted(d.items()))
print(sorted_d)
```

**Output:**

```python
{'apple': 5, 'banana': 3, 'cherry': 2}
```

---

# ✅ **2. Sort by key in reverse order**

```python
sorted_d = dict(sorted(d.items(), reverse=True))
```

---

# ✅ **3. Sort keys manually and rebuild dictionary**

```python
sorted_d = {k: d[k] for k in sorted(d)}
```

---

# ✅ **4. If keys need custom sorting (case-insensitive)**

```python
sorted_d = dict(sorted(d.items(), key=lambda x: x[0].lower()))
```

