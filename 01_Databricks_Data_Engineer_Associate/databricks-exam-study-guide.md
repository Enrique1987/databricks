Here’s a cleaned-up version of your notes with:

* **Index updated** so links match the actual headings.
* **Heading levels normalized** to:

  * `###` → chapter
  * `####` → subchapter
  * `#####` → sub-subchapter

I’ve also removed the `::contentReference[...]` leftovers so the Markdown is clean.

---

# Databricks Certified Data Engineer Associate

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
   * [5.2 Data Objects Privileges and Managing Permissions](#52-data-objects-privileges-and-managing-permissions)
   * [5.3 Unity Catalog — PDF Summary (Study Notes)](#53-unity-catalog--pdf-summary-study-notes)
   * [5.4 Delta Sharing — Quick study notes](#54-delta-sharing--quick-study-notes)
   * [5.5 Lakehouse Federation — Quick study notes](#55-lakehouse-federation--quick-study-notes)
   * [5.6 Cluster Best Practices — Quick study notes](#56-cluster-best-practices--quick-study-notes)

---

### 1. Databricks Intelligence Platform

**RDBMS**
Database → Schema → Table

**Databricks**
Catalog → Schema → Table

* **Metastore**: service that manages all catalogs.
* **`hive_metastore`** is the **default catalog**; often used for testing.

#### 1.1 Delta Lake, Delta Tables, Advanced Features

* **Transaction Log:** Ensures ACID properties, you will never read dirty data.

* **Advanced Features:**

| Advanced Feature         | Use Case                                                                                            |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| `VACUUM`                 | Removes old and unused files, helping to reduce latency and free up space.                          |
| `Time Travel`            | Restore a previous state of a table, enabling recovery to a desired point in time.                  |
| `Compacting Small Files` | Improves performance by merging many small files into larger ones, especially with streaming loads. |

* **Data File Layout:** Optimization helps leverage data-skipping algorithms.

| Technique                                  | What it is                                                                                         | When to use                                                                                                                                                                 | Good for                                                                | Avoid / notes                                                                                                                    |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Liquid Clustering**                      | Adaptive data layout that continuously clusters files by chosen keys without rewrites of old data. | **Default for new Delta tables.** Pick 1–3 selective keys you frequently filter/join on. Works with Streaming Tables & Materialized Views.                                  | Large (& growing) tables, mixed read/write, evolving query patterns.    | **Don’t mix with Z-ORDER.** Supersedes legacy partitioning & Z-ORDER.                                                            |
| **Partitioning (legacy Delta partitions)** | Physically separates data by a column (e.g., folders like `dt=2025-10-17`).                        | Use **sparingly** for coarse operational needs: lifecycle/retention by date, very large append-only logs, governance/SLA boundaries. Most tables **< ~1 TB don’t need it**. | Pruning big time-range scans; easy deletes by partition (retention).    | Over-partitioning hurts (many tiny files, skew). Prefer Liquid for performance-driven layout; this excludes “liquid partitions.” |
| **Z-ORDER (legacy)**                       | Reorders data files to colocate values of selected columns to improve data skipping.               | Only on **non-Liquid** legacy tables with stable access patterns where Liquid isn’t available.                                                                              | Speeding up filters/joins on a few columns when stuck on legacy layout. | **Incompatible with Liquid.** Long-term guidance is to move to Liquid; use Z-ORDER as a stopgap.                                 |

> Liquid Clustering is the new Databricks optimization technique that replaces traditional partitioning and Z-ORDER.

#### 1.5 Relational Entities

| Concept                 | RDBMS (SQL Server, PostgreSQL, …)                                      | Databricks (Unity Catalog)                                                       | Comment                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Top level**           | **Database** → logical container for schemas and tables                | **Catalog** → top-level container for schemas and tables                         | The **Catalog** in Databricks plays the same role as a **Database** in traditional RDBMS.                            |
| **Middle level**        | **Schema** → groups related tables, views, functions within a database | **Schema** → groups related objects within a catalog                             | Same concept and naming in both systems.                                                                             |
| **Bottom level**        | **Table** → physical/logical data structure containing rows            | **Table** → Delta Lake table stored in Unity Catalog                             | Identical concept; in Databricks, stored in Delta format with metadata managed by Unity Catalog.                     |
| **Full path reference** | `database.schema.table`                                                | `catalog.schema.table`                                                           | Equivalent structure; Unity Catalog adds one more layer of governance above the traditional “database.”              |
| **Extra notes**         | Database = storage and security boundary                               | Catalog = *governance + data-sharing* boundary (permissions, lineage, discovery) | Databricks uses the Catalog for cross-workspace governance, lineage, and access control (not just logical grouping). |

#### 1.2 Databases and Tables on Databricks (Hands On)

[database_and_tables](code/01_database_and_tables.md)

#### 1.3 CTAS, Clone, Views

##### CTAS

`CREATE TABLE … AS SELECT …`

###### 4) Does **CTAS** copy constraints, comments, properties, or identity columns?

**No.** `CREATE TABLE … AS SELECT …` (CTAS) creates a **new** table from the query’s result.

* Infers the **schema** from the SELECT output.
* **Does not** carry over table constraints, comments, properties, identity columns, or tags.
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

##### 5) Do **CLONEs** copy constraints, comments, and properties?

**Yes (in general).** `DEEP CLONE` and `SHALLOW CLONE` copy the **table’s metadata** (schema, comments, properties, constraints) and create a new Delta table.

* **Deep clone**: copies **data files** to target storage.
* **Shallow clone**: references source’s existing files (snapshot at clone time).

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

##### 6) Can I clone **across catalogs** or **workspaces**?

* **Same metastore**: clone across **schemas/catalogs** normally (permissions required).
* **Different metastores / workspaces**: `CLONE` doesn’t cross metastores. Pattern:

  1. **Deep clone** to an external `LOCATION` (shared cloud path).
  2. **Register** that path as Delta table in the target environment.

```sql
CREATE TABLE main.demo.emp_deep_ext
DEEP CLONE main.prod.employees
LOCATION 'abfss://container@account.dfs.core.windows.net/demo/emp_deep_ext/';
```

---

##### 7) What about **VACUUM** and shallow clones?

* Shallow clone depends on **source files** that existed at clone time.
* If you **VACUUM** the **source** and remove files the shallow clone references, the clone can **break**.
* Safe: don’t VACUUM below the default retention until sure no shallow clone needs those files.

```sql
VACUUM main.prod.employees RETAIN 168 HOURS; -- 7 days
```

---

##### 8) Can I clone a **specific point in time**?

**Yes.** Clone by **version** or **timestamp**.

```sql
CREATE TABLE main.demo.sales_deep_v42
DEEP CLONE main.prod.sales VERSION AS OF 42;

CREATE TABLE main.demo.sales_shallow_t
SHALLOW CLONE main.prod.sales TIMESTAMP AS OF '2025-09-30T12:00:00Z';
```

---

##### 9) Is a **shallow clone** like a **view**?

**No.**

* **View** re-runs a query against current source data.
* **Shallow clone** is a **stand-alone Delta table** with its own log, snapshotting files at clone time.

---

##### 10) After cloning, **where do new writes go**?

* Clones are **independent tables**.
* New writes to the **clone** create new files in the clone’s storage.
* They do **not** modify the source.

```sql
INSERT INTO main.demo.employees_shallow
VALUES (999, 'Test User', DATE '2025-10-01', 1.00);
```

---

##### 11) Does CTAS preserve **physical layout** (clustering)?

**No.** CTAS **rewrites files** from the query result; layout is not preserved.

```sql
OPTIMIZE main.demo.emp_ctas;
```

---

##### 12) Do **privileges** copy with clones?

* The clone is a **new object**; **grants/ACLs do not carry over**.
* Re-grant on the target table.

```sql
GRANT SELECT ON TABLE main.demo.employees_deep TO `data-analyst-role`;
```

---

##### 13) Quick reference: CTAS vs Deep/Shallow Clone

| Feature                 | CTAS                       | Deep Clone                                | Shallow Clone                              |
| ----------------------- | -------------------------- | ----------------------------------------- | ------------------------------------------ |
| Copies metadata         | Basic (schema only)        | **Yes** (schema, constraints, properties) | **Yes**                                    |
| Copies data files       | **Rewrites new files**     | **Yes** (physical copy)                   | **No** (references source files)           |
| Storage independence    | Yes                        | **Yes**                                   | **Partial**                                |
| Keeps in sync w/ source | No                         | No                                        | No                                         |
| Speed / cost            | Compute-heavy, new storage | Fast (storage copy), extra storage        | Fastest, minimal storage; VACUUM-sensitive |

---

#### 1.8 Views

Databricks supports several kinds of **views** you can use to abstract queries, control access, and speed up reads.

##### Quick overview

| View type                 | Scope & lifetime                             | Stored data? | Where it lives         | Typical use                                                |
| ------------------------- | -------------------------------------------- | ------------ | ---------------------- | ---------------------------------------------------------- |
| **Temporary view**        | Session-only                                 | No           | Not in metastore       | Ad-hoc exploration; chaining DataFrame → SQL               |
| **Global temporary view** | Cluster-wide while cluster lives             | No           | Schema `global_temp`   | Share temp view across notebooks on the same cluster       |
| **Persistent view**       | Permanent until dropped                      | No           | Catalog + schema       | Stable semantic layer, permissions, sharing                |
| **Materialized view**     | Permanent; system maintains precomputed data | Yes          | Catalog + schema (SQL) | Faster queries; pre-aggregation; maintained by the service |

---

##### 1) Temporary view

```sql
CREATE OR REPLACE TEMP VIEW v_recent_hires AS
SELECT emp_id, full_name, hired_date
FROM main.demo.employees
WHERE hired_date >= DATE '2025-01-01';
```

> Scope: current session only. Not grantable; not in UC.

---

##### 2) Global temporary view

```sql
CREATE OR REPLACE GLOBAL TEMP VIEW gv_recent_hires AS
SELECT emp_id, full_name, hired_date
FROM main.demo.employees
WHERE hired_date >= DATE '2025-01-01';
```

```sql
SELECT * FROM global_temp.gv_recent_hires;
```

> Scope: all sessions on the same cluster. Lives in `global_temp` schema.

---

##### 3) Persistent view (Unity Catalog)

```sql
CREATE OR REPLACE VIEW main.analytics.v_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

```sql
GRANT SELECT ON VIEW main.analytics.v_high_paid TO `analyst_role`;
```

> Stored in UC; every query re-runs the base SQL.

---

##### 4) Materialized view (Databricks SQL)

```sql
CREATE OR REPLACE MATERIALIZED VIEW main.analytics.mv_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

> Stores results and refreshes automatically; great for repeated BI queries.

---

##### 5) “Dynamic views” for row-level security (pattern)

Persistent view with predicates like `current_user()` / `is_account_group_member()`.

```sql
CREATE OR REPLACE VIEW main.secure.v_sales AS
SELECT *
FROM main.prod.sales
WHERE region IN (
  SELECT region
  FROM main.secure.user_region_map
  WHERE username = current_user()
);
```

---

##### Databricks — Persistent View vs Materialized View

* **Persistent view:** no stored data; always live; can be slower/expensive.
* **Materialized view:** stores results; reads fast; eventually consistent.

###### What each one is

**Persistent View (regular view)**

```sql
CREATE OR REPLACE VIEW main.analytics.v_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

**Materialized View**

```sql
CREATE OR REPLACE MATERIALIZED VIEW main.analytics.mv_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

###### Pros & Cons

| Aspect           | Persistent View             | Materialized View                         |
| ---------------- | --------------------------- | ----------------------------------------- |
| Freshness        | Always current              | Eventual (refresh cadence)                |
| Read latency     | Can be slow on large data   | Fast reads                                |
| Compute on read  | Higher                      | Lower                                     |
| Maintenance cost | None                        | Yes (storage + refresh)                   |
| SQL flexibility  | Broad                       | Some limitations                          |
| Best for         | Semantic layer, RLS, ad-hoc | BI dashboards, heavy recurring aggregates |

---

### 2. Data Processing & Transformations

**Can you create a table inside Databricks that is not a Delta table?**

Short answer: **yes**, but with limits.

* **Managed tables (UC):** always **Delta**.
* **External tables:** you can create non-Delta tables over files (Parquet/CSV/JSON/ORC/Avro) via `USING <format> LOCATION ...`.

```sql
-- External PARQUET table (non-Delta)
CREATE EXTERNAL TABLE main.analytics.events_parquet (
  id BIGINT,
  name STRING,
  ts TIMESTAMP
)
USING PARQUET
LOCATION 'abfss://data@acct.dfs.core.windows.net/raw/events/';
```

You can also CTAS:

```sql
CREATE EXTERNAL TABLE main.analytics.some_parquet
USING PARQUET
LOCATION 'abfss://data@acct.dfs.core.windows.net/out/some_parquet/'
AS SELECT * FROM main.analytics.source;
```

| Capability                | Delta Table (`USING DELTA`) | External Data-Source Table (`USING CSV/JSON/PARQUET ...`) |
| ------------------------- | --------------------------- | --------------------------------------------------------- |
| ACID                      | Yes                         | No                                                        |
| DML (UPDATE/DELETE/MERGE) | Supported                   | Generally not / non-ACID                                  |
| Time Travel               | Yes                         | No                                                        |
| CDF                       | Yes                         | No                                                        |
| Constraints               | Yes                         | Limited/none                                              |
| Schema enforcement        | Strict                      | Loose                                                     |
| Performance features      | OPTIMIZE, Z-ORDER, stats    | None                                                      |
| Small-files handling      | OPTIMIZE, Auto Optimize     | Manual                                                    |
| VACUUM                    | Yes                         | No                                                        |
| Cloning                   | Yes                         | No                                                        |

#### 2.1 Querying Files (ad-hoc over storage)

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

**PySpark — explicit schema (recommended for CSV/JSON)**

```python
from pyspark.sql.types import StructType, StructField, LongType, StringType, TimestampType

schema = StructType([
    StructField("id", LongType()),
    StructField("name", StringType()),
    StructField("ts", TimestampType()),
])

df = (spark.read
      .schema(schema)
      .option("header", True)        # for CSV
      .option("multiLine", True)     # for JSON with newlines
      .json("abfss://data@acct.dfs.core.windows.net/raw/events/*.json"))

df.select("id","name","ts").where("ts >= '2025-10-01'").show()
```

> Exam tip: querying by path is **schema-on-read**. For governance/ACID, load into **Delta tables**.

#### 2.3 Writing to Tables (Hands-On)

**A) SQL CTAS → managed Delta**

```sql
CREATE TABLE main.analytics.events_delta
USING DELTA
AS
SELECT id, name, ts
FROM parquet.`abfss://data@acct.dfs.core.windows.net/raw/events/*.parquet`;
```

**B) `INSERT INTO` existing Delta**

```sql
INSERT INTO main.analytics.events_delta (id, name, ts)
SELECT id, name, ts
FROM json.`abfss://data@acct.dfs.core.windows.net/raw/events/2025/10/*.json`;
```

**C) PySpark DataFrameWriter**

```python
from pyspark.sql.functions import to_date

df2 = df.withColumn("event_date", to_date("ts"))

(df2.write
    .format("delta")
    .mode("append")                  # overwrite | append | errorifexists
    .option("mergeSchema", "true")
    .partitionBy("event_date")
    .saveAsTable("main.analytics.events_delta"))
```

**D) External Delta table**

```sql
CREATE TABLE main.analytics.events_ext
USING DELTA
LOCATION 'abfss://data@acct.dfs.core.windows.net/curated/events_delta/';

INSERT INTO main.analytics.events_ext
SELECT * FROM main.analytics.events_delta;
```

##### `from_json` — Parse JSON strings into structs/arrays

**Input**

| id | payload                        |
| -- | ------------------------------ |
| 1  | `{"k":1,"tags":["a","b","a"]}` |
| 2  | `{"k":2,"tags":["b","c"]}`     |

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

##### `collect_set` — Aggregate unique values per group

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

##### `array_distinct` — Remove duplicates inside array

```sql
SELECT id, array_distinct(tags) AS tags_dedup
FROM (SELECT 1 AS id, array('a','b','a') AS tags);
```

##### `flatten` — Collapse nested arrays

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

##### `explode` — Array → multiple rows

```sql
WITH t AS (SELECT 10 AS id, array('a','b','a') AS tags)
SELECT id, explode(tags) AS tag
FROM t;
```

##### Summary table (array helpers)

| Function         | Purpose                                 | Pattern                         |
| ---------------- | --------------------------------------- | ------------------------------- |
| `from_json`      | JSON string → typed struct/array        | `from_json(col, 'STRUCT<...>')` |
| `collect_set`    | Aggregate unique values per group       | `GROUP BY id; collect_set(col)` |
| `array_distinct` | Remove duplicates inside array          | `array_distinct(arr)`           |
| `flatten`        | Collapse `array<array<T>>` → `array<T>` | `flatten(collect_list(arr))`    |
| `explode`        | Array → multiple rows                   | `SELECT explode(arr)`           |

#### 2.5 Higher Order Functions and SQL UDFs (Hands On)

##### `filter` — Keep only elements matching predicate

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

##### `size` — Length of array/map

```sql
WITH t AS (
  SELECT * FROM VALUES
    (1, array('a','b','a')),
    (2, array())
  AS t(id, tags)
)
SELECT id, size(tags) AS tag_count FROM t;
```

##### `transform` — Map each array element to new value

```sql
WITH t AS (
  SELECT 1 AS id, array(' A ','b ',' C') AS tags
)
SELECT
  id,
  transform(tags, x -> lower(trim(x))) AS tags_norm
FROM t;
```

##### SQL UDF — reusable logic

```sql
CREATE OR REPLACE FUNCTION main.analytics.normalize_tag(s STRING)
RETURNS STRING
RETURN lower(trim(s));
```

```sql
WITH t AS (SELECT 1 AS id, array('  Foo','BAR  ','  bar') AS tags)
SELECT
  id,
  transform(tags, x -> normalize_tag(x))                             AS tags_norm,
  array_distinct(transform(tags, x -> normalize_tag(x)))             AS tags_norm_unique
FROM t;
```

---

### 3. Incremental Data Processing

**Data Stream**

* Any data source that grows over time:

  * New files in cloud storage.
  * Updates to a DB captured in a CDC feed.
  * Events queued in pub/sub.

**Processing a data stream**

1. Reprocess entire source each time.
2. Or process only new data since last update → **Structured Streaming**.

**Unsupported operations (pure streaming)**

* Global sort
* Global dedup without watermark/state bounds

**Advanced methods**

* Windowing
* Watermarking

#### 3.0 Bronze Ingestion

##### Bronze ingestion on Databricks — first things first

Goal of Bronze: land **raw, append-only** data in Delta with minimal transforms.

**Quick decision**

| Source                 | Batch (low freq/backfill)       | Streaming (continuous)                                   |
| ---------------------- | ------------------------------- | -------------------------------------------------------- |
| Files in cloud storage | `COPY INTO` or batch `df.write` | Auto Loader (`cloudFiles` + `readStream` → `writeStream` |
| Database tables        | Batch JDBC extract → Delta      | CDC → landed to files/Delta → `readStream` + MERGE/CDF   |
| Event streams          | —                               | `readStream.format("kafka")` → Delta                     |
| Prefer managed         | DLT batch                       | DLT streaming                                            |

##### 1) Batch loading

`COPY INTO`, JDBC, or batch jobs.

##### 2) Streaming loading

Auto Loader, Kafka/Event Hubs, Delta CDF.

##### Delta Live Tables (DLT) — managed batch or streaming

Used for governance, quality, retries, lineage.

#### 3.1 Structured Streaming

##### `readStream` — streaming source

```python
src = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("dbfs:/mnt/bronze/raw/events/"))
```

##### 3) Where does the data live? Does the DF “grow”?

* `readStream` returns a **logical plan**, not a growing in-memory dataset.
* What persists is **sink tables**, **checkpoints**, and Auto Loader logs.

##### `writeStream` — streaming sink

```python
(spark.readStream.table("main.bronze.events_raw")
  .writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation","dbfs:/mnt/_chk/silver/events_raw")
  .toTable("main.silver.events_raw"))
```

##### Auto Loader options — 80/20

| Option                          | Why you care                     |
| ------------------------------- | -------------------------------- |
| `cloudFiles.format`             | File type                        |
| `cloudFiles.schemaLocation`     | Schema + discovery log           |
| `includeExistingFiles`          | Backfill on first run            |
| `cloudFiles.maxFilesPerTrigger` | Pace work per micro-batch        |
| `cloudFiles.useNotifications`   | Faster discovery at scale        |
| `checkpointLocation` (sink)     | Exactly-once / progress tracking |

---

### 4. Production Pipelines

#### 4.2 Delta Live Tables

##### Delta Live Tables (DLT) — what it is

Managed pipeline framework with declarative SQL/Python.

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

##### Why can’t I just create them as normal tables?

* Physical objects are Delta tables, but `LIVE` / `STREAMING LIVE` syntax is understood only by the **DLT engine**, which also manages ordering, retries, expectations, event log, etc.

##### `CREATE STREAMING LIVE TABLE` vs `CREATE LIVE TABLE`

| Aspect          | STREAMING LIVE TABLE (Bronze)       | LIVE TABLE (Silver)                                 |
| --------------- | ----------------------------------- | --------------------------------------------------- |
| Execution model | Streaming (incremental)             | Batch (per run), unless using `STREAM(...)` sources |
| Typical layer   | Bronze ingest                       | Silver transform                                    |
| State           | Managed streaming state/checkpoints | Stateless unless consuming `STREAM(...)`            |

#### 4.3 Change Data Capture

##### CDC on Databricks — concept vs features

* **CDC pattern**: process only changed rows.
* Implemented via **Delta MERGE**, **Delta CDF**, **Auto Loader**, **Structured Streaming**, **DLT**.

Key pieces:

1. **Delta CDF** (`delta.enableChangeDataFeed = true`)
2. **MERGE INTO** for upserts/deletes
3. Streaming ingest from CDC sources
4. **DLT `APPLY CHANGES INTO`** for declarative CDC

##### Delta Change Data Feed (CDF) — “publish/subscribe”

* Source table publishes changes.
* Consumers read via `table_changes` or `readChangeFeed` and apply to downstream tables.

#### 4.4 Processing CDC Feed with DLT

##### CDC with Delta Live Tables — `APPLY CHANGES INTO`

| Category                 | Pros                                                               | Cons/caveats                                 |
| ------------------------ | ------------------------------------------------------------------ | -------------------------------------------- |
| Simplicity & reliability | Declarative CDC with retries, checkpoints, expectations, lineage.  | Less control than hand-written MERGE         |
| Performance & scale      | Incremental processing, Photon, optimized tables.                  | Still costs compute on heavy churn           |
| Schema & governance      | Integrates with UC, handles some schema drift, strong lineage.     | Complex renames/type changes still manual    |
| Operational simplicity   | Single pipeline, monitored via DLT UI with logs and system tables. | Bound to DLT runtime (fewer low-level knobs) |

#### 4.5 Databricks Asset Bundles

##### Databricks Asset Bundles (DABs) — Dev → QA → Prod with YAML

Goal: single repo for code + jobs, promoted via `databricks.yml` + CLI/CI.

* Root file: `databricks.yml`
* Define **targets**: `dev`, `qa`, `prod` with `mode: development|production`
* Deploy with CLI: `bundle validate|plan|deploy|run|destroy|deployment bind`

###### 1) Repo layout

```text
.
├── databricks.yml
├── resources/
│   └── jobs/
│       └── etl_job.yml
├── notebooks/
│   └── 01_load.ipynb
└── src/
    └── main.py
```

###### 2) `databricks.yml` — targets & overrides

```yaml
bundle:
  name: my_project
workspace:
  root_path: /Shared/bundles/${bundle.name}/${bundle.target}

include:
  - resources/**/*.yml

variables:
  some_var:
    default: value

targets:
  dev:
    mode: development
    workspace:
      host: https://<dev-workspace>

  qa:
    mode: production
    workspace:
      host: https://<qa-workspace>

  prod:
    mode: production
    workspace:
      host: https://<prod-workspace>
    run_as:
      service_principal_name: ${var.spn_id}
```

###### 3) Example job resource

```yaml
resources:
  jobs:
    etl_job:
      name: ${bundle.name}-etl
      tasks:
        - task_key: load
          notebook_task:
            notebook_path: ../notebooks/01_load.ipynb
```

###### 4) Local workflow

```bash
databricks bundle validate -t dev
databricks bundle plan    -t dev
databricks bundle deploy  -t dev
databricks bundle run etl_job -t dev -- --param1=foo
```

###### 5) CI/CD (sketch)

```yaml
name: Deploy DABs
on:
  push:
jobs:
  dev:
    runs-on: ubuntu-latest
  qa:
    needs: dev
  prod:
    needs: qa
```

---

### 5. Data Governance & Security

#### 5.1 Databricks SQL

Self-explanatory: SQL over your tables. Belongs under governance because it’s how you **inspect, validate and serve** data (views, permissions, etc.).

#### 5.2 Data Objects Privileges and Managing Permissions

##### Data object privileges (Unity Catalog) — Quick study notes

**What can be protected**

| Object   | Scope                  |
| -------- | ---------------------- |
| CATALOG  | Entire catalog         |
| SCHEMA   | Database (schema)      |
| TABLE    | Managed/external table |
| VIEW     | SQL view               |
| FUNCTION | Named function         |
| ANY FILE | Underlying filesystem  |

> `GRANT <privilege> ON <object> TO <principal>`.

##### Privileges — what they allow

| Privilege                        | Ability                   |
| -------------------------------- | ------------------------- |
| SELECT                           | Read rows                 |
| MODIFY                           | Insert, update, delete    |
| CREATE                           | Create child objects      |
| READ_METADATA                    | See object & metadata     |
| USAGE / USE CATALOG / USE SCHEMA | Prerequisite gate         |
| ALL PRIVILEGES                   | All applicable privileges |

Typical pattern: **USE CATALOG + USE SCHEMA + SELECT/MODIFY**.

##### Who can grant what

| Granting role            | Scope                    |
| ------------------------ | ------------------------ |
| Databricks administrator | All catalog objects + FS |
| Catalog owner            | All objects in catalog   |
| Schema owner             | All objects in schema    |
| Object owner             | That object only         |

##### Access control operations

* `GRANT`, `REVOKE`, `DENY` (when supported), `SHOW GRANTS`.

##### Minimal examples

```sql
GRANT USAGE ON CATALOG main TO `user_1@company.com`;
GRANT USAGE ON SCHEMA main.analytics TO `user_1@company.com`;

GRANT SELECT ON TABLE main.analytics.my_table TO `user_1@company.com`;
GRANT MODIFY ON TABLE main.analytics.my_table TO `data_writers`;

REVOKE MODIFY ON TABLE main.analytics.my_table FROM `data_writers`;
SHOW GRANTS ON TABLE main.analytics.my_table;
```

##### Core Unity Catalog privileges (cheat sheet)

Assume: `main.analytics.sales`.

| Privilege    | Applies to     | Allows (short)                                  | Does **not** allow alone          |
| ------------ | -------------- | ----------------------------------------------- | --------------------------------- |
| BROWSE       | Catalog/schema | See metadata in Catalog Explorer/search         | No data read/write                |
| USE CATALOG  | Catalog        | Access catalog *if* you also have object rights | No SELECT/MODIFY; not auto-browse |
| USE SCHEMA   | Schema         | Access objects in schema with object rights     | No SELECT/MODIFY                  |
| SELECT       | Table/view     | Read rows                                       | Needs USE CATALOG + USE SCHEMA    |
| MODIFY       | Table          | INSERT/UPDATE/DELETE/MERGE                      | No read if SELECT missing         |
| CREATE TABLE | Schema/catalog | Create tables/views                             | No read/write existing tables     |
| MANAGE       | Any UC object  | Manage privileges/properties                    | No data read/write                |

##### Example privilege sets (A–F)

See who can do what in this scenario:

| User | Privileges on `main` / `main.analytics` / `sales`     | Can read rows? | Can write rows? | Manage grants? | See catalog? |
| ---- | ----------------------------------------------------- | -------------- | --------------- | -------------- | ------------ |
| A    | BROWSE on catalog                                     | ❌              | ❌               | ❌              | ✅ (Explorer) |
| B    | USE CATALOG                                           | ❌              | ❌               | ❌              | ✅            |
| C    | USE CATALOG + USE SCHEMA                              | ❌              | ❌               | ❌              | ✅            |
| D    | USE CATALOG + USE SCHEMA + SELECT on `sales`          | ✅ (`sales`)    | ❌               | ❌              | ✅            |
| E    | USE CATALOG + USE SCHEMA + SELECT + MODIFY on `sales` | ✅ (`sales`)    | ✅ (`sales`)     | ❌              | ✅            |
| F    | USE CATALOG + USE SCHEMA + MANAGE on `sales`          | ❌              | ❌               | ✅ (`sales`)    | ✅            |

#### 5.3 Unity Catalog — PDF Summary (Study Notes)

##### What is Unity Catalog?

* Centralized governance across workspaces/clouds.
* Governs data & AI assets: tables, files, models, dashboards.
* SQL-based access control (`GRANT`/`REVOKE`).

##### Architecture — before vs with UC

* **Before**: each workspace had its own Hive metastore.
* **With UC**: account-level UC metastores; workspaces share governance.

##### 3-Level Namespace & Hierarchy

* `catalog.schema.table` (e.g., `main.analytics.sales`).
* Hierarchy: Metastore → Catalog → Schema → Table/View/Function.
* Plus: Storage Credential, External Location, Share, Recipient.

##### Identities & Identity Federation

* Users, Service Principals, Groups (nested).
* Managed at account level; same identity across workspaces.

##### Security model

* Principals: users, groups, service principals.
* Securable objects: metastore, storage credential, external location, catalog, schema, table/view/function, share/recipient.
* Privileges: `SELECT`, `MODIFY`, `CREATE`, `READ FILES`, `WRITE FILES`, `USE CATALOG`, `USE SCHEMA`, etc.

##### Legacy Hive Metastore

* UC can coexist with `hive_metastore` as another catalog.
* Migration to UC can be gradual.

#### 5.4 Delta Sharing — Quick study notes

**When useful:** share **live Delta tables** across orgs/platforms without copying data.

* Open protocol for secure data sharing of Delta tables.
* Provider exposes **Delta Sharing server**; recipients can be any platform speaking the protocol.

Core idea:

* Provider defines **SHARE** and adds tables:

  ```sql
  CREATE SHARE bookstore;
  ALTER SHARE bookstore ADD TABLE orders;
  GRANT SELECT ON SHARE bookstore TO publisher1;
  ```

* Recipient gets short-lived pre-signed URLs to Parquet files and reads directly from storage.

* No replication required; read-only; only Delta tables are shareable.

#### 5.5 Lakehouse Federation — Quick study notes

**When useful:** query external systems **live** without ingesting data.

* Federation lets you run queries across external sources (MySQL, others) without migrating data.
* Databricks exposes them as **foreign catalogs/schemas**:

```sql
SELECT * FROM foreign_catalog.mysql_schema.table1;
```

* Good for ad-hoc/POCs and light operational reporting; heavy queries still depend on external system performance.

#### 5.6 Cluster Best Practices — Quick study notes

**Goal:** choose right compute type/instance family/serverless vs classic.

* **Classic compute:**

  * All-purpose clusters (interactive; higher DBUs).
  * Job clusters (per job; cheaper DBUs).
* **SQL Warehouses:**

  * Serverless where available; Pro for custom networking.
* **Serverless compute:**

  * Fast startup/scaling, Photon on, Python/SQL only.

Instance families:

* Memory-optimized: heavy shuffle/spill, caching, ML.
* Compute-optimized: streaming, `OPTIMIZE`, Z-ORDER.
* Storage-optimized: Delta caching, ad-hoc analytics.
* GPU: DL/ML.
* General purpose: default; good for VACUUM.

Cost tools:

* Spot instances, instance pools, autoscaling.

---

If you like, next step we can create a **separate mini-TOC per chapter** (e.g. for chapter 3 only) or add “Hands-On” markers consistently across sections.
