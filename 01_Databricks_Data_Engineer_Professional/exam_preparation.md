# Databricks Exam Questions — Reordered by Topic

---

# Delta Live Tables (DLT)

## Change Data Capture (CDC) in DLT

A data engineer is designing a **Delta Live Tables (DLT)** pipeline.  
The source system generates files containing **change events** (CDC). Each event includes:

- metadata indicating whether a record was **inserted**, **updated**, or **deleted**
- a **timestamp** column that indicates the order of changes

The data engineer needs to **apply these change events** to keep a target table up to date.

**Which of the following commands can the data engineer use to best solve this problem (in Delta Live Tables)?**

**Options:**
- `COPY INTO`
- `APPLY CHANGES INTO`
- `MERGE INTO`
- `UPDATE`

**✅ Correct answer:**  
- `APPLY CHANGES INTO`

**Explanation:**  
`APPLY CHANGES INTO` is designed specifically for CDC-style logic in Delta Live Tables, where records must be inserted, updated, or deleted based on change events and sequencing columns.

---

## DLT Data Quality Constraints

A data engineer has defined the following data quality constraint in a Delta Live Tables pipeline:

```sql
CONSTRAINT valid_id EXPECT (id IS NOT NULL) __________
````

Fill in the above blank so records violating this constraint will be added to the target table, and reported in metrics.

**Options:**

* `ON VIOLATION ADD ROW`
* `ON VIOLATION FAIL UPDATE`
* `ON VIOLATION SUCCESS UPDATE`
* `ON VIOLATION NULL`
* There is no need to add `ON VIOLATION` clause. By default, records violating the constraint will be kept, and reported as invalid in the event log.

**✅ Correct answer:**

* There is no need to add `ON VIOLATION` clause. By default, records violating the constraint will be kept, and reported as invalid in the event log.

---

## DLT Execution Mode: Triggered + Development

The data engineer team has a DLT pipeline that updates all the tables once and then stops.
The compute resources of the pipeline continue running to allow for quick testing.

Which of the following best describes the execution modes of this DLT pipeline?

**Options:**

* The DLT pipeline executes in Continuous Pipeline mode under Production mode.
* The DLT pipeline executes in Continuous Pipeline mode under Development mode.
* The DLT pipeline executes in Triggered Pipeline mode under Production mode.
* The DLT pipeline executes in Triggered Pipeline mode under Development mode.
* More information is needed to determine the correct response.

**✅ Correct answer:**

* The DLT pipeline executes in Triggered Pipeline mode under Development mode.

---

## DLT Execution Mode: Continuous + Production

The data engineer team has a DLT pipeline that updates all the tables at defined intervals until manually stopped.
The compute resources terminate when the pipeline is stopped.

Which of the following best describes the execution modes of this DLT pipeline?

**Options:**

* The DLT pipeline executes in Continuous Pipeline mode under Production mode.
* The DLT pipeline executes in Continuous Pipeline mode under Development mode.
* The DLT pipeline executes in Triggered Pipeline mode under Production mode.
* The DLT pipeline executes in Triggered Pipeline mode under Development mode.
* More information is needed to determine the correct response.

**✅ Correct answer:**

* The DLT pipeline executes in Continuous Pipeline mode under Production mode.

---

# Databricks SQL and Functions

## Higher-Order Functions on Arrays

A data engineer is working with a table called `faculties`.
The table contains a column `students` defined as:

```text
ARRAY<STRUCT<student_id STRING, total_courses INT>>
```

Each element in the `students` array represents a student and the number of courses they are enrolled in.

The engineer needs to create a new column that contains **only the students enrolled in fewer than 3 courses**, while preserving the original struct format.

**Which of the following expressions should be used?**

**Options:**

* `TRANSFORM(students, s -> s.total_courses < 3)`
* `FILTER(students, s -> s.total_courses < 3)`
* `WHERE s.total_courses < 3`
* `AGGREGATE(students, s -> s.total_courses < 3)`

**✅ Correct answer:**

* `FILTER(students, s -> s.total_courses < 3)`

**Explanation:**
`FILTER` returns only the array elements matching the condition, while preserving the original `STRUCT` type.

**Key pattern:**

* **Keep only elements** → `FILTER`
* **Modify elements** → `TRANSFORM`
* **Reduce to one value** → `AGGREGATE`
* **Turn into rows** → `EXPLODE`

---

## Filtering an Array Column

Given the following table `faculties`, fill in the blank to get the students enrolled in less than 3 courses from the array column `students`.

```sql
SELECT
    faculty_id,
    students,
    __________ AS few_courses_students
