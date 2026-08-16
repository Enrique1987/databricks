# Governed ingestion with Auto Loader

Status: **Reviewed local implementation — workspace execution pending**

Last reviewed: 2026-08-16

This project increment lands immutable JSON or Parquet files into a Unity Catalog Bronze table. It uses Auto Loader with explicit schema and checkpoint state, a rescued-data policy, source metadata, bounded execution, and separate development and production bundle targets.

The Python contracts, package build, entry-point metadata, and repository checks run locally. The bundle has not yet been validated or executed against a Databricks workspace, so this project must not be presented as a completed production reference.

## Problem

A useful ingestion example must demonstrate more than `readStream` and `writeStream`. An operator needs to know:

- where discovery and schema state live;
- what happens when input columns drift;
- which source file produced each row;
- how retries and concurrent runs behave;
- how development and production identities differ;
- how to replay or recover without deleting state blindly; and
- which resources remain after the deployed job is removed.

## Increment scope

This first increment includes:

- an Auto Loader Python task using `Trigger.AvailableNow`;
- Unity Catalog volume paths for the source, checkpoint, and schema state;
- rescue-mode schema evolution;
- file path, file modification time, and ingestion timestamp metadata;
- one serverless Lakeflow Job with bounded retries and concurrency;
- Declarative Automation Bundle targets for DEV and PROD;
- a required production service-principal identity; and
- an installable Python wheel with separate configuration, pipeline, and CLI modules;
- version-controlled, parameterized SQL reconciliation queries; and
- dependency-free local tests for configuration and safety invariants.

It intentionally does not yet include a schedule, file-event notification mode, alert destination, data-quality dashboard, integration test, or automated deployment workflow. Those are follow-up increments, not hidden assumptions.

## Project structure

```text
governed-ingestion/
├── databricks.yml
├── pyproject.toml
├── resources/
│   └── ingestion.job.yml
├── sql/
│   └── validate_ingestion.sql
├── src/
│   ├── governed_ingestion/
│   │   ├── cli.py
│   │   ├── config.py
│   │   └── pipeline.py
│   └── ingest_files.py
└── tests/
    └── test_ingest_files.py
```

`config.py` contains Spark-independent input invariants. `pipeline.py` owns Spark assembly. `cli.py` is the task boundary. The bundle builds this package into a wheel and installs it as the job task library. The standalone launcher remains a convenient source-level entry point, but the deployed job uses the wheel entry point.

The package declares no application dependencies: Databricks supplies PySpark and the example does not need a third-party library. Build-only dependencies are constrained in `pyproject.toml`, and the generated artifact is a platform-neutral `py3-none-any` wheel. Increment the package version whenever deployed code changes so that the serverless environment does not reuse a cached package. See [Professional engineering block 01](../../docs/certifications/data-engineer-professional/01-python-sql-and-testing.md) for the dependency and test-layer decisions.

## Architecture and guarantees

The job reads one immutable source directory, records discovery state in a dedicated checkpoint, and appends records to one Delta table. New or incompatible fields are placed in `_rescued_data` for review rather than silently discarded.

Auto Loader documents exactly-once file processing when the checkpoint is preserved and the sink is Delta. That guarantee does not make an upstream producer idempotent and does not prevent logical duplicates inside different files. The example therefore requires immutable source files and leaves business-key deduplication to Silver.

Reserved output columns:

- `_ingestion_source_file`
- `_ingestion_source_modified_at`
- `_ingestion_recorded_at`
- `_rescued_data`

Input data must not define these names.

## Prerequisites

- A Databricks workspace with Unity Catalog and serverless jobs support.
- Workspace files enabled.
- Databricks CLI `0.218.0` or later, authenticated with OAuth or another approved method.
- Python `3.10` or later with compatible `pip`, `setuptools`, and `wheel` on the build runner.
- Permission to use the target catalog, create or use the schema, read the landing volume, write the operations volume, and create the target table.
- A service-principal application ID and corresponding permissions before any PROD deployment.

The workstation used to author this increment currently has Databricks CLI `0.211.0`. Upgrade it before running bundle validation; do not interpret a local test pass as bundle-schema validation.

## Prepare the DEV data boundary

Run the following as an authorized principal. The example uses managed volumes so it does not embed cloud credentials or storage URLs.

```sql
CREATE SCHEMA IF NOT EXISTS main.governed_ingestion_dev;

CREATE VOLUME IF NOT EXISTS main.governed_ingestion_dev.landing
COMMENT 'Immutable source files for the governed ingestion example';

CREATE VOLUME IF NOT EXISTS main.governed_ingestion_dev.operations
COMMENT 'Auto Loader checkpoint and schema state for the governed ingestion example';
```

Upload immutable JSON records beneath:

```text
/Volumes/main/governed_ingestion_dev/landing/orders/
```

Example input:

