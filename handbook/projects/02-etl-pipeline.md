# 02 - ETL Pipeline Project

## Project Overview

Build a production-grade ETL (Extract, Transform, Load) pipeline that processes real-world data. This project integrates data engineering, SQL, cloud platforms, and monitoring.

**Duration:** 3-4 weeks
**Difficulty:** Intermediate-Advanced
**Best For:** Data Engineers
**Key Technologies:** Python, Pandas, Apache Spark, PostgreSQL, Airflow, AWS S3, Docker

---

## Learning Objectives

By completing this project, you'll learn:
- Design ETL architectures
- Extract data from multiple sources
- Transform and validate data
- Load data into data warehouses
- Schedule workflows with Airflow
- Monitor pipeline health
- Optimize for performance and cost
- Handle errors and retries

---

## Project Scenario

**Situation:** Build an ETL pipeline for an e-commerce company that:
- Ingests sales data from multiple sources (API, files, databases)
- Transforms raw data into business metrics
- Loads cleaned data into a data warehouse
- Generates daily reports
- Handles incremental loading (only new data)

**Data Sources:**
1. Orders API (REST, JSON)
2. Customer CSV files (uploaded daily)
3. Product database (SQL)
4. Click stream data (S3)

**Target:** PostgreSQL data warehouse with fact and dimension tables

---

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Data Sources                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Orders API  │  │ Customer CSVs│  │Product DB    │    │
│  └─────────────┘  └──────────────┘  └──────────────┘    │
└──────────────────────────────────────────────────────────┘
                         │
┌──────────────────────────────────────────────────────────┐
│              Extract (Apache Airflow)                     │
│  ┌──────────────────────────────────────────────────────┐│
│  │ Task 1: Fetch Orders API → S3/temp                  ││
│  │ Task 2: Download Customer CSVs → S3/temp            ││
│  │ Task 3: Query Products → S3/temp                    ││
│  └──────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
                         │
┌──────────────────────────────────────────────────────────┐
│              Transform (Spark/Pandas)                     │
│  ┌──────────────────────────────────────────────────────┐│
│  │ Task 1: Data Validation (Great Expectations)        ││
│  │ Task 2: Deduplicate Records                         ││
│  │ Task 3: Clean & Normalize                           ││
│  │ Task 4: Aggregate & Enrich Data                     ││
│  │ Task 5: Quality Checks                              ││
│  └──────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
                         │
┌──────────────────────────────────────────────────────────┐
│              Load (PostgreSQL)                            │
│  ┌──────────────────────────────────────────────────────┐│
│  │ Task 1: Load to Staging Tables                      ││
│  │ Task 2: Validate vs Production                      ││
│  │ Task 3: Atomic Swap to Production                   ││
│  │ Task 4: Update Metadata                             ││
│  └──────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
                         │
┌──────────────────────────────────────────────────────────┐
│       Data Warehouse (PostgreSQL) + Monitoring           │
│  ┌──────────────────────────────────────────────────────┐│
│  │ fact_orders (Transactions)                          ││
│  │ dim_customers (Customer profiles)                   ││
│  │ dim_products (Product catalog)                      ││
│  │ fact_daily_metrics (Aggregates)                     ││
│  └──────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

---

## Week-by-Week Implementation

### Week 1: Data Extraction & Initial Validation

**Goals:**
- Build data extractors for all sources
- Set up S3 for raw data storage
- Implement data validation
- Create logging framework

**Deliverables:**
- Orders API extractor
- CSV downloader
- Database query executor
- Data validation framework
- Logging and monitoring setup

**Key Code:**

