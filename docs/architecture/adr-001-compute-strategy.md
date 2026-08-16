# ADR 001: Compute selection and environment controls

Status: **Reviewed example**

Decision status: **Proposed**

Last reviewed: 2026-08-16

## Context

Databricks offers several compute products with different lifecycle, compatibility, isolation, and operational characteristics. Choosing only by environment — for example, “shared compute in DEV and jobs compute in PROD” — hides the more important questions:

- What task is executing?
- Is the workload interactive, scheduled, streaming, SQL, data engineering, or machine learning?
- Does serverless compute support the required runtime, language, library, API, network, and data-access behavior?
- What identity executes the workload and which Unity Catalog privileges does it receive?
- What startup, latency, isolation, recovery, and cost-attribution requirements apply?

Databricks currently recommends serverless compute for most new workloads and standard access mode for most classic-compute workloads. Some workloads still require classic jobs compute or dedicated access mode, including specific JAR, Spark Submit, RDD, R, GPU, machine-learning runtime, or privileged machine-access cases.

This ADR is a portable reference architecture. It is not an organization-wide policy until owners validate regional availability, security controls, workload compatibility, and cost behavior.

## Decision drivers

The compute decision must optimize, in order:

1. workload compatibility and correctness;
2. identity, data access, network, and isolation requirements;
3. reliability and recovery behavior;
4. operational effort and reproducibility;
5. performance and latency objectives; and
6. measured total cost, including idle time and engineering operations.

Sticker price or DBU rate alone is not sufficient evidence for a compute decision.

## Decision

### 1. Use a serverless-first selection process

For each new workload, select the Databricks-recommended serverless product when it supports the requirements:

| Workload | Default | Fallback or exception |
| --- | --- | --- |
| Interactive SQL, dashboards, and BI | Serverless SQL warehouse | Pro SQL warehouse when serverless is unavailable or incompatible |
| SQL task in a Lakeflow Job | Serverless SQL warehouse | Pro SQL warehouse when required |
| Notebook, Python script, Python wheel, or dbt CLI task | Serverless jobs compute | Classic jobs compute for documented compatibility or network constraints |
| JAR task | Classic jobs compute | Use serverless only after explicit compatibility validation |
| Spark Submit task | Classic jobs compute | No serverless default |
| Lakeflow pipeline | Serverless pipeline | Classic pipeline for unsupported requirements |
| Interactive notebook development | Serverless notebook compute | Classic all-purpose compute when serverless limitations apply |
| R, RDD, GPU, ML Runtime, or privileged host access | Classic dedicated compute | Reassess periodically as platform support changes |

“Fallback” is not a lower-quality option. It means the workload has an evidenced requirement that the default does not satisfy.

### 2. Treat environment controls separately from compute product

DEV, QA, and PROD can use the same compute product while applying different identities, permissions, deployment paths, data, schedules, and service levels.

| Control | DEV | QA | PROD |
| --- | --- | --- | --- |
| Primary activity | Interactive development and isolated test runs | Automated integration and release validation | Scheduled or event-driven production execution |
| Run identity | Named developer for interactive work; test identity for automation | Service principal | Service principal |
| Data access | Synthetic, masked, or least-privilege development data | Controlled pre-production data | Least-privilege production data |
| Change path | Feature branch and developer execution | CI/CD deployment and automated validation | Approved promotion of the same versioned artifact |
| Ad hoc execution | Allowed within development policy | Restricted | Break-glass or explicitly approved |
| Reliability controls | Fast feedback | Production-like recovery tests | Alerts, retries, timeouts, runbook, and SLOs |
| Cost controls | Auto-stop, quotas, and attribution | Attribution and bounded test schedules | Attribution, budgets, capacity review, and anomaly monitoring |

QA should match the production compute class when validating runtime-specific behavior. A deliberate difference must be recorded, because a test on one execution model does not prove another execution model.

### 3. Do not use all-purpose compute as the production job default

Classic all-purpose compute is reserved for interactive development or a documented exception. Production automation should use serverless jobs, classic jobs compute, a SQL warehouse, or Lakeflow pipeline compute according to task type.

This aligns compute lifecycle with execution lifecycle and reduces the risk of:

- jobs inheriting interactive cluster state;
- production libraries drifting through manual installation;
- human activity competing with scheduled workloads;
- an individual user becoming an operational dependency; and
- idle compute continuing after a scheduled run.

### 4. Use standard access mode for classic compute unless dedicated mode is required

Standard access mode is the default for supported general data engineering, SQL analytics, and collaborative data science workloads. Dedicated access mode requires a stated compatibility or isolation reason, such as:

- RDD APIs;
- GPU instances or Databricks Runtime for Machine Learning;
- R language support;
- privileged machine access; or
- a workload not supported on standard compute.

The access mode is a security and compatibility decision, not a synonym for DEV or PROD.

### 5. Make production execution non-human and reproducible

Automated QA and production jobs run as service principals with least-privilege Unity Catalog access. Job ownership and the `Run as` identity are managed independently so a user leaving or changing role does not break execution.

Production definitions are version controlled and promoted through CI/CD using Declarative Automation Bundles, APIs, SDKs, CLI, or an equivalently reviewed deployment path. A manual UI configuration without a reproducible source definition is not the production system of record.

### 6. Govern cost with attribution and evidence

