**Streamlit** is a Python library that turns a plain `.py` script into an interactive web app — no HTML, CSS, or
JavaScript required. You write Python, it renders a UI in the browser.

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")
st.title("My Dashboard")
st.dataframe(df)
```

That's a working app. Run it with `streamlit run app.py` and you get a live browser page.

---

**Use Streamlit when you want to:**

- **Share data work** — turn a notebook or analysis script into something a non-technical colleague can actually use,
  without building a real web app
- **Build internal tools** — dashboards, filters, file processors, report generators for your team
- **Prototype fast** — spin up a UI around a model or API in an afternoon, not a week
- **Explore data interactively** — add sliders, dropdowns, and filters to pandas/matplotlib/plotly output without a
  frontend

**Don't use it when you need:**

- A public-facing production app with many concurrent users (it's not a web framework)
- Complex routing, auth systems, or custom UX — that's Flask/FastAPI + React territory
- Real-time streaming data at scale
- Fine-grained control over the UI

---

The sweet spot is **the gap between a Jupyter notebook and a full web app** — when a notebook is too static to share,
but building a proper frontend is overkill. Data scientists, ML engineers, and analysts use it heavily for exactly that
reason.

**Sample application - [myxls](../../funstuff/myxls)**