# Data Engineer Professional Legacy Knowledge Summary

Status: Reviewed planning summary; not a technical reference

Last reviewed: 2026-08-16

## Purpose

This document answers one question: what knowledge exists in the historical notes, and what should be built from it next?

It summarizes capabilities at domain level. It does not certify that every legacy claim is correct, reproduce exam questions, or publish third-party course content. Reviewed technical claims live in the linked guides, ADRs, and projects instead.

## Domain map

| Official domain | Knowledge represented in the notes | Current public evidence | Main gap | Decision |
| --- | --- | --- | --- | --- |
| 1. Python and SQL development | Package structure, Bundles, CLI, REST API, Python functions, UDFs, testing, SQL and PySpark | [Engineering block 01](01-python-sql-and-testing.md) and governed-ingestion package | DataFrame equality tests, debugger exercise, pipeline-specific tests, and authenticated deployment | **Partly promoted** |
| 2. Ingestion and acquisition | Auto Loader, batch versus streaming, Bronze patterns, formats, triggers, schema evolution, Simplex and Multiplex designs | [Bronze ingestion guide](../../guides/bronze-ingestion-patterns.md) and governed-ingestion implementation | Format compatibility, message-bus ingestion, file events, and measured replay | **Partly promoted** |
| 3. Transformation, cleansing, and quality | Joins, windows, watermarks, aggregation, CDC/CDF, expectations, deduplication, quarantine, and SCD logic | Quarantine and rescue design in reviewed ingestion assets | A runnable late-data and CDC failure lab with bad-record metrics and backfill | **Rewrite next** |
| 4. Sharing and federation | Delta Sharing concepts and sharing identifiers | No reviewed implementation | Databricks-to-Databricks, open sharing, Lakehouse Federation, networking, governance, and cost | **Rewrite from first principles** |
| 5. Monitoring and alerting | Spark UI, query profile, cluster metrics, job monitoring, and logging | Operational requirements in current guides and ADR | System tables, pipeline event logs, SQL alerts, job notifications, SLOs, and incident response | **Rewrite as observability project** |
| 6. Cost and performance optimization | Partitioning, Z-ordering, liquid clustering, predictive optimization, deletion vectors, Photon, skew, shuffle, spill, file size, and compute selection | Compute ADR and performance requirements | Reproducible benchmarks, query-profile evidence, cost measurements, and current managed-table behavior | **Rewrite as measured lab** |
| 7. Security and compliance | PII, hashing, dynamic views, ACLs, least privilege, CDF-based propagation, retention, and deletion | Security constraints in reviewed architecture | Row filters, column masks, tokenization choices, compliant purge, access tests, and audit evidence | **Rewrite as governed pipeline** |
| 8. Data governance | Unity Catalog, grants, isolation, metadata, lineage, managed data, and access control | Unity Catalog controls in current assets | Permission inheritance, workspace bindings, ownership, discoverability, lineage, and audit implementation | **Rewrite as landing-zone project** |
| 9. Debugging and deployment | Multi-task jobs, CLI, Bundles, relative imports, CI/CD, environment promotion, Spark diagnostics, and retries | Engineering block 01 and multi-environment governed-ingestion bundle | Job repair, parameter overrides, event-log diagnosis, rollback, OIDC deployment, and staging gate | **Partly promoted** |
| 10. Data modeling | Bronze/Silver/Gold, CDC, CDF, SCD Type 2, deduplication, Delta layout, and serving tables | Medallion decisions in the Bronze guide | Dimensional model, business grain, facts and dimensions, late-arriving dimensions, SCD tests, and benchmark | **Rewrite as modeling lab** |

## What the notes demonstrate

The historical material has broad coverage. It shows repeated engagement with production-relevant subjects rather than a narrow collection of exam facts:

- incremental and streaming processing;
- schema drift and bad-data handling;
- CDC, CDF, SCD, and downstream propagation;
- Spark and Delta performance behavior;
- PII protection and governance;
- deployment automation and multi-environment delivery; and
- operational diagnosis through Spark and query tooling.

The weakness is evidence, not topic breadth. Most legacy sections state features or show isolated snippets without a reproducible workload, explicit assumptions, failure exercise, security boundary, measured result, or teardown. The portfolio should therefore convert breadth into fewer, deeper artifacts.

## Required terminology and architecture corrections

Every rewrite must check these historical patterns:

| Legacy pattern | Current rewrite rule |
| --- | --- |
| Delta Live Tables or `DLT` used as the primary name | Use the current Spark Declarative Pipelines or Lakeflow terminology from the referenced current documentation; mention former names only when necessary for migration context |
| Databricks Asset Bundles used as the primary name | Use **Declarative Automation Bundles**, noting the former name once when it aids discovery |
| DBFS mounts and `/mnt` paths as default production storage | Prefer Unity Catalog volumes, managed tables, or governed external locations unless a documented compatibility case requires otherwise |
| Static claim that one compute type is always best | Decide from workload, isolation, dependency, latency, performance, governance, and cost requirements |
| Fixed partitioning rules or Z-ordering as universal defaults | Compare current managed-table optimization and liquid clustering using measured workload evidence |
| Generic exactly-once claim | State the source, checkpoint, sink, replay, and upstream idempotency assumptions |
| Dynamic views as the only masking solution | Compare current row filters, column masks, views, privileges, and consumer requirements |
| Ganglia as the main monitoring model | Prioritize current system tables, query profile, Spark UI, pipeline event logs, alerts, and job telemetry |
| Percentage savings or performance claims without a run record | Remove or reproduce with workload, environment, time, cost basis, and limitations |
| Control-plane and data-plane statements presented as universal | Distinguish classic and serverless architecture and verify cloud-specific behavior |

## Highest-value next artifact

The next technical PR should be a **streaming and CDC failure lab** spanning domains 1, 3, 5, 9, and 10. It should include:

- synthetic ordered and out-of-order change events;
- event-time windows and a justified watermark;
- stream-static and stream-stream join constraints;
- CDC application with current pipeline APIs or a documented Delta alternative;
- late, duplicate, deleted, and malformed records;
- quarantine and observable data-quality metrics;
- checkpoint-preserving restart and an isolated backfill;
- unit tests plus Databricks integration gates; and
- measured state, latency, shuffle, and cost observations.

This lab converts the densest useful part of the legacy notes into evidence while avoiding third-party examples.

## Subsequent sequence

1. performance investigation with Spark UI, query profile, skew, shuffle, spill, file layout, and cost;
2. privacy and compliant purge pipeline with row filters, masks, pseudonymization, retention, and access tests;
3. sharing and federation decision guide with a sanitized governed lab;
4. Unity Catalog landing zone and discoverable data product; and
5. dimensional and Delta modeling lab with SCD, late-arriving data, and liquid-clustering measurements.

## Source boundary

This summary was derived from the topic coverage in the two repository drafts and the structural inventory of the private archive. The [legacy notes audit](legacy-notes-audit.md) records the file-level families and decisions. The [source and practice-question policy](source-and-practice-policy.md) remains authoritative for any future migration.

## Primary references

- [Databricks Certified Data Engineer Professional exam guide current for this review](https://www.databricks.com/sites/default/files/2025-11/databricks-certified-data-engineer-professional-exam-guide-november-30-2025_0.pdf)
- [Developer best practices on Databricks](https://docs.databricks.com/aws/en/developers/best-practices)
- [Spark Declarative Pipelines](https://docs.databricks.com/aws/en/ldp/)
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
