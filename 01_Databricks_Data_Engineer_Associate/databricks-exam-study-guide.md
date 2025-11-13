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

**Auto Loader Options**  


##### Auto Loader options — 80/20 table with one-sentence descriptions

| Option (where)                                  | Why you care                      | Typical value                       | One-sentence description                                                                                                                  |
| ----------------------------------------------- | --------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `cloudFiles.format` *(readStream)*              | File type                         | `json` | `csv` | `parquet`          | Chooses the source reader and performance profile (Parquet fastest; JSON/CSV often need schemas or inference).                            |
| `cloudFiles.schemaLocation` *(readStream)*      | Stores inferred schema & file log | `dbfs:/mnt/_schemas/<stream>`       | Directory where Auto Loader persists schema and discovery state so the stream can resume and evolve safely.                               |
| `includeExistingFiles` *(readStream)*           | Load backlog on first run         | `true` (default)                    | On the very first start, also ingests files that were already in the folder; ignored on later restarts unless you reset state.            |
| `pathGlobFilter` *(readStream)*                 | Keep only matching files          | e.g. `*.json`                       | Filters files by glob pattern before ingestion; pair with `cloudFiles.useStrictGlobber=true` for predictable matches.                     |
| `cloudFiles.useStrictGlobber` *(readStream)*    | Make globbing predictable         | `true` with `pathGlobFilter`        | Enforces strict Spark-style globbing so only paths that truly match your pattern are considered.                                          |
| `cloudFiles.inferColumnTypes` *(readStream)*    | Non-string types for JSON/CSV     | `true` (if no explicit schema)      | Upgrades JSON/CSV fields from STRING to concrete types (int, timestamp, etc.) at the cost of extra inference work.                        |
| `cloudFiles.schemaEvolutionMode` *(readStream)* | Handle new columns                | `rescue` (safe) or `addNewColumns`* | Choose **`rescue`** to dump unexpected fields into `_rescued_data`, or **`addNewColumns`** to automatically add new columns when allowed. |
| `rescuedDataColumn` *(readStream)*              | Capture unexpected fields         | `_rescued_data` (default)           | Name of the semi-structured column where unparsed or extra fields are stored for later auditing/repair.                                   |
| `cloudFiles.maxFilesPerTrigger` *(readStream)*  | Pace work per micro-batch         | Start `500–2000`                    | Caps the number of files per micro-batch to smooth throughput and control cost/latency.                                                   |
| `cloudFiles.maxBytesPerTrigger` *(readStream)*  | Cap data per batch                | e.g. `"2g"`                         | Limits total input bytes per micro-batch to prevent spikes from very large files.                                                         |
| `cloudFiles.useNotifications` *(readStream)*    | Lower-latency discovery at scale  | `true` when supported               | Uses cloud file events instead of directory listing for faster, more scalable new-file detection.                                         |
| `checkpointLocation` *(writeStream)*            | Exactly-once / progress           | `dbfs:/mnt/_chk/<stream>`           | Path where Structured Streaming stores offsets/state to guarantee exactly-once writes and reliable recovery.                              |

* `addNewColumns` is typically available when you haven’t provided a strict schema; with explicit schemas, prefer schema hints and evolve deliberately.

---

### 4. Production Pipelines

#### 4.2 Delta Live Tables


##### Delta Live Tables (DLT) — what it is

**What:** DLT is Databricks’ **managed pipeline framework** that lets you define tables **declaratively** (SQL/Python) and the service handles **ordering, checkpoints, retries, expectations (data quality), schema changes, lineage, and autoscaling**.

**Why useful (typical scenarios):**

* Continuous **files → Bronze** with Auto Loader (`cloud_files`) and quality checks.
* **CDC → Type 1/2** dimensions using `APPLY CHANGES INTO`.
* **Incremental aggregates** (streaming tables) and **batch materializations** (materialized views).
* **Operations built-in:** event log, system tables, SLA/alerts, one-click backfills.

**Tiny DLT SQL sketch**

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

---

### “Why can’t I just create them as normal tables?”

*(Is this about cost control, or is there a technical reason?)*

**Short answer:**

* The **physical objects** DLT creates **are normal Delta tables** (in your UC catalog/schema).
* What you **can’t** do outside a DLT pipeline is use the **`LIVE`/`STREAMING LIVE` syntax** and the managed semantics—because those are **compiled and orchestrated by the DLT service**, not by regular Spark SQL.

**Technical reasons (the real blockers):**

* **Different compiler/executor:** `CREATE [STREAMING] LIVE TABLE` and `APPLY CHANGES INTO` are **DLT directives**; only the DLT pipeline engine understands them, builds the DAG, wires checkpoints/state, and enforces expectations.
* **Managed lifecycle:** DLT owns **ordering, retries, backfills, schema tracking**, and writes an **event log/system tables**; ad-hoc `CREATE TABLE AS SELECT` can’t attach to that lifecycle.
* **State & quality coupling:** DLT ties **quality rules**, **expectations**, **SCD maintenance**, and **autoscaling** to each table; those guarantees require the pipeline runtime.
* **Reproducibility:** Pipeline configs (target catalog/schema, storage location, cluster policy) make tables **rebuildable** and auditable; ad-hoc creation breaks lineage & observability.

**Governance/cost angle (secondary, not the main reason):**

* Yes, DLT has its **own pricing/editions** on top of compute, so the platform naturally encourages using it when you need its guarantees—not for every one-off table.
* But the **restriction isn’t to prevent “forgotten tables”**; it’s because **DLT tables are a product of a pipeline**, not a standalone SQL statement.

**Practical takeaway:**

* You **query DLT outputs like any normal Delta table** (`SELECT * FROM catalog.schema.table`).
* To **create/maintain** them with DLT semantics, define them **inside a DLT pipeline**;
  if you instead `CREATE TABLE ... AS SELECT` in a notebook/job, you’ll just get a **regular Delta table** (no DLT expectations/event log/automanagement).

If you want, share your Bronze→Silver→Gold needs and we’ll map which ones merit DLT (managed) vs simple jobs (plain Delta).

##### `CREATE STREAMING LIVE TABLE bronze_events` vs `CREATE LIVE TABLE silver_events` (DLT)#
DLT support batching and streaming therefore one is for streaming `STREAMING LIVE TABLE` and the other declaration `CREATE LIVE TABLE` is for Batching.