FROM faculties
```

**Options:**

* `TRANSFORM(students, total_courses < 3)`
* `TRANSFORM(students, i -> i.total_courses < 3)`
* `FILTER(students, total_courses < 3)`
* `FILTER(students, i -> i.total_courses < 3)`
* `CASE WHEN students.total_courses < 3 THEN students ELSE NULL END`

**✅ Correct answer:**

* `FILTER(students, i -> i.total_courses < 3)`

---

## Creating a User Defined Function (UDF)

Which of the following code blocks can a data engineer use to create a user defined function (UDF)?

**Options:**

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURN value +1
```

```sql
CREATE UDF plus_one(value INTEGER)
RETURNS INTEGER
RETURN value +1;
```

```sql
CREATE UDF plus_one(value INTEGER)
RETURN value +1;
```

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURNS INTEGER
RETURN value +1;
```

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURNS INTEGER
value +1;
```

**✅ Correct answer:**

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURNS INTEGER
RETURN value +1;
```

---

# Streaming

## Querying an Existing Streaming Table

Which of the following code blocks can a data engineer use to query the existing streaming table `events`?

**Options:**

```python
spark.readStream("events")
```

```python
spark.read.table("events")
```

```python
spark.readStream.table("events")
```

```python
spark.readStream().table("events")
```

```python
spark.stream.read("events")
```

**✅ Correct answer:**

```python
spark.readStream.table("events")
```

---

# Tables, Views, and Databases

## Relational Object for Same Cluster Sessions Only

A data engineer wants to create a relational object by pulling data from two tables.
The relational object must be used by other data engineers in other sessions on the same cluster only.
In order to save on storage costs, the data engineer wants to avoid copying and storing physical data.

Which of the following relational objects should the data engineer create?

**Options:**

* Temporary view
* External table
* Managed table
* Global Temporary view
* View

**✅ Correct answer:**

* Global Temporary view

---

## Default Database Location

Given the following command:

```sql
CREATE DATABASE IF NOT EXISTS hr_db;
```

In which of the following locations will the `hr_db` database be located?

**Options:**

* `dbfs:/user/hive/warehouse`
* `dbfs:/user/hive/db_hr`
* `dbfs:/user/hive/databases/db_hr.db`
* `dbfs:/user/hive/databases`
* `dbfs:/user/hive`

**✅ Correct answer:**

* `dbfs:/user/hive/warehouse`

---

# Platform Architecture and Governance

## What Runs in the Customer’s Cloud Account?

According to the Databricks Lakehouse architecture, which of the following is located in the customer's cloud account?

**Options:**

* Databricks web application
* Notebooks
* Repos
* Cluster virtual machines
* Workflows

**✅ Correct answer:**

* Cluster virtual machines

---

## Granting Permissions on Tables

Which part of the Databricks Platform can a data engineer use to grant permissions on tables to users?

**Options:**

* Data Studio
* Cluster event log
* Workflows
* DBFS
* Data Explorer

**✅ Correct answer:**

* Data Explorer

---

# Maintenance and Administration

## VACUUM Default Retention Period

How long is the default retention period of the `VACUUM` command?

**Options:**

* 0 days
* 7 days
* 30 days
* 90 days
* 365 days

**✅ Correct answer:**

* 7 days

---

# Databricks SQL

## Unsupported Alert Destination

Which of the following alert destinations is **not** supported in Databricks SQL?

**Options:**

* Slack
* Webhook
* SMS
* Microsoft Teams
* Email

**✅ Correct answer:**

* SMS

# Databricks Data Engineer Professional — compact topic summary

> **Naming note:** current Databricks docs use **Lakeflow Spark Declarative Pipelines** (formerly DLT), **Lakeflow Jobs** (formerly Jobs), and **Declarative Automation Bundles** (formerly Databricks Asset Bundles / DABs). ([Databricks Dokumentation][1])

## Section 1: Developing Code for Data Processing using Python and SQL

* **Using Python and tools for development**: This topic is about writing reusable Python for Databricks using notebooks, files, SDK/CLI, and Git-aware workflows instead of leaving logic trapped in one notebook. You should be comfortable turning exploratory code into code that is versioned, debuggable, and automation-friendly on the platform. ([Databricks Dokumentation][2])

* **Design a scalable Python project structure for DABs**: Organize projects around a root `databricks.yml`, reusable resources, variables, and environment targets so the same codebase deploys cleanly to dev, test, and prod. The key skill is separating business logic from deployment configuration so CI/CD can validate and promote changes safely. ([Databricks Dokumentation][3])

* **Manage third-party libraries and dependencies**: You need to know how to install packages from PyPI, `requirements.txt`, wheels, workspace files, volumes, or object storage, and how library scope affects notebooks, jobs, and compute. You should also remember the newer security posture: workspace libraries are deprecated and DBFS library installs are disabled in newer runtimes. ([Databricks Dokumentation][4])

* **Develop UDFs using Pandas/Python UDF**: Python UDFs are for custom logic that built-in functions do not cover, but they add Python execution overhead. Pandas UDFs are vectorized with Arrow and usually the better choice when you must stay in Python and still want better performance. ([Databricks Dokumentation][5])

* **Build and test an ETL pipeline with Lakeflow, SQL, and Spark**: You should understand how declarative pipelines define datasets and flows, how pipeline updates work, and how dry-run style validation helps catch problems early. The goal is not just “make it run,” but “make it testable and production-ready.” ([Databricks Dokumentation][6])

* **Build reliable batch and streaming pipelines with Lakeflow and Auto Loader**: Auto Loader incrementally discovers new files, supports schema inference/evolution, and is designed for large-scale ingestion from cloud storage. At professional level, you should know how to keep these pipelines idempotent, resilient to schema drift, and easy to operate. ([Databricks Dokumentation][7])

* **Create and automate ETL workloads using Jobs via UI/APIs/CLI**: Lakeflow Jobs can be created and managed in the UI, through the REST API, or from the Databricks CLI. The real exam skill is knowing when to use each interface for repeatability, automation, and integration with external release processes. ([Databricks Dokumentation][8])

* **Explain streaming tables vs materialized views**: Streaming tables are best for incremental ingestion and low-latency append-style processing, but joins do not automatically recompute when dimensions change. Materialized views are better when you need precomputed results, joins, and aggregations to stay correct over time. ([Databricks Dokumentation][9])

* **Use APPLY CHANGES APIs for CDC**: In current docs, **AUTO CDC** replaces **APPLY CHANGES**, but the core idea is the same: declare keys, sequencing, and SCD behavior instead of hand-coding CDC logic. This simplifies deduplication, out-of-order handling, and SCD Type 1/Type 2 processing. ([Databricks Dokumentation][10])

* **Compare Structured Streaming and Lakeflow pipelines**: Use Structured Streaming when you need lower-level control over state, triggers, or custom streaming semantics. Use Lakeflow when you want a more declarative framework that reduces orchestration and CDC complexity for production ETL. ([Databricks Dokumentation][11])

* **Create pipeline components with control flow operators**: Jobs support `If/else` and `For each` tasks, so orchestration logic can live in the workflow DAG instead of being buried inside notebooks. You should also know how task values are passed between tasks to drive branching and iteration. ([Databricks Dokumentation][12])

* **Choose appropriate configs for environments and dependencies**: This topic is about selecting the right compute, task libraries, target overrides, retry/timeouts, and warnings for each workload and environment. At professional level, deployment targets and task-level settings are part of the solution design, not just operational cleanup afterward. ([Databricks Dokumentation][13])

* **Develop unit and integration tests**: `assertDataFrameEqual` and `assertSchemaEqual` are useful for verifying transformations, while `DataFrame.transform` helps keep logic composable and easy to test. You should also know the built-in Databricks Python debugger because debugging notebook and file-based code is part of production engineering on Databricks. ([Apache Spark][14])

## Section 2: Data Ingestion & Acquisition

* **Design ingestion pipelines for many formats and sources**: You should know which Databricks ingestion pattern fits which source: Auto Loader and `read_files` for cloud storage, streaming tables for incremental SQL ingestion, and streaming for sources like Kafka. The supported file-format surface is broad, including Delta, Parquet, ORC, Avro, JSON, CSV, XML, text, and binary. ([Databricks Dokumentation][15])

* **Create an append-only pipeline for batch and streaming with Delta**: Delta can act as both a batch table format and a streaming source/sink, so one architecture can support triggered and continuous-style processing. The exam focus is on idempotent ingestion patterns and append-oriented designs that avoid custom file-tracking hacks. ([Databricks Dokumentation][16])

## Section 3: Data Transformation, Cleansing, and Quality

* **Write efficient Spark SQL and PySpark transformations**: You are expected to be fluent in joins, aggregations, and window functions on large datasets, not just their syntax but their execution impact. Efficient code in Databricks means understanding lazy evaluation, shuffle, and stateful operations so your transformations scale cleanly. ([Databricks Dokumentation][17])

* **Quarantine bad data**: Instead of silently dropping bad records or failing entire pipelines, use expectations, rescued data columns, and explicit filtering/quarantine paths. The important mental model is that bad data handling should be visible, measurable, and recoverable downstream. ([Databricks Dokumentation][18])

## Section 4: Data Sharing and Federation

* **Demonstrate Delta Sharing securely with D2D or D2O**: Delta Sharing supports two main models: Databricks-to-Databricks for Unity Catalog-enabled Databricks recipients, and open sharing for recipients on any platform. You should understand the security/governance differences, especially managed Databricks connections versus token-based open-sharing access. ([Databricks Dokumentation][19])

* **Configure Lakehouse Federation with governance**: Lakehouse Federation lets Databricks query external systems through connections and foreign catalogs while enforcing Unity Catalog governance. The design question is when to federate for governed read access and when to ingest into Delta to unlock full lakehouse optimization. ([Databricks Dokumentation][20])

* **Use Delta Share to share live data to any platform**: Delta Sharing is designed to share governed live lakehouse data without copying it into every consumer platform first. You should connect this topic to interoperability, cross-platform access, and centralized governance/auditing in Unity Catalog. ([Databricks Dokumentation][21])

## Section 5: Monitoring and Alerting

* **Use system tables for observability**: System tables in the `system` catalog centralize billing, audit, compute, lineage, query history, and Lakeflow telemetry. You should know which system tables answer cost, usage, audit, or workload questions and how to join them for observability. ([Databricks Dokumentation][22])

* **Use Query Profiler UI and Spark UI**: Query Profile helps you find slow operators, full scans, pruning behavior, memory use, and expensive parts of SQL execution. Spark UI complements that by exposing stage, task, shuffle, skew, and spill details at execution level. ([Databricks Dokumentation][23])

* **Use REST APIs/CLI to monitor jobs and pipelines**: The CLI and APIs let you list runs, inspect status, retrieve details, and integrate monitoring into external tooling. Professional-level usage means observability should be scriptable, not limited to someone clicking in the UI. ([Databricks Dokumentation][24])

* **Use pipeline event logs to monitor pipelines**: Lakeflow event logs record progress, audit data, expectations, lineage, and operational events for pipelines. They are the main source for pipeline-specific monitoring and a core source for troubleshooting. ([Databricks Dokumentation][25])

* **Use SQL Alerts to monitor data quality**: SQL Alerts schedule a query, evaluate a condition, and notify when thresholds are crossed. They are a natural fit for data-quality checks, SLA breaches, and metric anomalies. ([Databricks Dokumentation][26])

* **Use Jobs UI and Jobs API for notifications**: Jobs support notifications for failures and slow tasks, and notification settings are available through API objects as well. You should also know that task duration or backlog thresholds can emit events that drive those notifications. ([Databricks Dokumentation][24])

## Section 6: Cost & Performance Optimisation

* **Understand why Unity Catalog managed tables reduce overhead**: Managed tables offload maintenance through predictive optimization, metadata caching, automatic cleanup, and tighter governance integration. That reduces the manual burden of file maintenance and makes them the recommended default for most new Databricks tables. ([Databricks Dokumentation][27])

* **Understand deletion vectors and liquid clustering**: Deletion vectors speed up updates, deletes, and merges by avoiding immediate full-file rewrites. Liquid clustering is the modern layout strategy that incrementally organizes data by clustering keys and replaces static partitioning and `ZORDER` for new tables. ([Databricks Dokumentation][28])

* **Understand query optimization techniques on large datasets**: Data skipping, file pruning, compaction, and good clustering reduce how much data is scanned, which is often the first major performance lever. The point is not memorizing feature names, but linking table layout and statistics to real scan reduction. ([Databricks Dokumentation][29])

* **Apply Change Data Feed (CDF)**: CDF exposes row-level inserts, updates, and deletes from Delta tables, which is useful when downstream systems need real change semantics rather than append-only refreshes. It is especially valuable where plain streaming-table patterns are not enough for low-latency propagation of updates and deletes. ([Databricks Dokumentation][30])

* **Use Query Profile to find bottlenecks**: You should be able to read a plan and spot exploding joins, full table scans, poor pruning, high shuffle, skew, spill, or expensive operators. The professional skill is mapping that symptom to a concrete fix, not just noticing the query is slow. ([Databricks Dokumentation][23])

## Section 7: Ensuring Data Security and Compliance

* **Applying data security mechanisms**: This area combines workspace permissions, Unity Catalog privileges, and row/column-level protections so security is enforced at the right layer. The exam is testing whether you can choose the correct control point instead of treating all security as the same kind of grant. ([Databricks Dokumentation][31])

* **Use ACLs to secure workspace objects**: Workspace ACLs protect folders, notebooks, queries, jobs, and other assets, and folder inheritance helps implement least privilege at scale. You should be comfortable granting only the minimum run/read/manage rights each persona needs. ([Databricks Dokumentation][32])

* **Use row filters and column masks**: These are fine-grained Unity Catalog controls that filter rows or redact values at query time based on user context or policy logic. They let one table serve multiple audiences securely without copying the same dataset into separate security-specific copies. ([Databricks Dokumentation][33])

* **Apply anonymization and pseudonymization methods**: This topic is about choosing masking, hashing, tokenization, suppression, or generalization patterns so data stays useful while exposure is reduced. Databricks docs also make the compliance point that when regulation requires true erasure, deletion is safer than relying only on obfuscation. ([Databricks Dokumentation][34])

* **Implement compliant batch and streaming PII masking**: You should be able to design pipelines where privacy rules are enforced during ingestion and transformation, not as a manual downstream cleanup step. In practice, that means consistent masking/detection behavior across both batch and streaming paths. ([Databricks Dokumentation][35])

* **Develop a data purging solution**: Retention compliance requires understanding logical deletion versus physical deletion, plus `VACUUM`, retention periods, and purge steps for metadata-only deletes. For streaming tables and materialized views, you also need to know when extra purge steps are required to physically remove data from storage. ([Databricks Dokumentation][34])

## Section 8: Data Governance

* **Create descriptions and metadata to improve discoverability**: Comments, tags, and other metadata in Unity Catalog make enterprise data easier to search, understand, and trust. Governance here is not only access control; it is also documentation and discoverability. ([Databricks Dokumentation][36])

* **Understand Unity Catalog permission inheritance**: Unity Catalog is hierarchical, so privileges granted on catalogs and schemas can flow to current and future child objects. The important design lesson is that higher-level grants are broad and should be used deliberately, with `USE CATALOG` and `USE SCHEMA` still mattering. ([Databricks Dokumentation][37])

## Section 9: Debugging and Deploying

* **Identify diagnostic information with Spark UI, logs, system tables, and query profiles**: Each tool answers a different layer of the problem: Spark UI for execution details, query profile for operators/plans, system tables for platform telemetry, and logs for runtime evidence. Good debugging starts by gathering the right evidence from the right layer. ([Databricks Dokumentation][23])

* **Analyze errors and remediate failed jobs with repairs and parameter overrides**: Lakeflow Jobs supports repairing failed/skipped tasks and overriding parameters during repair or rerun. That lets you recover faster without replaying everything from scratch. ([Databricks Dokumentation][38])

* **Use event logs and Spark UI to debug Lakeflow and Spark pipelines**: Pipeline event logs show what the declarative pipeline believed happened, while Spark UI shows how the underlying execution behaved. Using both together is the right mental model for debugging declarative ETL. ([Databricks Dokumentation][25])

* **Build and deploy Databricks resources using DABs**: Bundles package code plus resource definitions so jobs, pipelines, and related configs can be validated and deployed as source-controlled assets. This is the main infrastructure-as-code path for Databricks data engineering projects. ([Databricks Dokumentation][39])

* **Integrate Git-based CI/CD with Databricks Git folders**: Git folders support interactive development inside Databricks, while CI/CD workflows keep deployment folders or bundle artifacts synchronized from Git branches. A strong answer distinguishes day-to-day development in Git folders from production deployment through automated pipelines and bundles. ([Databricks Dokumentation][40])

## Section 10: Data Modelling

* **Design scalable data models using Delta Lake**: Data modeling on Databricks is about selecting grain, update patterns, and table design that match ETL and query behavior at scale. Delta Lake gives the transactional storage foundation, but the model still has to fit the workload. ([Databricks Dokumentation][41])

* **Use Liquid Clustering to simplify layout decisions**: Liquid clustering incrementally reorganizes data around clustering keys, which reduces the burden of committing to rigid partition design up front. It is especially useful for large, evolving tables where access patterns change over time. ([Databricks Dokumentation][42])

* **Know the benefits of Liquid Clustering over partitioning and ZOrder**: Compared with partitioning, liquid clustering is less prone to skew and less rigid operationally. Compared with `ZORDER`, it is the recommended modern layout strategy for new Databricks tables. ([Databricks Dokumentation][42])

* **Design dimensional models for analytics**: You should be comfortable with fact/dimension modeling and star-schema thinking for BI-style workloads. Databricks modeling guidance and metric-view documentation both reflect that star-schema mental model for efficient query serving and aggregation. ([Databricks Dokumentation][43])

## What to focus on most

The highest-yield themes across the whole outline are the **trade-offs**: **Lakeflow vs Structured Streaming**, **streaming tables vs materialized views**, **managed tables vs external/federated access**, **liquid clustering vs partitioning/ZORDER**, and **Git folders vs Bundles for deployment**. If you master those decisions, a lot of the exam outline starts to feel connected instead of memorized.

