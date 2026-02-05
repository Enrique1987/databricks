# Databricks Certified Data Engineer Associate — Study Notes

## General Table of Contents

1. [Databricks Intelligence Platform](#1-databricks-intelligence-platform)  
   * [1.1 Delta Lake, Delta Tables, Advanced Features](#11-delta-lake-delta-tables-advanced-features)  
   * [1.2 Databases and Tables on Databricks (Hands On)](#12-databases-and-tables-on-databricks-hands-on)  
   * [1.3 CTAS, Clone, Views](#13-ctas-clone-views)  
   * [1.5 Relational Entities](#15-relational-entities)  
   * [1.8 Views](#18-views)  

2. [Data Processing & Transformations](#2-data-processing--transformations)  
   * [2.1 Querying Files (ad-hoc over storage)](#21-querying-files-ad-hoc-over-storage)  
   * [2.3 Writing to Tables (Hands-On)](#23-writing-to-tables-hands-on)  
   * [2.5 Higher Order Functions and SQL UDFs (Hands On)](#25-higher-order-functions-and-sql-udfs-hands-on)  

3. [Incremental Data Processing](#3-incremental-data-processing)  
   * [3.0 Bronze Ingestion](#30-bronze-ingestion)  
   * [3.1 Structured Streaming](#31-structured-streaming)  

4. [Production Pipelines](#4-production-pipelines)  
   * [4.2 Delta Live Tables](#42-delta-live-tables)  
   * [4.3 Change Data Capture](#43-change-data-capture)  
   * [4.4 Processing CDC Feed with DLT](#44-processing-cdc-feed-with-dlt)  
   * [4.5 Databricks Asset Bundles](#45-databricks-asset-bundles)  

5. [Data Governance & Security](#5-data-governance--security)  
   * [5.1 Databricks SQL](#51-databricks-sql)  
   * [5.2 Data Objects Privileges & Managing Permissions](#52-data-objects-privileges--managing-permissions)  
   * [5.3 Managing Permissions (Hands On)](#53-managing-permissions-hands-on)  
   * [5.4 Unity Catalog — PDF Summary (Study Notes)](#54-unity-catalog--pdf-summary-study-notes)  
   * [5.5 Delta Sharing — Quick study notes](#55-delta-sharing--quick-study-notes)  
   * [5.6 Lakehouse Federation — Quick study notes](#56-lakehouse-federation--quick-study-notes)  
   * [5.7 Cluster Best Practices — Quick study notes](#57-cluster-best-practices--quick-study-notes)  

---

## 1. Databricks Intelligence Platform

**RDBMS**  
Database → Schema → Table

**Databricks (Unity Catalog)**  
Catalog → Schema → Table

**Metastore**: Service that manages all catalogs.  
**`hive_metastore`** Is often the default catalog in older workspaces and is commonly used for quick tests.

---

### 1.1 Delta Lake, Delta Tables, Advanced Features

* **Transaction Log:** ensures ACID properties; you will not read “dirty” (uncommitted) data.

* **Advanced features (Delta):**

| Feature                  | Use case                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| `VACUUM`                 | Removes old/unreferenced files (after retention). Reduces storage bloat.                      |
| `Time Travel`            | Query or restore older versions of a table (`VERSION AS OF`, `TIMESTAMP AS OF`).             |
| `OPTIMIZE` (compaction)  | Merges small files into larger files to improve read performance.                             |
| `Change Data Feed (CDF)` | Reads row-level changes (inserts/updates/deletes) between versions (when enabled).           |
| `Constraints`              | `NOT NULL`, `CHECK`, generated columns enforcement on write (Delta).                          |

* **Optimization** helps leverage data-skipping algorithms.

| Technique                                   | What it is                                                                                         | When to use (practical guidance)                                                                                                                         | Good for                                                                               | Avoid / notes                                                                                                                                          |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Liquid clustering**                       | Adaptive data layout that continuously clusters files by chosen keys without manual rewrites.      | Best for most new Delta tables: pick 1–3 selective keys you frequently filter/join on (e.g., `date`, `customer_id`). Works with batch + streaming writes. | Large (& growing) tables, mixed read/write, evolving query patterns, redefinable keys. | Don’t combine with Z-ORDER on the same table. Prefer it over “manual” performance partitioning for most use cases.                                     |
| **Partitioning (classic Delta partitions)** | Physical separation by column (Hive-style folders like `dt=2025-10-17`).                            | Use sparingly for coarse operations: retention by date, extremely large append-only logs, governance/SLAs, or when you must target deletes by partition. | Fast pruning for time-range filters; easy deletes by partition (retention).            | Over-partitioning hurts (tiny files, skew). Many tables don’t need partitioning if Liquid clustering is used and access patterns are not extreme.       |
| **Z-ORDER (legacy)**                        | Reorders files to colocate values of selected columns to improve data skipping.                    | Use only on legacy tables (non-Liquid) where access patterns are stable and you need a performance boost without changing layout strategy.               | Speeding up filters/joins on a few columns when stuck on legacy layout.                | Incompatible with Liquid clustering. Consider migrating to Liquid clustering instead of relying on repeated Z-ORDER long term.                          |

**One-liner:** Liquid clustering is Databricks’ modern layout optimization that reduces the need for heavy partitioning and Z-ORDER, while adapting over time.

---

### 1.5 Relational Entities

| Concept                 | **RDBMS (e.g., SQL Server / PostgreSQL)**                                     | **Databricks (Unity Catalog)**                                                                                  | Comment                                                                                                        |
| ----------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Top level**           | **Database** → logical container for schemas and objects                      | **Catalog** → top-level container for schemas and objects                                                       | Databricks “Catalog” is closest to a classic database boundary plus governance.                                |
| **Middle level**        | **Schema** → groups tables, views, functions within a database                | **Schema** → groups objects within a catalog (in SQL, “database” is often used as a synonym for schema)         | Same concept.                                                                                                  |
| **Bottom level**        | **Table** → data structure containing rows                                    | **Table** → Delta table managed by Unity Catalog (or external table pointing to a location)                     | Conceptually identical.                                                                                        |
| **Full path reference** | `database.schema.table`                                                       | `catalog.schema.table`                                                                                          | Unity Catalog adds the catalog layer.                                                                          |
| **Extra notes**         | Database is commonly a security + storage boundary in traditional RDBMS        | Catalog acts as a governance boundary (permissions, lineage, discovery, sharing) across workspaces and compute  | More “platform governance” emphasis.                                                                           |

---

### 1.2 Databases and Tables on Databricks (Hands On)

This section is a placeholder pointing to your separate notes file:

`code/01_database_and_tables.md`

---

### 1.3 CTAS, Clone, Views

#### CTAS

`CREATE TABLE … AS SELECT …`

##### Does **CTAS** copy constraints, comments, properties, or identity columns?

**No.** `CREATE TABLE … AS SELECT …` (CTAS) creates a **new** table from the query’s result.

* It infers the **schema** from the SELECT output.
* It **does not** carry over table constraints, comments, properties, identity columns, or tags from the source.
* If you need them, you must **define them again** after CTAS.

**Example: re-adding metadata after CTAS**

```sql
CREATE TABLE main.demo.emp_ctas AS
SELECT * FROM main.demo.employees;

-- Add back a comment and a NOT NULL
COMMENT ON TABLE main.demo.emp_ctas IS 'Copy created via CTAS';
ALTER TABLE main.demo.emp_ctas ALTER COLUMN full_name SET NOT NULL;

-- Add a CHECK constraint
ALTER TABLE main.demo.emp_ctas
ADD CONSTRAINT chk_salary_nonneg CHECK (salary_eur IS NULL OR salary_eur >= 0);
```

---

#### CLONE

##### Do **CLONEs** copy constraints, comments, and properties?

**Yes (in general).** `DEEP CLONE` and `SHALLOW CLONE` copy the **table’s metadata** (schema, comments, properties, constraints) and create a new Delta table object.

* **Deep clone** additionally copies **data files** to the target’s storage.
* **Shallow clone** references the source’s existing files (snapshot at clone time).

```sql
-- Deep clone (metadata + data files)
CREATE TABLE main.demo.employees_deep
DEEP CLONE main.demo.employees;

-- Shallow clone (metadata + file references)
CREATE TABLE main.demo.employees_shallow
SHALLOW CLONE main.demo.employees;
```

> Subsequent changes to the **source** do **not** propagate to the clone.

---

##### Can I clone **across catalogs** or **workspaces**?

* **Same metastore (Unity Catalog):** you can clone across **schemas/catalogs** (permissions required).
* **Different metastores / separate environments:** `CLONE` itself doesn’t cross metastores. Typical pattern:
  1. Deep clone or copy to an external location (cloud path).
  2. Register the location as a table in the other metastore.

```sql
CREATE TABLE main.demo.emp_deep_ext
DEEP CLONE main.prod.employees
LOCATION 'abfss://container@account.dfs.core.windows.net/demo/emp_deep_ext/';
```

---

##### What about **VACUUM** and shallow clones?

* **Shallow clone** depends on **source files** that existed at clone time.
* If you **VACUUM** the **source** and remove files the shallow clone still references, the clone can **break**.
* Safe practice: keep vacuum retention conservative unless you’re sure no shallow clones depend on old files.

```sql
VACUUM main.prod.employees RETAIN 168 HOURS;  -- example retention
```

---

##### Can I clone a **specific point in time**?

**Yes.** Clone by **version** or **timestamp**.

```sql
CREATE TABLE main.demo.sales_deep_v42
DEEP CLONE main.prod.sales VERSION AS OF 42;

CREATE TABLE main.demo.sales_shallow_t
SHALLOW CLONE main.prod.sales TIMESTAMP AS OF '2025-09-30T12:00:00Z';
```

---

##### Is a **shallow clone** like a **view**?

**No.**

* A **view** re-runs a query against the **current** source each time you read it.
* A **shallow clone** is an independent Delta table snapshot (its own log), referencing the source’s data files from the clone time.

---

##### After cloning, **where do new writes go**?

Both deep and shallow clones are **independent tables**. New writes create **new files** for the clone’s storage.

```sql
INSERT INTO main.demo.employees_shallow VALUES (999, 'Test User', DATE '2025-10-01', 1.00);
```

---

##### Does CTAS preserve **physical layout** (clustering/partitioning)?

**No.** CTAS rewrites the output files; re-apply optimization afterwards if needed.

```sql
OPTIMIZE main.demo.emp_ctas;
```

---

##### Do **privileges** copy with clones?

A clone is a **new object**; grants do **not automatically** carry over. Re-grant on the target.

```sql
GRANT SELECT ON TABLE main.demo.employees_deep TO `data-analyst-role`;
```

---

##### Quick reference: CTAS vs Deep/Shallow Clone

| Feature                 | CTAS                             | Deep Clone                                | Shallow Clone                                    |
| ----------------------- | -------------------------------- | ----------------------------------------- | ------------------------------------------------ |
| Copies metadata         | Basic (schema only)              | **Yes** (schema, constraints, properties) | **Yes**                                          |
| Copies data files       | **Rewrites new files**           | **Yes** (physical copy)                   | **No** (references source files)                 |
| Storage independence    | Yes                              | **Yes**                                   | **Partial** (depends on source’s retained files) |
| Keeps in sync w/ source | No                               | No                                        | No                                               |
| Speed / cost            | Compute-heavy + new storage       | Fast-ish + extra storage                  | Fastest + minimal storage, but fragile w/ VACUUM |

---

### 1.8 Views

Databricks supports several kinds of **views** you can use to abstract queries, control access, and speed up reads.

#### Quick overview

| View type                                       | Scope & lifetime                                            | Stored data? | Where it lives                              | Typical use                                                     |
| ----------------------------------------------- | ----------------------------------------------------------- | ------------ | ------------------------------------------- | --------------------------------------------------------------- |
| **Temporary view**                              | Session-only (ends when your session ends)                  | No           | Not in metastore                             | Ad-hoc exploration; chaining DataFrame → SQL                    |
| **Global temporary view**                       | Cluster-wide; lasts while the cluster runs                  | No           | Special schema **`global_temp`**             | Share a temp view across notebooks on the same cluster          |
| **Persistent view** (Unity Catalog/metastore)   | Permanent until dropped                                     | No           | `catalog.schema`                             | Semantic layer, permissions, sharing                            |
| **Materialized view**                           | Permanent; system maintains precomputed results             | **Yes**      | `catalog.schema` (often on SQL Warehouses)   | Dashboards, repeated analytics, aggregates                      |

---

#### 1) Temporary view

```sql
CREATE OR REPLACE TEMP VIEW v_recent_hires AS
SELECT emp_id, full_name, hired_date
FROM main.demo.employees
WHERE hired_date >= DATE '2025-01-01';
```

---

#### 2) Global temporary view

```sql
CREATE OR REPLACE GLOBAL TEMP VIEW gv_recent_hires AS
SELECT emp_id, full_name, hired_date
FROM main.demo.employees
WHERE hired_date >= DATE '2025-01-01';
```

Query:

```sql
SELECT * FROM global_temp.gv_recent_hires;
```

---

#### 3) Persistent view (Unity Catalog)

```sql
CREATE OR REPLACE VIEW main.analytics.v_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

Grant permissions:

```sql
GRANT SELECT ON VIEW main.analytics.v_high_paid TO `analyst_role`;
```

---

#### 4) Materialized view (Databricks SQL)

```sql
CREATE OR REPLACE MATERIALIZED VIEW main.analytics.mv_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

---

#### 5) “Dynamic views” for row-level security (pattern)

```sql
CREATE OR REPLACE VIEW main.secure.v_sales AS
SELECT *
FROM main.prod.sales
WHERE region IN (
  SELECT region FROM main.secure.user_region_map WHERE user = current_user()
);
```

---

#### Persistent view vs Materialized view

* **Persistent view:** stores no data; every query re-runs the underlying SQL (fresh but can be expensive).
* **Materialized view:** stores results; platform maintains it (fast reads, eventual refresh).

---

## 2. Data Processing & Transformations

### Can you create a table inside Databricks that is not a Delta table?

**Yes, but with limits.**

* **Managed tables (Unity Catalog):** effectively Delta.
* **External tables:** you can create non-Delta tables over files (Parquet/CSV/JSON/ORC/Avro) by pointing at a path.

```sql
-- External PARQUET table (non-Delta)
CREATE EXTERNAL TABLE main.analytics.events_parquet (
  id BIGINT,
  name STRING,
  ts TIMESTAMP
)
USING PARQUET
LOCATION 'abfss://data@acct.dfs.core.windows.net/raw/events/';

-- External JSON table
CREATE EXTERNAL TABLE main.analytics.events_json
USING JSON
LOCATION 'abfss://data@acct.dfs.core.windows.net/raw/events_json/';
```

CTAS in those formats:

```sql
CREATE EXTERNAL TABLE main.analytics.some_parquet
USING PARQUET
LOCATION 'abfss://data@acct.dfs.core.windows.net/out/some_parquet/'
AS SELECT * FROM main.analytics.source;
```

| Capability                | **Delta table** (`USING DELTA`)                                            | **External data-source table** (`USING CSV/JSON/PARQUET …`)               |
| ------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Storage & metadata        | Delta files + `_delta_log` transaction log                                  | Plain files; no transaction log                                           |
| ACID transactions         | **Yes**                                                                     | **No**                                                                    |
| DML (UPDATE/DELETE/MERGE) | **Supported** (transactional)                                               | Generally not supported                                                   |
| Time travel               | **Yes**                                                                     | No                                                                        |
| Change Data Feed          | **Yes** (when enabled)                                                      | No                                                                        |
| Constraints               | Supported/enforced                                                           | No enforcement                                                            |
| Schema enforcement        | Strict on write                                                              | Mostly schema-on-read                                                     |
| OPTIMIZE / VACUUM         | Supported                                                                    | Not available                                                             |
| Concurrency safety        | High                                                                         | Risky with concurrent writers                                             |
| Typical use               | Silver/Gold tables, reliable pipelines                                      | Ad-hoc reads over raw files                                               |

---

### 2.1 Querying Files (ad-hoc over storage)

**Databricks SQL — read files directly (no table)**

```sql
-- JSON
SELECT * 
FROM json.`abfss://data@acct.dfs.core.windows.net/raw/events/2025/10/31/*.json`;

-- Parquet
SELECT id, name, ts
FROM parquet.`abfss://data@acct.dfs.core.windows.net/raw/events/*.parquet`;

-- Delta by path
SELECT *
FROM delta.`abfss://data@acct.dfs.core.windows.net/curated/events_delta/`;
```

**PySpark — explicit schema + options (recommended for CSV/JSON)**

```python
from pyspark.sql.types import StructType, StructField, LongType, StringType, TimestampType

schema = StructType([
    StructField("id", LongType()),
    StructField("name", StringType()),
    StructField("ts", TimestampType()),
])

df = (spark.read
      .schema(schema)
      .option("multiLine", True)
      .json("abfss://data@acct.dfs.core.windows.net/raw/events/*.json"))

df.select("id","name","ts").where("ts >= '2025-10-01'").show()
```

---

### 2.3 Writing to Tables (Hands-On)

#### A) SQL CTAS → managed Delta table

```sql
CREATE TABLE main.analytics.events_delta
USING DELTA
AS
SELECT id, name, ts
FROM parquet.`abfss://data@acct.dfs.core.windows.net/raw/events/*.parquet`;
```

#### B) SQL INSERT INTO an existing Delta table

```sql
INSERT INTO main.analytics.events_delta (id, name, ts)
SELECT id, name, ts
FROM json.`abfss://data@acct.dfs.core.windows.net/raw/events/2025/10/*.json`;
```

#### C) PySpark DataFrameWriter → save as Delta table

```python
from pyspark.sql.functions import to_date

df2 = df.withColumn("event_date", to_date("ts"))

(df2.write
    .format("delta")
    .mode("append")                  # overwrite | append | errorifexists
    .option("mergeSchema", "true")   # allow new columns on write
    .partitionBy("event_date")       # optional but useful for pruning
    .saveAsTable("main.analytics.events_delta"))
```

#### D) Create an external Delta table (control the path)

```sql
CREATE TABLE main.analytics.events_ext
USING DELTA
LOCATION 'abfss://data@acct.dfs.core.windows.net/curated/events_delta/';

INSERT INTO main.analytics.events_ext
SELECT * FROM main.analytics.events_delta;
```

---

#### `from_json` — parse JSON strings into structs/arrays

```sql
WITH input AS (
  SELECT * FROM VALUES
    (1, '{"k":1,"tags":["a","b","a"]}'),
    (2, '{"k":2,"tags":["b","c"]}')
  AS input(id, payload)
)
SELECT
  id,
  from_json(payload, 'STRUCT<k INT, tags ARRAY<STRING>>') AS obj,
  from_json(payload, 'STRUCT<k INT, tags ARRAY<STRING>>').k    AS k,
  from_json(payload, 'STRUCT<k INT, tags ARRAY<STRING>>').tags AS tags
FROM input;
```

---

#### `collect_set` — aggregate unique values per group

```sql
WITH events AS (
  SELECT * FROM VALUES
    (1,'a'),(1,'b'),(1,'a'),(2,'b')
  AS events(user_id, tag)
)
SELECT user_id, collect_set(tag) AS unique_tags
FROM events
GROUP BY user_id;
```

---

#### `array_distinct` — remove duplicates inside a single array

```sql
SELECT id, array_distinct(tags) AS tags_dedup
FROM (SELECT 1 AS id, array('a','b','a') AS tags);
```

---

#### `flatten` — collapse array<array<T>> → array<T>

```sql
WITH per_event AS (
  SELECT * FROM VALUES
    (1, array('a','b')),
    (1, array('b','c'))
  AS per_event(user_id, tags)
)
SELECT
  user_id,
  array_distinct( flatten( collect_list(tags) ) ) AS unique_tags
FROM per_event
GROUP BY user_id;
```

---

#### `explode` — turn array elements into multiple rows

```sql
WITH t AS (SELECT 10 AS id, array('a','b','a') AS tags)
SELECT id, explode(tags) AS tag
FROM t;
```

> Variants: `posexplode` (keeps index), `explode_outer` (keeps rows when array is null).

---

#### Summary Table

| Function         | Purpose                                 | Common pattern                                     | Gotchas                                                       |
| ---------------- | --------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------- |
| `from_json`      | Parse JSON string to typed struct/array | parse then select fields                           | Must provide schema (string literal) or use `schema_of_json`. |
| `collect_set`    | Aggregate **unique** values per group   | `GROUP BY` + `collect_set(col)`                    | Order not guaranteed; arrays can grow large.                  |
| `array_distinct` | Remove duplicates inside array          | `array_distinct(arr)`                              | Only de-dupes; doesn’t sort.                                  |
| `flatten`        | Collapse nested arrays                  | `array_distinct(flatten(collect_list(arr)))`       | Works on `array<array<T>>` only.                              |
| `explode`        | Array → multiple rows                   | `SELECT explode(arr) AS x`                         | Duplicates rows; consider `distinct` afterwards.              |

---

### 2.5 Higher Order Functions and SQL UDFs (Hands On)

#### `filter` — keep only elements that match a predicate

```sql
WITH t AS (
  SELECT * FROM VALUES
    (1, array(1,2,3,4)),
    (2, array(10,11,NULL,12))
  AS t(id, nums)
)
SELECT
  id,
  filter(nums, x -> x IS NOT NULL AND x % 2 = 0) AS even_nums
FROM t;
```

---

#### `size` — count elements in arrays / entries in maps

```sql
WITH t AS (
  SELECT * FROM VALUES
    (1, array('a','b','a')),
    (2, array())
  AS t(id, tags)
)
SELECT id, size(tags) AS tag_count FROM t;
```

---

#### `transform` — map each element to a new value

```sql
WITH t AS (SELECT 1 AS id, array(' A ','b ',' C') AS tags)
SELECT
  id,
  transform(tags, x -> lower(trim(x))) AS tags_norm
FROM t;
```

---

#### SQL UDF — reusable logic as a function (pure SQL)

```sql
CREATE OR REPLACE FUNCTION main.analytics.normalize_tag(s STRING)
RETURNS STRING
RETURN lower(trim(s));
```

Use it:

```sql
WITH t AS (SELECT 1 AS id, array('  Foo','BAR  ','  bar') AS tags)
SELECT
  id,
  transform(tags, x -> normalize_tag(x))                 AS tags_norm,
  array_distinct(transform(tags, x -> normalize_tag(x))) AS tags_norm_unique
FROM t;
```

---

#### Summary Table

| Feature                     | Purpose                   | Common pattern                             | Gotchas                                           |
| --------------------------- | ------------------------- | ------------------------------------------ | ------------------------------------------------ |
| `filter(arr, x -> pred)`    | Keep only wanted elements | `filter(arr, x -> x IS NOT NULL AND cond)` | Use `IS NOT NULL` inside predicate to drop nulls |
| `size(arr/map)`             | Count items               | `size(arr)`                                | For maps: counts key/value pairs                 |
| `transform(arr, x -> expr)` | Element-wise transform    | `transform(arr, x -> lower(trim(x)))`      | Combine with `array_distinct` to dedupe          |
| SQL UDF                     | Reusable SQL expression   | `CREATE FUNCTION … RETURN <expr>`          | Define in UC schema; mind permissions            |

---

## 3. Incremental Data Processing

**Data stream** = any data source that grows over time:
* new files landing in cloud storage
* updates captured in a CDC feed
* events from pub/sub (Kafka/Event Hubs)

**Processing a data stream**
1. Reprocess the entire source each time (batch rewrite).
2. Process only new data added since the last update (incremental): **Structured Streaming**.

---

### 3.0 Bronze Ingestion

**Goal of Bronze:** land raw, append-only data in Delta with minimal transforms (schema enforcement, optional dedup).

#### Quick decision

| Source                    | Batch (scheduled / backfills)                 | Streaming (continuous / low-latency)                       |
| ------------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| Files in cloud storage    | `COPY INTO` or batch `df.write`               | Auto Loader (`readStream cloudFiles` → `writeStream`)      |
| Database tables           | JDBC extract → Delta                           | CDC landed to Delta → stream + MERGE / CDF                 |
| Event streams             | —                                             | Kafka / Event Hubs → Delta                                 |
| Prefer managed pipeline   | DLT batch                                      | DLT streaming                                               |

#### Batch loading: `COPY INTO`

```sql
COPY INTO main.bronze.events_raw
FROM 'dbfs:/mnt/landing/events/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('inferSchema'='true')
COPY_OPTIONS ('mergeSchema'='true');  -- loads only new files
```

#### JDBC → Delta (batch)

```python
df = (spark.read.format("jdbc")
  .option("url", "jdbc:postgresql://host/db")
  .option("dbtable", "public.orders")
  .option("user", "<user>").option("password", "<pwd>")
  .load())

(df.write.format("delta").mode("append")
  .saveAsTable("main.bronze.orders_raw"))
```

#### Streaming loading: Auto Loader

```python
raw = (spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("dbfs:/mnt/bronze/raw/events/"))

(raw.writeStream.format("delta")
  .option("checkpointLocation","dbfs:/mnt/_chk/bronze/events")
  .toTable("main.bronze.events_raw"))
```

#### Delta CDF as a stream (row-level changes)

```python
changes = (spark.readStream.format("delta")
  .option("readChangeFeed","true")
  .option("startingVersion","0")
  .table("main.staging.customers_cdc"))

(changes.writeStream.format("delta")
  .option("checkpointLocation","dbfs:/mnt/_chk/bronze/customers_cdf")
  .toTable("main.bronze.customers_cdf"))
```

#### DLT ingestion (example)

```sql
CREATE STREAMING LIVE TABLE bronze_events
AS SELECT * FROM cloud_files("dbfs:/mnt/bronze/raw/events","json",
  map("cloudFiles.inferColumnTypes","true"));
```

---

### 3.1 Structured Streaming

#### `readStream` & `writeStream`

`readStream` creates a streaming DataFrame; `writeStream` defines the sink + checkpoint.

```python
src = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("dbfs:/mnt/bronze/raw/events/"))
```

Write to Delta:

```python
(src.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation","dbfs:/mnt/_chk/silver/events_raw")
  .toTable("main.silver.events_raw"))
```

#### Where does state live?

* Sink Delta table grows over time
* Checkpoint stores progress and state

```
dbfs:/mnt/_chk/<pipeline>/...      ← offsets/state
dbfs:/mnt/_schemas/<pipeline>/...  ← Auto Loader schema + discovery log
```

#### Upsert pattern (foreachBatch + MERGE)

```python
src = spark.readStream.table("main.bronze.events_raw")

def upsert_to_b(microbatch_df, _):
    microbatch_df.createOrReplaceTempView("a")
    microbatch_df.sparkSession.sql("""
      MERGE INTO main.silver.events AS b
      USING (SELECT * FROM a) s
      ON b.id = s.id
      WHEN MATCHED THEN UPDATE SET *
      WHEN NOT MATCHED THEN INSERT *;
    """)

(src.writeStream
  .option("checkpointLocation","dbfs:/mnt/_chk/silver/events_merge")
  .foreachBatch(upsert_to_b)
  .start())
```

#### Triggers

| Trigger                      | What it does                                       | When to use                 |
| ---------------------------- | -------------------------------------------------- | --------------------------- |
| default                      | micro-batches back-to-back                         | lowest latency              |
| `processingTime='2 minutes'` | run a batch every 2 minutes                        | pacing / cost control       |
| `availableNow=True`          | process all backlog then stop                      | backfills / catch-ups       |

#### Auto Loader options (80/20)

| Option                              | Why you care                                             |
| ----------------------------------- | -------------------------------------------------------- |
| `cloudFiles.format`                 | file type (json/csv/parquet/…)                           |
| `cloudFiles.schemaLocation`         | persisted schema + discovery log                         |
| `cloudFiles.inferColumnTypes`       | infer non-string types (CSV/JSON)                        |
| `cloudFiles.schemaEvolutionMode`    | handle new columns (`rescue` / add columns)              |
| `cloudFiles.maxFilesPerTrigger`     | pace ingestion                                            |
| `cloudFiles.useNotifications`       | scalable low-latency discovery (no heavy directory list)  |
| `checkpointLocation` (writeStream)  | exactly-once progress/state                              |

---

## 4. Production Pipelines

### 4.2 Delta Live Tables

DLT is a managed pipeline framework where you define tables declaratively and Databricks handles dependencies, checkpoints, retries, expectations, lineage, and more.

```sql
CREATE STREAMING LIVE TABLE bronze_events
AS SELECT * FROM cloud_files('dbfs:/mnt/landing/events', 'json',
  map('cloudFiles.inferColumnTypes','true'));

CREATE LIVE TABLE silver_events
AS SELECT * FROM LIVE.bronze_events WHERE is_valid = true;

APPLY CHANGES INTO LIVE.dim_customers
FROM STREAM(LIVE.customers_cdc)
  KEYS (customer_id)
  SEQUENCE BY event_ts
  STORED AS SCD TYPE 2;
```

**`CREATE STREAMING LIVE TABLE` vs `CREATE LIVE TABLE`**

| Aspect          | Streaming live table                        | Live table                                      |
| --------------- | ------------------------------------------- | ---------------------------------------------- |
| Model           | streaming incremental                         | batch/materialized per pipeline update         |
| Typical layer   | Bronze                                        | Silver/Gold                                    |
| Reads           | `LIVE.*` or `STREAM(LIVE.*)`                 | usually `LIVE.*`; use `STREAM()` when needed   |

---

### 4.3 Change Data Capture

CDC captures row-level changes from a source system and applies them to a target table.

Common CDC patterns:
* append-only change log with operation type (I/U/D)
* “latest record wins” (sequence column such as timestamp or version)
* delete handling (hard or soft delete)

#### Delta Change Data Feed (CDF)

Enable:

```sql
ALTER TABLE main.prod.customers
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

Read (batch):

```sql
SELECT *
FROM table_changes('main.prod.customers', 10, 20);
```

Read (streaming):

```python
cdf = (spark.readStream
  .option("readChangeFeed","true")
  .table("main.prod.customers"))

(cdf.writeStream
  .option("checkpointLocation","dbfs:/mnt/_chk/cdf/customers")
  .toTable("main.bronze.customers_cdf"))
```

---

### 4.4 Processing CDC Feed with DLT

DLT supports CDC application with `APPLY CHANGES INTO`.

#### SCD Type 1

```sql
APPLY CHANGES INTO LIVE.dim_customer
FROM STREAM(LIVE.customer_cdc)
  KEYS (customer_id)
  SEQUENCE BY event_ts
  STORED AS SCD TYPE 1;
```

#### SCD Type 2

```sql
APPLY CHANGES INTO LIVE.dim_customer
FROM STREAM(LIVE.customer_cdc)
  KEYS (customer_id)
  SEQUENCE BY event_ts
  STORED AS SCD TYPE 2;
```

#### Delete handling (pattern)

```sql
APPLY CHANGES INTO LIVE.dim_customer
FROM STREAM(LIVE.customer_cdc)
  KEYS (customer_id)
  SEQUENCE BY event_ts
  APPLY AS DELETE WHEN op = 'D'
  STORED AS SCD TYPE 1;
```

Mental model:
* `KEYS` = match key(s)
* `SEQUENCE BY` = ordering column so latest change wins
* `SCD TYPE 1` = overwrite, `SCD TYPE 2` = history

---

### 4.5 Databricks Asset Bundles

Asset Bundles let you package and deploy Databricks assets (jobs, pipelines, notebooks, permissions) as code.

Typical structure:

```
my_project/
  databricks.yml
  src/
    notebooks/
  resources/
    jobs.yml
    pipelines.yml
```

Minimal conceptual `databricks.yml`:

```yaml
bundle:
  name: my_project

targets:
  dev:
    workspace:
      host: https://<dev-workspace>
  prod:
    workspace:
      host: https://<prod-workspace>

resources:
  jobs:
    etl_job:
      name: "ETL Job"
      tasks:
        - task_key: run_notebook
          notebook_task:
            notebook_path: ./src/notebooks/etl
```

---

## 5. Data Governance & Security

### 5.1 Databricks SQL

Databricks SQL is the SQL-first experience on Databricks using SQL Warehouses for BI/query workloads, plus UI for queries, dashboards, and alerts.

Key ideas:
* SQL Warehouses are optimized for SQL/BI.
* UC governance applies (catalog/schema/table/view permissions).

---

### 5.2 Data Objects Privileges & Managing Permissions

#### Main securable objects (Unity Catalog)

| Object              | Examples                               |
| ------------------- | -------------------------------------- |
| Catalog             | `main`                                 |
| Schema              | `main.analytics`                       |
| Table / View        | `main.analytics.sales`                 |
| Function            | `main.analytics.normalize_tag`         |
| External location   | cloud storage paths (S3/ADLS/GCS)      |
| Storage credential  | credential to access storage           |
| Volume              | managed files in UC                    |

#### Common privileges (high level)

| Privilege                     | Applies to                  | Meaning (practical)                                      |
| ---------------------------- | --------------------------- | -------------------------------------------------------- |
| `USAGE`                      | catalog/schema              | ability to reference objects within                      |
| `SELECT`                     | table/view                  | read data                                                |
| `MODIFY` / `INSERT`          | table                       | write data (varies by config)                            |
| `CREATE`                     | schema                      | create objects inside schema                             |
| `OWN`                        | any                         | full control, can grant/revoke others                    |
| `READ FILES` / `WRITE FILES` | external location           | access underlying cloud storage via UC                   |

Exam idea: You often need **USAGE on catalog + schema** plus object-level privileges (e.g., SELECT).

---

### 5.3 Managing Permissions (Hands On)

Grant examples:

```sql
GRANT USAGE ON CATALOG main TO `analyst_role`;
GRANT USAGE ON SCHEMA main.analytics TO `analyst_role`;

GRANT SELECT ON TABLE main.analytics.sales TO `analyst_role`;
GRANT SELECT ON VIEW  main.analytics.v_high_paid TO `analyst_role`;
```

Revoke:

```sql
REVOKE SELECT ON TABLE main.analytics.sales FROM `analyst_role`;
```

Ownership transfer (conceptual):

```sql
ALTER TABLE main.analytics.sales OWNER TO `data-admin-role`;
```

---

### 5.4 Unity Catalog — PDF Summary (Study Notes)

Unity Catalog provides:
* centralized permissions
* lineage
* discovery
* cross-workspace governance

Mental model:
* UC secures both **objects** (tables/views/functions) and **storage access** (external locations/credentials).

---

### 5.5 Delta Sharing — Quick study notes

Delta Sharing is an open protocol to securely share data across organizations and platforms without copying data.

Key points:
* share tables/views
* provider controls what is shared and to whom

---

### 5.6 Lakehouse Federation — Quick study notes

Lakehouse Federation enables querying external data sources from Databricks (federated query), useful for transitional architectures and avoiding unnecessary copies for some workloads.

---

### 5.7 Cluster Best Practices — Quick study notes

Compute:
* All-purpose clusters: development/interactive.
* Job clusters: production (ephemeral, isolated, reproducible).

Performance:
* Prefer Delta over raw files for repeated queries.
* Avoid small files; use compaction when needed.
* Watch skew; pick join strategies appropriately.

Cost:
* Autoscaling where helpful.
* Auto-terminate idle clusters.
* Use SQL Warehouses for BI/SQL workloads.

Security:
* Use Unity Catalog with least privilege.
* Avoid embedding credentials; use UC storage credentials/external locations.

---

_End of document._