**Quick idea:** use a **streaming live table** for *ingest/append* (Bronze) and a **live table** for *transform/serve* (Silver) unless you explicitly need streaming semantics in Silver.

| Aspect                | `CREATE STREAMING LIVE TABLE bronze_events`                                                                 | `CREATE LIVE TABLE silver_events`                                                                             | Notes                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Primary purpose       | **Streaming ingest** of new data (files/Kafka/CDC) into a Delta table.                                      | **Batch/materialized view** style transform over upstream tables.                                             | DLT manages orchestration, retries, expectations for both. ([docs.azure.cn][1])           |
| Execution model       | **Streaming**: processes only data added since last update; maintains offsets/state.                        | **Batch**: recomputes the result each update (or reads a streaming source explicitly).                        | Streaming tables are incremental by design. ([Stack Overflow][2])                         |
| Typical layer         | **Bronze** (raw append-only)                                                                                | **Silver** (cleansed, conformed)                                                                              | Common pattern in lakehouse pipelines.                                                    |
| Source functions      | Often `cloud_files(...)`, `read_files(...)`, or `STREAM(...)` from another dataset.                         | Usually reads `LIVE.bronze_*`; can opt into streaming read with `STREAM(LIVE.bronze_*)`.                      | Use `STREAM(...)` to get streaming semantics from a source. ([Microsoft Learn][3])        |
| State & checkpoints   | **Yes** (DLT handles streaming checkpoints/state under the hood).                                           | **No** by default; becomes streaming-only if you read via `STREAM(...)`.                                      | Streaming tables are stateful; batch tables are not. ([Stack Overflow][2])                |
| Latency               | **Low** latency (micro-batch); governed by pipeline schedule/trigger.                                       | **Update cadence** per pipeline run (typically higher latency).                                               | Both can be scheduled/triggered by the pipeline. ([docs.databricks.com][4])               |
| Allowed patterns      | Append ingest, windowing/watermarks, dedup, CDC into downstream.                                            | Cleansing, joins, enrichments; can do CDC via `APPLY CHANGES`/`AUTO CDC`.                                     | Use CDC APIs for SCD1/2 in Silver. ([Microsoft Learn][5])                                 |
| Reprocessing behavior | Processes **only new data** since the last successful version.                                              | By default **recomputes** result for the run from sources (not incremental) unless reading via `STREAM(...)`. | “Streaming live table” ≈ incremental; “live table” ≈ batch. ([Stack Overflow][2])         |
| Output mode           | Usually **append** (ingest facts).                                                                          | Often **overwrite/materialize** transform; or **upsert** when using CDC.                                      | Pick per business need.                                                                   |
| Consuming upstream    | Downstream tables refer to it as `LIVE.bronze_events` (or `STREAM(LIVE.bronze_events)` for streaming read). | Typically defined as `CREATE LIVE TABLE silver AS SELECT ... FROM LIVE.bronze ...`.                           | `LIVE` is a DLT namespace for dependencies. ([Stack Overflow][2])                         |
| Quality rules         | Supports **EXPECT** constraints (fail, drop, warn).                                                         | Same.                                                                                                         | Expectations apply to both. ([Databricks][6])                                             |
| When to choose        | You ingest **growing sources** and need **exactly-once** incremental processing.                            | You transform to **curated** tables and don’t require streaming semantics in the step.                        | Promote to streaming read in Silver only if it’s truly needed. ([docs.databricks.com][4]) |

**Tiny sketches**

```sql
-- Bronze (streaming ingest)
CREATE STREAMING LIVE TABLE bronze_events
AS SELECT * FROM cloud_files('dbfs:/mnt/landing/events','json',
  map('cloudFiles.inferColumnTypes','true'));
```

```sql
-- Silver (batch transform of Bronze)
CREATE LIVE TABLE silver_events
AS SELECT * FROM LIVE.bronze_events WHERE is_valid = true;
-- If you need streaming semantics here, read as:
-- SELECT ... FROM STREAM(LIVE.bronze_events)
```

Use **`STREAMING LIVE TABLE`** for incremental ingest; use **`LIVE TABLE`** for downstream transforms unless you explicitly need **`STREAM(...)`** semantics in Silver (for true end-to-end streaming). 

#### 4.3 Change Data Capture  

##### CDC on Databricks — concept vs features

**Short answer:**

* **CDC (Change Data Capture)** is a **design pattern** (a way of working): process only changed rows instead of full reloads.
* On **Databricks**, you implement CDC using **platform features/tools** like **Delta Lake MERGE**, **Delta Change Data Feed (CDF)**, **Auto Loader**, **Structured Streaming**, and **Delta Live Tables (DLT)**.  
* So: CDC is the *model*, while CDF/DLT/MERGE/etc. are the *technical knobs* you use to realize it.  
**CDC**: Insert, delete, update (that are the changes)   
---

##### What you “turn on” (technical pieces)

1. **Delta Change Data Feed (CDF)** — *publish row changes from a Delta table*
   Enable on a table to let downstream readers consume `insert / update_preimage / update_postimage / delete`.

```sql
ALTER TABLE main.sales.orders
SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true,
  delta.changeDataFeed.minRetentionDuration = '30 days'
);
```

Read changes:

```sql
SELECT *
FROM table_changes('main.sales.orders', 100, 120)
WHERE _change_type IN ('insert','update_postimage','delete');
```

2. **MERGE INTO** — *perform upserts/deletes on a target Delta table*
   You use `MERGE` to apply incoming changes (whether they came from files, Kafka, or CDF).

```sql
MERGE INTO main.silver.orders_current t
USING main.bronze.orders_cdc s        -- your change set
ON t.id = s.id
WHEN MATCHED AND s.op = 'delete' THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

3. **Auto Loader + Structured Streaming** — *ingest incremental files reliably*
   You don’t “turn on CDC” here; you **build a streaming job** that reads new files and applies `MERGE` in `foreachBatch`.

```python
stream = (spark.readStream
  .format("cloudFiles").option("cloudFiles.format","json")
  .load("dbfs:/mnt/bronze/orders_cdc"))

# foreachBatch → MERGE logic (Type 1)
```

4. **Delta Live Tables (DLT)** — *declarative CDC in pipelines*
   You declare CDC semantics; DLT does the heavy lifting.

```sql
APPLY CHANGES INTO LIVE.orders_current
FROM STREAM(LIVE.orders_cdc_raw)
  KEYS (id)
  SEQUENCE BY updated_at
  APPLY AS DELETE WHEN op = 'delete';