```json
{"order_id":"A-100","customer_id":"C-42","amount":"19.95","event_time":"2026-08-16T10:15:00Z"}
```

## Validate locally

From the repository root:

```bash
python -m unittest discover -s projects/governed-ingestion/tests -v
python -m pip wheel --no-cache-dir --no-build-isolation --no-deps \
  --wheel-dir projects/governed-ingestion/dist \
  projects/governed-ingestion
python scripts/check_repository.py
```

The wheel is generated evidence and is ignored by Git. These checks validate pure-Python configuration, package construction, and repository policy. They do not emulate Spark, Auto Loader, Unity Catalog, serverless compute, permissions, or cloud storage.

## Validate, deploy, and run in DEV

From `projects/governed-ingestion` with an authenticated current Databricks CLI:

```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev governed_ingestion_job
```

The DEV target uses development mode and deploys beneath the current user's workspace directory. The job is intentionally unscheduled; running it is an explicit action that can incur compute and storage cost.

Validate the result:

```sql
SELECT
  COUNT(*) AS row_count,
  COUNT_IF(_rescued_data IS NOT NULL) AS rescued_count,
  MIN(_ingestion_recorded_at) AS first_recorded_at,
  MAX(_ingestion_recorded_at) AS last_recorded_at
FROM main.governed_ingestion_dev.orders_raw;

DESCRIBE HISTORY main.governed_ingestion_dev.orders_raw;
```

Then run [`sql/validate_ingestion.sql`](sql/validate_ingestion.sql) in the Databricks SQL editor with the named parameter `target_table` bound to `main.governed_ingestion_dev.orders_raw`. The queries fail visibly on missing lineage metadata, reconcile record counts per source file, and expose rescued records for investigation.

Run the job again without adding a file and verify that the row count does not increase. Then add one new immutable file and verify only that file is processed. Capture both results before changing the project status to **Reviewed**.

## Validate a PROD configuration

The PROD target uses production mode and refuses to resolve without a service-principal application ID:

```bash
databricks bundle validate -t prod \
  --var="prod_service_principal=<application-id>"
```

Before deployment, override the example catalog, schema, and volume paths if the production boundary differs. Confirm that the service principal can read the landing volume, write the operations volume, create the target table, and run the job — and nothing broader.

## Failure recovery and replay

- Do not delete the checkpoint to fix a failed run. Repair the cause and rerun with the same state first.
- Keep checkpoint and schema paths outside source-file lifecycle rules.
- Alert on any non-null `_rescued_data` before downstream promotion.
- If a replay is required, choose a new checkpoint and a new replay table or isolate the replay batch. Reusing the production table with fresh state can append duplicates.
- If a producer overwrites existing filenames, stop the pipeline and define a source correction procedure. This project assumes immutable files.
- `bundle destroy` removes deployed bundle resources; it does not constitute a data-retention or checkpoint-deletion procedure.

## Teardown

First remove the deployed DEV job:

```bash
databricks bundle destroy -t dev
```

The following SQL is destructive. Run it only for the exact DEV objects after confirming that no shared data or active checkpoint depends on them:

```sql
DROP TABLE IF EXISTS main.governed_ingestion_dev.orders_raw;
DROP VOLUME IF EXISTS main.governed_ingestion_dev.operations;
DROP VOLUME IF EXISTS main.governed_ingestion_dev.landing;
DROP SCHEMA IF EXISTS main.governed_ingestion_dev;
```

Dropping managed volumes removes their managed data according to Databricks retention behavior. This teardown is not appropriate for production.

## Evidence required for promotion

- [ ] Current CLI successfully runs `databricks bundle validate` for DEV and PROD.
- [x] Local wheel builds from `pyproject.toml` and contains the expected package entry point.
- [x] Twelve local unit tests cover the package contract, configuration, CLI mapping, schema collisions, and stream assembly.
- [x] Parameterized SQL validation is version controlled with the implementation.
- [ ] DEV deployment is linked to a commit SHA.
- [ ] Initial load, empty rerun, and one-new-file run are recorded.
- [ ] A schema-drift example produces a visible rescued record.
- [ ] A failed run resumes from the preserved checkpoint.
- [ ] Job output and table history contain no secrets or personal data.
- [ ] The production service principal and Unity Catalog grants pass least-privilege review.
- [ ] Compute and storage usage for the sample run are recorded.
- [ ] Teardown is tested only in the isolated DEV boundary.

## Primary references

- [What is Auto Loader?](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader)
- [Configure Auto Loader for production workloads](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/production)
- [Auto Loader schema inference and evolution](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema)
- [What are Declarative Automation Bundles?](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [Bundle configuration](https://docs.databricks.com/aws/en/dev-tools/bundles/settings)
- [Bundle configuration examples](https://docs.databricks.com/aws/en/dev-tools/bundles/examples)
- [Run identity for Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/run-as)
- [Configure compute for Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/compute)
