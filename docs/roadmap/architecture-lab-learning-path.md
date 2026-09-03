# Architecture-First Learning Path

Status: **Reviewed planning document**

Last reviewed: 2026-09-03

## Objective

Build Databricks depth through repeatable architecture decisions rather than a catalogue of disconnected features. Each learning cycle starts with a business problem, compares credible designs, and produces evidence that explains where Databricks fits, what it replaces or integrates with, and which trade-offs remain.

The target profile is T-shaped:

- deep implementation and operational knowledge of Databricks;
- enough ecosystem breadth to explain why PostgreSQL, Kafka, Redis, search engines, and other platforms exist and when they remain the better choice.

Deep administration of every adjacent product is not the initial goal. The required depth is the ability to place it correctly in an end-to-end architecture and identify when specialist expertise is needed.

## Learning loop

Every Architecture Lab follows the same reasoning sequence:

```text
Business problem
      |
      v
Functional and non-functional requirements
      |
      v
Simplest viable architecture
      |
      v
Scale, reliability, governance, and cost pressures
      |
      v
Credible alternatives and specialist boundaries
      |
      v
Databricks option and explicit trade-offs
      |
      v
Implementation evidence, failure tests, and decision record
```

This order prevents product availability from becoming the requirement. A technology is introduced only when a documented constraint justifies it.

## Questions every lab must answer

1. What business or technical problem created the need?
2. Which measurable requirements and constraints define success?
3. What credible architecture options exist, including a non-Databricks option?
4. Which Databricks capabilities add specific value?
5. What complexity, lock-in, cost, maturity, or capability gaps does the choice accept?
6. When should the proposed Databricks design not be used?
7. How will the decision be validated, operated, recovered, and revisited?

Use the [Architecture Lab template](../architecture/architecture-lab-template.md) so that labs remain comparable and reviewable.

## Lab sequence

The sequence is organized by architecture problem. Industries and use cases provide realistic constraints inside a lab; they are not the primary navigation structure.

| Order | Architecture Lab | Central decision | Databricks depth | Ecosystem comparison |
| --- | --- | --- | --- | --- |
| 1 | OLTP and Lakehouse | When should operational data live inside the Databricks ecosystem? | Lakebase, Delta Lake, Unity Catalog, Lakebase Change Data Feed | External PostgreSQL or cloud-native OLTP plus CDC |
| 2 | Event-driven systems | When should producers and consumers communicate through durable events? | Structured Streaming, Lakeflow, Delta Lake | Kafka and cloud event brokers |
| 3 | Caching and low-latency applications | When is repeated database or analytical access too slow or expensive? | Application-serving boundaries and governed data access | Redis and application caches |
| 4 | Real-time Lakehouse | When does a workload require continuous processing rather than batch or micro-batch? | Real-time mode, Structured Streaming, Lakeflow | Stream processors and event platforms |
| 5 | Enterprise governance | How can policy scale across thousands of assets? | Unity Catalog, ABAC, lineage, row filters, column masks | Object-level RBAC and external governance controls |
| 6 | Analytical data serving | How should applications consume governed analytical data at low latency? | SQL warehouses and Lakehouse Real-Time | Search engines, serving stores, caches, and operational databases |
| 7 | Governed AI and RAG | How can enterprise data support a measurable, operable AI system? | AI Search, model serving, MLflow, Unity Catalog | External vector stores, model providers, and application frameworks |
| 8 | Open Lakehouse and portability | How can the platform create value without making departure impractical? | Delta Lake, Iceberg, Parquet, Unity Catalog interfaces | Open formats, external engines, export and migration paths |

These labs complement the production project backlog in the [Champion readiness roadmap](databricks-champion-roadmap.md). A lab develops and tests a decision; a portfolio project proves a larger production capability. Strong labs can become ADRs or implementation slices inside those projects.

## First lab: OLTP and Lakehouse

Use a ticketing application as the initial scenario because it exposes both transactional and analytical pressure without assuming that Lakebase is the answer.

### Baseline

```text
Frontend -> Backend API -> PostgreSQL
```

The operational model includes users, events, venues, seats, reservations, orders, payments, and tickets. The baseline is valid until a requirement demonstrates otherwise.

### Growth pressures to introduce

- reporting and customer analytics;
- recommendations and demand forecasting;
- fraud detection and personalization;
- near-real-time operational dashboards;
- centralized governance and lineage;
- increasing transaction volume, availability, and recovery requirements.

### Options to compare

1. Keep PostgreSQL outside Databricks and propagate changes through a managed or specialist CDC path.
2. Use Lakebase for OLTP and Lakebase Change Data Feed for downstream Delta processing.
3. Use a cloud-native operational database and event or CDC services with Databricks as the analytical platform.

The decision is not whether Lakebase is universally better than PostgreSQL. It is whether platform integration creates enough measurable value to justify workload fit, maturity, dependency, and switching cost.

### Questions that trigger adjacent components

- Does repeated read traffic justify a cache such as Redis?
- Do multiple independent consumers justify a durable event backbone such as Kafka or a cloud event broker?
- Which actions require synchronous transactions, and which can be asynchronous events?
- What latency and freshness does analytics actually require?
- Can the system meet its RTO and RPO, and how is recovery tested?
- What data and logic can be exported if the platform choice changes?

The completed lab must benchmark representative transactional and change-propagation behavior; a diagram and feature comparison alone are not sufficient evidence.

## Repository organization

Architecture Labs should become the center of the portfolio as they are implemented:

```text
docs/
|-- architecture/
|   |-- architecture-lab-template.md
|   `-- labs/
|       |-- 01-oltp-lakehouse/
|       |-- 02-event-driven/
|       |-- 03-caching-low-latency/
|       |-- 04-real-time-lakehouse/
|       |-- 05-enterprise-governance/
|       |-- 06-analytical-serving/
|       |-- 07-governed-ai-rag/
|       `-- 08-open-lakehouse-portability/
|-- guides/       # reusable implementation techniques
|-- reference/    # concise feature and SQL reference
`-- roadmap/      # sequence, readiness, and evidence gaps
```

Create a lab directory only when it contains an original design or implementation. Do not pre-create empty folders or move stable reference material merely to match the future layout.

## Definition of a useful learning session

A session is complete when it produces or improves a reusable artifact: a requirement, decision matrix, ADR, benchmark, implementation, failure test, runbook, or reviewed explanation. Raw conversation notes are inputs to this process, not portfolio deliverables.

Feature knowledge should always be attached to a durable chain:

```text
Problem -> Requirement -> Architecture -> Decision -> Technology -> Evidence
```

This makes the portfolio resilient to product renaming and feature churn while preserving the reasoning that selected each component.
