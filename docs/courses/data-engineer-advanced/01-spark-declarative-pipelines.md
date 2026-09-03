# 01 — Advanced Techniques with Apache Spark Declarative Pipelines

## Local coverage

| Course point | Status | Local evidence |
| --- | --- | --- |
| Multi-flow Bronze tables from CSV and JSON (`CREATE FLOW`) | Pending study | No specific local example found. |
| Incremental Gold materialized views and Unity Catalog tags | Pending study | No specific local example found. |
| Multiplex pattern and `VARIANT` into domain Silver tables | Pending study | `docs/reference/databricks-specific-sql.md` documents `VARIANT`, but not this pipeline pattern. |
| Delta Sinks and Iceberg reads through Delta UniForm | Pending study | No specific local material found. |
| SCD Type 2 CDC with `AUTO CDC INTO` | Pending study | Legacy CDC notes use `APPLY CHANGES INTO`; no `AUTO CDC INTO` example found. |
| Expectations, `schemaHints`, rescued data, and Bronze schema evolution | Local draft available | `drafts/certifications/data-engineer-professional/advanced-data-engineering.md`; `docs/guides/bronze-ingestion-patterns.md`. |
| Quarantine pattern and Pipelines UI violation metrics | Pending study | No specific local example found. |

## Outline to document

- Introduction to Multi Flows, Expectations, and Liquid Clustering in SDP
- Multiplex Streaming, Delta Sinks, and Iceberg Reads
- CDC review and SCD Type 2 with `AUTO CDC`
- Advanced data-quality checks and expectations
- Multi-source ecommerce pipeline lab

## Related local material

- `drafts/certifications/data-engineer-professional/advanced-data-engineering.md`
- `drafts/certifications/data-engineer-associate/study-notes.md`
- `docs/guides/bronze-ingestion-patterns.md`
- `docs/reference/databricks-specific-sql.md`