```

---

##### How to think about it

* **CDC (pattern)** answers: *What is a “change”? How do we sequence/dedupe? What is the target state (Type 1 vs SCD2)?*
* **Databricks features** answer: *How do we implement that pattern reliably and at scale?*

**When useful:**

* Source systems emit change logs (Debezium/Fivetran/Attunity) → you upsert into Delta.
* You want downstream tables to subscribe to **changes** of an upstream Delta table → enable **CDF**.
* You prefer **declarative pipelines** with retries, expectations, and lineage → use **DLT + APPLY CHANGES INTO**.

---

#### Quick mapping (pattern → tool)

| Need (pattern)                       | Databricks feature(s)                                 |
| ------------------------------------ | ----------------------------------------------------- |
| Upsert/delete into a “current” table | `MERGE INTO` (Photon), Z-Order by keys                |
| Publish/consume row-level changes    | **Delta CDF** (`table_changes`, `readChangeFeed`)     |
| Ingest new files continuously        | **Auto Loader** + Structured Streaming                |
| Declarative CDC pipeline             | **DLT `APPLY CHANGES INTO`**                          |
| Build SCD2 history (valid_from/to)   | MERGE two-step or DLT SCD2 pattern                    |
| Ordering, dedupe, idempotency        | Use sequence columns (`lsn/scn/ts`), `dropDuplicates` |

---

#### Gotchas / tips

* **CDC ≠ CDF**: CDC is the *concept*; **CDF** is a *Delta feature* that exposes changes.
* Always define a **sequence column** (e.g., `updated_at`, `lsn`) for correct ordering in `MERGE`/DLT.
* Set **CDF retention** long enough for your slowest consumer/backfill.
* For performance, run on **Photon** and **Z-Order** by join keys used in `MERGE`.

---

Szenario

#### Delta **Change Data Feed (CDF)** — “publish/subscribe” between Delta tables

 **CDF does not “auto-bind” tables.** CDF is a Publisher/Subscribes mode.

* A **source Delta table** (Table A) **publishes** row-level changes when CDF is enabled.
* One or more **consumer jobs** (SQL or PySpark, DLT, Jobs) **read those changes** and **apply** them to downstream Delta tables (Table B, C, …).
* So changes **flow when you run a pipeline** (MERGE/INSERT), not automatically.

---

**Mental model**
Between two tables A and B. <-->  
* **Publisher:** Table A with `delta.enableChangeDataFeed = true` keeps a change log (by commit version/timestamp).
* **Subscribers:** Your code reads `table_changes('A', …)` (SQL) or `.option("readChangeFeed","true")` (PySpark) and **MERGEs** into B.
* **You track progress** by remembering the **last applied version**; next run starts at `last_version + 1`.
* **Many subscribers** can consume the same CDF independently.

---

**Notes / gotchas**

* **Not push-based:** CDF is **pull/read**; you schedule the consumer.
* **Retention matters:** keep `delta.changeDataFeed.minRetentionDuration` long enough for your slowest consumer/backfill.
* **Use post-image for Type 1:** prefer `insert` + `update_postimage` + `delete`; use `update_preimage` only for diffs/audits.
* **Permissions (UC):** consumers need `SELECT` on the source **table** and its **catalog/schema**.
* **Schema drift:** if A adds columns, B must evolve (e.g., `ALTER TABLE … ADD COLUMN` or `MERGE` with compatible schema).
* **Ordering:** consume by **version** (or timestamp) to keep deterministic application.

CDF lets Table A *publish* changes; Table B receives them **when your job reads those changes and applies them**.

##### Szenario 2 CDF in a Bronze → Silver → Gold pipeline — practical scenarios (no code)

**Idea:** Use **CDF** wherever a **Delta table publishes changes** that downstream tables can **incrementally** apply. In medallion terms, the **publisher** is often **Silver**, sometimes **Bronze** (if it’s a Delta landing table), and **Gold** is usually a **subscriber**.

---

##### 1) Bronze → Silver fan-out (raw CDC landing → curated projections)

**Story:** You land raw CDC events (append-only) from multiple operational systems into **Bronze** Delta tables. You **enable CDF on Bronze** so different **Silver** pipelines can **subscribe** to the same raw changes and build purpose-specific curated tables (e.g., `orders_current`, `orders_history`, `customer_current`).
**Why CDF here:**

* Multiple consumers can **independently** pick up only new changes since their last version.
* Easy **replay/backfill** by version without re-reading all Bronze data.
* Keeps Bronze **append-only** while letting each Silver apply its own business rules.

---

##### 2) Silver → Gold incremental marts (fast aggregates)

**Story:** A **Silver “current”** table (clean keys, deduped, business types) publishes CDF. **Gold marts** (sales by day, active customers, inventory KPIs) subscribe and **incrementally update** aggregates instead of recomputing full history.
**Why CDF here:**

* **Low-latency** updates to KPIs/BI without full table scans.
* Deterministic **delete handling** (Gold can subtract prior contributions when a row is deleted/changed).
* Multiple **domain Golds** can evolve independently.

---

##### 3) Quality gates & quarantine (Bronze CDF powers selective promotion)

**Story:** Bronze holds raw data; a **Silver Quality** table promotes only records that **pass expectations** (valid schema, referential checks). Silver reads **Bronze CDF** and only applies **new/changed** rows; **failed records** are written to a separate quarantine table for triage.
**Why CDF here:**

* Clean separation of **raw vs curated** with incremental promotion.
* **Auditable trail** of what was promoted and when (via commit versions).
* Efficient **reprocessing** after fixing bad data (re-read specific versions).

---

##### 4) SCD2 dimensions + facts maintenance (Silver publishes, Gold consumes)

**Story:** Silver builds **Type 2 dimensions** (e.g., `dim_customer`) and **facts** (`fact_orders`). Both tables **publish CDF**. Gold data models (star schema for BI) **subscribe** to apply incremental **dimension upserts** and **fact adjustments** (including late-arriving corrections).
**Why CDF here:**

* Preserves **slowly changing** attributes with clear valid-from/valid-to transitions.
* **Late data** and **retractions** propagate downstream correctly.
* Gold refresh stays **incremental** even with complex joins.

---

##### 5) Near-real-time operational views & alerts (Silver → Gold/serving)

**Story:** Silver publishes CDF for **operational signals** (e.g., “order stuck > 30 min”, “inventory below threshold”). A lightweight Gold/serving table **subscribes** and updates **alerts dashboards** or triggers jobs.
**Why CDF here:**

* **Push-like** behavior via frequent pulls on change feed.
* Only changed rows trigger alert logic → **cheap & timely**.

---

##### 6) Multi-tenant / multi-region fan-out

**Story:** One central Silver table in a **governed catalog** publishes CDF. Several **regional Gold** layers subscribe and materialize only their region’s slice (e.g., EU, US, APAC) with regional transformations.
**Why CDF here:**

* **Decoupled** subscribers with independent SLAs.
* **Least-privilege** access: readers need only SELECT on the publisher and can track their own offsets.

---

##### 7) ML features & data contracts (Silver → Gold/feature tables)

**Story:** Silver publishes CDF for customer, product, and event streams. **Gold feature tables** (e.g., rolling 7-day spend, churn signals) subscribe and maintain **incremental aggregates** for training/serving.
**Why CDF here:**

* **Deterministic reproducibility** via commit versions.
* Avoids expensive full recompute of feature windows.

---

### How to place CDF in the medallion

* **Bronze as publisher** when: Bronze is **Delta**, append-only, and many downstream **Silver** consumers need independent incremental reads.
* **Silver as publisher** (most common): Silver has the **clean contract** and business rules; **Gold** subscribes to **incremental** changes.
* **Gold rarely publishes** unless other domains subscribe to curated outputs (e.g., centralized KPIs).

---

### Operational ideas (no code)

* Keep a tiny **offsets table** per subscriber (records the **last applied version**).
* Set **CDF retention** ≥ the **maximum subscriber lag** + backfill window.
* Document for each publisher: **keys**, **sequence/order columns**, **delete semantics**, and **expected SLA**.
* For performance, organize publishers for **pruning** (Z-Order by join keys) to speed incremental reads.
* For governance, expose CDF publishers via **Unity Catalog** and manage privileges at **catalog/schema/table** level.

---

#### 4.4 Processing CDC Feed with DLT 
CDC with DLT use code `Apply Changes Into`  
#### CDC with **Delta Live Tables — `APPLY CHANGES INTO` (80/20 Summary)**

| Category                     | **Pros (What you gain)**                                                                                                                                          | **Cons / Caveats (What to watch)**                                                           |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Simplicity & Reliability** | Declarative CDC — one SQL command handles inserts, updates, and deletes automatically with built-in retries, checkpoints, lineage, and data quality expectations. | Less control than manual `MERGE`; limited flexibility for complex custom logic (e.g., SCD2). |
| **Performance & Scale**      | Photon-optimized, incremental processing, and auto-optimized tables (compaction, Z-Order). Great for continuous pipelines.                                        | Heavy churn still costs compute — design proper keys and clustering.                         |
| **Schema & Governance**      | Handles schema drift (new columns), integrates tightly with Unity Catalog, gives automatic lineage and auditability.                                              | Column renames or type changes still require manual handling.                                |
| **Operational Simplicity**   | One managed pipeline replaces custom jobs — easier monitoring and error recovery via DLT UI.                                                                      | Bound to the DLT service — fewer knobs than raw Structured Streaming.                        |

✅ **Use it when:** You want fast, reliable **Type 1 CDC** (“latest state”) pipelines with minimal code and strong governance.
⚠️ **Avoid it when:** You need very custom logic (SCD2, cross-table merges) or fine-grained operational control.


#### 4.5 Databricks Asset Bundles.  
## Databricks Asset Bundles (DABs) — Dev → QA → Prod with YAML

**Goal:** keep one repo with your notebooks / code and declarative job definitions, then promote the *same commit* through **dev**, **qa**, and **prod** using targets in `databricks.yml` and CI/CD.

At a glance:

* One required root file: **`databricks.yml`** (+ optional included resource files). ([learn.microsoft.com][1])
* **Targets** model your environments and can run in **development** or **production** mode. ([docs.databricks.com][2])
* Deploy/Run with the **Databricks CLI**: `bundle validate | plan | deploy | run | destroy | deployment bind`. ([docs.databricks.com][3])

---

### 1) Repo layout (minimal, modular)

```
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

