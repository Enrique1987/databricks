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

# What you can do

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

# Trade-offs vs Delta

* No ACID transactions, time travel, `MERGE`, `OPTIMIZE`, `ZORDER`, schema evolution, or generated columns.
* Governance/features in UC (lineage, constraints, etc.) are more limited.
* Good for **read-only** or **interop** with systems expecting raw files; use Delta for anything you update, merge, or serve to BI.


#### 2.1 Querying Files
#### 2.2 Querying Files (Hands On)
#### 2.3 Writing to Tables (Hands On)
#### 2.4 Advanced Transformations (Hands On)
#### 2.5 Higher Order Functions and SQL UDFs (Hands On)

---

### 3. Incremental Data Processing
#### 3.1 Structured Streaming
#### 3.2 Structured Streaming (Hands On)
#### 3.3 Incremental Data Ingestion
#### 3.4 Auto Loader (Hands On)

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
