# Data Engineer Advanced — course map

This directory is the working map for the four half-day modules in the supplied
course outline. It is intentionally an inventory, not new course material.

## Status legend

- **Local draft available**: related content exists locally, but is under
  `drafts/` and has not completed technical review.
- **Reviewed reference available**: related content exists in a document marked
  reviewed in this repository.
- **Pending study**: no sufficiently specific local source has been identified.

## Modules

0. [Prerequisites](00-prerequisites.md)
1. [Advanced Techniques with Apache Spark Declarative Pipelines](01-spark-declarative-pipelines.md)
2. [Databricks Data Privacy](02-data-privacy.md)
3. [Databricks Performance Optimization](03-performance-optimization.md)
4. [Automated Deployment with Declarative Automation Bundles](04-declarative-automation-bundles.md)

## Local evidence used

- `drafts/certifications/data-engineer-professional/advanced-data-engineering.md`
  — legacy draft covering streaming, privacy, performance, and deployment.
- `drafts/certifications/data-engineer-associate/study-notes.md` — legacy draft
  covering Delta, streaming, CDC, Unity Catalog, compute, and bundles.
- `docs/guides/bronze-ingestion-patterns.md` — draft on Bronze ingestion,
  Auto Loader, schema evolution, and CDF.
- `docs/reference/databricks-specific-sql.md` — reviewed navigation reference
  for masks, row filters, CDF, VARIANT, and current pipeline terminology.
- `docs/architecture/adr-001-compute-strategy.md` — draft compute guidance by
  environment.

The private extraction in `02_reference/databricks-local-materials-2026-08-16`
is deliberately not linked or copied here. See the repository README and its
content policy before promoting any material from that location.

## Working rule

When a topic is studied, add only an original, reviewed explanation or a
reproducible exercise. Change its status here after the evidence is added.
