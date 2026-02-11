# Databricks Study Notes

## Streaming, Data Privacy, Performance & Automated Deployment

---

# Databricks Streaming and Lakeflow Spark Declarative Pipelines

## ⇾ Streaming Data Concepts

* **Unbounded data**: Continuous flow of records (e.g., IoT, logs, CDC).
* **Micro-batch processing**: Structured Streaming processes data in small incremental batches.
* **Stateful vs Stateless**:

  * Stateless: map, filter.
  * Stateful: aggregations, joins, windowing.
* **Checkpointing**: Required for fault tolerance and exactly-once guarantees.
* **Exactly-once semantics**: Achieved via idempotent sinks + checkpointing in Databricks.

---

## ⇾ Introduction to Structured Streaming

Structured Streaming in Databricks is built on Spark SQL and treats streaming data as a continuously updating table.

**Core concepts:**

* Streaming source (Kafka, Auto Loader, Delta)
* Streaming transformation (SQL / PySpark)
* Streaming sink (Delta table, console, memory)
* Checkpoint location

### Example (Databricks SQL)

```sql
CREATE OR REFRESH STREAMING LIVE TABLE bronze_events
AS SELECT * FROM STREAM read_files(
  "dbfs:/mnt/bronze/events",
  format => "json"
);
```

### PySpark Example

```python
df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .load("dbfs:/mnt/bronze/events")
)

query = (
    df.writeStream
      .format("delta")
      .option("checkpointLocation", "dbfs:/mnt/checkpoints/bronze")
      .table("main.bronze.events")
)
```

---

## ⇾ Demo: Reading from a Streaming Query

* Use `readStream`
* Must write with `writeStream`
* Checkpoint required for production

```python
spark.readStream.table("main.bronze.events")
```

---

## ⇾ Streaming from Delta Lake

Delta tables can be used as streaming sources.

```python
spark.readStream \
  .format("delta") \
  .table("main.bronze.events")
```

**When useful:**

* CDC pipelines
* Multi-hop (Bronze → Silver → Gold)

---

## ⇾ Streaming Query Lab

Practice:

* Build Bronze ingestion
* Add checkpoint
* Validate with `query.lastProgress`
* Restart cluster and verify recovery

---

## ⇾ Aggregation, Time Windows, Watermarks

### Aggregations

Streaming aggregations maintain state.

```sql
SELECT
  user_id,
  COUNT(*) AS event_count
FROM STREAM main.bronze.events
GROUP BY user_id;
```

### Time Windows

```sql
SELECT
  window(event_time, "10 minutes"),
  COUNT(*)
FROM STREAM main.bronze.events
GROUP BY window(event_time, "10 minutes");
```

### Watermarks

```python
df.withWatermark("event_time", "10 minutes")
```

**Purpose:** Remove late data state after threshold.

---

## ⇾ Event Time + Aggregations over Time Windows

* Event time != processing time
* Required for correct windowed aggregation
* Must define watermark for state cleanup

---

## ⇾ Trigger Types and Output Modes

### Trigger Types

* Default (micro-batch)
* `trigger(once=True)`
* `trigger(availableNow=True)`
* `processingTime="10 seconds"`

### Output Modes

* append
* update
* complete

```python
.writeStream.outputMode("append")
```

---

## ⇾ Stream Aggregation Lab

Practice:

* Create sliding window
* Apply watermark
* Test late arriving data

---

## ⇾ Demo: Windowed Aggregation with Watermark

```python
df.groupBy(
    window("event_time", "10 minutes")
).count()
```

---

## ⇾ Stream Joins (Optional)

* Stream-Stream join
* Stream-Static join
* Requires watermark for stream-stream

```python
stream_df.join(static_df, "user_id")
```

---

## ⇾ Data Ingestion Pattern

**Medallion Architecture:**

* Bronze → Raw ingest
* Silver → Cleaned
* Gold → Aggregated

---

## ⇾ Demo: Auto Loader to Bronze

```python
spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .load("dbfs:/mnt/raw") \
  .writeStream.table("main.bronze.events")
```

---

## ⇾ Demo: Stream from Multiplex Bronze

Multiple Bronze sources → unified Silver transformation.

---

## ⇾ Data Quality Enforcement

Use:

* Expectations in Lakeflow
* Delta constraints
* `dropMalformed`

---

## ⇾ Demo: Data Quality Enforcement

```sql
CONSTRAINT valid_amount EXPECT (amount > 0);
```

---

## ⇾ Streaming ETL Lab

* Bronze ingestion
* Silver transformation
* Gold aggregation
* Validate checkpoint recovery

---

# Databricks Data Privacy

## ⇾ Regulatory Compliance

* GDPR
* CCPA
* HIPAA

Use Unity Catalog for governance.

---

## ⇾ Data Privacy

* Protect PII
* Limit access via RBAC
* Use row-level & column-level security

---

## ⇾ Key Concepts and Components

* Unity Catalog
* Dynamic views
* Audit logs
* Delta Change Data Feed (CDF)

---

## ⇾ Audit Your Data

```sql
SHOW GRANTS ON TABLE main.silver.users;
```

---

