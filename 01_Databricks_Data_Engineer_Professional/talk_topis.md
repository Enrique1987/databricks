
## Databricks Concepts – Summary Notes

#### 1. Databricks Cluster

* A **cluster** is the compute engine used to execute workloads.
* It is **not physically inside Databricks**, but deployed on cloud infrastructure (e.g. Azure VMs).
* Databricks acts as an **orchestration and control layer**.
* You configure:

  * VM type
  * Number of nodes
  * Autoscaling
* **Cost model:**

  * Cloud provider → infrastructure (VMs, storage, networking)
  * Databricks → DBUs (Databricks Units for runtime & features)

---

#### 2. Photon

* **Photon** is an optimized execution engine (C++ vectorized engine).
* Works on top of the same cluster infrastructure.
* Improves performance mainly for:

  * Large-scale queries
  * SQL / DataFrame workloads
* **Important limitation:**

  * Cannot be enabled/disabled dynamically.
  * Requires **cluster restart**.

👉 Recommendation:

* Use Photon by default for production workloads unless proven otherwise.

---

#### 3. Databricks Connect:

Coe Idea, is for developers that love his own local IDE and do not want to use the one from Databricks.

* Allows running code from **local IDE (e.g. VS Code, PyCharm)** against a Databricks cluster.
* Execution happens **remotely**, not locally.
* Use cases:

  * Developer productivity
  * Debugging
  * Avoiding notebook-only workflows

👉 Positioning:

* Best for engineers who prefer **code-first workflows over notebooks**.

---

#### 4. Delta Sharing & Sharing Identifier

* **Delta Sharing** enables secure data sharing across:
  * Workspaces
  * Accounts
  * Organizations

* A **sharing identifier** acts like:
  * A **resource locator + access reference**
  * Comparable to an API endpoint identifier

* Authentication is handled via:
  * Tokens / credentials (not just identifier alone)

👉 Key concept:

* Data is **not copied**, it is accessed remotely.

---

#### 5. Auto Loader

##### Schema Evolution

When new columns appear in source data:

* Without configuration → pipeline may fail
* With rescue mode:
  * New/unexpected fields go into:

    ```
    _rescued_data
    ```

### Behavior with new columns

* Existing data → `NULL`
* New data → populated values

---

#### 6. Auto Loader Triggers

**Available Trigger Modes**

##### 1. `trigger(once=True)`

* Runs **once**
* Processes all available data
* Then stops

👉 Use case:

* Batch ingestion
* Backfills

---

##### 2. `trigger(availableNow=True)`

* Processes all currently available data
* Stops after completion
* Can be triggered repeatedly

👉 Use case:
* Incremental batch processing
* Scheduled pipelines
---

##### 3. Continuous / Micro-batch (default streaming)

* Runs continuously
* Processes data as it arrives

👉 Use case:

* Near real-time ingestion
---

#### 7. Constraint Handling (`ON VIOLATION`)

##### `ON VIOLATION DROP`

* Keeps the row
* Sets invalid column value → `NULL`

##### `ON VIOLATION DELETE`

* Removes the entire row

👉 Design implication:

* **DROP → data preservation**
* **DELETE → strict data quality**

---

#### 8. Delta Live Tables (DLT)

##### Live Table

* General concept in DLT
* Can read from:
  * Batch sources
  * Streaming sources

##### Live Streaming Table

* Special case of Live Table
* Reads from **streaming source only**

---

##### Key Rule

| Table Type           | Input Type Allowed |
| -------------------- | ------------------ |
| Live Table           | Batch or Streaming |
| Live Streaming Table | Streaming only     |

---

##### Important Clarification

* A **Live Streaming Table cannot read from batch**
* If it reads batch → it is just a **Live Table**

---

#### Design Insight

Even if source is batch:

* You may still use DLT for:
  * Automation
  * Dependency management
  * Data quality enforcement

---

#### 9. Streaming vs Live Concepts (Clarification)

