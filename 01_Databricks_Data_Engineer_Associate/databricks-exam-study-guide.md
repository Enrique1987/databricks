# Databricks Certified Data Engineer Associate

## General Table of Contents
1. [Databricks Intelligence Platform](#1-databricks-intelligence-platform)
   - [1.1 Delta Lake](#11-delta-lake)
   - [1.2 Understanding Delta Tables (Hands On)](#12-understanding-delta-tables-hands-on)
   - [1.3 Advanced Delta Lake Features](#13-advanced-delta-lake-features)
   - [1.4 Apply Advanced Delta Features (Hands On)](#14-apply-advanced-delta-features-hands-on)
   - [1.5 Relational Entities](#15-relational-entities)
   - [1.6 Databases and Tables on Databricks (Hands On)](#16-databases-and-tables-on-databricks-hands-on)
   - [1.7 Set Up Delta Tables](#17-set-up-delta-tables)
   - [1.8 Views](#18-views)
   - [1.9 Working with Views (Hands On)](#19-working-with-views-hands-on)

2. [Data Processing & Transformations](#2-data-processing--transformations)
   - [2.1 Querying Files](#21-querying-files)
   - [2.2 Querying Files (Hands On)](#22-querying-files-hands-on)
   - [2.3 Writing to Tables (Hands On)](#23-writing-to-tables-hands-on)
   - [2.4 Advanced Transformations (Hands On)](#24-advanced-transformations-hands-on)
   - [2.5 Higher Order Functions and SQL UDFs (Hands On)](#25-higher-order-functions-and-sql-udfs-hands-on)

3. [Incremental Data Processing](#3-incremental-data-processing)
   - [3.1 Structured Streaming](#31-structured-streaming)
   - [3.2 Structured Streaming (Hands On)](#32-structured-streaming-hands-on)
   - [3.3 Incremental Data Ingestion](#33-incremental-data-ingestion)
   - [3.4 Auto Loader (Hands On)](#34-auto-loader-hands-on)

4. [Production Pipelines](#4-production-pipelines)
   - [4.1 Multi-hop Architecture](#41-multi-hop-architecture)
   - [4.2 Delta Live Tables (Hands On)](#42-delta-live-tables-hands-on)
   - [4.3 Change Data Capture](#43-change-data-capture)
   - [4.4 Processing CDC Feed with DLT (Hands On)](#44-processing-cdc-feed-with-dlt-hands-on)
   - [4.5 Jobs (Hands On)](#45-jobs-hands-on)

5. [Data Governance & Security](#5-data-governance--security)
   - [5.1 Databricks SQL](#51-databricks-sql)
   - [5.2 Data Objects Privileges](#52-data-objects-privileges)
   - [5.3 Managing Permissions (Hands On)](#53-managing-permissions-hands-on)
   
6. [What Changed Since 2023](#6-what-changed--since-2023)
	- [6.1 Unity Catalog Evolution](#61-unity-catalog-evolution)
	- [6.2 SQL, Analytics & BI Updates](#62-sql-analytics--bi-updates)
	- [6.3 Delta Live Tables (DLT) & Pipeline Enhancements](#63-delta-live-tables-dlt--pipeline-enhancements)
	- [6.4 Runtime, Notebooks & Developer Experience](#64-runtime-notebooks--developer-experience)
	- [6.5 Generative AI, ML & Agent Workflows](#65-generative-ai-ml--agent-workflows)
	- [6.6 Platform & Collaboration Features](#66-platform--collaboration-features)
	- [6.7 Key Skills to Refresh for 2025](#67-key-skills-to-refresh-for-2025)   

---

### 1. Databricks Intelligence Platform

**RDBMS**  
Database → Schema → Table  
**Databricks**  
Catalog → Schema → Table   

**metastore**: service that manages all catalogs.   
**hive_metastore** is the **default catalog** its often use for testing.  


#### 1.1 Delta Lake, Delta Tables, Advance Features

1.1 Delta Lake, Delta Tables, Advanced Features

- **Transaction Log:** Ensure ACID Properties, you will never read dirty data.
  
- **Advanced Features:**

| Advanced Feature           | Use Case                                                                 |
|----------------------------|--------------------------------------------------------------------------|
| `VACUUM`                   | Removes old and unused files, helping to reduce latency and free up space. |
| `Time Travel`              | Allows restoring a previous state of a table, enabling recovery to a desired point in time. |
| `Compacting Small Files`   | Improves query performance by merging small files into larger ones, especially useful when dealing with many small files. |

- **Data File Layout:** Optimization helps leverage data-skipping algorithms.


| Technique                                  | What it is                                                                                         | When to use (2025–2026)                                                                                                                                                             | Good for                                                                               | Avoid / notes                                                                                                                                                             |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Liquid Clustering**                      | Adaptive data layout that continuously clusters files by chosen keys without rewrites of old data. | **Default for new Delta tables.** Pick 1–3 selective keys you frequently filter/join on (e.g., `org_urn`, `date`, `customer_id`). Works with Streaming Tables & Materialized Views. | Large (& growing) tables, mixed read/write, evolving query patterns, redefinable keys. | **Don’t mix with Z-ORDER.** Supersedes legacy partitioning & Z-ORDER. Generally available for Delta; recommended for new tables. ([Databricks Dokumentation][1])          |
| **Partitioning (legacy Delta partitions)** | Physically separates data by a column (e.g., folders like `dt=2025-10-17`).                        | Use **sparingly** for coarse operational needs: lifecycle/retention by date, very large append-only logs, governance/SLA boundaries. Most tables **< ~1 TB don’t need it**.         | Pruning big time-range scans; easy deletes by partition (retention).                   | Over-partitioning hurts (many tiny files, skew). Prefer Liquid for performance-driven layout; this guidance excludes “liquid partitions.” ([Databricks Dokumentation][2]) |
| **Z-ORDER (legacy)**                       | Reorders data files to colocate values of selected columns to improve data skipping.               | Only on **non-Liquid** legacy tables with stable access patterns where Liquid isn’t available.                                                                                      | Speeding up filters/joins on a few columns when stuck on legacy layout.                | **Incompatible with Liquid.** Long-term guidance is to move to Liquid; use Z-ORDER as a stopgap. ([Databricks Dokumentation][3])                                          |

`Liquid Clustering is the new Databricks optimization technique that replaces traditional partitioning and Z-ORDER
 — it automatically manages data layout, adapts over time, and supports both batch and streaming workloads.`


#### 1.5 Relational Entities

| Concept                 | **RDBMS (e.g. SQL Server, PostgreSQL, Oracle)**                        | **Databricks (Unity Catalog)**                                                        | Comment                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Top level**           | **Database** → logical container for schemas and tables                | **Catalog** → top-level container for schemas and tables                              | The **Catalog** in Databricks plays the same role as a **Database** in traditional RDBMS.                            |
| **Middle level**        | **Schema** → groups related tables, views, functions within a database | **Schema** → groups related objects within a catalog In Databricks SQL, “database” and “schema” are synonyms.                                 | Same concept and naming in both systems.                                                                             |
| **Bottom level**        | **Table** → physical/logical data structure containing rows            | **Table** → Delta Lake table stored in Unity Catalog                                  | Identical concept; in Databricks, stored in Delta format with metadata managed by Unity Catalog.                     |
| **Full path reference** | `database.schema.table`                                                | `catalog.schema.table`                                                                | Equivalent structure; Unity Catalog simply adds one more layer of governance above the traditional “database.”       |
| **Extra notes**         | Database = storage and security boundary                               | Catalog = *governance + data-sharing* boundary (permissions, lineage, data discovery) | Databricks uses the Catalog for cross-workspace governance, lineage, and access control (not just logical grouping). |


#### 1.2 Databases and Tables on Databricks (Hands On)
[database_and_tables](code/01_database_and_tables.md)

#### 1.3 CTAs, Clone, Views

##### CTAs  
`CREATE TABLE … AS SELECT …`

##### 4) Does **CTAS** copy constraints, comments, properties, or identity columns?

**No.** `CREATE TABLE … AS SELECT …` (CTAS) creates a **new** table from the query’s result.
- It infers the **schema** from the SELECT output.
- It **does not** carry over table constraints, comments, table properties, identity columns, or tags from the source.
- If you need them, you must **define them again** after CTAS.

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

**Yes (in general).** `DEEP CLONE` and `SHALLOW CLONE` copy the **table’s metadata** (schema, comments, properties, constraints) and create a new Delta table object.  
- **Deep clone** additionally copies **data files** to the target’s storage.
- **Shallow clone** references the source’s existing files (snapshot at clone time).

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

- **Same metastore (Unity Catalog)**: You can clone across **schemas/catalogs** normally (permissions required).
- **Different metastores or separate workspaces**: The `CLONE` command itself doesn’t cross metastores. Typical pattern:
  1) **Deep clone to an external LOCATION** (cloud path both environments can access).
  2) **Register** that path as a Delta table in the target environment.

```sql
-- Deep clone to an external path (within same metastore)
CREATE TABLE main.demo.emp_deep_ext
DEEP CLONE main.prod.employees
LOCATION 'abfss://container@account.dfs.core.windows.net/demo/emp_deep_ext/';
```

---

##### 7) What about **VACUUM** and shallow clones?

- **Shallow clone** depends on **source files** that existed at clone time.
- If you **VACUUM** the **source** and remove files the shallow clone still references, the clone can **break**.
- Safe practice: Don’t VACUUM below the default retention until you’re sure no shallow clone references those files.

```sql
-- Example: conservative vacuum (default retention)
VACUUM main.prod.employees RETAIN 168 HOURS; -- 7 days (example)
```

---

##### 8) Can I clone a **specific point in time**?

**Yes.** You can clone by **version** or **timestamp**.

```sql
-- Versioned deep clone
CREATE TABLE main.demo.sales_deep_v42
DEEP CLONE main.prod.sales VERSION AS OF 42;

-- Timestamped shallow clone
CREATE TABLE main.demo.sales_shallow_t
SHALLOW CLONE main.prod.sales TIMESTAMP AS OF '2025-09-30T12:00:00Z';
```

---

##### 9) Is a **shallow clone** like a **view**?

**No.**  
- A **view** re-runs a query against the **current** source every time you read it.  
- A **shallow clone** is a **stand-alone Delta table** with its own transaction log, capturing a **snapshot** (metadata + references to files at clone time). It does **not** update when the source changes.

---

##### 10) After cloning, **where do new writes go**?

- Both deep and shallow clones are **independent tables**.  
- New writes to the **clone** produce **new data files in the clone’s storage** (managed location or the external `LOCATION` you specified).  
- They do **not** modify the source, and vice versa.

```sql
-- Writes to the shallow clone produce new files under the clone's storage
INSERT INTO main.demo.employees_shallow VALUES (999, 'Test User', DATE '2025-10-01', 1.00);
```

---

##### 11) Does CTAS preserve **physical layout** (e.g., clustering) of the source?

**No.** CTAS **rewrites files** from the query result; any prior layout/optimization of the source is not preserved.  
- If you rely on specific clustering/optimization, re-apply afterward.

```sql
-- Re-apply an optimize step to the CTAS output if needed
OPTIMIZE main.demo.emp_ctas;
```

---

##### 12) Do **privileges** copy with clones?

- The clone is a **new object**; **grants/ACLs do not automatically carry over**.  
- Re-grant permissions on the target table (and external location if applicable).

```sql
GRANT SELECT ON TABLE main.demo.employees_deep TO `data-analyst-role`;
```

---

##### 13) Quick reference: CTAS vs Deep/Shallow Clone

| Feature                 | CTAS                                | Deep Clone                               | Shallow Clone                            |
|-------------------------|-------------------------------------|-------------------------------------------|------------------------------------------|
| Copies metadata         | Basic (schema only)                 | **Yes** (schema, constraints, properties) | **Yes**                                  |
| Copies data files       | **Rewrites new files**              | **Yes** (physical copy)                   | **No** (references source files)         |
| Storage independence    | Yes                                 | **Yes**                                   | **Partial** (depends on source files)    |
| Keeps in sync w/ source | No                                  | No                                        | No                                       |
| Speed / cost            | Compute-heavy, storage new files    | Fast (storage copy), extra storage        | Fastest (minimal storage), fragile w/ VACUUM |
| Cross-metastore         | Register path manually (no direct)  | Requires same metastore; path workaround  | Requires same metastore; path workaround |

---


#### 1.8 Views

Databricks supports several kinds of **views** you can use to abstract queries, control access, and speed up reads.

---

#### Quick overview

| View type | Scope & lifetime | Stored data? | Where it lives | Typical use |
|---|---|---|---|---|
| **Temporary view** | Session-only (ends when your notebook/cluster session ends) | No | Not in metastore | Ad-hoc exploration; chaining DataFrame → SQL |
| **Global temporary view** | Cluster-wide across sessions; lasts while the cluster lives | No | Special schema **`global_temp`** | Share a temp view across multiple notebooks on the same cluster |
| **Persistent view** (Unity Catalog / metastore) | Permanent until dropped | No | Catalog + schema (e.g., `main.analytics`) | Stable semantic layer, permissions, sharing |
| **Materialized view** | Permanent; system maintains precomputed results | **Yes** (physically stores results) | Catalog + schema (Databricks SQL) | Faster queries; pre-aggregation; incremental refresh by the service |

> Notes  
> - “Temporary” and “Global temporary” are **ephemeral** (no data stored; definitions vanish with the session/cluster).  
> - “Persistent view” and “Materialized view” are **metastore objects** you can grant privileges on (Unity Catalog recommended).  
> - Materialized views are supported in **Databricks SQL** (best on SQL Warehouses). They store results and are maintained by the platform.

---

##### 1) Temporary view

```sql
CREATE OR REPLACE TEMP VIEW v_recent_hires AS
SELECT emp_id, full_name, hired_date
FROM main.demo.employees
WHERE hired_date >= DATE '2025-01-01';
```

> **Scope:** Only your current session can see it. Disappears when the session ends. Usefull to storing intermediate results in a table that may later be useful to use.  
> **Permissions:** Not grantable; not part of Unity Catalog.  

---

##### 2) Global temporary view

```sql
CREATE OR REPLACE GLOBAL TEMP VIEW gv_recent_hires AS
SELECT emp_id, full_name, hired_date
FROM main.demo.employees
WHERE hired_date >= DATE '2025-01-01';
```

Query

```sql
SELECT * FROM global_temp.gv_recent_hires;
```

> **Scope:** Visible to **all sessions** attached to the **same cluster**.  
> **Lifetime:** Exists until the **cluster** stops.  
> **Namespace:** Always lives under the **`global_temp`** schema.

---

##### 3) Persistent view (Unity Catalog)

```sql
CREATE OR REPLACE VIEW main.analytics.v_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```
Grant permissions

```sql
GRANT SELECT ON VIEW main.analytics.v_high_paid TO `analyst_role`;
```

> **Scope:** Stored in the metastore (e.g., Unity Catalog), can be shared and permissioned.  
> **Data:** Not stored; every query re-runs the underlying SQL.

---

##### 4) Materialized view (Databricks SQL)

Create
```sql
CREATE OR REPLACE MATERIALIZED VIEW main.analytics.mv_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

> **What it is:** A view whose **results are materialized** (physically stored) and **maintained** by Databricks.  
> **Why use it:** Faster reads for repeated queries, dashboards, or expensive aggregations.  
> **Refresh:** Databricks maintains it automatically; it reflects changes in source tables per the platform’s maintenance schedule.  
> **Best practice:** Build them on relatively stable/append-heavy sources and on SQL Warehouses.

---

##### 5) “Dynamic views” for row-level security (pattern)

This is a **pattern** using a persistent view with predicates based on the requester (e.g., `current_user()` or `is_account_group_member()`), often combined with Unity Catalog grants.

```sql
CREATE OR REPLACE VIEW main.secure.v_sales AS
SELECT *
FROM main.prod.sales
WHERE region IN (
  SELECT region FROM main.secure.user_region_ma
```
#####  Databricks — Persistent View vs Materialized View

- **Persistent view** (a regular SQL view): **stores no data**. Every query **re-runs** the underlying SQL against source tables. Always “fresh” have live data, but can be **slow/expensive** on large data.
- **Materialized view**: **stores query results** and Databricks **maintains** them automatically. Reads are **fast/cheap**, but results are **eventually consistent** (not always up-to-the-millisecond). Has **maintenance cost** and some SQL limitations.

---

##### What each one is

##### Persistent View (a.k.a. regular view), its the clasical view we had in RDBMS
- **Definition** only; no stored result.
- Lives in the metastore (e.g., `main.analytics.v_sales`).
- Querying the view re-executes its SQL against the latest source data.
- Great as a **semantic layer** and for **governance** (grants, RLS via predicates).
  
```sql
CREATE OR REPLACE VIEW main.analytics.v_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

##### Materialized View
- Stores **precomputed results** that Databricks **refreshes** automatically.
- Designed for **BI/analytics** patterns (repeated queries, aggregates).
- Reads are fast; writes/refresh happen in the background.
- Results are **up-to-date on a schedule** (eventually consistent), not “instant”.
  
```sql
CREATE OR REPLACE MATERIALIZED VIEW main.analytics.mv_high_paid AS
SELECT emp_id, full_name, salary_eur
FROM main.demo.employees
WHERE salary_eur >= 70000;
```

---

##### Pros & Cons

| Aspect | Persistent View | Materialized View |
|---|---|---|
| Freshness | **Always current** (re-queries sources) | **Eventual** (refresh cadence) |
| Read latency | Can be **slow** on large data | **Fast** (reads precomputed results) |
| Compute cost on read | **Higher** (runs full query) | **Lower** (reads stored results) |
| Maintenance cost | None (no stored data) | **Yes** (background refresh/storage) |
| SQL flexibility | **Broad** (most SQL allowed) | **Some limits** (designed for maintainable queries) |
| Best for | Semantic layer, RLS, ad-hoc | Dashboards, recurring analytics, aggregates |

| View Type | Stores Data? | Needs Refresh? | Who Updates It? |
|------------|--------------|----------------|-----------------|
| **Persistent View** | ❌ No | ❌ Not needed (always live) | Query runs every time |
| **Materialized View** | ✅ Yes (cached results) | ✅ Yes (auto refresh by Databricks) | Databricks background job |


---

##### When to use which

##### Choose **Persistent View** when:
- You need **always-fresh** results (no staleness). For example some user need to acces to a table but just some columns of the table, but the data need to be live.  
- You want a **governed semantic layer** (views with grants, RLS).  
- Query is **lightweight** or data volume is modest.  
- Logic changes **frequently** and you don’t want maintenance overhead.

##### Choose **Materialized View** when:
- You have **repeated/BI** queries that re-read the same heavy results.
- You can tolerate **slight staleness** in exchange for **speed**.
- The query is **expensive** (joins/aggregations over large data).
- You want to **reduce SQL Warehouse costs** for BI consumers.

---

##### Quick decision checklist

- Need fastest reads for recurring dashboards? → **Materialized View** ✅  
- Need always-current data with minimal infra overhead? → **Persistent View** ✅  
- Need security predicates / RLS? → **Persistent View** (often called “dynamic views”) ✅  
- Query is complex and heavy, run many times/day? → **Materialized View** ✅

---

### 2. Data Processing & Transformations


**Can you create a table inside databricks that is not a delta table ?**  

Short answer: **yes**, but with limits.

* **Managed tables (Unity Catalog):** always **Delta**. You **cannot** make a managed non-Delta table.
* **External tables:** you *can* create non-Delta tables over files (Parquet/CSV/JSON/ORC/Avro) by pointing at a path.

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

You can also do CTAS in those formats:

```sql
CREATE EXTERNAL TABLE main.analytics.some_parquet
USING PARQUET
LOCATION 'abfss://data@acct.dfs.core.windows.net/out/some_parquet/'
AS SELECT * FROM main.analytics.source;
```
| Capability                | **Delta Table** (`USING DELTA`)                                                                 | **External Data-Source Table** (`USING CSV/JSON/PARQUET ...`)                                                          |
| ------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Storage & metadata        | Delta files + **_delta_log** transaction log                                                    | Plain files only; **no transaction log**                                                                               |
| ACID transactions         | **Yes** (optimistic concurrency)                                                                | **No**                                                                                                                 |
| DML (UPDATE/DELETE/MERGE) | **Supported** and transactional                                                                 | Generally **not supported** (append-only; some formats allow inserts but not ACID)                                     |
| Time Travel               | **Yes** (`VERSION AS OF` / `TIMESTAMP AS OF`)                                                   | **No**                                                                                                                 |
| Change Data Feed (CDC)    | **Yes** (`TBLPROPERTIES (delta.enableChangeDataFeed=true)`)                                     | **No**                                                                                                                 |
| Constraints               | **NOT NULL**, **CHECK**, generated columns enforced                                             | Limited/none; schema is “best-effort” on read; no constraint enforcement                                               |
| Schema enforcement        | **Strict** (types enforced on write)                                                            | **Loose** (CSV/JSON inferred; Parquet typed but not enforced at write)                                                 |
| Schema evolution          | **Yes** (`mergeSchema`, `ALTER TABLE … ADD COLUMN`)                                             | **Manual/limited**; may require redefining table/refreshing metadata                                                   |
| Performance features      | **OPTIMIZE** (compaction), **Z-ORDER**/data skipping, stats                                     | None of the Delta optimizations                                                                                        |
| Small-files handling      | Auto Optimize / OPTIMIZE                                                                        | None; you manage files yourself                                                                                        |
| VACUUM (file retention)   | **Yes**                                                                                         | **No**                                                                                                                 |
| Cloning                   | **Shallow/Deep clone**                                                                          | **No**                                                                                                                 |
| Streaming semantics       | Exactly-once supported as a sink                                                                | At-least-once behaviors; no transactional guarantees                                                                   |
| Concurrency & reliability | **High** (conflict detection via log)                                                           | Risk of **corruption** with concurrent writers                                                                         |
| Partition management      | Delta manages partition metadata                                                                | Hive-style partition discovery; may need `MSCK REPAIR TABLE`                                                           |
| Refresh behavior          | New commits are visible via the Delta log; Spark caches can be invalidated with `REFRESH TABLE` | Engine lists files each query; **partitions** often need `MSCK REPAIR TABLE`; cached metadata may need `REFRESH TABLE` |
| Governance (UC)           | Best integration (lineage, constraints, privileges)                                             | Basic table object; several advanced features unavailable                                                              |
| Typical use               | Gold/Silver tables, BI, reliable pipelines                                                      | Quick reads over raw files, ad-hoc exploration                                                                         |

##### Trade-offs vs Delta

* No ACID transactions, time travel, `MERGE`, `OPTIMIZE`, `ZORDER`, schema evolution, or generated columns.
* Governance/features in UC (lineage, constraints, etc.) are more limited.
* Good for **read-only** or **interop** with systems expecting raw files; use Delta for anything you update, merge, or serve to BI.

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
      .option("header", True)        # for CSV
      .option("multiLine", True)     # for JSON with newlines
      .json("abfss://data@acct.dfs.core.windows.net/raw/events/*.json"))

df.select("id","name","ts").where("ts >= '2025-10-01'").show()
```

> **Exam tips:** Querying files by path is **schema-on-read** (no ACID). Use it for exploration and quick filters. For governance/ACID/time travel, load into **Delta tables**.

---

#### 2.3 Writing to Tables (Hands-On)

**A) SQL CTAS → managed Delta table (snapshot copy)**

```sql
CREATE TABLE main.analytics.events_delta
USING DELTA
AS
SELECT id, name, ts
FROM parquet.`abfss://data@acct.dfs.core.windows.net/raw/events/*.parquet`;
```

**B) SQL INSERT INTO an existing Delta table**

```sql
-- Table must exist (managed or external Delta)
INSERT INTO main.analytics.events_delta (id, name, ts)
SELECT id, name, ts
FROM json.`abfss://data@acct.dfs.core.windows.net/raw/events/2025/10/*.json`;
```

**C) PySpark DataFrameWriter → save as Delta table**

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

**D) Create an *external* Delta table (control the path)**

```sql
CREATE TABLE main.analytics.events_ext
USING DELTA
LOCATION 'abfss://data@acct.dfs.core.windows.net/curated/events_delta/';

-- then load data into it
INSERT INTO main.analytics.events_ext
SELECT * FROM main.analytics.events_delta;
```

> **Exam tips:**
>
> * CTAS without `LOCATION` → **managed Delta** (data copied to managed storage).
> * `USING DELTA LOCATION '...'` → **external Delta** (you control the path).
> * Use `mergeSchema`, `partitionBy`, `OPTIMIZE`, `VACUUM` with **Delta**—not available for raw CSV/JSON/Parquet tables.



##### `from_json` — Parse JSON strings into structs/arrays

**When useful:** ingesting logs/APIs that land as raw JSON strings; making nested fields queryable & typed.

**Input (table):**

| id | payload                        |
| -- | ------------------------------ |
| 1  | `{"k":1,"tags":["a","b","a"]}` |
| 2  | `{"k":2,"tags":["b","c"]}`     |

**SQL**

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

**Output (selected columns):**

| id | k | tags            |
| -- | - | --------------- |
| 1  | 1 | `["a","b","a"]` |
| 2  | 2 | `["b","c"]`     |

---

##### `collect_set` — Aggregate unique values per group

**When useful:** build de-duplicated tag lists, feature sets, or distinct device types per user/session.

**Input (events):**

| user_id | tag |
| ------- | --- |
| 1       | a   |
| 1       | b   |
| 1       | a   |
| 2       | b   |

**SQL**

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

**Output:**

| user_id | unique_tags |
| ------- | ----------- |
| 1       | `["a","b"]` |
| 2       | `["b"]`     |

> Tip: `collect_list` keeps duplicates; `collect_set` removes them. Array order is not guaranteed.

---

##### `array_distinct` — Remove duplicates inside a single array

**When useful:** clean up arrays after merges/joins; normalize tags/ids.

**Input:**

| id | tags            |
| -- | --------------- |
| 1  | `["a","b","a"]` |

**SQL**

```sql
SELECT id, array_distinct(tags) AS tags_dedup
FROM (SELECT 1 AS id, array('a','b','a') AS tags);
```

**Output:**

| id | tags_dedup  |
| -- | ----------- |
| 1  | `["a","b"]` |

---

##### `flatten` — Collapse array<array<T>> → array<T>

**When useful:** you grouped arrays (e.g., `collect_list(tags)`) and need one flat list.

**Input (per event):**

| user_id | tags        |
| ------- | ----------- |
| 1       | `["a","b"]` |
| 1       | `["b","c"]` |

**SQL (unique tags per user):**

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

**Output:**

| user_id | unique_tags     |
| ------- | --------------- |
| 1       | `["a","b","c"]` |

---

##### `explode` — Turn array elements into multiple rows

**When useful:** normalize arrays to rows for joins, counts, deduping, or downstream modeling.

**Input:**

| id | tags            |
| -- | --------------- |
| 10 | `["a","b","a"]` |

**SQL**

```sql
WITH t AS (SELECT 10 AS id, array('a','b','a') AS tags)
SELECT id, explode(tags) AS tag
FROM t;
```

**Output:**

| id | tag |
| -- | --- |
| 10 | a   |
| 10 | b   |
| 10 | a   |

> Variants: `posexplode` (keeps index), `explode_outer` (keeps rows when array is null).

---

**Summary Table**

| Function         | Purpose                                 | Typical Input → Output                                       | Common Pattern                                     | Gotchas                                                       |
| ---------------- | --------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------- |
| `from_json`      | Parse JSON string to typed struct/array | `"{"k":1,"tags":["a","b"]}"` → `STRUCT{k:1, tags:["a","b"]}` | `from_json(col, 'STRUCT<...>')` then select fields | Must provide schema (string literal) or use `schema_of_json`. |
| `collect_set`    | Aggregate **unique** values per group   | rows `(user_id, tag)` → `(user_id, ["a","b"])`               | `GROUP BY user_id` + `collect_set(tag)`            | Order not guaranteed; arrays can grow large.                  |
| `array_distinct` | Remove duplicates inside array          | `["a","b","a"]` → `["a","b"]`                                | `array_distinct(tags)`                             | Only de-dupes, doesn’t sort.                                  |
| `flatten`        | Collapse nested arrays                  | `[ ["a","b"], ["b","c"] ]` → `["a","b","c"]`                 | `array_distinct(flatten(collect_list(tags)))`      | Works on `array<array<T>>` only.                              |
| `explode`        | Array → multiple rows                   | `["a","b","a"]` → 3 rows                                     | `SELECT explode(tags) AS tag`                      | Duplicates rows; consider `distinct` afterwards.              |

> **Exam-friendly combo:**
> Unique tags per user from per-event arrays → `array_distinct(flatten(collect_list(tags)))`.
> Parse JSON log lines → `from_json` → `explode` nested arrays → aggregate with `collect_set`.


#### 2.5 Higher Order Functions and SQL UDFs (Hands On)


> Focused on **array higher-order functions** and **SQL UDFs** you’ll see on the Associate exam.

---

##### `filter` — Keep only elements that match a predicate

**When useful:** clean arrays (drop nulls, keep evens/tags with a prefix), pre-normalize before `explode`.

**Input**

| id | nums              |
| -: | ----------------- |
|  1 | `[1,2,3,4]`       |
|  2 | `[10,11,null,12]` |

**SQL**

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

**Output**

| id | even_nums |
| -: | --------- |
|  1 | `[2,4]`   |
|  2 | `[10,12]` |

---

##### `size` — Count elements in arrays / entries in maps

**When useful:** quick array length, QA checks after `filter`/`array_distinct`.

**Input**

| id | tags            |
| -: | --------------- |
|  1 | `["a","b","a"]` |
|  2 | `[]`            |

**SQL**

```sql
WITH t AS (
  SELECT * FROM VALUES
    (1, array('a','b','a')),
    (2, array())
  AS t(id, tags)
)
SELECT id, size(tags) AS tag_count FROM t;
```

**Output**

| id | tag_count |
| -: | --------- |
|  1 | 3         |
|  2 | 0         |

---

##### `transform` — Map each array element to a new value

**When useful:** normalize strings, compute scores, safe math with `CASE` inside the lambda.

**Input**

| id | tags                |
| -: | ------------------- |
|  1 | `[" A ","b "," C"]` |

**SQL**

```sql
WITH t AS (
  SELECT 1 AS id, array(' A ','b ',' C') AS tags
)
SELECT
  id,
  transform(tags, x -> lower(trim(x))) AS tags_norm
FROM t;
```

**Output**

| id | tags_norm       |
| -: | --------------- |
|  1 | `["a","b","c"]` |

> Combo pattern: `array_distinct(transform(...))` to **normalize + dedupe**.

---

#### SQL UDF — Reusable logic as a function (pure SQL)

**When useful:** avoid repeating expressions, standardize business rules in SQL.

**Create a scalar SQL UDF (Unity Catalog schema recommended):**

```sql
-- In UC: create it inside a catalog & schema you own
CREATE OR REPLACE FUNCTION main.analytics.normalize_tag(s STRING)
RETURNS STRING
RETURN lower(trim(s));
```

**Use it (alone and inside `transform`):**

```sql
WITH t AS (SELECT 1 AS id, array('  Foo','BAR  ','  bar') AS tags)
SELECT
  id,
  transform(tags, x -> normalize_tag(x))                             AS tags_norm,
  array_distinct(transform(tags, x -> normalize_tag(x)))             AS tags_norm_unique
FROM t;
```

**Output**

| id | tags_norm             | tags_norm_unique |
| -: | --------------------- | ---------------- |
|  1 | `["foo","bar","bar"]` | `["foo","bar"]`  |

> Note: Databricks also supports **Python SQL UDFs** (`LANGUAGE PYTHON`) in UC, but for the Associate level a **pure SQL UDF** like above is enough.

---

##### Summary Table

| Feature                     | Purpose                   | Typical Input → Output             | Common Pattern                             | Gotchas                                                       |
| --------------------------- | ------------------------- | ---------------------------------- | ------------------------------------------ | ------------------------------------------------------------- |
| `filter(arr, x -> pred)`    | Keep only wanted elements | `[1,2,3,4]` → `[2,4]`              | `filter(arr, x -> x IS NOT NULL AND cond)` | Use `IS NOT NULL` inside predicate to drop nulls.             |
| `size(arr/map)`             | Count items               | `["a","b","a"]` → `3`              | `size(arr)`                                | For maps: counts key/value pairs.                             |
| `transform(arr, x -> expr)` | Element-wise transform    | `[" A ","b "]` → `["a","b"]`       | `transform(arr, x -> lower(trim(x)))`      | Combine with `array_distinct` to dedupe.                      |
| **SQL UDF**                 | Reusable SQL expression   | `normalize_tag(' Foo ')` → `'foo'` | `CREATE FUNCTION … RETURN <expr>`          | Define in UC schema; mind permissions and name qualification. |

> Exam tip: Higher-order functions (`filter`, `transform`, etc.) **never leave arrays** unless you later `explode`. Chain them to clean data before `explode` and downstream joins.

---

### 3. Incremental Data Processing
**Data Stream**
- Any data source that grows over time.
- New Fileslanding in cloud storage.
- Updates to a database captured in a CDC feed.
- Events queued in a pub/sub messaging feed.
**Processing Data Stream**
  1) Reprocess the entire source dataset each time.
  2) Only process those new data added since last update
     - Structured Streaming
**Unsupported Operations**
  1) Sorting  
  2) Deduplication
**Advanced methods**
  1)  Windowing.  
  2)  Watermarking.
 
#### 3.1 Structured Streaming

#### 3.0 Bronze Ingestion

##### Bronze ingestion on Databricks — first things first

**Goal of Bronze:** land **raw, append-only** data in Delta with minimal transforms (schema enforcement, optional dedup).
There are **two fundamental modes** to load Bronze—**Batch** and **Streaming**—plus **DLT** to manage either.

---

##### Quick decision (what to pick)

| Source                    | Low frequency / backfills -->BATCH      | Continuous / low-latency  -->  STREAMING                       |
| ------------------------- | --------------------------------------- | -------------------------------------------------------------- |
| Files in cloud storage    | **`COPY INTO`** or batch **`df.write`** | **Auto Loader** (`readStream cloudFiles` → `writeStream`)      |
| Database tables           | Batch **JDBC** extract → Delta          | CDC landed to files/Delta → **`readStream` + MERGE** / **CDF** |
| Event streams (Kafka, EH) | —                                       | **`readStream.format("kafka")` → Delta**                       |
| Prefer managed pipeline   | **DLT batch**                           | **DLT streaming** (`APPLY CHANGES`, expectations)              |

---

##### 1) Batch loading (on-demand or scheduled)

**When useful:** simple daily/hourly jobs, backfills, first loads.

**a) `COPY INTO` (idempotent file loads)**

```sql
COPY INTO main.bronze.events_raw
FROM 'dbfs:/mnt/landing/events/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('inferSchema'='true')
COPY_OPTIONS ('mergeSchema'='true');  -- loads only new files
```

**b) JDBC → Delta (tables in RDBMS)**

```python
df = (spark.read.format("jdbc")
  .option("url", "jdbc:postgresql://host/db")
  .option("dbtable", "public.orders")
  .option("user", "<user>").option("password", "<pwd>")
  .load())

(df.write.format("delta").mode("append")
  .saveAsTable("main.bronze.orders_raw"))
```

**c) Batch “catch-up” using streaming once**

```python
(spark.readStream.table("main.bronze.events_raw")
 .writeStream.format("delta")
 .trigger(availableNow=True)  # process all available data, then stop
 .option("checkpointLocation", "dbfs:/mnt/_chk/bronze/reload")
 .toTable("main.bronze.events_full"))
```

---

##### 2) Streaming loading (continuous)

**When useful:** new files/events arrive constantly; you want near-real-time tables.

**a) Auto Loader (files → only-new)**

```python
raw = (spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("dbfs:/mnt/bronze/raw/events/"))

(raw.writeStream.format("delta")
  .option("checkpointLocation","dbfs:/mnt/_chk/bronze/events")
  .toTable("main.bronze.events_raw"))
```

**b) Kafka/Event Hubs → Delta**

```python
from pyspark.sql.functions import from_json, col
schema = "user_id STRING, ts TIMESTAMP, url STRING"

src = (spark.readStream.format("kafka")
  .option("kafka.bootstrap.servers","broker:9092")
  .option("subscribe","pageviews").load())

parsed = (src.selectExpr("CAST(value AS STRING) AS json")
  .select(from_json("json", schema).alias("r")).select("r.*"))

(parsed.writeStream.format("delta")
  .option("checkpointLocation","dbfs:/mnt/_chk/bronze/pageviews")
  .toTable("main.bronze.pageviews"))
```

**c) Delta CDF (row-level changes as a stream)**

```python
changes = (spark.readStream.format("delta")
  .option("readChangeFeed","true")
  .option("startingVersion","0")
  .table("main.staging.customers_cdc"))

(changes.writeStream.format("delta")
  .option("checkpointLocation","dbfs:/mnt/_chk/bronze/customers_cdf")
  .toTable("main.bronze.customers_cdf"))
```

---

#####  Delta Live Tables (DLT) — managed batch or streaming

**When useful:** governance, data quality, retries, lineage, CDC (`APPLY CHANGES`).

```sql
CREATE STREAMING LIVE TABLE bronze_events
AS SELECT * FROM cloud_files("dbfs:/mnt/bronze/raw/events","json",
  map("cloudFiles.inferColumnTypes","true"));
```

---

##### Choosing wisely (rules of thumb)

* **Files & simplicity:** `COPY INTO` (batch). Need continuous? **Auto Loader**.
* **Databases:** small → **JDBC batch**; CDC → land changes, then **stream with MERGE/CDF**.
* **Events:** always **streaming** (Kafka/Event Hubs).
* **Operational rigor:** prefer **DLT** (same code style, managed infra).

**Bronze best practices:** append-only, unique **checkpoint per stream**, enforce schema, avoid tiny files (Auto Loader helps), and keep transformations minimal (push heavy logic to Silver).

##### 3.1 `readStream` & `writeStream` — the core of Structured Streaming on Databricks


* `readStream` creates a **streaming DataFrame** that *incrementally* reads from a growing source (files, Kafka, Delta table).
* `writeStream` defines a **streaming sink** that continuously writes results to Delta, memory, console, etc., using a **checkpoint** for exactly-once semantics.

> They do **not** “auto-sync Table A → Table B” by themselves. You build the logic (append, upsert, aggregates), run it as a job, and the job keeps B updated while it’s running.

---

##### `readStream` — read new data as it arrives

**When useful:** consuming new files from cloud storage, Kafka events, or appends/changes from a Delta table.

```python
# Files (Auto Loader → only new files)
src = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("dbfs:/mnt/bronze/raw/events/"))

# OR: Delta table as a stream (append-only changes)
src_delta = spark.readStream.table("main.bronze.events_raw")
```

**Notes**

* `readStream` is **declarative**—no checkpoint here; it becomes stateful when you `writeStream`.
* For Delta with updates/deletes, pair with **CDF** (`option("readChangeFeed","true")`) to get row-level changes.

  #### `readStream` — what it is, how it relates to Auto Loader, and where the data “lives”

**When useful:** continuously read only-new data from files (Auto Loader), Kafka/Event Hubs, or Delta/CDF to build Bronze → Silver pipelines.

---


##### 3) Where does the data live? Does the DF “grow” over time?

* `readStream` returns a **streaming DataFrame** = a **lazy logical plan** plus source offsets, not a materialized dataset.
* Nothing is stored permanently by `readStream` itself. Data is processed **micro-batch by micro-batch** only when you attach a **`writeStream`**.
* The **DataFrame object does not accumulate rows**. Each micro-batch:

  * reads the next slice (new files/offsets),
  * processes it on executors (RAM + spill if needed),
  * **writes to your sink** (typically a Delta table),
  * then frees executor memory.
* What **persists** is:
  * **Sink**: your **Delta table** (e.g., `main.bronze.events_raw`) grows over time.
  * **Checkpoint** (set on `writeStream`): progress/state for exactly-once (`dbfs:/…/_chk/...`).
  * **Auto Loader schema/file log**: at `cloudFiles.schemaLocation` (tracks seen files + schema evolution).

```
dbfs:/mnt/_chk/bronze/events/         ← writeStream checkpoint (progress/state)
dbfs:/mnt/_schemas/bronze/events/     ← Auto Loader schema & file discovery log
```

> Only **stateful** ops (aggregations, dedup, sessions) keep **state** between micro-batches; that state is **sharded on disk under the checkpoint**, not kept unbounded in RAM. Use **`withWatermark`** to bound it.

---

```python
# 1) Source: streaming DF (Auto Loader)
src = (spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("dbfs:/mnt/bronze/raw/events/"))

# 2) Sink: persist increments to Delta with exactly-once semantics
(src.writeStream
  .format("delta")
  .option("checkpointLocation", "dbfs:/mnt/_chk/bronze/events")
  .toTable("main.bronze.events_raw"))
```

---

##### Quick tips / gotchas

* **No global cache/collect** on streaming DFs; persist to Delta, then query in batch/SQL.
* **One unique checkpoint per sink**; don’t reuse paths.
* For CDC/row updates: use **Delta CDF** with `option("readChangeFeed","true")` and upsert in the sink.
* Bound state with **watermarks** for dedup/windowed aggregates.


---

##### `writeStream` — continuously write results with exactly-once Delta

**When useful:** appending to Bronze, upserting to Silver, producing Gold aggregates, or feeding dashboards.

```python
# 1) Append-only copy (Table A -> Table B) — simple “sync” for inserts
(spark.readStream.table("main.bronze.events_raw")
  .writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation","dbfs:/mnt/_chk/silver/events_raw")
  .toTable("main.silver.events_raw"))
```

```python
# 2) Upsert (keep B in sync with A when keys update) — idempotent MERGE
src = spark.readStream.table("main.bronze.events_raw")

def upsert_to_b(microbatch_df, _):
    microbatch_df.createOrReplaceTempView("a")
    microbatch_df.sparkSession.sql("""
      MERGE INTO main.silver.events AS b
      USING (
        SELECT * FROM a                     -- add dedup/window logic if needed
      ) s
      ON b.id = s.id
      WHEN MATCHED THEN UPDATE SET *
      WHEN NOT MATCHED THEN INSERT *;
    """)

(src.writeStream
  .option("checkpointLocation","dbfs:/mnt/_chk/silver/events_merge")
  .foreachBatch(upsert_to_b)
  .start())
```

**Notes**

* **Checkpoint is required** (unique per sink) to achieve exactly-once with Delta.
* Choose an **output mode**: `append` (most common), `update`, or `complete` (aggregates).
* Control cadence with `trigger(availableNow=True)` (catch-up then stop) or fixed intervals.

---

##### `readStream` + Auto Loader to ADLS → Delta (Bronze): do they “sync” A → B?

**Short answer:** Auto Loader + `writeStream` keeps **Table B** (Delta) **incrementally up to date** with new files from **ADLS A**, but it’s **not a real-time mirror**. It runs in **micro-batches**, so B will always lag by **discovery + trigger interval + processing time**. You don’t *have* to set a trigger—without one it runs **as fast as possible**.

---

### How it works

* **Source (A = ADLS path):** `readStream.format("cloudFiles")` (Auto Loader) discovers **only-new** files and reads them once.
* **Sink (B = Delta table):** `writeStream` appends rows (or upserts if you implement `foreachBatch + MERGE`) and maintains a **checkpoint**.
* **Job lifecycle:** Your streaming job must be **running**. If it stops, ingestion pauses—no background sync.

---

### Triggers (cadence of micro-batches)

| Trigger                      | What it does                                         | When to use                |
| ---------------------------- | ---------------------------------------------------- | -------------------------- |
| *(default)*                  | Run micro-batches **back-to-back** (lowest latency). | Most pipelines.            |
| `processingTime='2 minutes'` | Run a batch **every 2 min**.                         | SLA pacing / cost control. |
| `availableNow=True`          | Process all backlog **then stop**.                   | Backfills / catch-ups.     |

```python
raw = (spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/_schemas/bronze/events")
  .load("abfss://landing@acct.dfs.core.windows.net/events/"))

(raw.writeStream
  .format("delta")
  # .trigger(processingTime="2 minutes")    # optional — default = as fast as possible
  # .trigger(availableNow=True)             # one-time catch-up
  .option("checkpointLocation","dbfs:/mnt/_chk/bronze/events")
  .toTable("main.bronze.events_raw"))
```

---

##### Latency levers (ADLS + Auto Loader)

* **Discovery:** enable notifications for ADLS (`cloudFiles.useNotifications = true`) to reduce listing delays.
* **Batch size:** `cloudFiles.maxFilesPerTrigger` / `minRowsPerTrigger` to control work per batch.
* **Processing:** Photon runtimes + simple transforms in Bronze; push heavy logic to Silver.

---

##### “Synchronized” caveats

* **Files only:** if a file in A is **overwritten**, Auto Loader won’t reload it by default (already marked processed).
* **Deletes/updates:** A isn’t a table—file deletions don’t auto-delete from B. Handle such semantics in **Silver** with CDC or rules.
* **Exactly-once:** guaranteed at the **sink** (B) thanks to Delta + checkpointing; still **eventual** w.r.t. A.

---

##### Quick tips

* Use **Auto Loader** for files; **Kafka** for events; **Delta CDF** for row-level changes.
* Add **watermarks + dropDuplicates** when deduplicating streams.
* Enable schema evolution for upserts:
  `spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled","true")`.

---

### 4. Production Pipelines
#### 4.1 Multi-hop Architecture
#### 4.2 Delta Live Tables (Hands On)
#### 4.3 Change Data Capture
#### 4.4 Processing CDC Feed with DLT (Hands On)
#### 4.5 Jobs (Hands On)

---

### 5. Data Governance & Security
#### 5.1 Databricks SQL
#### 5.2 Data Objects Privileges
#### 5.3 Managing Permissions (Hands On)
