# Databricks Platform Capability Map

Status: **Reviewed**

Last reviewed: 2026-09-03

## Purpose and assumptions

This document places recent Databricks capabilities in their architectural layers so that unlike features are not compared as interchangeable product announcements. It is intended for architects and senior data engineers evaluating platform boundaries. Availability, cloud support, pricing, and Preview or Beta status must be rechecked before a production decision.

## Capability map

| Layer | Capability | Architectural role | Current decision note |
| --- | --- | --- | --- |
| Operational data | Lakebase | Managed PostgreSQL-compatible OLTP within the Databricks platform | Evaluate transaction, extension, regional, recovery, and workload limits against the application SLO |
| Ingestion and change propagation | Lakebase Change Data Feed | Captures Postgres WAL changes into Unity Catalog managed Delta history tables | Public Preview; changes are flushed in batches of about 15 seconds, so it is not a synchronous replication path |
| Data representation | `VARIANT` | Native representation for flexible semi-structured values | Keeps Bronze flexible but does not replace typed Silver contracts |
| Physical storage | Parquet v2 | More efficient encodings, page metadata, and timestamp representation | Runtime 18.1+; new writes use v2 after enablement, while existing files require an explicit rewrite |
| Governance | Unity Catalog ABAC | Applies row filters, column masks, and supported dynamic grants from governed tags | Design the tag taxonomy and policy ownership before broad rollout |
| Stream processing | Real-time mode | Executes Structured Streaming with millisecond-level processing latency | Requires dedicated compute and workload benchmarking; micro-batch remains preferable for ordinary ETL |
| Query serving | Lakehouse Real-Time (Lakehouse//RT) | Serverless, sub-second, high-concurrency analytical reads over Unity Catalog data | Beta; read-only with material SQL, table, connectivity, network, and governance limitations |

## Lakebase: an operational boundary, not a universal database

Lakebase expands Databricks from analytical workloads into managed Postgres for application transactions. Its native Change Data Feed can publish inserts, updates, deletes, and update pre/post-images from the Postgres write-ahead log into Unity Catalog managed Delta tables.

```text
Application
    |
    v
Lakebase Postgres (OLTP)
    |
    | WAL-based Lakebase Change Data Feed
    v
Unity Catalog managed Delta history tables
    |
    v
Lakeflow / Structured Streaming / SQL consumers
```

This can remove an external CDC component for suitable architectures, but it does not erase the OLTP/OLAP distinction. Confirm application latency, transactional semantics, connection behavior, extensions, high availability, recovery objectives, and CDF lag rather than selecting it only for platform consolidation.

The original fixed-size product, Lakebase Provisioned, was upgraded to the autoscaling Lakebase platform in 2026. Current Lakebase adds autoscaling, scale-to-zero, branching, and instant restore; use the current name unless discussing legacy configuration.

## Real-time processing versus real-time serving

These capabilities solve different problems:

```text
Incoming events                                  Governed tables
      |                                                |
      v                                                v
Real-time mode                                  Lakehouse//RT
process and react                               query and serve
      |                                                |
      v                                                v
decisions, alerts, state                       apps, operational BI
```

Real-time mode is a Structured Streaming trigger for operational processing. Databricks documents end-to-end latency as low as five milliseconds for suitable workloads, but the design trades toward dedicated resources, less frequent checkpointing for longer batches, and potentially longer replay after failure. Benchmark the complete source-to-sink path; do not treat the minimum published latency as an SLO.

Lakehouse//RT serves selective analytical SQL reads with sub-second latency and high concurrency. During Beta it is read-only, uses the Statement Execution API, supports a constrained set of Unity Catalog table types, and does not support ABAC. It is therefore a candidate for operational analytics and application-facing reads, not a drop-in replacement for transactional writes, full-text search, caching, or every existing serving database.

## ABAC: policy follows governed metadata

ABAC complements object-level grants by evaluating governed tags through centrally scoped policies. For example, a `data_classification = pii` tag can activate a column-mask policy across many matching tables instead of relying on repeated manual configuration.

Policy design should separate:

- the governed tag taxonomy and who may assign tags;
- policy scope at catalog, schema, or table level;
- row-filter and column-mask logic;
- supported dynamic GRANT policies;
- audit, performance, exceptions, and conflict handling.

A single policy can scale enforcement, but a wrong inherited tag or overly broad policy can also scale a mistake. Treat taxonomy changes as governed production changes.

## Parquet v2: a physical optimization

Parquet v2 changes the file representation beneath compatible Delta Lake and Iceberg tables through newer encodings, v2 page headers, improved page statistics/indexes, and `INT64` timestamps. Logical schemas and SQL consumers can remain unchanged.

Databricks can automatically upgrade compatible Unity Catalog managed tables. After manual enablement, subsequent writes use v2; Parquet v1 and v2 files may coexist, and old files are not rewritten automatically. `REORG TABLE ... APPLY (SET PARQUET ...)` can rewrite existing Delta files on Runtime 18.2+.

Check external Iceberg and OpenSharing reader compatibility before enabling v2. The optimization is valuable only if end-to-end interoperability remains acceptable.

## Platform selection rule

Prefer an integrated Databricks capability when it meets the workload SLO and materially reduces integration, security, operations, and skill overhead. Retain a specialist when its advantage in search semantics, caching latency, event guarantees, transactional behavior, or isolation is large enough to justify another production system.

That decision belongs in an architecture decision record with workload evidence, cost, failure modes, portability, and an exit path—not in a generic rule to use either one platform or best-of-breed tools everywhere.

## Primary sources

- [Lakebase Postgres](https://docs.databricks.com/aws/en/oltp/projects/postgres)
- [Lakebase Change Data Feed](https://docs.databricks.com/aws/en/oltp/projects/lakebase-cdf)
- [Real-time mode concepts](https://docs.databricks.com/aws/en/structured-streaming/real-time/concepts)
- [Lakehouse Real-Time](https://docs.databricks.com/gcp/en/compute/sql-warehouse/real-time)
- [Unity Catalog attribute-based access control](https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac)
- [Parquet v2](https://docs.databricks.com/aws/en/tables/features/parquet-v2)