* **Streaming** → data ingestion mode
* **Live Table** → managed pipeline abstraction
* **Live Streaming Table** → Live Table + streaming input

👉 Think:



## Databricks Exam Notes

### Question 1

**Question**

A data analyst is running a shell script in all the notebooks attached to the cluster. The shell script contains a long set of commands which is taking a lot of time to complete. As a data engineer, which of the following statements will you suggest to the data analyst?

**Correct answer**

- **Use the init script to execute the shell script faster**

**Why this is correct**

In Databricks, long-running shell or environment setup commands should usually be moved to a **cluster init script** instead of being executed repeatedly inside notebooks.

Init scripts run during **cluster startup**, so the environment is prepared before notebook execution begins.

**Why the other options are wrong**

- **Run the script as the Workspace admin**  
  Permissions do not make the shell script run faster.

- **Use `%md` to run the script faster**  
  `%md` is for Markdown, not shell execution.

- **Increase the number of worker nodes to speed up the script**  
  Worker nodes help with distributed Spark workloads, not with notebook-side shell setup.

- **Run the notebook using Databricks API**  
  This changes how the notebook is triggered, not how fast the shell script executes.

**Exam takeaway**

- **Cluster / OS setup** → use **init scripts**
- **Notebook shell commands** → use `%sh` only for small ad-hoc tasks
- **Distributed compute scaling** → helps Spark jobs, not general shell setup

---

### Question 2

**Question**

Which of the following is a valid response to a JSON workload passed to the `2.0/jobs/create` endpoint of the Databricks REST API?

**Correct answer**

```json
{
  "job_id": 13746
}

* *Streaming = how data arrives*
* *Live Table = how pipeline is managed*

## Databricks — Streaming, Ingestion Patterns & Optimization (Study Notes)

### 1. Ingestion Patterns: `Simplex vs Multiplex`

#### `Simplex` — 1:1 ingestion

**When useful:** clear source → target mapping, batch pipelines, simple lineage.

* One source → one target table
* Typical in batch ingestion from on-prem / external systems
* Easy to debug and maintain

#### `Multiplex` — N:1 ingestion

**When useful:** streaming ingestion (e.g., Kafka), shared ingestion layer.

* Multiple sources (e.g., Kafka topics) → one Bronze table
* Bronze acts as a **raw multi-entity container**
* Later split into Silver tables

**Key insight**

* Multiplex is **most useful in streaming**, not batch
* Batch pipelines usually remain **simplex**

---

### 2. Auto Loader — Schema Evolution

#### `rescuedDataColumn` — Capture unexpected columns

**When useful:** schema drift, semi-structured ingestion.

* Unknown fields are stored in a special column (e.g., `_rescued_data`)
* Prevents pipeline failures

```python
.option("rescuedDataColumn", "_rescued_data")
```

**Pattern**

* Bronze: keep rescued data
* Silver: explicitly parse / promote fields

**Gotchas**

* If you never process `_rescued_data`, you silently lose usability of data

---

### 3. `withWatermark` — Late data handling

#### Concept (non-technical)

Watermark = **“how long am I willing to wait for late events?”**

* You do **NOT delay results**
* You define a **maximum allowed lateness**
* Data arriving later than that → ignored in aggregations

#### Example (books sales)

* Sale at `12:10`
* Watermark = `5 minutes`

| Arrival time | Included? |
| ------------ | --------- |
| 12:12        | ✅ Yes     |
| 12:14        | ✅ Yes     |
| 12:20        | ❌ No      |

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

* Not related to duplicates directly
* Enables **closing windows in streaming**
* Trade-off: **freshness vs completeness**

---

### 4. Stream Joins

#### Stream–Stream join

**Reality**

* Not “continuous infinite join”
* Executed via **state + micro-batches**

**Requirements**

* Watermarks on both sides
* Time constraints to bound state

---

#### Stream–Static join

**Behavior**

* Static table changes → **NO immediate effect**
* Join updates only when **new stream data arrives**

**Key insight**

* Stream = **trigger**

---

### 5. Delta Change Data Feed (CDF)

#### `CDF` — Track row-level changes

**When useful:**

* Incremental pipelines
* Propagating updates downstream
* Audit / debugging

```sql
ALTER TABLE my_table SET TBLPROPERTIES (
  delta.enableChangeDataFeed = true
);
```

#### Reading changes

```sql
SELECT * FROM table_changes('my_table', 10);
```

---

#### CDF vs Append-only tables

* Append-only → every row is already “new”
* CDF shines when:

  * `UPDATE`
  * `DELETE`
  * `MERGE`

**Typical Lakehouse use cases**

* Dimension tables (customer updates)
* Lookup tables
* GDPR deletes
* Data corrections

---

### 6. CDF vs CDC

| Concept | Meaning                           |
| ------- | --------------------------------- |
| CDC     | General concept (capture changes) |
| CDF     | Delta Lake implementation         |

**Key idea**

* CDF = **CDC inside Delta Lake**

---

### 7. Applying CDF (Batch pattern)

```sql
MERGE INTO target t
USING changes c
ON t.id = c.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

