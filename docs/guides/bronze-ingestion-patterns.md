# Bronze ingestion patterns in Databricks

Status: **Reviewed**

Last reviewed: 2026-08-16

This guide provides a practical decision framework for landing source data in a Bronze layer on Databricks. It favors managed capabilities, makes ingestion state explicit, and separates raw capture from Silver-layer business logic.

> [!IMPORTANT]
> An ingestion guarantee is only meaningful when its boundary is explicit. File discovery, source offsets, the Delta sink, and downstream consumption can each have different delivery semantics. Validate the complete path for the specific connector, source, cloud, and runtime.

## Scope

Use this guide to select a pattern for:

- cloud object storage;
- operational databases and data warehouses;
- upstream Delta tables;
- SaaS applications and REST APIs; and
- shared or federated data that might not require ingestion.

This guide does not define Silver transformations, data products, or source-specific network and authentication configuration.

## Bronze contract

A durable Bronze implementation should establish these properties before production:

1. **Source fidelity** — preserve the source payload with minimal interpretation. Cast, deduplicate, standardize, and apply business rules in Silver.
2. **Append-oriented history** — keep arrivals or change events so a downstream table can be rebuilt. If the source only exposes current state, record the snapshot boundary.
3. **Provenance** — add an ingestion timestamp, source identifier, run or batch identifier, and the native source position when available. For files, retain relevant `_metadata` fields.
4. **Replayability** — document how to replay a bounded interval without silently duplicating data or losing previously accepted records.
5. **Schema policy** — choose whether new columns are accepted, stop the pipeline, or are rescued for review. Do not allow uncontrolled type changes.
6. **Failure isolation** — quarantine malformed or policy-violating records without hiding the failure rate.
7. **Ownership and retention** — name the owner of source access, checkpoints, state, tables, alerts, and retention policies.

## Choose the most managed suitable pattern

Start at the top of this list and move down only when the source or required behavior is unsupported:

1. Use **OpenSharing** when a provider can share governed data and a durable local Bronze copy is not required.
2. Use a **Lakeflow Connect managed connector** for a supported SaaS application, database, or file source.
3. Use **Auto Loader** for incremental ingestion from cloud object storage.
4. Use **`COPY INTO`** for simple, bounded file loads with modest operational requirements.
5. Use a **Lakeflow Connect query-based connector** when a database table has a reliable, monotonically increasing cursor.
6. Use a **Lakeflow Connect CDC connector** when database inserts, updates, and deletes must be captured with managed state.
7. Build custom Spark, JDBC, or API ingestion only when a managed option cannot meet the requirement.

Lakehouse Federation is a governed query path, not a durable Bronze ingestion pattern. Use it for live, read-only access or exploration; materialize data only when isolation, history, performance, or replay requirements justify a copy.

## Decision matrix

| Source and requirement | Preferred pattern | State boundary | Deletes | Main constraint |
| --- | --- | --- | --- | --- |
| Supported SaaS source | Lakeflow Connect managed connector | Managed by the connector | Connector-specific | Regional and connector feature availability |
| Supported database with low-latency changes | Lakeflow Connect CDC connector | Managed gateway and pipeline state | Yes, when supported by the source connector | Source permissions, networking, staging, and serverless cost |
| Database table with an increasing cursor | Lakeflow Connect query-based connector | Cursor or high-water mark | No, unless the query emits tombstones | Cursor must be stable and monotonically increasing |
| Many or continuously arriving cloud files | Auto Loader | Checkpoint plus schema location | Not applicable | Checkpoint durability and immutable-file assumptions |
| Small or bounded cloud-file delivery | `COPY INTO` | Files already recorded as loaded | Not applicable | Less suitable for high-scale discovery and complex schema drift |
| Upstream Delta changes | Change Data Feed (CDF) | Table version or timestamp | Yes, as change events | CDF is transient within table retention |
| Unsupported API or protocol | Custom job | Explicit cursor, token, or time window | Source-specific | You own retries, rate limits, state, observability, and replay |
| Governed data that should remain at the source | OpenSharing or Lakehouse Federation | Provider or remote system | Reflected by the source | Not a locally retained Bronze history |

## Pattern 1: Auto Loader for cloud files

Use Auto Loader when files arrive incrementally, the number of objects can grow, late arrivals are expected, or schema drift needs controlled handling. Auto Loader records discovered files in its checkpoint and provides exactly-once processing when writing to Delta under the documented assumptions.

Use a separate checkpoint and schema location for each ingestion stream. Keep both outside lifecycle policies that can delete active state. The default assumes files are immutable; enabling overwrite processing can cause the same logical data to be ingested more than once.

```python
from pyspark.sql import functions as F

source_path = "/Volumes/main/landing/orders/incoming"
schema_path = "/Volumes/main/operations/autoloader/orders/schema"
checkpoint_path = "/Volumes/main/operations/autoloader/orders/checkpoint"

orders = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_path)
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("rescuedDataColumn", "_rescued_data")
    .load(source_path)
    .select(
        "*",
        F.col("_metadata.file_path").alias("_source_file"),
        F.col("_metadata.file_modification_time").alias("_source_modified_at"),
        F.current_timestamp().alias("_ingested_at"),
    )
)

query = (
    orders.writeStream
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable("main.bronze.orders_raw")
)

query.awaitTermination()
```

Operational decisions:

- Alert on non-empty `_rescued_data`; a rescued record is evidence of drift, not a successful schema contract.
- Decide whether a newly inferred column should stop and restart the stream after review or be added automatically.
- Preserve file path and modification time, but do not use them alone as a business key.
- Test a checkpoint restore and a bounded replay before production.

## Pattern 2: `COPY INTO` for simple file loads

