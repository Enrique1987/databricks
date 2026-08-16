# Databricks Engineering and Architecture Portfolio

A public, evolving portfolio of Databricks data engineering, platform architecture, data warehousing, machine learning, and AI work.

> [!NOTE]
> This independent repository is not affiliated with or endorsed by Databricks. Product behavior, Preview status, and certification objectives change over time. Validate important details against the [official Databricks documentation](https://docs.databricks.com/).

## North star

The goal is not to collect notes. It is to publish original, reproducible work that demonstrates the broad and deep technical judgment expected of a Databricks Champion candidate: engineering reliable data products, designing governed platforms, explaining trade-offs, and operating workloads in production.

This portfolio supports technical readiness; it does not replace the separate Databricks nomination and acceptance process. Start with the [Databricks Champion readiness roadmap](docs/roadmap/databricks-champion-roadmap.md).

## Reviewed references

| Area | Resource | Review date |
| --- | --- | --- |
| Platform | [Databricks cheat sheet](docs/reference/cheat-sheet.md) | 2026-08-16 |
| SQL | [Databricks-specific SQL reference](docs/reference/databricks-specific-sql.md) | 2026-08-16 |
| Data engineering | [Bronze ingestion patterns](docs/guides/bronze-ingestion-patterns.md) | Reviewed 2026-08-16 |
| Architecture | [ADR 001: compute selection and environment controls](docs/architecture/adr-001-compute-strategy.md) | Reviewed 2026-08-16 |

Only documents explicitly marked **Reviewed** should be treated as current reference material. Older certification and interview notes live under `drafts/` until they are verified, rewritten, or removed.

## Portfolio projects

Production-style projects will live under `projects/` and must include runnable code, automated checks, governance, observability, cost considerations, failure recovery, and teardown instructions.

Planned sequence:

1. Governed ingestion with Auto Loader or Lakeflow Connect.
2. CDC with Lakeflow Spark Declarative Pipelines.
3. Unity Catalog landing zone and governed data product.
4. SQL warehouse performance and dimensional-modeling lab.
5. Multi-environment delivery, observability, resilience, and FinOps.
6. Governed ML or AI application with MLflow evaluation and monitoring.
7. End-to-end architecture capstone with requirements, alternatives, migration, recovery, and cost analysis.

## Quality and safety

- Read the [content standard](docs/quality/content-standard.md) before promoting a draft.
- See the [August 2026 repository audit](docs/quality/repository-audit-2026-08.md) for cleanup decisions and remaining debt.
- Do not commit exam dumps, paid training exports, third-party screenshots without permission, customer data, secrets, generated MLflow state, or large binaries.
- Prefer primary sources, text, executable examples, and original diagrams.

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code and original documentation in this repository are available under the [MIT License](LICENSE). Third-party product names and trademarks belong to their respective owners.