**Pattern**

* Source table → CDF enabled
* Target table → apply changes via `MERGE`

---

### 8. Partitioning Strategy

#### Best practices

**When useful:** large tables (>1GB per partition)

* Use **low cardinality columns**
* Target: ~**1GB per partition**

#### Datetime partitioning

* Valid but:

  * Prefer `date` (day) instead of full timestamp
  * Avoid too many small partitions

---

#### Rule of thumb

* ~**5M – 20M rows ≈ 1GB**
* Depends on row size

---

#### Anti-pattern

* ❌ Over-partitioning small tables (<1GB)

---

### 9. Z-ORDER vs Liquid Clustering

#### `ZORDER`

**When useful:** selective filters

```sql
OPTIMIZE table ZORDER BY (user_id, country);
```

* Improves data skipping
* Manual operation

---

#### `Liquid Clustering`

**When useful:** evolving query patterns

```sql
CREATE TABLE t
CLUSTER BY (user_id);
```

or

```sql
CLUSTER BY AUTO
```

* Dynamic clustering
* No rigid partitions

---

### 10. Predictive Optimization

#### What it is

Databricks automatically:

* Runs `OPTIMIZE`
* Runs `VACUUM`
* Adjusts clustering
* Maintains stats

#### Scope

* Works on **Delta tables (Unity Catalog)**

#### When useful

* Large tables
* Frequent queries
* High operational overhead

---

#### Relationship

| Feature                 | Scope                     |
| ----------------------- | ------------------------- |
| Auto Optimize           | Basic (write-time)        |
| Liquid Clustering       | Data layout               |
| Predictive Optimization | **Full automation layer** |

---

### 11. `ANALYZE` — Statistics collection

#### `ANALYZE TABLE`

**When useful:** query planning optimization

```sql
ANALYZE TABLE my_table COMPUTE STATISTICS;
```

* Collects column stats
* Helps query optimizer (Photon)

---

### 12. Auto Optimize

#### Features

* Auto compaction
* Optimized writes

```sql
SET spark.databricks.delta.optimizeWrite = true;
SET spark.databricks.delta.autoCompact = true;
```

**Scope**

* Write-time optimization (not full lifecycle)

---

### 13. Deletion Vectors

#### `Deletion Vectors` — Efficient deletes

**What it does**

* Marks rows as deleted **without rewriting files**

#### Benefits

* Faster `DELETE` / `MERGE`
* Less file rewriting

#### Behavior

* Applied lazily
* Cleaned later via `OPTIMIZE`

---

#### Activation

* Often **enabled by default** (new runtimes)
* Or via table properties



### Final Mental Model

* **Bronze** → ingest (minimal optimization)

* **Silver** → transform + enforce schema

* **Gold** → optimize for queries (ZORDER / clustering)

* **Watermark** → controls lateness

* **CDF** → enables incremental processing

* **Predictive Optimization** → removes manual tuning



