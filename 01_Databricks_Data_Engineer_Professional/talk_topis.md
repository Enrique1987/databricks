# Databricks Concepts — Organized Study Notes

> Reordered, grouped by topic, and rewritten with **simple clickable anchors** for Markdown files such as GitHub.

## Index

* [Platform and Compute](#platform-and-compute)

  * [Databricks Cluster](#databricks-cluster)
  * [Photon](#photon)
  * [Databricks Connect](#databricks-connect)
  * [Query Profile](#query-profile)
* [Development and Deployment](#development-and-deployment)

  * [Databricks Asset Bundles](#databricks-asset-bundles)
  * [Python Function vs UDF vs Pandas UDF](#python-function-vs-udf-vs-pandas-udf)
* [Streaming Ingestion and Pipeline Management](#streaming-ingestion-and-pipeline-management)

  * [Streaming vs Live Concepts](#streaming-vs-live-concepts)
  * [Lakeflow Declarative Pipelines and Delta Live Tables](#lakeflow-declarative-pipelines-and-delta-live-tables)
  * [Auto Loader](#auto-loader)
  * [Auto Loader Triggers](#auto-loader-triggers)
  * [Ingestion Patterns Simplex vs Multiplex](#ingestion-patterns-simplex-vs-multiplex)
  * [withWatermark](#withwatermark)
  * [Stream Joins](#stream-joins)
* [Change Processing and Data Quality](#change-processing-and-data-quality)

  * [Delta Change Data Feed](#delta-change-data-feed)
  * [CDF and CDC](#cdf-and-cdc)
  * [Auto CDC](#auto-cdc)
  * [Expectations](#expectations)
  * [Constraint Handling](#constraint-handling)
* [Delta Lake Storage Layout and Optimization](#delta-lake-storage-layout-and-optimization)

  * [Partitioning Strategy](#partitioning-strategy)
  * [ZORDER vs Liquid Clustering](#zorder-vs-liquid-clustering)
  * [Predictive Optimization](#predictive-optimization)
  * [Auto Optimize](#auto-optimize)
  * [Analyze Table](#analyze-table)
  * [Deletion Vectors](#deletion-vectors)
* [Governance Sharing and Access](#governance-sharing-and-access)

  * [Delta Sharing](#delta-sharing)
  * [Sharing Identifier](#sharing-identifier)
  * [Governance](#governance)
* [Mental Models and Final Takeaways](#mental-models-and-final-takeaways)

  * [Bronze Silver Gold](#bronze-silver-gold)
  * [Final Mental Model](#final-mental-model)
* [Exam Notes](#exam-notes)

  * [Question 1](#question-1)
  * [Question 2](#question-2)

---

## Platform and Compute

### Databricks Cluster

* A **cluster** is the compute engine used to execute workloads.
* It is **not physically inside Databricks**, but deployed on cloud infrastructure such as Azure VMs.
* Databricks acts as an **orchestration and control layer**.
* You configure:

  * VM type
  * Number of nodes
  * Autoscaling

**Cost model**

* **Cloud provider** → infrastructure cost such as VMs, storage, and networking
* **Databricks** → DBUs for runtime and platform features

---

### Photon

* **Photon** is an optimized execution engine.
* It is a **C++ vectorized engine** running on the same cluster infrastructure.
* It improves performance mainly for:

  * Large-scale queries
  * SQL workloads
  * DataFrame workloads

**Important limitation**

* Photon cannot be enabled or disabled dynamically on a running cluster.
* It requires a **cluster restart**.

**Recommendation**

* Use Photon by default for production workloads unless there is a reason not to.

---

### Databricks Connect

**Core idea:** this is for developers who prefer working in a local IDE instead of only in notebooks.

* Lets you run code from **VS Code**, **PyCharm**, or another local IDE against a Databricks cluster.
* Code execution happens **remotely on the Databricks cluster**, not on your local machine.

**When useful**

* Developer productivity
* Debugging
* Code-first workflows
* Teams that prefer local project structure over notebook-only development

---

### Query Profile

* **Query Profile** is the execution analysis tool for understanding how a query ran.
* It helps inspect:

  * The execution plan
  * Time spent per stage
  * Bottlenecks

**Key insight**

Even though Spark optimizes queries automatically, it is **not magic**.

Better query design still matters.

**Typical improvements**

* Filter before joins
* Avoid Python UDFs when built-in functions exist
* Prefer built-in SQL and PySpark expressions

---

## Development and Deployment

### Databricks Asset Bundles

* **Asset Bundles** are a declarative way to deploy Databricks projects.

**Before**

* Move code manually through repos or CI pipelines
* Configure jobs and infrastructure separately

**Now**

* Define everything together in one bundle:

  * Jobs
  * Pipelines
  * Configurations

**Key difference**

| Before       | Bundles      |
| ------------ | ------------ |
| Code only    | Code + infra |
| Manual setup | Declarative  |
| Error-prone  | Reproducible |

---

### Python Function vs UDF vs Pandas UDF

#### Python function

* Runs locally
* Not distributed by Spark

**When useful**

* Small data
* Driver-side logic
* Helper functions outside distributed execution

---

#### Python UDF

* Custom Python logic executed inside Spark
* Processes data **row by row**

```python
from pyspark.sql.functions import udf

@udf("int")
def plus_one(x):
    return x + 1
```

**Main downside**

* High **serialization overhead** between JVM and Python
* Slower than built-in Spark functions

---

#### Pandas UDF

* Uses **vectorized execution**
* Processes data in batches instead of row by row

```python
from pyspark.sql.functions import pandas_udf

@pandas_udf("int")
def plus_one(s):
    return s + 1
```

**Important concepts**

| Concept       | Meaning                                                 |
| ------------- | ------------------------------------------------------- |
| Serialization | Converting data to bytes to move between JVM and Python |
| Vectorization | Processing data in batches instead of one row at a time |

**Takeaway**

* First choice → built-in Spark functions
* If custom Python logic is required:

  * **Pandas UDF** is usually better than **Python UDF**
  * **Python UDF** is usually more expensive

---

## Streaming Ingestion and Pipeline Management

### Streaming vs Live Concepts

* **Streaming** = how data arrives
* **Live Table** = how the pipeline is managed
* **Live Streaming Table** = managed table with streaming input

**Mental model**

* **Streaming** → ingestion mode
* **Live Table** → pipeline abstraction
* **Live Streaming Table** → live pipeline + streaming source

---

### Lakeflow Declarative Pipelines and Delta Live Tables

> Lakeflow Declarative Pipelines is the newer framing of what used to be commonly discussed as Delta Live Tables.

#### Live Table

* General concept in managed Databricks pipelines
* Can read from:

  * Batch sources
  * Streaming sources

#### Live Streaming Table

* Special case of a Live Table
* Reads from **streaming source only**

**Key rule**

| Table type           | Input type allowed |
| -------------------- | ------------------ |
| Live Table           | Batch or streaming |
| Live Streaming Table | Streaming only     |

**Clarification**

* A **Live Streaming Table cannot read from batch**
* If it reads from batch, it is just a **Live Table**

**Design insight**

Even if the source is batch, managed pipelines are still useful for:

* Automation
* Dependency management
* Data quality rules
* Retries
* Observability

**Rule of thumb**

Use Lakeflow when you need:

* SCD Type 2 or history tracking
* Multiple dependencies
* Partial reprocessing
* Stronger operational control

Not every simple A → B → C pipeline needs it.

---

### Auto Loader

#### Schema evolution

When new columns appear in the source data:

* Without configuration, the pipeline may fail
* With rescue mode, unexpected fields can be captured safely

```text
_rescued_data
```

#### rescuedDataColumn

* Unknown fields are stored in a special column instead of failing the pipeline

```python
.option("rescuedDataColumn", "_rescued_data")
```

**Behavior with new columns**

* Existing rows → `NULL` for the new field
* New rows → populated values where available

**Recommended pattern**

* **Bronze** → keep rescued data
* **Silver** → explicitly parse, promote, or clean the rescued fields

**Gotcha**

* If `_rescued_data` is never processed later, the data is technically kept but practically unused.

---

### Auto Loader Triggers

#### trigger once true

* Runs once
* Processes all currently available data
* Then stops

**When useful**

* Batch-style ingestion
* Backfills

---

#### trigger availableNow true

* Processes all currently available data
* Stops after completion
* Can be run again later

**When useful**

* Incremental batch ingestion
* Scheduled ingestion jobs

---

#### Continuous micro batch mode

* Runs continuously
* Processes data as it arrives

**When useful**

* Near real-time ingestion

---

### Ingestion Patterns Simplex vs Multiplex

#### Simplex

* **One source to one target**
* Clear source-to-target mapping
* Common in batch pipelines

**When useful**

* Simple lineage
* Easier debugging
* Easier maintenance

---

#### Multiplex

* **Multiple sources to one target**
* Common in streaming ingestion
* Example: multiple Kafka topics into one Bronze table

**When useful**

* Shared ingestion layer
* Multi-entity Bronze design

**Key insight**

* Multiplex is more common and more useful in **streaming**
* Batch pipelines usually remain **simplex**

---

### withWatermark

**Concept**

Watermark means:

> How long am I willing to wait for late events?

* It does **not delay results**
* It defines the **maximum allowed lateness**
* Events arriving later than that may be ignored in aggregations

**Example**

* Sale event time = `12:10`
* Watermark = `5 minutes`

| Arrival time | Included |
| ------------ | -------- |
| 12:12        | Yes      |
| 12:14        | Yes      |
| 12:20        | No       |

#### SQL

```sql
SELECT
  window(event_time, '10 minutes'),
  COUNT(*) AS sales
FROM STREAM(bronze_sales)
WATERMARK event_time DELAY '5 minutes'
GROUP BY window(event_time, '10 minutes');
```

#### PySpark

```python
df \
  .withWatermark("event_time", "5 minutes") \
  .groupBy(window("event_time", "10 minutes")) \
  .count()
```

**Key takeaways**

* It is not mainly about duplicates
* It is important for **closing windows in streaming**
* There is always a trade-off between:

  * **Freshness**
  * **Completeness**

---

### Stream Joins

#### Stream to stream join

* Not a truly infinite continuous join
* Implemented through **state + micro-batches**

**Requirements**

* Watermarks on both sides
* Time constraints to keep state bounded

---

#### Stream to static join

* Changes in the static table do **not** instantly refresh results
* The join is re-evaluated only when **new stream data arrives**

**Key insight**

* The **stream is the trigger**

---

## Change Processing and Data Quality

### Delta Change Data Feed

* **CDF** tracks row-level changes in a Delta table

**When useful**

* Incremental pipelines
* Downstream propagation of changes
* Auditing
* Debugging

#### Enable CDF

```sql
ALTER TABLE my_table SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
);
```

#### Read changes

```sql
SELECT * FROM table_changes('my_table', 10);
```

#### Apply changes pattern

```sql
MERGE INTO target t
USING changes c
ON t.id = c.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

**CDF vs append-only tables**

* Append-only tables already make new rows easy to detect
* CDF is most useful when the source table has:

  * `UPDATE`
  * `DELETE`
  * `MERGE`

**Typical use cases**

* Dimension tables
* Lookup tables
* GDPR deletes
* Data corrections

---

### CDF and CDC

| Concept | Meaning                              |
| ------- | ------------------------------------ |
| CDC     | General concept of capturing changes |
| CDF     | Delta Lake implementation of CDC     |

**Key idea**

* **CDF = CDC inside Delta Lake**

---

### Auto CDC

* **Auto CDC** automatically tracks row-level changes
* It uses the **Delta log**, not a full scan of the source table

**Tracks**

* Inserts
* Updates
* Deletes

```sql
ALTER TABLE catalog.schema.table
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

**When useful**

* Multiple downstream consumers
* Real-time or incremental pipelines
* Replication patterns

**When not always needed**

* Very simple linear ETL such as bronze to silver only

---

### Expectations

* **Expectations** are declarative data quality rules in managed Databricks pipelines

**Final understanding**

| Feature           | Constraint | Expectation |
| ----------------- | ---------- | ----------- |
| Enforced strictly | Yes        | Optional    |
| Blocks data       | Yes        | Optional    |
| Logs issues       | No         | Yes         |
| Flexible behavior | No         | Yes         |

**Common behaviors**

* **Warn** → log only
* **Drop** → remove bad rows
* **Fail** → stop pipeline

```sql
CONSTRAINT valid_price EXPECT (price > 0)
```

**Key idea**

* Expectations are more flexible than strict SQL constraints
* They are a natural fit for managed Databricks pipelines

---

### Constraint Handling

#### ON VIOLATION DROP

* Keeps the row
* Sets the invalid column value to `NULL`

#### ON VIOLATION DELETE

* Removes the entire row

**Design implication**

* **DROP** → preserve as much data as possible
* **DELETE** → enforce stricter data quality

---

## Delta Lake Storage Layout and Optimization

### Partitioning Strategy

**Best practices**

* Prefer **low-cardinality columns**
* Best for larger tables
* Good target is roughly **1 GB per partition**

#### Datetime partitioning

* Valid, but usually prefer **date** or day-level partitioning
* Avoid full timestamps when they create too many tiny partitions

#### Rule of thumb

* Around **5M to 20M rows** can be close to **1 GB**
* Real size depends on row width and file format

#### Anti-pattern

* Over-partitioning small tables, especially tables under roughly 1 GB

---

### ZORDER vs Liquid Clustering

#### ZORDER

```sql
OPTIMIZE table ZORDER BY (user_id, country);
```

**When useful**

* Selective filters
* Manual tuning of data skipping

**Key points**

* Improves data skipping
* Manual operation

---

#### Liquid Clustering

```sql
CREATE TABLE t
CLUSTER BY (user_id);
```

or

```sql
CLUSTER BY AUTO
```

**When useful**

* Query patterns evolve over time
* You want more adaptive storage layout

**Key points**

* Dynamic clustering
* No rigid partition dependency
* Reduces the need for manual layout tuning

---

### Predictive Optimization

* Predictive Optimization is about **data layout optimization**, not compute autoscaling

**Databricks can automatically handle**

* `OPTIMIZE`
* `VACUUM`
* Clustering adjustments
* Statistics maintenance

**Scope**

* Mainly associated with **Delta tables in Unity Catalog**

**When useful**

* Large tables
* Frequent queries
* High operational overhead from manual maintenance

**Relationship**

| Feature                 | Scope                         |
| ----------------------- | ----------------------------- |
| Auto Optimize           | Basic write-time optimization |
| Liquid Clustering       | Data layout strategy          |
| Predictive Optimization | Broader automation layer      |

---

### Auto Optimize

**Features**

* Optimized writes
* Auto compaction

```sql
SET spark.databricks.delta.optimizeWrite = true;
SET spark.databricks.delta.autoCompact = true;
```

**Scope**

* Write-time optimization only
* Not full table lifecycle maintenance

---

### Analyze Table

* Collects table and column statistics
* Helps the optimizer generate better plans

```sql
ANALYZE TABLE my_table COMPUTE STATISTICS;
```

**When useful**

* Better query planning
* Better join and scan decisions

---

### Deletion Vectors

* **Deletion Vectors** allow logical row-level deletes without rewriting files immediately

**What happens**

* Rows are marked as deleted
* Files are not fully rewritten at delete time

**Why it matters**

* Faster `DELETE`
* Faster `MERGE`
* Less file rewriting

```sql
DELETE FROM catalog.schema.table WHERE id = 1;
```

**Notes**

* Transparent to users
* Physical cleanup happens later during maintenance such as `OPTIMIZE` and `VACUUM`
* Often enabled by default in newer runtimes, or controlled through table properties

---

## Governance Sharing and Access

### Delta Sharing

* **Delta Sharing** enables secure data sharing across:

  * Workspaces
  * Accounts
  * Organizations

**Key concept**

* Data is **not copied**
* It is **accessed remotely**

**How it works**

* Access is provided through controlled sharing
* Authentication uses tokens or other credentials

**Important distinction**

| Feature          | Delta Sharing | Traditional movement |
| ---------------- | ------------- | -------------------- |
| Copies data      | No            | Often yes            |
| External sharing | Yes           | Depends              |
| Access method    | API based     | Varies               |

**Key idea**

* Delta Sharing is an **access layer**, not a data movement tool

---

### Sharing Identifier

* A **sharing identifier** acts like:

  * A resource locator
  * An access reference
  * Something similar to an API endpoint identifier

**Important note**

* The identifier alone is **not enough**
* Authentication still requires tokens or credentials

---

### Governance

> Governance = control + traceability

In Databricks, governance usually means:

* Who changed what
* When pipelines ran
* What data was produced
* Better visibility and accountability across data operations

---

## Mental Models and Final Takeaways

### Bronze Silver Gold

* **Bronze** → raw ingestion with minimal transformation
* **Silver** → cleaned and transformed data with schema enforcement
* **Gold** → optimized data for reporting, BI, and serving use cases

---

### Final Mental Model

* **Delta Lake** → storage + ACID
* **Lakeflow** → pipelines
* **Expectations** → data quality
* **CDC and CDF** → incremental changes
* **Bundles** → deployment
* **Delta Sharing** → data access
* **Predictive Optimization** → less manual tuning
* **Watermark** → controls lateness in streaming

**Final takeaway**

Databricks automates a lot, but good design still matters.

Many features aim to:

* Reduce manual work
* Improve performance
* Increase governance
* Make pipelines more reliable

---

## Exam Notes

### Question 1

**Question**

A data analyst is running a shell script in all the notebooks attached to the cluster. The shell script contains a long set of commands which is taking a lot of time to complete. As a data engineer, which of the following statements will you suggest to the data analyst?

**Correct answer**

* **Use an init script to execute the shell script faster**

**Why this is correct**

In Databricks, long-running shell or environment setup commands should usually be moved to a **cluster init script** instead of being executed repeatedly inside notebooks.

Init scripts run during **cluster startup**, so the environment is prepared before notebook execution begins.

**Why the other options are wrong**

* **Run the script as Workspace admin**
  Permissions do not make the shell script run faster.

* **Use `%md` to run the script faster**
  `%md` is for Markdown, not shell execution.

* **Increase the number of worker nodes**
  Worker nodes help distributed Spark workloads, not notebook-side shell setup.

* **Run the notebook using Databricks API**
  That changes how the notebook is triggered, not how fast the shell script executes.

**Exam takeaway**

* Cluster or OS setup → use **init scripts**
* Notebook shell commands → use `%sh` only for small ad hoc tasks
* Cluster scaling helps Spark jobs, not general shell initialization

---

### Question 2

**Question**

Which of the following is a valid response to a JSON workload passed to the `2.0/jobs/create` endpoint of the Databricks REST API?

**Correct answer**

```json
{
  "job_id": 13746
}
```

**Exam takeaway**

* The `jobs/create` endpoint returns a **job identifier**
* That `job_id` is then used for later operations on the job

---

## Notes About Clickable Links

These links should work better in a normal `.md` renderer such as GitHub because the headings use:

* simple text
* no numbering in the heading itself
* minimal punctuation

If you want, next I can turn this into an even cleaner **GitHub study guide version** with:

* consistent emoji-free style
* shorter bullets
* exam-focused phrasing
