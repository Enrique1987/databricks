# Data Engineer Professional Objectives and Evidence Matrix

Status: Reviewed planning document

Last reviewed: 2026-08-16

## How to use this matrix

The official exam outline supplies the domains. The mastery questions and evidence bar are specific to this portfolio. A certification result is a milestone; a domain is considered demonstrated here only when reviewed, original evidence is available.

| Official domain | Mastery question | Current evidence | Next evidence | Status |
| --- | --- | --- | --- | --- |
| 1. Python and SQL development | Can a modular data project be built, tested, packaged, debugged, and delivered across environments? | [Professional engineering block 01](01-python-sql-and-testing.md), [installable governed-ingestion package](../../../projects/governed-ingestion/), and [SQL reference](../../reference/databricks-specific-sql.md) | Current-CLI bundle validation, DEV integration run, and staging deployment gate | Reviewed local evidence; platform validation pending |
| 2. Ingestion and acquisition | Can batch and streaming data from varied formats and sources be ingested safely and replayed? | [Bronze ingestion patterns](../../guides/bronze-ingestion-patterns.md) and [governed-ingestion implementation](../../../projects/governed-ingestion/) | DEV initial load, empty rerun, drift, and failure-recovery evidence | Reviewed local evidence; platform validation pending |
| 3. Transformation, cleansing, and quality | Can large datasets be transformed efficiently while bad records are explained, quarantined, and recovered? | Bronze quarantine design | Transformation lab with joins, windows, expectations, metrics, and backfill | Planned |
| 4. Sharing and federation | Can live data be shared or federated with correct governance, networking, cost, and consumer constraints? | None reviewed | Open-sharing and Lakehouse Federation decision guide with a governed lab | Planned |
| 5. Monitoring and alerting | Can cost, utilization, data quality, jobs, pipelines, and query behavior be observed and acted upon? | Operational requirements in the Bronze guide and compute ADR | System-tables observability project, alerts, SLOs, and incident runbook | Partial |
| 6. Cost and performance optimization | Can bottlenecks be measured and improved without trading away reliability or governance? | [Compute strategy ADR](../../architecture/adr-001-compute-strategy.md) | Spark UI and query-profile lab covering skew, shuffle, spill, file layout, and Photon | Partial |
| 7. Security and compliance | Can least privilege, masking, pseudonymization, retention, and deletion be applied to batch and streaming systems? | Security requirements in existing reviewed documents | PII pipeline with row filters, column masks, purge workflow, and access tests | Planned |
| 8. Data governance | Can ownership, metadata, permission inheritance, lineage, auditability, and environment boundaries be defended? | Unity Catalog controls in existing reviewed documents | Unity Catalog landing-zone design and governed data-product implementation | Partial |
| 9. Debugging and deployment | Can failed workloads be diagnosed, repaired, promoted, rolled back, and operated through code? | [Professional engineering block 01](01-python-sql-and-testing.md) and the governed-ingestion multi-environment bundle | Automated non-production deploy, job repair exercise, and pipeline event-log investigation | Partial |
| 10. Data modeling | Can Delta and dimensional models be designed for scale, change, serving patterns, and query efficiency? | Medallion decisions in the Bronze guide | SCD/CDC lab, dimensional warehouse model, and liquid-clustering benchmark | Planned |

## Cross-domain proof bar

Every implementation promoted from this matrix should include:

- requirements and non-functional constraints;
- alternatives and an explicit decision;
- runnable code and automated checks;
- a failure or degraded-mode exercise;
- governance and security controls;
- observability and recovery guidance;
- performance and cost evidence;
- limitations and teardown instructions; and
- current primary sources.

## Source

The domain names are based on the [Databricks Certified Data Engineer Professional exam guide current for this review](https://www.databricks.com/sites/default/files/2025-11/databricks-certified-data-engineer-professional-exam-guide-november-30-2025_0.pdf). This matrix does not reproduce exam questions or claim to be an official Databricks curriculum.
