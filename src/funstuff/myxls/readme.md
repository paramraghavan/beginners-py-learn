# Run this app
```shell
streamlit run app.py
```

## 1. The "Editable Grid" Pattern
For an Excel-like experience, `st.dataframe` (read-only) isn't enough. You need `st.data_editor`.

```python
# Turns your dataframe into a live spreadsheet
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

if st.button("Save Changes"):
    st.session_state.master_df = edited_df
    st.success("Spreadsheet updated!")
```
* **Why it's resourceful:** It allows users to fix typos or manually add rows—bridging the gap between a "tool" and a "spreadsheet."

---

## 2. The "Graceful Failure" Pattern
Data operations (like joins or math) often crash due to mismatched types or missing columns.

```python
try:
    result = pd.merge(df1, df2, on=join_key)
except KeyError:
    st.error(f"Error: The column '{join_key}' was not found in one of the files.")
    st.stop() # Stops execution before the app crashes
except Exception as e:
    st.exception(e)
```
* **The Pattern:** Always wrap your **Pandas** operations in `try/except` blocks to keep the UI from showing a "Red Screen of Death" to the user.

---

## 3. The "Stateful Pipeline" Pattern
Since you want to "save results and perform further actions," you need a way to track the **history of dataframes**.

```python
# Initialise a dictionary to hold named versions of data
if "data_versions" not in st.session_state:
    st.session_state.data_versions = {}

# When a join is done:
new_version_name = f"Join_{len(st.session_state.data_versions)}"
st.session_state.data_versions[new_version_name] = result_df

# Let the user pick WHICH version to work on next
source = st.selectbox("Select source for next operation", 
                      options=list(st.session_state.data_versions.keys()))
```

---

## 4. Enhanced "Data Cleaning" Pattern
Add a utility section for common "Swiss Army" tasks that users expect.

```python
# Quick Cleaning Actions
col1, col2, col3 = st.columns(3)
if col1.button("Drop Duplicates"):
    df.drop_duplicates(inplace=True)
if col2.button("Fill Empty with 0"):
    df.fillna(0, inplace=True)
if col3.button("Drop Empty Rows"):
    df.dropna(inplace=True)
```

---

## 5. Performance for "N Number" of Files
If a user uploads 50 files, your sidebar will get messy. Use an **Expander** for file management.

```python
with st.sidebar.expander("📁 Managed Loaded Files", expanded=False):
    for name in list(st.session_state.dfs.keys()):
        cols = st.columns([3, 1])
        cols[0].write(name)
        if cols[1].button("🗑️", key=f"del_{name}"):
            del st.session_state.dfs[name]
            st.rerun()
```

---

## Updated "Swiss Army" Cheatsheet Additions

| Feature | Pattern / Command | Goal |
| :--- | :--- | :--- |
| **Spreadsheet Edit** | `st.data_editor(df)` | Let users edit data directly. |
| **Safe Execution** | `try: ... except: st.stop()` | Prevent app crashes on bad data. |
| **Dynamic Keys** | `key=f"widget_{index}"` | Use in loops to avoid DuplicateKeyErrors. |
| **Memory Cleanup** | `del st.session_state.key` | Free up RAM when handling large CSVs. |
| **Progress Tracking** | `st.status("Processing...")` | Better UX for long-running joins. |

### Pro-Tip for the Team:
When building the "Join" logic, use `st.multiselect` to allow users to select multiple columns for a composite key (e.g., joining on both "Date" AND "Store_ID").
