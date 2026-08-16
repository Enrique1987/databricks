# Databricks Engineering Portfolio

A public, evolving portfolio of Databricks data engineering, platform architecture, machine learning, and AI work.

> [!NOTE]
> This independent repository is not affiliated with or endorsed by Databricks. Product behavior, Preview status, and certification objectives change over time. Validate important details against the [official Databricks documentation](https://docs.databricks.com/).

## North star

The goal is not to collect notes. It is to publish original, reproducible work that helps other practitioners and demonstrates the consistency, technical depth, and community contribution associated with a Databricks Community Champion.

Start with the [Community Champion roadmap](docs/roadmap/community-champion-roadmap.md).

## Reviewed references

| Area | Resource | Review date |
| --- | --- | --- |
| Platform | [Databricks cheat sheet](docs/reference/cheat-sheet.md) | 2026-08-16 |
| SQL | [Databricks-specific SQL reference](docs/reference/databricks-specific-sql.md) | 2026-08-16 |
| Data engineering | [Bronze ingestion patterns](docs/guides/bronze-ingestion-patterns.md) | Review in progress |
| Architecture | [ADR 001: compute strategy by environment](docs/architecture/adr-001-compute-strategy.md) | Review in progress |

Only documents explicitly marked **Reviewed** should be treated as current reference material. Older certification and interview notes live under `drafts/` until they are verified, rewritten, or removed.

## Portfolio projects

Production-style projects will live under `projects/` and must include runnable code, automated checks, governance, observability, cost considerations, failure recovery, and teardown instructions.

Planned sequence:

1. Governed ingestion with Auto Loader or Lakeflow Connect.
2. CDC with Lakeflow Spark Declarative Pipelines.
3. Unity Catalog data product and OpenSharing.
4. Multi-environment delivery with Declarative Automation Bundles.
5. Governed AI agent or RAG application with AI Search and MLflow evaluation.

## Quality and safety

- Read the [content standard](docs/quality/content-standard.md) before promoting a draft.
- See the [August 2026 repository audit](docs/quality/repository-audit-2026-08.md) for cleanup decisions and remaining debt.
- Do not commit exam dumps, paid training exports, third-party screenshots without permission, customer data, secrets, generated MLflow state, or large binaries.
- Prefer primary sources, text, executable examples, and original diagrams.

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code and original documentation in this repository are available under the [MIT License](LICENSE). Third-party product names and trademarks belong to their respective owners.
