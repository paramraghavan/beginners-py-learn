# Apache Superset

Apache Superset is an open-source **data exploration and visualization platform** built by Airbnb and donated to the
Apache Software Foundation. It lets you connect to almost any database, explore data with SQL, and build interactive
dashboards — all through a browser UI with no coding required.

Superset is best suited for **analysts and teams** who want Tableau/Looker-like dashboards without the licensing cost.
It's production-ready and used at Airbnb, Twitter, Netflix, and many others.

---

## Key Features

| Feature              | Description                                                        |
|----------------------|--------------------------------------------------------------------|
| **SQL Lab**          | In-browser SQL editor with autocomplete                            |
| **Charts**           | 40+ chart types (bar, line, map, heatmap, etc.)                    |
| **Dashboards**       | Drag-and-drop, filterable, shareable                               |
| **Database support** | PostgreSQL, MySQL, BigQuery, Snowflake, Redshift, SQLite, and more |
| **No-code explore**  | Point-and-click data exploration without writing SQL               |
| **Access control**   | Role-based permissions per dashboard/dataset                       |

---

## Installation

### Option 1 — Docker (easiest)

```bash
# Clone the repo
git clone https://github.com/apache/superset.git
cd superset

# Start with Docker Compose
docker compose -f docker-compose-image-tag.yml up
```

Then open `http://localhost:8088` — default login is `admin` / `admin`.

### Option 2 — pip

```bash
# Install Superset
pip install apache-superset

# Set a secret key
export SUPERSET_SECRET_KEY='your-secret-key'

# Initialize the database
superset db upgrade

# Create an admin user
superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin

# Load example data (optional)
superset load_examples

# Start the server
superset run -p 8088 --with-threads --reload
```

---

## How to Use It — Step by Step

### 1. Connect a Database

Go to **Settings → Database Connections → + Database**, pick your DB type and enter the connection string.

```
# Example SQLAlchemy URIs
postgresql://user:pass@localhost/mydb
mysql://user:pass@localhost/mydb
bigquery://your-project-id
sqlite:////path/to/file.db
```

### 2. Register a Dataset

Go to **Datasets → + Dataset**, select your database and table. This creates a logical layer Superset uses for charts.

### 3. Explore Data (No-Code)

Click a dataset → **Explore**. Use the sidebar to:

- Pick a **chart type** (bar, pie, time-series, etc.)
- Set **Metrics** (SUM, COUNT, AVG)
- Set **Dimensions** / Group By columns
- Apply **Filters**
- Hit **Run** to preview

### 4. Write SQL in SQL Lab

Go to **SQL Lab → SQL Editor**:

```sql
SELECT
  order_date,
  region,
  SUM(revenue) AS total_revenue
FROM sales
WHERE order_date >= '2024-01-01'
GROUP BY 1, 2
ORDER BY 1;
```

You can save the result as a **virtual dataset** and build charts from it.

### 5. Build a Dashboard

Go to **Dashboards → + Dashboard**:

- Drag saved charts onto the canvas
- Add **filters** that apply across all charts
- Set **auto-refresh** for live data
- Share via link or embed with an iframe

---

## Connecting Popular Databases

```bash
# Install the right driver alongside Superset
pip install apache-superset

# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install mysqlclient

# BigQuery
pip install sqlalchemy-bigquery

# Snowflake
pip install snowflake-sqlalchemy

# Amazon Redshift
pip install sqlalchemy-redshift
```

---

## Example: Full Workflow in Python (Superset API)

Superset also has a REST API you can automate:

```python
import requests

BASE = "http://localhost:8088/api/v1"

# 1. Login and get token
token = requests.post(f"{BASE}/security/login", json={
    "username": "admin",
    "password": "admin",
    "provider": "db"
}).json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# 2. List all dashboards
dashboards = requests.get(f"{BASE}/dashboard/", headers=headers).json()
for d in dashboards["result"]:
    print(d["id"], d["dashboard_title"])

# 3. Get a specific chart's data
chart_data = requests.get(f"{BASE}/chart/1", headers=headers).json()
print(chart_data["result"]["viz_type"])
```

---

## TL;DR

```
Database  →  Dataset  →  Chart  →  Dashboard
   ↑                                    ↓
Connect your DB        Share / embed / schedule
```

