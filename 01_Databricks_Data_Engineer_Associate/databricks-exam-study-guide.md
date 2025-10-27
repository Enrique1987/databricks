# Databricks Certified Data Engineer Associate — Clickable Index (Introduction skipped)

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

#### 1.7 Set Up Delta Tables
#### 1.8 Views
#### 1.9 Working with Views (Hands On)

---

### 2. Data Processing & Transformations
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