## ⇾ Data Isolation

* Catalog-level isolation
* Workspace binding
* Secure clusters

---

## ⇾ Demo: Securing Data in Unity Catalog

```sql
GRANT SELECT ON TABLE main.silver.users TO `analyst_role`;
```

---

## ⇾ Pseudonymization & Anonymization

```sql
SELECT sha2(email, 256) FROM main.silver.users;
```

---

## ⇾ Summary & Best Practices

* Least privilege
* Use dynamic views
* Enable audit logs
* Use CDF for compliance tracking

---

## ⇾ Demo: PII Data Security

Masking via dynamic views:

```sql
CREATE VIEW secure_users AS
SELECT
  user_id,
  CASE WHEN is_member('admin') THEN email ELSE 'REDACTED' END
FROM main.silver.users;
```

---

## ⇾ Capturing Changed Data

Enable CDF:

```sql
ALTER TABLE main.silver.users SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

---

## ⇾ Deleting Data in Databricks

```sql
DELETE FROM main.silver.users WHERE user_id = 123;
```

---

## ⇾ Demo: Processing Records from CDF and Propagating Changes

```python
spark.readStream \
  .option("readChangeFeed", "true") \
  .table("main.silver.users")
```

---

## ⇾ Lab: Propagating Changes with CDF Lab

* Enable CDF
* Process updates
* Apply MERGE to downstream table

---

# Databricks Performance Optimization

## ⇾ DevOps Spark UI Introduction

* DAG visualization
* Stages & Tasks
* Shuffle read/write
* Spill detection

---

## ⇾ Introduction to Designing Foundation

* Partitioning
* File size optimization
* Schema evolution strategy

---

## ⇾ Demo: File Explosion

Small files → performance degradation

Use:

```sql
OPTIMIZE main.silver.events;
```

---

## ⇾ Data Skipping and Liquid Clustering

```sql
ALTER TABLE main.silver.events CLUSTER BY (user_id);
```

---

## ⇾ Lab: Data Skipping and Liquid Clustering

* Compare query plan before/after clustering

---

## ⇾ Skew

* Uneven partition distribution
* Causes long-running tasks

---

## ⇾ Shuffles

Expensive data redistribution across cluster.

---

## ⇾ Demo: Shuffle

Observe shuffle metrics in Spark UI.

---

## ⇾ Spill

* Memory exceeded → spill to disk
* Impacts performance

---

## ⇾ Lab: Exploding Join

* Diagnose skew
* Apply broadcast join

---

## ⇾ Serialization

Kryo recommended for performance.

---

## ⇾ Demo: User-Defined Functions

Prefer built-in functions over UDF.

---

## ⇾ Fine-Tuning: Choosing the Right Cluster

* Autoscaling
* Photon enabled
* Job clusters vs All-purpose

---

## ⇾ Pick the Best Instance Types

* Memory-optimized for shuffle-heavy jobs
* Compute-optimized for CPU-heavy workloads

---

# Automated Deployment with Databricks Asset Bundles

## ⇾ DevOps Review

* Version control
* Git integration
* Environment separation

---

## ⇾ CI/CD Review

* Automated testing
* Environment promotion
* Infrastructure as Code

---

## ⇾ Demo: Course Setup and Authentication

```bash
databricks auth login
```

---

## ⇾ Deploying Databricks Projects

* Notebooks
* Jobs
* Workflows
* Clusters

---

## ⇾ Introduction to Databricks Asset Bundles (DABs)

Declarative YAML-based deployment framework.

---

## ⇾ Demo: Deploying a Simple DAB

```bash
databricks bundle deploy
```

---

## ⇾ Lab: Deploying a Simple DAB

* Define job
* Deploy to dev
* Run validation

---

## ⇾ Variable Substitutions in DABs

```yaml
${var.environment}
```

---

## ⇾ Demo: Deploying a DAB to Multiple Environments

* dev
* staging
* prod

---

## ⇾ Lab: Deploy a DAB to Multiple Environments

* Parameterize cluster configs

---

## ⇾ DAB Project Templates Overview

* Default templates
* ML template
* Data engineering template

---

## ⇾ Lab: Use a Databricks Default DAB Template

```bash
databricks bundle init
```

---

## ⇾ CI/CD Project Overview with DABs

* GitHub Actions
* Azure DevOps
* GitLab CI

---

## ⇾ Demo: Continuous Integration and Continuous Deployment with DABs

* Lint
* Test
* Deploy

---

## ⇾ Lab: Adding ML to Engineering Workflows with DABs

* Integrate MLflow
* Register model
* Deploy job pipeline

---

## ⇾ Developing Locally with Visual Studio Code (VSCode)

* Databricks VSCode extension
* Local file sync

---

## ⇾ Demo: Using VSCode with Databricks

* Sync workspace
* Run remote job

---

## ⇾ CI/CD Best Practices for Data Engineering

* Use job clusters
* Separate catalogs per env
* Immutable deployments
* Monitor via logs + alerts

---

## ⇾ Next Steps: Automated Deployment with GitHub Actions

* Setup workflow YAML
* Store secrets securely
* Deploy on merge to main

---

# End of Notes