> DAB supports **splitting config**: put jobs/pipelines/etc. under `resources/*.yml` and include them from `databricks.yml`. ([learn.microsoft.com][1])

---

### 2) `databricks.yml` — targets & environment overrides

```yaml
# databricks.yml
bundle:
  name: my_project
  # Optional: pin CLI version so dev/CI match
  databricks_cli_version: '>= 0.218.0'  # example
  git:
    branch: main  # prod can validate you're on main
workspace:
  # Where files land in the workspace; keeps bundle identity stable
  root_path: /Shared/bundles/${bundle.name}/${bundle.target}

include:
  - resources/**/*.yml

# Common variables you override per target
variables:
  some variables

# Environments
targets:
  dev:
    some values as mode, workspace variables, presets..
  qa:
    some values, mode: production
  prod:
    some values mode: production

```

**Why this works**

* **Development mode** pauses schedules, allows concurrent job runs, and lets you override compute for fast iteration. **Production mode** adds safety checks (e.g., branch validation) and blocks ad-hoc compute overrides. ([docs.databricks.com][2])
* Setting `workspace.host` per target + a **stable `root_path`** gives a consistent bundle identity and prevents collisions across users/targets. (Identity ties to name/target and workspace; `root_path` is used to track state.) ([docs.databricks.com][3])
* Prefer `workspace.host` (match via your local/CI profile) instead of embedding a profile name inside YAML to keep configs portable. ([learn.microsoft.com][4])

> Secrets: don’t hardcode them in YAML. Use **variables** + `BUNDLE_VAR_*` env vars or CI secrets; define secret scopes as resources if needed. ([docs.databricks.com][5])

---

### 3) A small job (in `resources/jobs/etl_job.yml`)

```yaml
# resources/jobs/etl_job.yml
resources:
  jobs:
    etl_job:
  other values as task, schedule..
```

> See examples for serverless jobs, parameters, and schedules in the official DAB samples. ([docs.databricks.com][6])

---