```python
# extractors.py
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import boto3

logger = logging.getLogger(__name__)

class OrdersAPIExtractor:
    """Extract orders from REST API"""
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.s3 = boto3.client('s3')

    def extract(self, start_date: datetime, end_date: datetime) -> str:
        """Extract orders and save to S3"""
        logger.info(f"Extracting orders from {start_date} to {end_date}")

        orders = []
        page = 1

        while True:
            response = requests.get(
                f"{self.api_url}/orders",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "page": page,
                    "limit": 1000
                }
            )

            if response.status_code != 200:
                logger.error(f"API error: {response.status_code}")
                raise Exception(f"API error: {response.text}")

            data = response.json()
            if not data.get("results"):
                break

            orders.extend(data["results"])
            logger.info(f"Fetched {len(data['results'])} orders (page {page})")
            page += 1

        # Save to S3
        df = pd.DataFrame(orders)
        s3_path = f"s3://data-lake/raw/orders/{start_date.date()}.parquet"
        df.to_parquet(s3_path)
        logger.info(f"Saved {len(orders)} orders to {s3_path}")

        return s3_path


class CSVExtractor:
    """Extract customer data from CSV files"""
    def __init__(self, bucket: str):
        self.s3 = boto3.client('s3')
        self.bucket = bucket

    def extract(self, prefix: str) -> str:
        """Download CSVs from S3 and consolidate"""
        logger.info(f"Extracting CSVs from s3://{self.bucket}/{prefix}")

        # List all CSV files
        response = self.s3.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix
        )

        all_data = []
        for obj in response.get('Contents', []):
            key = obj['Key']
            logger.info(f"Processing {key}")

            # Download and read
            file_obj = self.s3.get_object(Bucket=self.bucket, Key=key)
            df = pd.read_csv(file_obj['Body'])
            all_data.append(df)

        # Consolidate
        consolidated = pd.concat(all_data, ignore_index=True)
        logger.info(f"Consolidated {len(consolidated)} customer records")

        # Save consolidated
        s3_path = f"s3://data-lake/raw/customers/{datetime.now().date()}.parquet"
        consolidated.to_parquet(s3_path)

        return s3_path


class DatabaseExtractor:
    """Extract from relational databases"""
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def extract(self, query: str, partition_key: str = None) -> str:
        """Execute query and save results"""
        logger.info(f"Executing query for {partition_key}")

        engine = create_engine(self.connection_string)
        df = pd.read_sql(query, engine)
        logger.info(f"Retrieved {len(df)} records")

        # Save to S3
        s3_path = f"s3://data-lake/raw/products/{datetime.now().date()}.parquet"
        df.to_parquet(s3_path)

        return s3_path


# Data validation
from great_expectations.dataset import PandasDataset

def validate_data(df: pd.DataFrame, expectations: dict) -> bool:
    """Validate data quality"""
    dataset = PandasDataset(df)

    for column, rules in expectations.items():
        for rule_name, rule_params in rules.items():
            if rule_name == "not_null":
                dataset.expect_column_values_to_not_be_null(column)
            elif rule_name == "unique":
                dataset.expect_column_values_to_be_unique(column)
            elif rule_name == "type":
                dataset.expect_column_values_to_be_of_type(column, rule_params)

    results = dataset.validate()
    logger.info(f"Validation: {results['success']}")
    return results['success']
```

---

### Week 2: Data Transformation & Quality

**Goals:**
- Design star schema (fact and dimension tables)
- Implement transformations
- Handle duplicates and nulls
- Create data quality checks

**Deliverables:**
- Transformation logic for each data source
- Dimension tables (customers, products)
- Fact table (orders)
- Quality validation tests
- Transformation documentation

**Key Code:**

```python
# transformations.py
import pandas as pd
from datetime import datetime

class OrderTransformer:
    """Transform raw orders into fact table format"""

    @staticmethod
    def transform(orders_df: pd.DataFrame, customers_df: pd.DataFrame,
                  products_df: pd.DataFrame) -> pd.DataFrame:
        """Transform and join data"""

        # Clean orders
        orders = orders_df.copy()
        orders['order_id'] = orders['order_id'].astype(int)
        orders['customer_id'] = orders['customer_id'].astype(int)
        orders['product_id'] = orders['product_id'].astype(int)
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        orders['amount'] = orders['amount'].astype(float)

        # Remove duplicates
        orders = orders.drop_duplicates(subset=['order_id'])
        print(f"After dedup: {len(orders)} orders")

        # Handle nulls
        orders = orders.dropna(subset=['order_id', 'customer_id', 'amount'])

        # Add surrogate keys for dimensions
        customers = customers_df[['customer_id', 'email', 'country']].copy()
        customers['customer_id'] = customers['customer_id'].astype(int)

        products = products_df[['product_id', 'name', 'category']].copy()
        products['product_id'] = products['product_id'].astype(int)

        # Join dimensions
        fact = orders.merge(customers, on='customer_id', how='left')
        fact = fact.merge(products, on='product_id', how='left')

        # Add computed columns
        fact['year'] = fact['order_date'].dt.year
        fact['month'] = fact['order_date'].dt.month
        fact['day'] = fact['order_date'].dt.day

        # Add load timestamp
        fact['loaded_at'] = datetime.now()

        return fact


# Data quality expectations
QUALITY_RULES = {
    'order_id': {
        'not_null': True,
        'unique': True
    },
    'amount': {
        'not_null': True,
        'min': 0,
        'max': 1000000
    },
    'customer_id': {
        'not_null': True
    }
}

def validate_transformed_data(df: pd.DataFrame) -> bool:
    """Validate transformed data meets expectations"""
    errors = []

    # Check nulls
    if df['order_id'].isnull().any():
        errors.append("order_id has nulls")

    # Check uniqueness
    if df['order_id'].duplicated().any():
        errors.append("order_id has duplicates")

    # Check value ranges
    if (df['amount'] < 0).any():
        errors.append("amount has negative values")

    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        return False

    print("All validations passed")
    return True
```

**Database Schema:**

