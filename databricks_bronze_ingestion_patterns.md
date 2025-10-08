# 🪶 Bronze Ingestion Patterns in Databricks

## Overview

This document summarizes the **main ingestion patterns** used for the Bronze layer within the Databricks Lakehouse ecosystem.  
Each pattern is fully contained inside Databricks — no Kafka, no external orchestration tools — and emphasizes **idempotency**, **simplicity**, and **maintainability**.

---

## 📁 File Sources (CSV / JSON / Parquet on ADLS / S3 / GCS)

### 1️⃣ COPY INTO (Idempotent Batch)

**Use case:**  
Vendor drops one small file per day under `USE_CASE/YYYY/MM/DD/`.

**Databricks solution:**  
Unity Catalog *external location* → `COPY INTO` a Bronze Delta table (append).  
Schedule with Workflows once per day. Enable schema evolution if needed.

**Why this fits:**  
`COPY INTO` remembers which files it loaded and will only ingest new ones.  
Simple, low-ops, and perfectly idempotent.

---

### 2️⃣ Auto Loader (cloudFiles) — Scheduled Micro-Batch

**Use case:**  
Team drops many files per day; late files arrive days later; schema might add columns.

**Databricks solution:**  
Auto Loader from the base folder → Bronze Delta (append).  
Run on a schedule using `Trigger.AvailableNow` (batch semantics).  
Manage schema with evolution + rescued data column.

**Why this fits:**  
Checkpointed, scalable discovery; automatic catch-up after pauses; safe with schema drift.

---

### 3️⃣ Periodic Full Snapshot to Files (Append)

**Use case:**  
Data warehouse exports a fresh monthly snapshot (hundreds of GB / billions of rows) to ADLS in many Parquet files.

**Databricks solution:**  
Land under `year=/month=` partitions.  
Ingest with Auto Loader (if many files/long arrival window) or `COPY INTO` (if file count is modest).  
Bronze remains append-only; do diffs/dedup in Silver.

**Why this fits:**  
Keeps Bronze simple and fast; avoids heavy JDBC pulls.

---

## 🗄️ RDBMS / DWH Sources (via JDBC — Inside Databricks)

### 4️⃣ Incremental (Watermark / last_modified)

**Use case:**  
ERP table with `last_modified_ts`; you only need new or updated rows each run.

**Databricks solution:**  
Spark JDBC read with a `WHERE last_modified_ts > watermark`.  
Store the watermark in a tiny Delta *state table*.  
Append to Bronze; merge/dedupe in Silver using global helpers.  
Schedule with Workflows.

**Why this fits:**  
Efficient on the source and predictable. No external tools required.

---

### 5️⃣ Native CDC Table over JDBC (Database-Provided CDC)

**Use case:**  
Source DB exposes CDC tables (insert/update/delete rows) you can query.

**Databricks solution:**  
Spark JDBC read the CDC table for the time/window since the last run.  
Land the raw CDC events (I/U/D) into a Bronze `_cdc` Delta table.  
In Silver, consolidate to current state with `MERGE` (SCD2 if needed).

**Why this fits:**  
True change history without extra infrastructure; still just JDBC + Delta.

---

### 6️⃣ Synthetic CDC via Monthly Snapshots (No CDC Available)

**Use case:**  
Big table, no watermark/CDC available; you get a full extract each month only.

**Databricks solution:**  
Pull current month via partitioned JDBC (split by ID/date ranges) → Bronze append.  
In Silver, compute delta vs. last month using joins or hash-diff, then `MERGE` to maintain history.

**Why this fits:**  
Works with any RDBMS.  
Heavier compute in Databricks, but zero extra systems.

---

## 🧱 Upstream Delta (Already in the Lakehouse)

### 7️⃣ Delta → Delta Using CDF (Change Data Feed)

**Use case:**  
Another team publishes a Delta table and enables CDF; you want only changes.

**Databricks solution:**  
Read with `readChangeFeed` from the starting version/timestamp.  
Land to Bronze (append). Use DLT or Workflows to orchestrate and promote to Silver.

**Why this fits:**  
Clean, versioned increments — fully inside Databricks.

---

### 8️⃣ Delta Sharing (Zero-Copy)

**Use case:**  
External provider shares a dataset to your workspace (no files/JDBC).

**Databricks solution:**  
Consume the shared table directly in Unity Catalog.  
Treat it as your upstream Bronze and pipeline it to Silver with DLT/Workflows.

**Why this fits:**  
Simplest path when sharing is available; governance built-in.

---

## 🌐 APIs (No External Ingestion Tool)

### 9️⃣ API Micro-Batch (REST / SaaS)

**Use case:**  
SaaS app exposes a paginated REST API with `updated_at`.

**Databricks solution:**  
Use Python inside a Job (`requests` or `httpx`) to page through the endpoint.  
Persist a cursor (`last_updated_at` / token) in a small Delta *state table*.  
Land raw JSON to Bronze.

**Why this fits:**  
All within Databricks; reliable with retries/backoff and idempotent by cursor.

---

## 🧭 “Which One When?” — Quick Mapping to Outcomes

| Scenario | Recommended Pattern | Key Benefit |
|-----------|--------------------|--------------|
| Few files & predictable cadence | **COPY INTO** | Idempotent, low maintenance |
| Many files / late files / schema drift | **Auto Loader** | Checkpointed discovery |
| Monthly billion-row drop | **Auto Loader** or **COPY INTO** | Scalable & append-only |
| RDBMS with last_modified | **Incremental JDBC** | Efficient and predictable |
| RDBMS with deletes/history | **CDC over JDBC** | True change capture |
| Upstream Delta with changes | **CDF** | Native incremental in Delta |
| SaaS / REST API | **API Micro-Batch** | Flexible & stateful |

---

## 🧩 Databricks Building Blocks (Reusable Across All Patterns)

- **Unity Catalog External Locations & Credentials** — secure access to staging and Bronze paths.  
- **Delta Lake** — exactly-once writes, schema evolution, time travel.  
- **Workflows (Jobs)** — scheduling, retries, parameterization (DEV/QAS/PROD).  
- **Delta Live Tables (optional)** — declarative pipelines with built-in quality and lineage.  
- **Global Helper Functions** — enforce keys, dedup, and `MERGE` metrics consistently across Bronze → Silver → Gold.

---

**Author:** Enrique Benito  
**Role:** Data Solution Architect — FMG/MGA Databricks Project  
**Last Updated:** October 2025  