Use `COPY INTO` for scheduled or ad hoc ingestion when the source is a bounded set of immutable files and operational simplicity matters more than scalable discovery. By default, Databricks tracks previously loaded files and skips them on a retried command. That makes the file-loading operation retriable; it does not prove end-to-end exactly-once delivery if producers overwrite files or downstream logic duplicates records.

```sql
CREATE TABLE IF NOT EXISTS main.bronze.orders_raw (
  order_id STRING,
  customer_id STRING,
  order_timestamp TIMESTAMP,
  amount DECIMAL(18, 2),
  _rescued_data STRING
);

COPY INTO main.bronze.orders_raw
FROM '/Volumes/main/landing/orders/incoming'
FILEFORMAT = JSON
FORMAT_OPTIONS (
  'rescuedDataColumn' = '_rescued_data'
)
COPY_OPTIONS (
  'mergeSchema' = 'true'
);
```

Use Auto Loader instead when directory listing, arrival volume, latency, or schema evolution becomes operationally significant. Do not use `force = true` as a routine retry mechanism; it intentionally allows already-loaded files to be processed again.

## Pattern 3: Lakeflow Connect for databases and SaaS

Prefer a managed connector when the source is supported. Managed SaaS connectors can handle authentication, incremental reads, schema evolution, and retries. Managed database CDC connectors add gateway and pipeline state to capture source changes. Query-based connectors incrementally read rows using a cursor or high-water mark and can publish append, SCD Type 1, or SCD Type 2 targets depending on the connector configuration.

Before selecting the connector, verify:

- exact source, region, authentication, network, and serverless-compute support;
- required database logs, replication slots, permissions, and retention;
- whether deletes, schema changes, and historical backfills are supported;
- the failure behavior when the source cursor is reset or a log position expires;
- the staging-volume and gateway ownership model; and
- expected ingestion and source-system cost.

A custom JDBC watermark table should be an exception, not the default. If it is unavoidable, the cursor must be stable and monotonically increasing, overlapping windows must be deduplicated downstream, and the state update must not advance before the landed batch is durable.

## Pattern 4: Delta Change Data Feed

Use CDF when the upstream Delta table is under your control and downstream consumers need row-level inserts, updates, and deletes. Record the starting table version or timestamp and keep a durable checkpoint for streaming consumers.

```python
from pyspark.sql import functions as F

changes = (
    spark.readStream
    .option("readChangeFeed", "true")
    .table("main.upstream.customers")
    .withColumn("_ingested_at", F.current_timestamp())
)

query = (
    changes.writeStream
    .option(
        "checkpointLocation",
        "/Volumes/main/operations/cdf/customers/checkpoint",
    )
    .toTable("main.bronze.customers_cdf")
)
```

CDF records are not a permanent audit log: they follow the source table's retention lifecycle. If consumers need longer recovery or audit history, archive the change events in a durable table before the source versions can be vacuumed.

## Pattern 5: custom API ingestion

Build a custom API job only when no supported managed connector meets the requirement. Store the raw response and enough request context to reproduce or explain it. The ingestion state normally includes a vendor cursor, pagination token, source update time, or bounded request window.

A production implementation needs:

- secrets in Databricks secrets or an approved identity integration, never in code;
- bounded exponential backoff with explicit handling for `429` and `5xx` responses;
- a maximum page count or request window to prevent infinite pagination;
- atomic state progression after the corresponding raw payload is durable;
- an idempotency key or downstream duplicate model;
- rate-limit, latency, record-count, and cursor-staleness metrics; and
- a documented backfill and replay endpoint strategy.

## Operational acceptance checklist

Do not promote an ingestion pipeline until these controls are evidenced:

- [ ] Source owner, pipeline owner, and on-call route are recorded.
- [ ] Unity Catalog objects, connections, external locations, and service principals follow least privilege.
- [ ] Secrets and personal data are absent from notebooks, logs, fixtures, and commits.
- [ ] Freshness, completeness, duplicate, rescued-record, and failure-rate SLOs have alerts.
- [ ] Checkpoint, schema, cursor, and source-log retention exceed the recovery objective.
- [ ] Delete behavior and late-arriving data behavior are tested.
- [ ] A bounded replay has been executed without corrupting the target.
- [ ] A quarantine path has an owner and resolution workflow.
- [ ] Backfill resource limits and cost expectations are documented.
- [ ] Silver consumers can distinguish initial snapshots, incremental batches, and replays.

## Anti-patterns

- Deleting a checkpoint to fix a stalled stream without first defining the replay boundary.
- Treating a mutable filename as a unique event identifier.
- Advancing a custom watermark before the raw batch is durable.
- Applying business deduplication or destructive type coercion in Bronze.
- Treating federation or shared data as retained history when the provider controls availability.
- Relying on CDF after its source-table retention window.
- Building custom JDBC or REST ingestion before checking supported Lakeflow Connect connectors.
- Claiming exactly-once delivery without naming the source, state store, sink, and overwrite assumptions.

## Primary references

- [Ingest data into a Databricks lakehouse](https://docs.databricks.com/aws/en/ingestion/overview)
- [Lakeflow Connect managed connectors](https://docs.databricks.com/aws/en/connect/managed-ingestion)
- [Managed SaaS connectors](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/saas-overview)
- [Managed database CDC connectors](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/cdc-overview)
- [Query-based database connectors](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/query-based-overview)
- [Auto Loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader)
- [Auto Loader production considerations](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/production)
- [`COPY INTO`](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into)
- [Delta Change Data Feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed)
- [Medallion lakehouse architecture](https://docs.databricks.com/aws/en/lakehouse/medallion)
- [Lakehouse Federation and external connections](https://docs.databricks.com/aws/en/connect)
