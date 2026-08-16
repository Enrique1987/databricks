# Databricks Data Engineer Professional Knowledge Hub

Status: Reviewed navigation document

Last reviewed: 2026-08-16

## Purpose

This hub turns the learning behind the Databricks Certified Data Engineer Professional credential into a public, evidence-based body of work. It is designed for production data engineering and Databricks Champion technical readiness, not for memorizing exam questions.

The portfolio owner earned the credential in 2026. A public verification URL has not yet been added. The repository does not store a private certificate, credential identifier, score report, or exam-session information.

## Scope

The structure follows the ten sections in the official exam guide that is current for this review:

1. developing data-processing code with Python and SQL;
2. data ingestion and acquisition;
3. data transformation, cleansing, and quality;
4. data sharing and federation;
5. monitoring and alerting;
6. cost and performance optimization;
7. data security and compliance;
8. data governance;
9. debugging and deployment; and
10. data modeling.

The official guide is an organizing baseline, not the limit of this portfolio. Champion readiness requires deeper architecture judgment, failure analysis, security, operability, and cost reasoning than a certification alone demonstrates.

## Navigate the hub

- [Professional engineering block 01: Python, SQL, dependencies, and testing](01-python-sql-and-testing.md) — connects the first exam domain to an installable package, SQL controls, automated tests, and explicit platform gates.
- [Objectives and evidence matrix](objectives-matrix.md) — maps every official domain to existing and planned portfolio evidence.
- [Learning and evidence log](learning-log.md) — records reviewed milestones without exposing private exam information.
- [Source and practice-question policy](source-and-practice-policy.md) — defines what can and cannot move from the private study archive into this public repository.
- [Migration backlog](migration-backlog.md) — converts legacy notes into small, reviewable technical deliverables.
- [Databricks Champion readiness roadmap](../../roadmap/databricks-champion-roadmap.md) — places the certification inside the wider engineering and architecture goal.

## Reviewed evidence already available

| Capability | Evidence | What it demonstrates |
| --- | --- | --- |
| Python, SQL, dependencies, and testing | [Professional engineering block 01](01-python-sql-and-testing.md) | Modular package design, wheel delivery, safe SQL parameters, dependency boundaries, layered testing, and debugging |
| Production ingestion design | [Bronze ingestion patterns](../../guides/bronze-ingestion-patterns.md) | Source selection, Auto Loader behavior, schema evolution, replay, quarantine, observability, and cost trade-offs |
| Compute architecture | [ADR 001: compute selection and environment controls](../../architecture/adr-001-compute-strategy.md) | Requirements, serverless-first decisions, exceptions, isolation, policy, observability, and cost controls |
| Platform fundamentals | [Databricks cheat sheet](../../reference/cheat-sheet.md) | Reviewed platform concepts and operational references |
| SQL implementation | [Databricks-specific SQL reference](../../reference/databricks-specific-sql.md) | Databricks SQL syntax and platform-specific behavior |

Reviewed evidence is linked rather than duplicated. Each future topic should point to runnable code, a measured experiment, an architecture decision, or an operational exercise.

## Legacy material

Two preserved drafts contain useful conversation-derived explanations:

- [organized topic notes](../../../drafts/certifications/data-engineer-professional/topic-notes.md);
- [advanced data engineering notes](../../../drafts/certifications/data-engineer-professional/advanced-data-engineering.md).

They remain drafts because some claims use former product names, simplified mental models, old APIs, or unverified examples. They must be rewritten by domain and checked against primary sources before promotion.

The private historical archive also contains third-party course resources and practice-question collections. Those files are inputs for identifying concepts only; they will not be copied, paraphrased question by question, or committed here.

## Evidence standard

Knowledge is promoted only when it answers all of these questions:

- What production problem does this solve?
- What assumptions and workload characteristics apply?
- Which credible alternatives were considered?
- How is the solution tested, monitored, secured, and recovered?
- What are its performance and cost implications?
- Which limitations or cloud-specific behaviors remain?
- Which current primary sources support the claims?

See the repository [content standard](../../quality/content-standard.md) for the complete review checklist.

## Official sources

- [Databricks Certified Data Engineer Professional exam guide — current for this review](https://www.databricks.com/sites/default/files/2025-11/databricks-certified-data-engineer-professional-exam-guide-november-30-2025_0.pdf)
- [Databricks documentation](https://docs.databricks.com/)

Certification objectives and product behavior change. Recheck the official guide before using this hub for exam preparation or recertification.
