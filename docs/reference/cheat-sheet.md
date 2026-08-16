# Databricks Cheat Sheet

Status: **Reviewed**  
Last reviewed: 2026-08-16

A compact map of the Databricks Data Intelligence Platform. Availability, naming, and limits can differ by cloud, region, runtime, and Preview status; follow the linked official documentation for implementation details.

## Data and governance

**Unity Catalog** — Governance layer for data and AI assets across workspaces, including permissions, discovery, lineage, auditing, and secure data access.

**Delta Lake** — Open table format and storage layer with ACID transactions, schema controls, time travel, and batch/streaming interoperability.

**Managed and external tables** — Unity Catalog manages governance for both; the key difference is who controls the data lifecycle and storage location.

**Volumes** — Unity Catalog objects for governing non-tabular files. Prefer volumes or external locations to legacy DBFS root patterns.

**OpenSharing** — Open protocol for sharing live data and AI assets without copying them into each recipient's platform. Formerly Delta Sharing; older APIs and billing fields can retain the previous name.

**Row filters and column masks** — Unity Catalog policies implemented with SQL UDFs to enforce row- and column-level access at query time.

## Ingestion and transformation

**Lakeflow Connect** — Managed and standard connectors for ingesting data from SaaS applications, databases, cloud storage, and other sources.

**Auto Loader** — Incremental file ingestion for cloud object storage using the `cloudFiles` source or `read_files()` in streaming tables.

**Lakeflow Spark Declarative Pipelines** — Declarative batch and streaming pipelines with flows, streaming tables, materialized views, expectations, orchestration, and monitoring. Formerly Delta Live Tables (DLT).

**Change Data Feed (CDF)** — Row-level Delta change records for downstream incremental processing; consumers must account for retention.

**Medallion architecture** — A common Bronze/Silver/Gold design pattern, not a mandatory platform hierarchy. Define each layer by contract and business purpose.

## Compute and orchestration

**Serverless compute** — Databricks-managed compute with reduced infrastructure operations; supported features and regional availability vary.

**Classic compute** — Customer-configurable compute used when workload, network, library, or policy requirements need more control.

**SQL warehouses** — Compute optimized for Databricks SQL, BI, dashboards, and SQL applications.

**Lakeflow Jobs** — Orchestration for multi-task workflows, schedules, triggers, dependencies, retries, parameters, and notifications.

**Photon** — Databricks vectorized execution engine for supported SQL and DataFrame workloads.

## Development and delivery

**Declarative Automation Bundles** — Source-controlled definition of code and Databricks resources for testing and deployment across targets. Formerly Databricks Asset Bundles; the CLI command remains `databricks bundle`.

**Git folders** — Workspace integration with remote Git repositories. Formerly called Repos.

**Databricks Connect** — Run Spark code from an IDE against Databricks compute while using local development tools.

**Databricks CLI, SDKs, and REST APIs** — Programmatic interfaces for automation. Prefer workload identity or OAuth-based authentication where supported.

## AI and machine learning

**MLflow** — Open-source lifecycle tooling for experiments, evaluation, models, deployments, and observability; Databricks provides a managed integration.

**Models in Unity Catalog** — Governed model registry with permissions, lineage, aliases, and cross-workspace access.

**Model Serving** — Managed real-time endpoints for custom, foundation, and external models.

**AI Search** — Governed vector, hybrid, and full-text retrieval for AI applications. Formerly Databricks Vector Search.

**Agent Framework and MLflow evaluation** — Tools for building, tracing, evaluating, deploying, and monitoring AI agents.

## Operations

**Data quality monitoring** — Unity Catalog capabilities for anomaly detection and data profiling. Data profiling was formerly called Lakehouse Monitoring.

**System tables** — Unity Catalog system schemas that expose operational data such as billing, audit, lineage, jobs, and warehouse events where enabled.

**Query profile and Spark UI** — Primary tools for diagnosing SQL and Spark execution behavior.

**Predictive optimization** — Managed optimization for supported Unity Catalog managed tables.

**Cluster policies and budgets** — Guardrails for compute configuration and spend; combine them with permissions, tags, system tables, and alerts.

## Official starting points

- [Databricks documentation](https://docs.databricks.com/)
- [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- [Data engineering and Lakeflow](https://docs.databricks.com/aws/en/data-engineering/)
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [Machine learning](https://docs.databricks.com/aws/en/machine-learning/)
- [Build AI agents](https://docs.databricks.com/aws/en/agents/)
