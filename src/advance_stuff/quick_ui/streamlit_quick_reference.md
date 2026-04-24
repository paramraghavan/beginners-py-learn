# Streamlit Quick Reference

A short, practical guide to the patterns you'll use in almost every app.

---

## Run & Structure

```bash
# run
streamlit run app.py

# specific port
streamlit run app.py --server.port 8080
```

```python
import streamlit as st
import pandas as pd

# must be the very first st call — nothing before it
st.set_page_config(page_title="App", layout="wide")
st.title("My App")
```

> **Key mental model:** Streamlit reruns the entire script top-to-bottom on every interaction. Keep heavy work inside
> cached functions. Never put side effects (DB writes, API calls) at the top level — wrap them in buttons or cached
> functions.

---

## Text Output

```python
st.title("H1")
st.header("H2")
st.subheader("H3")
st.write("accepts anything: str, df, fig…")
st.markdown("**bold**, `code`, [link](url)")
st.code(some_string, language="python")
st.metric("Revenue", "$4.2M", delta="+12%")
```

---

## Input Widgets

### Text & numbers

```python
name = st.text_input("Name", value="Alice")
note = st.text_area("Notes", height=100)
n = st.number_input("Count", min_value=0, step=1)
pwd = st.text_input("Pass", type="password")
```

### Selectors

```python
opt = st.selectbox("Pick one", ["a", "b", "c"])
many = st.multiselect("Pick many", options)
val = st.slider("Value", 0, 100, 50)
rng = st.slider("Range", 0, 100, (20, 80))  # tuple = range slider
r = st.radio("Mode", ["A", "B"], horizontal=True)
```

### Actions & toggles

```python
clicked = st.button("Run")
toggled = st.toggle("Dark mode")
checked = st.checkbox("Agree")

# button is True only on the click frame
if st.button("Go"):
    st.success("Clicked!")
```

### Files & dates

```python
f = st.file_uploader("Upload", type=["csv", "xlsx"])
fs = st.file_uploader("Multi", accept_multiple_files=True)
d = st.date_input("Date")
t = st.time_input("Time")

if f:
    df = pd.read_csv(f)  # f is a file-like object
```

### Feedback

```python
st.success("Done ✓")
st.error("Something went wrong")
st.warning("Watch out")
st.info("FYI")
st.exception(err)  # shows full traceback

with st.spinner("Loading…"):
    result = slow_fn()
```

### The `key=` param — important!

```python
# Give widgets explicit keys when:
# • same widget type appears twice
# • widget lives inside a loop
# • you read the value from session_state

for i, row in df.iterrows():
    st.checkbox(row["name"], key=f"cb_{i}")
```

> **Warning:** Duplicate keys crash the app. Always use unique keys in loops.

---

## Layout

### Columns

```python
# even split
col1, col2 = st.columns(2)

# ratio split (3:1)
col1, col2 = st.columns([3, 1])

with col1:
    st.metric("Sales", 1200)
with col2:
    st.metric("Costs", 800)
```

### Sidebar

```python
# context manager
with st.sidebar:
    st.header("Filters")
    choice = st.selectbox("Region", regions)

# dot notation (same result)
choice = st.sidebar.selectbox("Region", regions)
```

> Put all inputs/filters in the sidebar — keeps the main area clean for output.

### Tabs

```python
tab1, tab2, tab3 = st.tabs(["Data", "Chart", "Info"])

with tab1:
    st.dataframe(df)
with tab2:
    st.line_chart(df["value"])
with tab3:
    st.write("some notes")
```

### Expander & empty placeholder

```python
with st.expander("Show details", expanded=False):
    st.dataframe(df)

# reserve a slot, fill it later
placeholder = st.empty()
# ... later in the script ...
placeholder.success("Done!")
```

### Forms — batch input

```python
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(name, age)
```

> Widgets inside a form don't trigger reruns until submit is clicked — great for multi-field inputs.

### Display data

```python
st.dataframe(df, use_container_width=True)
st.dataframe(df, height=300)  # fixed height
st.table(df)  # static, no sorting
st.json({"key": "value"})
st.image(img, caption="fig", width=400)
st.pyplot(fig)  # matplotlib
st.plotly_chart(fig, use_container_width=True)
```

---

## Session State

### Basics

```python
# initialise — always guard with `in`
if "count" not in st.session_state:
    st.session_state.count = 0

# read (dot or dict syntax — both work)
x = st.session_state.count
x = st.session_state["count"]

# write
st.session_state.count += 1
```

### Widget ↔ state sync

```python
# widget value auto-syncs to session_state via key=
st.text_input("Name", key="username")
# now st.session_state.username holds the current value

# pre-populate a widget default
if "username" not in st.session_state:
    st.session_state.username = "Alice"
st.text_input("Name", key="username")
```

> **Warning:** Never set a keyed widget's value via `session_state` after it has already been rendered — causes a
> conflict error.

