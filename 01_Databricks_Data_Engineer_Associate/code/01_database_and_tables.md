# PySpark + Databricks (Unity Catalog) — Minimal Example

#### 1) Select your catalog and schema

```python
# Select catalog and schema (database)
spark.sql("""
USE CATALOG main;
CREATE SCHEMA IF NOT EXISTS demo;
USE demo;
""")
```

#### 2) Create Delta Table

```sql
CREATE TABLE IF NOT EXISTS main.demo.employees (
  emp_id     INT,
  full_name  STRING,
  hired_date DATE,
  salary_eur DECIMAL(10,2)
)
USING DELTA
COMMENT 'Simple demo table';
```

#### 3) Insert values into the table

```sql
INSERT INTO main.demo.employees (emp_id, full_name, hired_date, salary_eur) VALUES
  (1, 'Alice Müller', DATE '2024-06-01', 65000.00),
  (2, 'Bob García',   DATE '2024-09-15', 72000.00),
  (3, 'Carmen Rossi', DATE '2025-01-10', 68000.00);
```
#### 4) Create an external table at a specific location

> Assumes you have permissions and the path is accessible to your workspace (e.g., registered as an External Location in Unity Catalog).

```sql
-- Option A: Create external table with explicit schema
CREATE EXTERNAL TABLE main.demo.employees_ext (
  emp_id INT,
  full_name STRING,
  hired_date DATE,
  salary_eur DECIMAL(10,2)
)
USING DELTA
LOCATION 'abfss://container@account.dfs.core.windows.net/demo/employees_ext/';
```