### 4) Local workflow (developer loop)

```bash
# 1) Validate and preview what will change
databricks bundle validate -t dev
databricks bundle plan -t dev

# 2) Deploy to dev (development mode)
databricks bundle deploy -t dev

# 3) Run the job from the bundle
databricks bundle run etl_job -t dev -- --param1=foo

# 4) Promote the same commit to QA/Prod
databricks bundle deploy -t qa
databricks bundle deploy -t prod
```

> Command reference: `deploy`, `run`, `plan`, `validate`, `destroy`, and `deployment bind` (to adopt an existing workspace resource into your bundle). ([docs.databricks.com][3])

---

### 5) CI/CD (GitHub Actions example)

Use the official action to install the CLI, inject secrets (`DATABRICKS_HOST`, OAuth or PAT), then validate/deploy per target.

```yaml
# .github/workflows/deploy.yml
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

> The docs include end-to-end GitHub Actions examples for dev/prod bundle deployments and show how to wire secrets. ([docs.databricks.com][7])

---

### 6) Promotion model & keeping QA/Prod “in sync”

* **Promote the same commit/tag**: build/test in dev, then tag `vX.Y.Z` and deploy the **same commit** to QA, then Prod (with approval).
* **Production mode** validates branch and disallows ad-hoc compute overrides, which enforces repeatability. ([docs.databricks.com][2])
* Keep **environment deltas** in `targets.*` only (host, catalogs/schemas, cluster policy IDs, run identity). Everything else should be identical.
* If adopting an existing job/pipeline, **bind** it once so it’s managed by the bundle thereafter. ([docs.databricks.com][3])

---

### 7) Tips / gotchas

* **Only one `databricks.yml`** at the root; use `include:` for additional resource YAMLs. ([learn.microsoft.com][
* **Use `run_as`** with a **service principal** in prod; it separates deployer from runtime identity. ([learn.microsoft.com][4])
* **Variables & secrets:** use DAB **variables** and pass values from CI (`BUNDLE_VAR_*` envs), don’t inline secrets in YAML. ([docs.databricks.com][5])
* **Compute choices:** in **dev mode** you can point runs to a personal/all-purpose cluster (`--cluster-id`), but **prod mode** won’t accept compute overrides. ([docs.databricks.com][2])
* **Preview changes** with `bundle plan` before deploying; `bundle summary` gives deep links to deployed resources; `bundle destroy` cleans up. ([docs.databricks.com][3])

---

### 8) A tiny end-to-end test

```bash
# (Once per workspace) Login & create a profile
databricks auth login --host https://<dev-workspace>
# Validate & deploy to dev
databricks bundle validate -t dev
databricks bundle deploy   -t dev
# Run the job
databricks bundle run etl_job -t dev -- --param1=example
# Promote to QA (same commit)
databricks bundle deploy -t qa
```

> For first-time setup and profiles, see the DAB job tutorial & auth notes. ([docs.databricks.com][8])

---

Summarize

* **`databricks.yml`**: define `bundle`, `include`, `variables`, and **`targets: dev|qa|prod`** with `mode: development|production`, `workspace.host`, optional `presets`, and `run_as` for prod.  
* **`resources/jobs/*.yml`**: declarative job(s) with notebook/script tasks and schedules. ([docs.databricks.com][6])
* **CLI** (`validate/plan/deploy/run`) locally and from **CI** (GitHub Actions + `databricks/setup-cli`). ([docs.databricks.com][3])


---

#### 5. Data Governance & Security
##### 5.1 Databricks SQL
Self-explanatory, i´s SQL within the tables, you have. It fall under Data Governance beccause we can check oru data. Befor this solution existed, we had to create our talbe as a temp table and query it whin a notebook to check the results.  
##### 5.2 Data Objects Privileges  and Managing Permissions.  

##### Data object privileges (Unity Catalog) — Quick study notes

**When useful:** grounding yourself on what you can secure in Databricks, which privileges exist, who can grant them, and the minimal SQL you’ll actually run. 

---

##### 1) Governance model — what can be protected

| Object       | Scope you control                   |
| ------------ | ----------------------------------- |
| **CATALOG**  | Access to the entire catalog        |
| **SCHEMA**   | Access to a database (schema)       |
| **TABLE**    | Access to a managed/external table  |
| **VIEW**     | Access to a SQL view                |
| **FUNCTION** | Access to a named function          |
| **ANY FILE** | Access to the underlying filesystem |

> Privileges are granted with `GRANT <privilege> ON <object> TO <principal>`. 

---

##### 2) Privileges — what they allow

| Privilege          | Ability (summary)                                           |
| ------------------ | ----------------------------------------------------------- |
| **SELECT**         | Read rows                                                   |
| **MODIFY**         | Insert, update, delete data                                 |
| **CREATE**         | Create child objects                                        |
| **READ_METADATA**  | See object & metadata (e.g., list, describe)                |
| **USAGE**          | Required prerequisite to act on objects (no read by itself) |
| **ALL PRIVILEGES** | All applicable privileges on the object                     |

> Typical pattern: `USAGE` on catalog/schema + `SELECT`/`MODIFY` on table/view. 

---

### 3) Who can grant what (ownership rules)

| Granting role                  | Can grant over…                     |
| ------------------------------ | ----------------------------------- |
| **Databricks administrator**   | All catalog objects + underlying FS |
| **Catalog owner**              | All objects in the catalog          |
| **Database/Schema owner**      | All objects in the schema           |
| **Object owner (e.g., table)** | Only that specific object           |

> Grant authority follows **ownership** or admin privileges. 

---

##### 4) Access control operations

* **GRANT** — give privileges
* **DENY** — explicitly deny (when supported)
* **REVOKE** — remove previously granted privileges
* **SHOW GRANTS** — inspect active permissions


---

##### 5) Minimal examples (Databricks SQL)

```sql
-- Visibility: let a user reach the catalog and schema
GRANT USAGE ON CATALOG main TO `user_1@company.com`;
GRANT USAGE ON SCHEMA main.analytics TO `user_1@company.com`;

-- Read access to a table
GRANT SELECT ON TABLE main.analytics.my_table TO `user_1@company.com`;

-- Writers group: data modifications
GRANT MODIFY ON TABLE main.analytics.my_table TO `data_writers`;

-- Remove write access if needed
REVOKE MODIFY ON TABLE main.analytics.my_table FROM `data_writers`;

-- Quick audit
SHOW GRANTS ON TABLE main.analytics.my_table;
```

> `USAGE` alone doesn’t read data—pair it with `SELECT` (and with `MODIFY` for writes). 

---

##### 6) Notes / gotchas

* Keep object **owners** clear; owners (or admins) are the ones who can grant.
* Prefer granting to **groups** (e.g., `data_readers`, `data_writers`) instead of individuals.
* Use Unity Catalog names (`catalog.schema.table`) for unambiguous statements. 

---
Nice, you’re asking exactly the right “but why?” questions. Let’s make this really concrete.

---

## 1. Answer to your direct question

> **If I give `USE CATALOG` to User A, can that user see Catalog A but not the schemas?**

**Roughly: yes.**

With **only** `USE CATALOG` on a catalog:

* ✅ The user **can see that catalog** exists and can set it as current (`USE CATALOG my_catalog`). ([Azure-Dokumentation][1])
* ❌ The user **cannot do anything inside it**:

  * cannot access schemas or tables (needs `USE SCHEMA` and object privileges). ([Azure-Dokumentation][2])
  * cannot easily browse schemas/tables in Catalog Explorer unless they also have **`BROWSE`** on the catalog or schemas. ([Databricks Dokumentation][3])

So:

* `USE CATALOG` = “I’m allowed to work *somewhere* in this catalog if I also have more rights.”
* **It does *not* automatically mean** “I can see all schemas and tables.”

“See what exists” is more about **`BROWSE`**. ([Microsoft Learn][4])

---

## 2. Core Unity Catalog privileges (cheat sheet)

Let’s focus on the main ones you actually care about for catalogs/schemas/tables.

Assume we are in UC with:
`catalog = main`, `schema = analytics`, `table = sales`.

### 2.1 Privileges overview

| Privilege          | Applies to                    | What it allows (short)                                                                                                              | What it does **not** allow by itself                                                         |
| ------------------ | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **BROWSE**         | Catalog, schema, table        | See **metadata** in Catalog Explorer / search / lineage / `information_schema`. No data. ([Microsoft Learn][4])                     | Does **not** let you read rows or modify data.                                               |
| **USE CATALOG**    | Catalog                       | Be allowed to **access** a catalog and its data *if* you also have other privileges. ([Databricks Dokumentation][5])                | Does not give `SELECT` / `MODIFY`. Does not automatically show all schemas.                  |
| **USE SCHEMA**     | Schema                        | Be allowed to **access objects in a schema** when combined with object privileges. ([Databricks Dokumentation][5])                  | Does not read or write any table.                                                            |
| **SELECT**         | Table / view                  | Read rows from a table/view (queries). ([Databricks Dokumentation][6])                                                              | Needs `USE CATALOG` + `USE SCHEMA` on parents to actually work. ([Azure-Dokumentation][2])   |
| **MODIFY**         | Table (or via schema/catalog) | `INSERT`, `UPDATE`, `DELETE` rows; full DML on the table (requires `SELECT` + `USE*`). ([Microsoft Learn][7])                       | Doesn’t itself give read access if `SELECT` is missing.                                      |
| **CREATE TABLE**   | Schema (or catalog)           | Create tables/views in that schema (or in any schema in the catalog if granted at catalog level). ([Microsoft Learn][7])            | Needs `USE CATALOG` + `USE SCHEMA` too; doesn’t grant read or write to existing tables.      |
| **MANAGE**         | Any UC object                 | Manage **privileges on that object** (grant/revoke); manage some properties. ([Databricks Dokumentation][8])                        | You still need `USE CATALOG` + `USE SCHEMA` and it does not grant data read/write by itself. |
| **ALL PRIVILEGES** | Catalog/schema/table          | Shortcut meaning “all applicable privileges on this object” (e.g. SELECT+MODIFY+MANAGE on a table). ([Databricks Dokumentation][9]) | Still respects the hierarchy: you also need `USE CATALOG`/`USE SCHEMA` at parents.           |

Key rule from docs:

> For **any operation inside a catalog/schema**, you need **`USE CATALOG` and `USE SCHEMA`** on the parents *plus* the object privilege (e.g. `SELECT`, `MODIFY`, `MANAGE`). ([Azure-Dokumentation][2])

---

## 3. “User exercise” with different privilege sets

Let’s redo the exercise with **clear privilege combos** for each user on `main.analytics.sales`.

### 3.1 Users and grants

#### User A — *Metadata-only browser*

```sql
GRANT BROWSE ON CATALOG main TO user_a;
```

* ✅ Can see **that the catalog exists** in Catalog Explorer.
* ✅ Can see some metadata (depending how far you grant BROWSE down). ([Microsoft Learn][4])
* ❌ Cannot `USE CATALOG`, `USE SCHEMA`, or read rows.
* ❌ Cannot run `SELECT * FROM main.analytics.sales`.

---

#### User B — *Catalog gate only*

```sql
GRANT USE CATALOG ON CATALOG main TO user_b;
```

* ✅ Can **see and use** the catalog `main` (e.g. `USE CATALOG main`). ([Azure-Dokumentation][1])
* ❌ Cannot see schemas/tables nicely in UI unless they also have `BROWSE`.
* ❌ Cannot read or write any table (no `USE SCHEMA`, no `SELECT`/`MODIFY`).

Think of B as: “is allowed in the building, but has no floor/room access yet.”

---

#### User C — *Can reach schema, but no data rights*

```sql
GRANT USE CATALOG ON CATALOG main TO user_c;
GRANT USE SCHEMA  ON SCHEMA  main.analytics TO user_c;
```

* ✅ Can `USE CATALOG main; USE SCHEMA main.analytics;`
* ✅ Can **reference objects** inside `main.analytics` (name resolution works).
* ❌ Cannot run `SELECT` or write — there is no `SELECT`/`MODIFY`.
* ❌ May or may not see table names in Explorer depending on `BROWSE`.

C is “inside the correct floor”, but still has **no key to any room**.

---

#### User D — *Read-only on one table (this is the common pattern)*

```sql
GRANT USE CATALOG ON CATALOG main TO user_d;
GRANT USE SCHEMA  ON SCHEMA  main.analytics TO user_d;
GRANT SELECT      ON TABLE   main.analytics.sales TO user_d;
```

* ✅ Can **query**:

  ```sql
  SELECT * FROM main.analytics.sales;
  ```

* ✅ Cannot read any **other** table in `main.analytics` (no `SELECT` there).

* ❌ Cannot modify data (no `MODIFY`).

* ❌ Cannot change privileges (no `MANAGE`).

D is a **classic reader**: proper combination of `USE + SELECT`.

---

#### User E — *Full DML (read + write) on one table*

```sql
GRANT USE CATALOG ON CATALOG main TO user_e;
GRANT USE SCHEMA  ON SCHEMA  main.analytics TO user_e;
GRANT SELECT      ON TABLE   main.analytics.sales TO user_e;
GRANT MODIFY      ON TABLE   main.analytics.sales TO user_e;
```

* ✅ Can **read rows** (`SELECT`).
* ✅ Can **write**: `INSERT`, `UPDATE`, `DELETE`, `MERGE` target, `TRUNCATE` (depending on SQL). ([Microsoft Learn][7])
* ❌ Still cannot touch other tables, unless they have `SELECT`/`MODIFY` there.
* ❌ Cannot change privileges (no `MANAGE`).

E is a **writer** for that specific table.

---

#### User F — *Permission admin for one table*

```sql
GRANT USE CATALOG ON CATALOG main TO user_f;
GRANT USE SCHEMA  ON SCHEMA  main.analytics TO user_f;
GRANT MANAGE      ON TABLE   main.analytics.sales TO user_f;
```

* ✅ Can **grant/revoke privileges** on `main.analytics.sales` for other principals. ([Databricks Dokumentation][8])
* ❌ Doesn’t automatically have `SELECT` / `MODIFY` (unless also granted or owner).
* ❌ Cannot operate on other tables unless granted there too.

F is the **“ACL admin”** for that table.

---

##### 3.2 Summary table (who can do what in this exercise)

| User  | Privileges (on `main` / `main.analytics` / `sales`)           | Can they read rows? | Can they write rows? | Can they manage grants? | Can they see that catalog exists? |
| ----- | ------------------------------------------------------------- | ------------------- | -------------------- | ----------------------- | --------------------------------- |
| **A** | `BROWSE` on catalog                                           | ❌ No                | ❌ No                 | ❌ No                    | ✅ Yes (in Explorer)               |
| **B** | `USE CATALOG`                                                 | ❌ No                | ❌ No                 | ❌ No                    | ✅ Yes                             |
| **C** | `USE CATALOG` + `USE SCHEMA`                                  | ❌ No                | ❌ No                 | ❌ No                    | ✅ Yes                             |
| **D** | `USE CATALOG` + `USE SCHEMA` + `SELECT` on `sales`            | ✅ Yes (on `sales`)  | ❌ No                 | ❌ No                    | ✅ Yes                             |
| **E** | `USE CATALOG` + `USE SCHEMA` + `SELECT` + `MODIFY` on `sales` | ✅ Yes (on `sales`)  | ✅ Yes (on `sales`)   | ❌ No                    | ✅ Yes                             |
| **F** | `USE CATALOG` + `USE SCHEMA` + `MANAGE` on `sales`            | ❌ Not automatically | ❌ Not automatically  | ✅ Yes (on `sales`)      | ✅ Yes                             |

---

If you like this structure, we can turn it into a **Markdown cheat sheet** for your Git repo, and then add a section with ready-made `GRANT` / `REVOKE` scripts for roles like `data_readers`, `data_writers`, `data_stewards`.

#### Unity Catalog — PDF Summary (Study Notes)

> Source: “Unity Catalog” slide deck (Databricks Certified Data Engineer Associate prep). 

---

### 1. What is Unity Catalog?

* **Centralized governance solution** across *all* Databricks workspaces and clouds.
* Unifies governance for **data & AI assets**:

  * files, tables, ML models, dashboards.
* **SQL-based** access control: you manage permissions with `GRANT` / `REVOKE`. 

---

### 2. Architecture — Before vs With Unity Catalog

**Before UC (per-workspace Hive Metastore):**

* Each workspace had its own:

  * Hive Metastore
  * User/group management
  * Access controls
  * Compute resources

→ Governance is **isolated per workspace**. 

**With UC:**

* One or more **UC Metastores** at the account level.
* Central:

  * User / group management
  * Access controls
* Workspaces mainly provide **compute resources**, but share the same UC. 

---

### 3. 3-Level Namespace & Hierarchy

**3-level namespace:**

* Old style: `schema.table`
* UC style: `catalog.schema.table`

Example:

```sql
SELECT * FROM main.analytics.sales;
```

* `main`   = catalog
* `analytics` = schema (database)
* `sales` = table


**Hierarchy of securable objects:**

* **Metastore**

  * **Catalog**

    * **Schema (Database)**

      * **Table**
      * **View**
      * **Function**

Extended hierarchy also introduces:

* **Storage Credential**
* **External Location**
* **Share & Recipient** (for data sharing). 

---

### 4. Identities & Identity Federation

**Identities:**

* **Users** – identified by email (e.g., `user1@company.com`).
* **Service principals** – identified by application IDs (used for automation).
* **Groups** – can contain users and service principals, including **nested groups**. 

**Identity Federation:**

* Identities are managed at the **account** level.
* The same user identity (e.g., `user1@company.com`) is recognized **across multiple workspaces**. 

---

### 5. Privileges & Usage Privileges

**Main privileges (examples):**

* `CREATE`
* `SELECT`
* `MODIFY`
* `READ FILES`
* `WRITE FILES`
* `EXECUTE` 

**Usage-related privileges:**

* On **Catalog** → `USE CATALOG`
* On **Schema (database)** → `USE SCHEMA`
* On **Table** → `SELECT`

These form the **“usage path”**:

````text
Catalog (USE CATALOG) → Schema (USE SCHEMA) → Table (SELECT / MODIFY)
``` :contentReference[oaicite:9]{index=9}  

---

### 6. Security Model

**Principals (who):**

- Users  
- Service principals  
- Groups  

**Securable objects (what):**

- Metastore  
- Storage Credential  
- External Location  
- Catalog  
- Schema  
- Table / View / Function  
- Share / Recipient  

**Privileges (how):**

- `CREATE`, `SELECT`, `MODIFY`, `READ FILES`, `WRITE FILES`, `EXECUTE`, `USE CATALOG`, `USE SCHEMA`, …  

**Grant pattern:**

```sql
GRANT <privilege>
ON <securable_object>
TO <principal>;
````

Example idea (not in slides but matching the model):

````sql
GRANT SELECT ON TABLE main.analytics.sales TO data_readers;
``` :contentReference[oaicite:10]{index=10}  

---

### 7. Accessing Legacy Hive Metastore

- UC can coexist with the **legacy `hive_metastore`**.  
- Diagram shows:
  - `UC Metastore`
  - `hive_metastore` catalog with schemas like `dev`, `prod`.  
- Unity Catalog sits alongside the older metastore as another catalog. :contentReference[oaicite:11]{index=11}  

---

### 8. Key Features

- **Centralized governance** for data and AI.  
- **Built-in data search** and **audit logging**.  
- **Automated lineage** (track where data comes from and where it goes).  
- **No hard migration required** (you can adopt UC gradually). :contentReference[oaicite:12]{index=12}  

---

### 9. Account Console

To manage the account (metastores, identities, workspaces), you log in as an **account administrator** to the **account console**:

- AWS: `https://accounts.cloud.databricks.com`  
- Azure: `https://accounts.azuredatabricks.net/`  
- GCP: `https://accounts.gcp.databricks.com/` :contentReference[oaicite:13]{index=13}  

---

If you want, next step we can turn this into a **1-page exam cheat sheet** (with a small table: “Object → Securable? → Typical privileges”).
::contentReference[oaicite:14]{index=14}
````
Here you go — three short “GitHub note style” summaries in Markdown: **Delta Sharing**, **Lakehouse Federation**, and **Cluster Best Practices**.

---

#### `Delta Sharing` — Quick study notes

**When useful:** share **live Delta tables** with other organizations or platforms **without copying data**. 

**Core idea**

* **Open protocol** for **secure data sharing** of Delta tables.
* Provider exposes data via a **Delta Sharing server**; recipient can be **any platform** that speaks the protocol (Databricks or not). 

**How it works (under the hood)**

* Data provider has a **Delta table** stored in cloud storage (e.g. S3).
* Recipient sends a **read request** (e.g. for table `orders`) to the **Delta Sharing server**.
* Server returns a list of **short-lived pre-signed URLs** for underlying **Parquet files**.
* Recipient reads the Parquet files **directly from storage**, using the URLs. 

**On Databricks**

* You define a **share** and add tables to it, then grant recipients:

  ```sql
  CREATE SHARE bookstore;
  ALTER SHARE bookstore ADD TABLE orders;
  GRANT SELECT ON SHARE bookstore TO publisher1;
  ```
* Two flavors mentioned:

  * **Databricks-to-Databricks sharing** (across workspaces/accounts).
  * **Open protocol sharing** with **any computing platform**. 

**Costs & limitations**

* **No data replication** is required — data stays where it is.
* **Egress costs** apply when data crosses **regions or clouds** (within same region: usually no egress).
* To reduce egress:

  * Clone data to a **local region**, or
  * Use something like **Cloudflare R2** as edge storage.
* **Read-only model**: recipients cannot write back.
* **Format constraint**: only **Delta tables** are shareable. 

---

#### `Lakehouse Federation` — Quick study notes

**When useful:** avoid copying data into the lakehouse; instead **query external systems live** (for ad-hoc, POC, or low-volume lookup scenarios).

**Ingestion challenges (motivation)**

* Ingestion is usually recommended (especially for **high volume**, **low-latency analytics**, or **API limits**).
* But ingestion creates **duplicate data** that can become **stale**.
* Alternative: use **Delta Sharing** or **federation** to access live data.

**What Lakehouse Federation is**

* Ability to **run queries across multiple external data sources** (e.g. MySQL, other DBs) **without migrating the data**.
* Databricks exposes external sources under a **“foreign catalog”** and schemas, so you can query like:

  ```sql
  SELECT * FROM foreign_catalog.mysql_schema.table1;
  ```

**How it works (conceptually)**

* You **establish a connection** to external sources.
* Databricks acts as a **query federation platform**, pushing down reads to the external system where possible.

**Use cases**

* Maintain **live access** to external operational databases.
* **Ad-hoc reporting** or **proof-of-concept** analytics, without building full ingestion pipelines yet.

**Limitations**

* Complex queries may **not benefit from Databricks’ full engine power**, because execution depends heavily on the external system.

---

#### `Cluster Best Practices` — Quick study notes

**When useful:** choosing the right **compute type**, **instance family**, and **serverless vs classic** strategy for cost/perf on Databricks. 

**Compute types in Databricks**

* **Classic compute**

  * **All-purpose clusters**: interactive notebooks; manually or auto-terminated; **more expensive DBUs**.
  * **Job clusters**: created by the job scheduler; terminate when job finishes; **cheaper DBUs**. 
* **SQL Warehouses**

  * Optimized for SQL workloads (ETL, BI, exploration).
  * **Serverless SQL warehouses** when available; **Pro** when you need custom networking or serverless is not offered. 
* **Serverless compute** for notebooks, jobs, and pipelines:

  * Fully managed, **fast startup & scaling**, **latest runtime**, **Photon on by default**, supports **Python and SQL only**. 

**Instance family selection (very exam-relevant)**

* **Memory optimized**: heavy shuffle/spill, caching, ML workloads.
* **Compute optimized**: structured streaming, full scans with no reuse, `OPTIMIZE` and Z-ORDER commands.
* **Storage optimized**: to leverage **Delta caching**, ad-hoc/intermediate analytics, ML/DL with cached data.
* **GPU optimized**: ML/DL with very high memory and GPU needs.
* **General purpose**: default choice, and often used for **VACUUM**. 

**Cost tools**

* **Spot instances**: cheap but can be **preempted** when market price exceeds bid.
* **Pools**: keep a set of **warm instances** to **reduce startup & autoscaling time**, but cloud charges still apply. 

**Serverless vs classic — key differences**

* **Serverless**

  * No config, automatic instance selection & scaling, very fast startup, Photon on, only Python/SQL.
* **Classic**

  * Full control (instance type, networking), Photon optional, manual runtime upgrades and autoscaling config, supports Python/SQL/Scala/R/Java. 

If you’d like, next step I can turn these three into a **single exam cheat-sheet page** (one table per topic + 3–4 MCQ-style practice questions).