```sql
-- Dimension tables
CREATE TABLE dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT UNIQUE NOT NULL,
    email VARCHAR(255),
    country VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    name VARCHAR(255),
    category VARCHAR(50),
    price DECIMAL(10,2),
    created_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Fact table
CREATE TABLE fact_orders (
    order_key SERIAL PRIMARY KEY,
    order_id INT UNIQUE NOT NULL,
    customer_key INT REFERENCES dim_customers,
    product_key INT REFERENCES dim_products,
    order_date DATE,
    amount DECIMAL(10,2),
    quantity INT,
    year INT,
    month INT,
    day INT,
    loaded_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_fact_customer ON fact_orders(customer_key);
CREATE INDEX idx_fact_product ON fact_orders(product_key);
CREATE INDEX idx_fact_date ON fact_orders(order_date);
```

---

### Week 3: Airflow Orchestration

**Goals:**
- Design DAG (Directed Acyclic Graph)
- Implement task dependencies
- Handle retries and failures
- Monitor execution

**Deliverables:**
- Airflow DAG with all ETL tasks
- Error handling and alerts
- Monitoring dashboard
- Documentation

**Key Code:**

```python
# dags/etl_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

from extractors import OrdersAPIExtractor, CSVExtractor, DatabaseExtractor
from transformations import OrderTransformer, validate_transformed_data

# DAG definition
default_args = {
    'owner': 'data_engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email': ['alerts@company.com'],
    'email_on_failure': True,
}

dag = DAG(
    'ecommerce_etl',
    default_args=default_args,
    description='Daily ETL for e-commerce data',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=days_ago(1),
    catchup=False,
)

# Extract tasks
def extract_orders():
    extractor = OrdersAPIExtractor("https://api.example.com", "{{ var.value.api_key }}")
    return extractor.extract(
        start_date=days_ago(1),
        end_date=days_ago(0)
    )

def extract_customers():
    extractor = CSVExtractor("data-lake")
    return extractor.extract("uploads/customers/")

def extract_products():
    extractor = DatabaseExtractor("postgresql://...")
    return extractor.extract("SELECT * FROM products WHERE updated_at > now() - interval '1 day'")

# Transform task
def transform_and_validate():
    import pandas as pd
    from s3fs import S3FileSystem

    s3 = S3FileSystem()

    # Load extracted data
    orders = pd.read_parquet("s3://data-lake/raw/orders/latest.parquet")
    customers = pd.read_parquet("s3://data-lake/raw/customers/latest.parquet")
    products = pd.read_parquet("s3://data-lake/raw/products/latest.parquet")

    # Transform
    transformer = OrderTransformer()
    fact_orders = transformer.transform(orders, customers, products)

    # Validate
    if not validate_transformed_data(fact_orders):
        raise ValueError("Data quality checks failed")

    # Save transformed
    fact_orders.to_parquet("s3://data-lake/transformed/orders/latest.parquet")
    return len(fact_orders)

# Load task
def load_to_warehouse():
    from sqlalchemy import create_engine
    import pandas as pd

    engine = create_engine("postgresql://...")

    # Load from transformed
    df = pd.read_parquet("s3://data-lake/transformed/orders/latest.parquet")

    # Load to staging
    df.to_sql('staging_orders', engine, if_exists='replace', index=False)
    print(f"Loaded {len(df)} rows to staging")

# Task definitions
extract_orders_task = PythonOperator(
    task_id='extract_orders',
    python_callable=extract_orders,
    dag=dag,
)

extract_customers_task = PythonOperator(
    task_id='extract_customers',
    python_callable=extract_customers,
    dag=dag,
)

extract_products_task = PythonOperator(
    task_id='extract_products',
    python_callable=extract_products,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_and_validate',
    python_callable=transform_and_validate,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_warehouse',
    python_callable=load_to_warehouse,
    dag=dag,
)

validate_task = PostgresOperator(
    task_id='validate_load',
    sql='SELECT COUNT(*) as cnt FROM staging_orders;',
    postgres_conn_id='warehouse',
    dag=dag,
)

swap_task = PostgresOperator(
    task_id='swap_tables',
    sql='''
    BEGIN;
    DROP TABLE IF EXISTS fact_orders_old;
    ALTER TABLE fact_orders RENAME TO fact_orders_old;
    ALTER TABLE staging_orders RENAME TO fact_orders;
    COMMIT;
    ''',
    postgres_conn_id='warehouse',
    dag=dag,
)

# Set dependencies
[extract_orders_task, extract_customers_task, extract_products_task] >> transform_task
transform_task >> load_task >> validate_task >> swap_task
```

---

### Week 4: Monitoring & Optimization

**Goals:**
- Set up monitoring and alerting
- Optimize for performance
- Document operational procedures
- Create runbooks

**Deliverables:**
- Monitoring dashboard
- Alert thresholds
- Performance optimization report
- Operational runbooks