Every workload must be attributable to an environment, product or project, owner, and cost center where supported. Use:

- custom tags for classic compute and SQL warehouses;
- serverless usage policies for serverless attribution, subject to their current availability status;
- `system.billing.usage` for consumption analysis; and
- account or workspace budgets for monitoring and notifications.

Tags must not contain personal or sensitive data. Budgets are monitoring controls and can report with delay; they are not a universal real-time kill switch.

## Selection procedure

Document these answers in the workload design or pull request:

1. **Task type:** notebook, Python, JAR, Spark Submit, SQL, dbt, pipeline, streaming, BI, or ML.
2. **Serverless compatibility:** supported languages, APIs, libraries, runtime behavior, network paths, storage, and maximum duration.
3. **Data plane:** Unity Catalog objects, external connections, credentials, and regional requirements.
4. **Execution identity:** developer, service principal, or approved group; include required privileges.
5. **Lifecycle:** interactive, scheduled, continuous, or triggered batch; define timeout and termination behavior.
6. **Isolation:** shared standard compute or dedicated compute, with the reason for dedicated mode.
7. **Performance:** startup, throughput, concurrency, and latency targets with a representative test.
8. **Recovery:** retries, idempotency boundary, checkpoints, and maximum acceptable interruption.
9. **Cost:** usage attribution, budget owner, and a measured comparison if choosing a non-default product.
10. **Review trigger:** platform support, workload shape, security rule, SLA, or cost change that should reopen the decision.

## Required production controls

- [ ] The task uses the recommended compute type or records an exception.
- [ ] The workload is deployed from a versioned definition.
- [ ] The `Run as` identity is a service principal with least privilege.
- [ ] Unity Catalog-compatible compute and governed data paths are used.
- [ ] Classic compute uses the latest compatible LTS runtime and an approved compute policy.
- [ ] Classic access mode is standard unless a dedicated-mode requirement is evidenced.
- [ ] Retries, timeouts, concurrency, and overlapping-run behavior are explicit.
- [ ] Long-running or streaming behavior is compatible with the selected compute product.
- [ ] Logs and metrics identify the job, task, environment, and run.
- [ ] Cost attribution and a budget owner are configured.
- [ ] QA validates the production compute class or documents the gap.
- [ ] A rollback or compute-fallback path has been tested for critical workloads.

## Consequences

### Benefits

- Compute follows workload requirements instead of a rigid environment label.
- Serverless reduces infrastructure configuration for compatible workloads.
- Classic-compute exceptions remain explicit, supported, and reviewable.
- Production runs are less dependent on interactive state or individual users.
- Identity, cost, and environment controls become auditable.
- QA provides stronger evidence because compute differences are visible.

### Trade-offs

- Teams must maintain a compatibility assessment rather than applying one cluster template everywhere.
- Serverless limitations and regional availability can change, so decisions require periodic review.
- Service principals, Unity Catalog grants, policies, budgets, and deployment automation add initial setup.
- Matching QA and PROD can cost more than a lightweight QA environment, but reduces release uncertainty.
- Some workloads need multiple compute products within one Lakeflow Job.

## Alternatives considered

### Shared classic all-purpose compute in every environment

Rejected as a default. It is simple initially but couples production execution to interactive lifecycle, mutable state, and human access.

### Classic jobs compute for every automated workload

Rejected as a blanket rule. It remains the correct fallback for unsupported workloads, but serverless jobs are the current default for supported task types and remove cluster configuration work.

### Serverless compute for every workload

Rejected as an absolute rule. Serverless has language, API, library, streaming, runtime-duration, networking, and regional limitations. Compatibility must precede preference.

### Separate compute products solely by DEV, QA, and PROD

Rejected. Environment labels determine controls and promotion boundaries, while task requirements determine the compute product. Conflating them creates unnecessary drift and weak test evidence.

## Review triggers

Reopen this ADR when:

- Databricks changes recommended compute for a supported task;
- a serverless limitation blocking a workload is removed;
- the workload adopts RDD, R, GPU, JAR, Spark Submit, continuous streaming, or privileged access;
- network or data-residency requirements change;
- measured cost or performance breaches the agreed threshold;
- QA and PROD stop using equivalent execution behavior; or
- ownership, identity, or Unity Catalog boundaries change.

Review at least every six months even if no trigger is reported.

## Primary references

- [Configure compute for Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/compute)
- [Production job scheduling cheat sheet](https://docs.databricks.com/aws/en/cheat-sheet/jobs)
- [Serverless compute limitations](https://docs.databricks.com/aws/en/compute/serverless/limitations)
- [Classic compute configuration best practices](https://docs.databricks.com/aws/en/compute/cluster-config-best-practices)
- [Dedicated compute overview](https://docs.databricks.com/aws/en/compute/dedicated-overview)
- [Manage identities and privileges for Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/privileges)
- [Create and manage compute policies](https://docs.databricks.com/aws/en/admin/clusters/policies)
- [Connect to a SQL warehouse](https://docs.databricks.com/aws/en/compute/sql-warehouse)
- [Use tags to attribute and track usage](https://docs.databricks.com/aws/en/admin/account-settings/usage-detail-tags)
- [Monitor the cost of serverless compute](https://docs.databricks.com/aws/en/admin/system-tables/serverless-billing)