### Callbacks

```python
def on_change():
    # runs before the rerun, value is already updated
    st.session_state.derived = st.session_state.raw * 2


st.number_input("Input", key="raw", on_change=on_change)

# on_click for buttons
st.button("Reset", on_click=lambda:
st.session_state.update({"count": 0}))
```

### Accumulate history

```python
if "log" not in st.session_state:
    st.session_state.log = []

if st.button("Add entry"):
    st.session_state.log.append("new item")

for entry in st.session_state.log:
    st.write(entry)
```

> Lists and dicts in `session_state` persist across reruns — use them to build chat history, undo stacks, or multi-step
> wizards.

---

## Data & Caching

### `@st.cache_data` — for data

```python
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)


# ttl — expire cache after N seconds
@st.cache_data(ttl=300)
def fetch_api(url):
    return requests.get(url).json()
```

> Use `cache_data` for anything that returns serialisable data: DataFrames, dicts, strings, numbers.

### `@st.cache_resource` — for connections

```python
@st.cache_resource
def get_db():
    return psycopg2.connect(DB_URL)


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")
```

> Use `cache_resource` for objects that shouldn't be copied: DB connections, ML models, API clients.

### File upload → DataFrame

```python
f = st.file_uploader("CSV or Excel", type=["csv", "xlsx", "xls"])
if f:
    if f.name.endswith(".csv"):
        df = pd.read_csv(f)
    else:
        df = pd.read_excel(f)
    st.dataframe(df)
```

### Download button

```python
# CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download CSV",
                   data=csv,
                   file_name="result.csv",
                   mime="text/csv")

# Excel
import io

buf = io.BytesIO()
df.to_excel(buf, index=False)
st.download_button("⬇ Excel", buf, "output.xlsx")
```

---

## Power Patterns

### 1. Gated execution — run expensive work only on button press

```python
if "result" not in st.session_state:
    st.session_state.result = None

if st.button("Run analysis"):
    with st.spinner():
        st.session_state.result = slow_fn()

if st.session_state.result is not None:
    st.dataframe(st.session_state.result)
```

> Result persists after the button press — expensive logic never re-runs on unrelated interactions.

### 2. Early stop — clean prerequisite handling

```python
uploaded = st.file_uploader("Upload CSV")
if not uploaded:
    st.info("Upload a file to continue.")
    st.stop()  # nothing below this line runs

df = pd.read_csv(uploaded)
st.dataframe(df)
```

> Avoids deeply nested `if` blocks — the rest of the script assumes the prerequisite is met.

### 3. Multi-step wizard

```python
if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.header("Step 1: Upload")
    # ... widgets ...
    if st.button("Next"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.header("Step 2: Configure")
    # ...
    col1, col2 = st.columns(2)
    if col1.button("Back"):
        st.session_state.step = 1
        st.rerun()
    if col2.button("Next"):
        st.session_state.step = 3
        st.rerun()
```

### 4. Dynamic sidebar filters

```python
with st.sidebar:
    regions = df["region"].unique().tolist()
    sel = st.multiselect("Region", regions, default=regions)
    min_v, max_v = st.slider(
        "Revenue",
        int(df["rev"].min()), int(df["rev"].max()),
        (int(df["rev"].min()), int(df["rev"].max()))
    )

filtered = df[
    df["region"].isin(sel) &
    df["rev"].between(min_v, max_v)
    ]
st.dataframe(filtered)
```

### 5. Live progress with placeholder

```python
status = st.empty()
progress = st.progress(0)

for i, item in enumerate(big_list):
    status.text(f"Processing {i + 1}/{len(big_list)}")
    progress.progress((i + 1) / len(big_list))
    process(item)

status.success("All done!")
progress.empty()
```

### 6. Secrets & config

```toml
# .streamlit/secrets.toml  (gitignored)
[db]
host = "localhost"
password = "secret"

# .streamlit/config.toml
[theme]
primaryColor = "#7b8cde"
```

```python
# access in your app
host = st.secrets["db"]["host"]
pw = st.secrets["db"]["password"]
```

> Never hardcode secrets. On Streamlit Cloud, set them in the project dashboard instead of `secrets.toml`.

---

## Quick Cheatsheet

| Need                                  | Use                              |
|---------------------------------------|----------------------------------|
| Persist value across reruns           | `st.session_state`               |
| Cache a slow data load                | `@st.cache_data`                 |
| Cache a DB connection / model         | `@st.cache_resource`             |
| Prevent rerun until all fields filled | `st.form`                        |
| Halt script if prerequisite missing   | `st.stop()`                      |
| Update a slot defined earlier         | `st.empty()`                     |
| Force a rerun programmatically        | `st.rerun()`                     |
| Batch-update state                    | `st.session_state.update({...})` |
| Show progress                         | `st.progress()` + `st.spinner()` |
| Read uploaded file                    | treat it as a file-like object   |
