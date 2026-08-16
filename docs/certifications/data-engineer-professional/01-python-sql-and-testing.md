# Professional Engineering Block 01: Python, SQL, Dependencies, and Testing

Status: **Reviewed design; Databricks execution pending**

Last reviewed: 2026-08-16

## Outcome

This block turns the first Professional domain into engineering evidence. The companion [governed-ingestion project](../../../projects/governed-ingestion/README.md) is not a notebook demonstration: it is a small deployable product with an importable Python package, a wheel artifact, explicit runtime boundaries, parameterized SQL validation, local unit tests, and a multi-environment Declarative Automation Bundle.

Local evidence proves the pure-Python contracts and the wheel contents. It does not prove workspace authentication, bundle schema compatibility, serverless execution, Unity Catalog permissions, Auto Loader behavior, or end-to-end data quality. Those claims remain pending until the workspace evidence checklist is completed.

## Artifact map

| Concern | Artifact | Reason |
| --- | --- | --- |
| Deployment contract | `projects/governed-ingestion/databricks.yml` | Builds one versioned wheel and separates DEV from PROD |
| Job contract | `resources/ingestion.job.yml` | Defines bounded execution, parameters, retries, concurrency, and run identity |
| Configuration | `src/governed_ingestion/config.py` | Validates paths, identifiers, formats, and workload limits without Spark |
| Pipeline | `src/governed_ingestion/pipeline.py` | Builds the Auto Loader read, metadata projection, and Delta write |
| CLI boundary | `src/governed_ingestion/cli.py` | Converts job parameters into a validated configuration |
| Package metadata | `pyproject.toml` | Defines the artifact name, Python floor, build tools, and entry points |
| SQL controls | `sql/validate_ingestion.sql` | Provides safe, reusable reconciliation and rescued-data diagnostics |
| Automated checks | `tests/test_ingest_files.py` | Exercises safety invariants without pretending to emulate Databricks |

## Python design

### Keep orchestration thin

The job entry point contains no business logic. It parses arguments, obtains the active Spark session, and delegates to an importable function. Configuration validation has no `pyspark` import, so it is fast to test on every pull request. Spark functions are imported lazily at the execution boundary and can be replaced by test doubles.

This separation creates three useful failure domains:

1. invalid user or job input fails before a stream starts;
2. source-schema collisions fail before the sink is opened; and
3. platform failures occur only after the local contracts have passed.

### Prefer expressions over Python UDFs

For row and column transformations, use this decision order:

1. built-in Spark or SQL functions;
2. a SQL UDF when a governed reusable function is justified;
3. a pandas UDF for vectorized Python that cannot be expressed with built-ins; and
4. a scalar Python UDF only when the alternatives do not fit.

Built-ins preserve Catalyst visibility and avoid Python serialization. A UDF is not automatically wrong, but its governance, dependency, performance, and failure behavior must be measured. The ingestion project therefore uses built-in column expressions for file metadata and does not introduce a UDF.

### Make unsafe states unrepresentable early

`IngestionConfig.validate()` rejects:

- non-Unity Catalog volume paths;
- checkpoint or schema state stored under the source path;
- a shared checkpoint and schema directory;
- malformed three-part table identifiers;
- unsupported input formats; and
- non-positive workload bounds.

These checks are guardrails, not authorization. Unity Catalog grants and the production run-as identity remain the enforcement layer.

## SQL design

SQL belongs in version-controlled `.sql` files when it is part of the product contract. The validation script uses a named parameter and `IDENTIFIER(:target_table)` instead of constructing an identifier with Python string interpolation. This keeps values separate from SQL text and makes the target table explicit at execution time.

The three queries answer different operational questions:

- **metadata gate:** can every row be traced to a source file and ingestion time?
- **source reconciliation:** how many records arrived per source file, and when?
- **drift investigation:** which records were rescued and require a schema decision?

A zero rescued-row count is not the universal success condition. Rescue mode is designed to preserve unexpected data for investigation. Promotion to Silver needs an explicit policy for accepted evolution, quarantine, or rejection.

## Dependency contract

| Dependency class | Current decision | Control |
| --- | --- | --- |
| Python standard library | Used for configuration, CLI, types, and tests | Minimum Python version in `pyproject.toml` |
| PySpark | Supplied by Databricks compute | Deliberately absent from project dependencies; do not install PySpark on serverless compute |
| Application libraries | None in this increment | Add only to `project.dependencies`, constrain versions, test the resolved environment, and rebuild the wheel |
| Build tools | Setuptools and wheel | Constrained in `build-system`; required only on the build runner |
| Databricks CLI | Deployment tool, not an application library | Bundle requires CLI `0.218.0` or later; upgrade and validate before deployment |

