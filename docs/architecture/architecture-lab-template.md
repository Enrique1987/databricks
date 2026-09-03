# Architecture Lab Template

Status: **Reviewed template**

Last reviewed: 2026-09-03

Use this template for architecture-focused learning and portfolio labs. Replace guidance text with evidence from the chosen scenario; do not retain sections that make unsupported claims.

## 1. Problem statement

Describe the business situation and pain without naming the preferred product. Identify users, outcomes, current limitations, and the cost of leaving the problem unsolved.

## 2. Scope and assumptions

State what the lab includes and excludes, supported cloud and region assumptions, expected data sensitivity, dependencies, and which parts are illustrative rather than executed.

## 3. Requirements

### Functional requirements

List required behaviors such as transactions, ingestion, analytics, machine learning, event handling, governance, or application serving.

### Non-functional requirements

Give measurable targets or explicit unknowns for:

- latency, throughput, concurrency, and freshness;
- consistency and transaction boundaries;
- availability, RTO, and RPO;
- security, privacy, audit, and residency;
- scalability and expected growth;
- cost ceiling and team-operating constraints.

## 4. Baseline architecture

Model the simplest credible current or non-Databricks design. Explain why it is valid and which requirement causes it to evolve.

## 5. Architecture options

Compare at least two credible options. Include components, data flow, trust boundaries, ownership, and operational responsibility.

| Decision dimension | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Requirement fit | | | |
| Latency and scale | | | |
| Reliability and recovery | | | |
| Security and governance | | | |
| Operational complexity | | | |
| Cost and skills | | | |
| Portability and lock-in | | | |
| Maturity and limitations | | | |

## 6. Selected option and rationale

Identify the selected design, the requirements that drive it, and why the alternatives were rejected. Separate measured evidence from assumptions and inference.

### Why Databricks

Name the exact Databricks capabilities that create value. Platform consolidation alone is not sufficient unless its operational or economic benefit is demonstrated.

### When not to use this design

Describe workloads, constraints, maturity risks, or specialist capabilities that should lead to another option.

## 7. End-to-end design

Include an architecture diagram and describe:

- synchronous and asynchronous paths;
- systems of record and derived stores;
- schemas, contracts, and ownership boundaries;
- identity, network, encryption, and policy enforcement;
- observability and lineage;
- failure domains and degraded behavior.

All text inside diagrams must be in English.

## 8. Data lifecycle

Trace create, read, update, delete, replay, retention, archival, and purge behavior. For analytical paths, explain Bronze, Silver, and Gold responsibilities where applicable.

## 9. Failure and recovery plan

Test or explicitly plan for component outage, malformed data, duplicate or late events, checkpoint or state loss, deployment rollback, accidental deletion, regional failure, and dependency throttling. Record observed recovery time and potential data loss against RTO and RPO.

## 10. Performance and cost validation

Define representative data volume, concurrency, test duration, warm-up, metrics, and acceptance thresholds before running benchmarks. Include infrastructure, data movement, storage, licensing, and operational effort in cost comparisons.

## 11. Portability and exit path

Inventory proprietary APIs, SQL, formats, policies, orchestration, and operational dependencies. Describe how critical data and business logic would be exported, reconstructed, and validated on an alternative platform.

## 12. Implementation and reproduction

Provide prerequisites, sanitized sample data, deployment commands, configuration, tests, expected results, monitoring, and teardown. Never publish secrets, customer data, private partner material, or paid-course content.

## 13. Evidence and open questions

Link ADRs, code, test output, query plans, dashboards, failure records, and runbooks. List unresolved assumptions and the next experiment that would close each gap.

## 14. Decision review

Record the decision date, owner, reviewers, expiry or review date, and reversal triggers. Revisit the design when workload requirements, feature maturity, price, compliance, or supported interfaces change.

## 15. Primary sources

Cite current official Databricks documentation and upstream documentation for compared technologies. Date volatile claims and distinguish product documentation from measured lab evidence.
