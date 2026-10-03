# Databricks Study Index

Status: **Reviewed** navigation. Last reviewed: 2026-10-03.

This is the study entrance to my Databricks second brain. Start with a reminder, follow the full explanation, and use practice to find what needs another pass. A topic has one maintained home; certification paths link to it.

## Find a concept

| Topic | Quick recall | Deeper explanation or example |
| --- | --- | --- |
| Platform | [General cheat sheet](../reference/cheat-sheet.md) | [Platform capability map](../architecture/platform-capability-map.md) |
| Views and semantics | [Visual cheat sheet](../../img/databricks-views-cheat-sheet.png) | [Views guide and decision table](../reference/databricks-views.md) |
| SQL | [Databricks SQL reference](../reference/databricks-specific-sql.md) | [Python, SQL, and testing](../certifications/data-engineer-professional/01-python-sql-and-testing.md) |
| Ingestion | [Source selection](../guides/bronze-ingestion-patterns.md) | [Process many tables using metadata](../guides/metadata-driven-processing.md) |
| Access control | [Objects and responsibilities](../guides/project-membership-row-security.md#remember-first) | [Project-membership row filter](../guides/project-membership-row-security.md) |
| Semi-structured data | [STRING, STRUCT, and VARIANT](../guides/variant-for-semi-structured-data.md) | Same guide: examples, limits, and migration decisions |
| Compute | [Compute strategy](../architecture/adr-001-compute-strategy.md) | Same ADR: constraints, alternatives, and operations |
| GenAI | [Consolidated learning notes](../../01_Databricks_Champions/KNOWLEDGE.md) | [Sessions and learning roadmap](../../01_Databricks_Champions/README.md) |

The ingestion and compute links currently lead to longer guides. Dedicated visual summaries can be added after reviewing each concept; they are not implied to exist already.

## Practice and learning paths

- [Professional certification hub](../certifications/data-engineer-professional/README.md).
- [Advanced course map](../courses/data-engineer-advanced/README.md).
- [Original GenAI scenarios](../../01_Databricks_Champions/genai-associate/QUESTION_BANK.md) and [mistakes](../../01_Databricks_Champions/genai-associate/MISTAKES.md).
- Original recall questions at the end of the [metadata guide](../guides/metadata-driven-processing.md#check-your-understanding) and [security guide](../guides/project-membership-row-security.md#check-your-understanding).
- [Governed ingestion project](../../projects/governed-ingestion/README.md), with local and workspace validation distinguished.
- [Architecture learning path](../roadmap/architecture-lab-learning-path.md).

## Historical notes awaiting review

These links preserve access to past learning. **Legacy drafts can contain outdated terminology, incomplete examples, and incorrect claims.** Use the maintained guides above where available; the presence of a topic here does not make it reviewed.

| Source | Topics to recover or review |
| --- | --- |
| [Associate study notes](../../drafts/certifications/data-engineer-associate/study-notes.md) | Tables, clones, SQL transformations, ingestion, CDC/SCD, and governance |
| [Database and table example](../../drafts/certifications/data-engineer-associate/database-and-tables.md) | Basic Unity Catalog/Delta operations |
| [Professional topic notes](../../drafts/certifications/data-engineer-professional/topic-notes.md) | Streaming, joins, watermarks, change processing, and optimization |
| [Advanced engineering notes](../../drafts/certifications/data-engineer-professional/advanced-data-engineering.md) | Streaming, privacy, performance, and deployment |
| [Concepts by audience](../../drafts/explainers/concepts-by-audience.md) | Mental models for platform and engineering concepts |
| [Architecture interview practice](../../drafts/interview/architecture-and-engineering.md) | Historical questions and explanations needing review |

## Assimilation progress

This is a content map, not a claim that all local sources have been exhausted.

| Historical/local knowledge | Current disposition |
| --- | --- |
| Views guide and visual | Included in this study collection; examples remain illustrative |
| Metadata-driven processing comparison | Rewritten as a focused guide with limitations and a validation plan |
| Project-membership security scenario | Rewritten with consistent SQL names and explicit multi-user validation pending |
| ML fundamentals and older retrieval notes | Further reconciliation and updating pending |
| Model preparation/serving walkthrough | Completion and validation pending |
| Professional practice collections | Deduplication, provenance review, and assimilation of useful explanations pending |

When revisiting a topic, improve its explanation and links first. Add a visual summary or deeper lab when it helps learning, and record what was actually checked.
