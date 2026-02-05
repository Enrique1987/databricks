# ADR: Databricks Compute Strategy by Environment (DEV / QA / PROD)


## Context

In Databricks, there are two fundamentally different usage patterns for compute:

1. **Interactive development**
   - Humans work in notebooks: explore, debug, iterate.
   - Collaboration matters: multiple people may share the same runtime.
   - A cluster can stay up for a while to avoid repeated start-up time.

2. **Scheduled execution**
   - No interactive development happens.
   - Workloads are executed as Jobs: **run → finish**.
   - The main goal is reliable, repeatable execution with clear cost control and governance.

## Problem

When **Shared / All-Purpose** clusters are used to run scheduled workloads (especially in QA/PROD), the cluster lifecycle is optimized for **interactive use**, not for **job completion**.

A common symptom is “idle tail” cost:

- the job finishes,
- but the cluster remains running until an **inactivity-based auto-termination** threshold is reached,
- resulting in unnecessary idle runtime and a weaker operational model for production schedules.

## Decision

We standardize compute by environment and workload type:

- **DEV:** interactive → **All-Purpose / Shared Compute**
- **QA & PROD:** scheduled & reproducible → **Jobs Compute (job clusters)** or **Serverless Jobs** (if available)
- **BI / Reporting:** **SQL Warehouse** is the preferred compute for BI tools (e.g., Power BI)

## Rationale

### Why Shared Compute is the best fit for DEV
- Optimized for notebook-driven iteration.
- Good developer experience (DX): faster feedback loops.
- Enables collaboration and shared troubleshooting.

### Why Jobs / Serverless Compute is the best fit for QA/PROD
- Lifecycle matches job execution (**run → terminate**).
- Reduces idle tail cost (cluster doesn’t stay up “just in case”).
- Improves governance and stability:
  - clearer separation between “development” and “production execution”
  - reproducible runs (job definition + parameters)
  - easier to enforce policies (cluster policies, permissions, approved runtimes)

## Alternatives Considered

1. **Use Shared / All-Purpose clusters everywhere**
   - ✅ Simple to set up
   - ❌ Higher risk of idle tail cost and weaker production governance
   - ❌ Encourages interactive use in production-like environments

2. **Dedicated All-Purpose clusters per environment**
   - ✅ Better isolation than fully shared
   - ❌ Still not job-lifecycle-driven
   - ❌ Still invites interactive usage and operational drift

3. **Serverless for all workloads**
   - ✅ Excellent ops simplicity when available and supported
   - ❌ May not fit every workload / security constraint / budget model
   - ✅ Keep as an option, but not a blanket default

## Consequences

### Positive
- Clear compute separation between DEV and QA/PROD.
- Lower idle/runtime waste for scheduled workloads.
- More predictable, reproducible production runs.
- Cleaner governance model (policies + access patterns are easier to enforce).

### Trade-offs
- Slightly more setup effort (job definitions, cluster policies, environment guardrails).
- Developers may need a small mindset shift: QA/PROD runs are *executions*, not *development sessions*.

## Implementation Guidance (Practical)

- **Enforce cluster policies**
  - DEV: allow interactive clusters for developer groups.
  - QA/PROD: restrict interactive clusters; prefer job clusters / serverless jobs.
- **Use job clusters for scheduled workflows**
  - new cluster per run (or a controlled pool, if applicable)
  - terminate immediately after completion
- **Keep BI on SQL Warehouses**
  - stable endpoints and concurrency handling for BI tools
- **Operational guardrails**
  - align permissions with environment intent (no ad-hoc notebook execution in PROD)
  - standardize runtimes, libraries, and approval process for production jobs

## References (public docs)

- Databricks “Compute” documentation: https://docs.databricks.com/
- Databricks Jobs: https://docs.databricks.com/en/workflows/jobs/
- SQL Warehouses: https://docs.databricks.com/en/sql/admin/sql-warehouses.html