**Monitoring Code:**

```python
# monitoring.py
import logging
from datetime import datetime
from metrics import emit_metric

logger = logging.getLogger(__name__)

class PipelineMonitor:
    """Monitor pipeline health"""

    @staticmethod
    def monitor_extraction(source: str, records: int, duration_seconds: float):
        """Monitor extraction metrics"""
        emit_metric('extraction.records', records, tags=[f'source:{source}'])
        emit_metric('extraction.duration', duration_seconds, tags=[f'source:{source}'])

        # Alert if too slow
        if duration_seconds > 600:  # 10 minutes
            logger.warning(f"{source} extraction took {duration_seconds}s")

        # Alert if no data
        if records == 0:
            logger.error(f"{source} extraction returned 0 records")

    @staticmethod
    def monitor_quality(check_name: str, passed: bool, failed_count: int):
        """Monitor quality checks"""
        emit_metric('quality.passed', 1 if passed else 0, tags=[f'check:{check_name}'])
        if not passed:
            emit_metric('quality.failed_records', failed_count, tags=[f'check:{check_name}'])
            logger.error(f"Quality check {check_name} failed: {failed_count} bad records")

    @staticmethod
    def monitor_load(rows_loaded: int, rows_skipped: int):
        """Monitor load metrics"""
        emit_metric('load.rows_loaded', rows_loaded)
        emit_metric('load.rows_skipped', rows_skipped)

        if rows_skipped > rows_loaded * 0.1:  # More than 10% skipped
            logger.warning(f"High skip rate: {rows_skipped}/{rows_loaded + rows_skipped}")

    @staticmethod
    def monitor_end_to_end(dag_run_id: str, success: bool, duration: float):
        """Monitor overall pipeline health"""
        emit_metric('dag.duration', duration, tags=[f'dag_run:{dag_run_id}'])
        emit_metric('dag.success', 1 if success else 0, tags=[f'dag_run:{dag_run_id}'])

        if duration > 3600:  # 1 hour
            logger.warning(f"DAG took {duration}s, which is longer than SLA")
```

---

## Project Completion Checklist

### Extraction
- [ ] API extractor working
- [ ] CSV loader working
- [ ] Database query executor working
- [ ] Error handling for all sources
- [ ] S3 storage working

### Transformation
- [ ] Data cleaning logic
- [ ] Dimension table logic
- [ ] Fact table logic
- [ ] Deduplication working
- [ ] Data quality checks passing

### Loading
- [ ] Staging table strategy
- [ ] Atomic swap logic
- [ ] Rollback capability
- [ ] Incremental loading (only new data)

### Orchestration
- [ ] Airflow DAG defined
- [ ] Task dependencies correct
- [ ] Retry logic working
- [ ] Error notifications
- [ ] Monitoring in place

### Operations
- [ ] Documentation complete
- [ ] Runbooks written
- [ ] Monitoring dashboard
- [ ] Alert thresholds set
- [ ] Performance optimized

---

## Interview Questions

1. **How do you handle schema changes in the source systems?**
   - Version your schemas
   - Implement gradual migration
   - Maintain backward compatibility
   - Add validation for new columns

2. **What happens if the pipeline fails mid-way?**
   - Transactions for atomic operations
   - Idempotent transformations
   - Staging tables for safety
   - Automatic retries with exponential backoff

3. **How do you ensure data quality?**
   - Great Expectations for automated checks
   - Test data before loading to production
   - Comparison with previous runs
   - Row counts and checksums

4. **How would you scale this to petabyte scale data?**
   - Replace Pandas with Spark
   - Partition data by date
   - Parallel processing
   - Data federation

5. **How do you handle late-arriving data?**
   - Idempotent designs (reprocess same data safely)
   - Late load windows
   - Recalculate aggregates when needed
   - Audit trails for all changes

---

## Resources

- [Database Operations Guide](../database-operations-guide.md) - Schema design and SQL
- [ML Workflow Guide](../ml-workflow-guide.md) - Data preprocessing patterns
- [Cloud & DevOps Guide](../cloud-devops-guide.md) - AWS and Docker

---

## Time Estimate

- **Week 1:** 15-18 hours (Extraction, validation)
- **Week 2:** 15-18 hours (Transformations, schema)
- **Week 3:** 12-15 hours (Airflow, orchestration)
- **Week 4:** 10-12 hours (Monitoring, optimization)

**Total: 52-63 hours**

---

## Next Steps

After completing this project:
1. Add incremental loading (CDC)
2. Implement data lineage tracking
3. Add data catalog
4. Build BI dashboards on top
5. Implement data quality monitoring
6. Add cost optimization (compression, archiving)
7. Scale to Spark for larger datasets

**This is a production-ready pipeline!** Use it as your data engineering portfolio piece.
