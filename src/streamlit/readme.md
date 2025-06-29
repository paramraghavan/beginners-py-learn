# Streamlit Tutorial for Python Developers

## What is Streamlit?

Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine
learning and data science. You can build interactive dashboards, data visualizations, and web applications with just a
few lines of Python code.

## Installation

```bash
pip install streamlit
```

## Basic Streamlit App Structure

Every Streamlit app follows this basic pattern:

```python
import streamlit as st

# App title
st.title("My First Streamlit App")

# Your app logic here
st.write("Hello, World!")
```

## Core Components

### 1. Text and Markdown

```python
import streamlit as st

# Different ways to display text
st.title("Main Title")
st.header("Header")
st.subheader("Subheader")
st.text("Fixed width text")
st.markdown("**Bold** and *italic* text")
st.write("General purpose write function")

# Code blocks
st.code("""
def hello():
    print("Hello, Streamlit!")
""", language='python')
```

### 2. Data Display

```python
import pandas as pd
import numpy as np

# Create sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Tokyo']
})

# Display dataframe
st.dataframe(df)

# Static table
st.table(df)

# Metrics
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
```

### 3. Charts and Visualizations

```python
import matplotlib.pyplot as plt
import plotly.express as px

# Line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

# Bar chart
st.bar_chart(chart_data)

# Plotly chart
fig = px.bar(df, x='Name', y='Age')
st.plotly_chart(fig)

# Matplotlib
fig, ax = plt.subplots()
ax.hist(np.random.randn(100), bins=20)
st.pyplot(fig)
```

### 4. Input Widgets

```python
# Text input
name = st.text_input("Enter your name:")

# Number input
age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)

# Slider
temperature = st.slider("Temperature", -10, 50, 25)

# Select box
city = st.selectbox("Choose your city:", ['New York', 'London', 'Tokyo'])

# Multi-select
languages = st.multiselect("Programming languages:",
                           ['Python', 'JavaScript', 'Java', 'C++'])

# Checkbox
agree = st.checkbox("I agree to the terms")

# Radio buttons
gender = st.radio("Gender:", ['Male', 'Female', 'Other'])

# Date input
import datetime

date = st.date_input("Select date:", datetime.date.today())

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
```

### 5. Layout and Containers

```python
# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")
with col3:
    st.write("Column 3")

# Sidebar
st.sidebar.title("Sidebar")
sidebar_input = st.sidebar.slider("Sidebar slider", 0, 100, 50)

# Expander
with st.expander("Click to expand"):
    st.write("Hidden content here")

# Container
with st.container():
    st.write("This is inside a container")
```

## Session State

Streamlit reruns your script from top to bottom every time you interact with widgets. Session state helps maintain state
across reruns:

```python
# Initialize session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0


# Button with callback
def increment_counter():
    st.session_state.counter += 1


st.button("Increment", on_click=increment_counter)
st.write(f"Counter: {st.session_state.counter}")
```

## Complete Example App

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Interactive Data Dashboard")

# Sidebar
st.sidebar.header("Configuration")
num_points = st.sidebar.slider("Number of data points:", 10, 1000, 100)
chart_type = st.sidebar.selectbox("Chart type:", ['scatter', 'line', 'bar'])


# Generate data
@st.cache_data
def generate_data(n):
    return pd.DataFrame({
        'x': np.random.randn(n),
        'y': np.random.randn(n),
        'category': np.random.choice(['A', 'B', 'C'], n)
    })


data = generate_data(num_points)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Data Visualization")
    if chart_type == 'scatter':
        fig = px.scatter(data, x='x', y='y', color='category')
    elif chart_type == 'line':
        fig = px.line(data, x='x', y='y', color='category')
    else:
        fig = px.bar(data.groupby('category').size().reset_index(name='count'),
                     x='category', y='count')

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Data Summary")
    st.dataframe(data.describe())

# Show raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(data)
```

## Running Your App

Save your Python file (e.g., `app.py`) and run:

```bash
streamlit run app.py
```

Your app will open in your browser at `http://localhost:8501`

## Best Practices

1. **Use caching**: Use `@st.cache_data` for expensive computations
2. **Organize with functions**: Break your app into functions for better organization
3. **Handle errors gracefully**: Use try-except blocks for file uploads and API calls
4. **Use session state wisely**: Only store necessary data in session state
5. **Optimize performance**: Avoid expensive operations in the main flow

## Debugging Streamlit Apps in PyCharm

### Method 1: Direct Debugging

1. **Create a run configuration:**
    - Go to `Run` → `Edit Configurations`
    - Click `+` and select `Python`
    - Set the following:
        - Name: `Streamlit App`
        - Script path: Path to your `streamlit` executable (find with `which streamlit`)
        - Parameters: `run your_app.py`
        - Working directory: Your project directory

2. **Set breakpoints** in your Python code as usual

3. **Run in debug mode** using the debug button

### Method 2: Using Python Script

Create a separate debug script (`debug_app.py`):

```python
import subprocess
import sys
import os

# Add your app directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your app modules here for debugging
import your_app_module

if __name__ == "__main__":
    # You can set breakpoints here and test individual functions
    # your_app_module.some_function()

    # Or run streamlit normally
    subprocess.run([sys.executable, "-m", "streamlit", "run", "your_app.py"])
```

### Method 3: Remote Debugging

For more complex debugging:

1. **Install debugpy:**
   ```bash
   pip install debugpy
   ```

2. **Add to your Streamlit app:**
   ```python
   import debugpy
   
   # Enable debugging (only in development)
   if st.sidebar.button("Enable Debug"):
       debugpy.listen(5678)
       debugpy.wait_for_client()
   ```

3. **Configure PyCharm:**
    - Go to `Run` → `Edit Configurations`
    - Add `Python Debug Server`
    - Set port to `5678`

### Debugging Tips

1. **Use st.write() for quick debugging:**
   ```python
   st.write("Debug info:", variable_name)
   ```

2. **Use st.sidebar for debug controls:**
   ```python
   debug_mode = st.sidebar.checkbox("Debug Mode")
   if debug_mode:
       st.write("Current state:", st.session_state)
   ```

3. **Create debug functions:**
   ```python
   def debug_dataframe(df, name="DataFrame"):
       if st.checkbox(f"Show {name} debug info"):
           st.write(f"{name} shape:", df.shape)
           st.write(f"{name} dtypes:", df.dtypes)
           st.write(f"{name} sample:", df.head())
   ```

4. **Use logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   
   def my_function():
       logging.debug("Function called")
       # Your code here
   ```

5. **Check the terminal output:** Streamlit shows errors and print statements in the terminal where you ran the app