An empty application dependency list is intentional. Adding a library merely to demonstrate dependency management would increase supply-chain and compatibility risk without solving a workload requirement.

For every future dependency change:

1. document the feature that requires it and reject an unnecessary alternative;
2. constrain the version range and review transitive dependencies;
3. increment the package version and build a new wheel rather than modifying a deployed environment in place;
4. run unit, bundle, and staging integration gates; and
5. record runtime, security, performance, and rollback evidence.

The bundle installs the project wheel through the serverless job environment. The current artifact is pure Python (`py3-none-any`), avoiding the architecture mismatch that native wheels can encounter when serverless compute changes between `aarch64` and `x86_64`. Generated wheels, build directories, credentials, and local environments are excluded from Git; source and configuration remain the source of truth.

## Testing model

| Layer | What it catches | Current state | Promotion gate |
| --- | --- | --- | --- |
| Unit | Package metadata, invalid paths and identifiers, drift policy, reserved-column collisions, CLI mapping, stream assembly | 12 local tests passing | Required on every PR |
| Package | Missing modules or entry-point metadata | Wheel builds locally and contains both `console_scripts` and Databricks `packages` entry points | Build a fresh artifact from the commit |
| Bundle | Invalid resource schema, variables, targets, and artifact references | Pending: local CLI is below the declared minimum | Validate DEV and PROD with current authenticated CLI |
| Integration | Auto Loader state, Delta writes, permissions, idempotent empty rerun, drift rescue, and recovery | Pending | Deploy to isolated DEV and capture run/table evidence |
| Staging | Representative identity, data boundary, alerts, throughput, and rollback | Not yet implemented | Required before any production claim |

Mocks verify the calls this module owns; they do not verify Spark semantics. A test suite that mocks Databricks and then claims end-to-end correctness would be misleading.

## Debugging sequence

When a run fails, reduce uncertainty in this order:

1. reproduce configuration validation locally with the exact non-secret parameters;
2. inspect the job task output and identify whether the failure is build, install, authorization, read, transform, or write related;
3. verify the run-as identity and Unity Catalog privileges for the exact objects;
4. inspect Auto Loader checkpoint and schema state without deleting either;
5. inspect rescued records and Delta table history;
6. rerun with preserved state after repairing the cause; and
7. use an isolated table and new checkpoint for a deliberate replay.

Deleting a checkpoint is not a generic repair. It changes the processing history and can duplicate data.

## Original review scenarios

These prompts test reasoning without reproducing certification questions:

1. A team wants to add `pyspark` to the serverless environment. Explain why this can conflict with the platform runtime and how local type checking can be handled separately.
2. A new JSON field appears and lands in `_rescued_data`. Decide when to evolve Bronze, quarantine the record, or block Silver, and state what evidence is required.
3. The same wheel passes unit tests but fails in DEV. Classify likely failures by package, bundle, identity, storage, and runtime layers before changing code.
4. A developer proposes a scalar Python UDF for timestamp normalization. Compare it with built-in expressions and define the benchmark needed to justify the UDF.
5. An operator deletes the checkpoint to replay a corrected file into the production table. Identify the duplicate risk and design an isolated replay.

## Remaining evidence

- [x] Importable `src/` package with a thin task entry point.
- [x] Reproducible wheel build and inspected entry-point metadata.
- [x] Version-controlled SQL validation with safe identifier binding.
- [x] Unit tests for configuration and pipeline assembly.
- [ ] Current CLI validates both bundle targets.
- [ ] DEV deployment and run are linked to a commit SHA.
- [ ] Initial load, empty rerun, schema drift, and failed-run recovery are captured.
- [ ] A staging gate and automated non-production deployment are implemented.

## Primary references

- [Developer best practices on Databricks](https://docs.databricks.com/aws/en/developers/best-practices)
- [Build a Python wheel with Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/python-wheel)
- [Declarative Automation Bundles library dependencies](https://docs.databricks.com/aws/en/dev-tools/bundles/library-dependencies)
- [Configure the serverless environment](https://docs.databricks.com/aws/en/compute/serverless/dependencies)
- [Python unit testing in the workspace](https://docs.databricks.com/aws/en/files/python-unit-tests)
- [User-defined functions](https://docs.databricks.com/aws/en/udf/)
- [Parameter markers](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-parameter-marker)
