# Content Standard

Last reviewed: 2026-10-03 (study purpose and validation guidance; terminology table retains its earlier review baseline)

This repository is a public personal knowledge base with engineering projects. Preserve useful explanations, mental models, and learning context in one canonical home per topic. Reviewed documentation needs current sources and clear examples; executable projects additionally need reproducible evidence. A study guide can be useful before a full production lab exists, provided its validation limits are explicit.

## Required for reviewed content

- State the problem, intended audience, assumptions, and supported cloud when relevant.
- Prefer runnable code over screenshots. Include prerequisites, validation, and cleanup steps.
- Cite primary sources: official Databricks documentation, official exam guides, release notes, or upstream open-source documentation.
- Record `Last reviewed: YYYY-MM-DD` and distinguish current names from former names.
- Explain operational trade-offs: security, governance, reliability, performance, cost, and maintainability.
- Remove secrets, customer information, private company material, tracking parameters, and generated runtime state.
- Use accessible images only when they add information; include meaningful alt text and attribution.
- Use scenario-based practice created for this repository. Do not publish exam dumps or paid training questions.

## Status labels

- **Reviewed** — checked against current primary sources and validated where practical.
- **Draft** — original work in progress; not yet suitable as a reference.
- **Legacy** — retained for migration or historical context; accessible through a clearly labelled historical section of the study index, not presented as current reference material.

Unlabelled content is not considered reviewed.

For illustrative SQL, Python, or configuration, say whether it was executed and where. A documentation review does not prove runtime behavior, performance, or access-control outcomes. Record those separately.

## Review checklist

- [ ] Links and relative paths resolve.
- [ ] No secrets or private data are present in the current tree or proposed diff.
- [ ] No generated outputs, course exports, large binaries, or notebook checkpoints are committed.
- [ ] Product terminology matches current Databricks documentation.
- [ ] Code examples have a validation method or clearly state that they are illustrative.
- [ ] Claims have a primary source or are explicitly identified as experience-based guidance.
- [ ] Markdown headings, filenames, spelling, and language are consistent.
- [ ] The change adds a useful entry to the README or intentionally remains a draft.

## Current terminology

Current Databricks documentation uses several names that older repository content does not. When former names are necessary for searchability or certification context, introduce them once and then use the current name.

| Current name | Former name | Compatibility note |
| --- | --- | --- |
| Lakeflow Spark Declarative Pipelines | Delta Live Tables (DLT) | Existing `dlt` code can still work, but Databricks recommends the `pyspark.pipelines` API. |
| Declarative Automation Bundles | Databricks Asset Bundles | The `databricks bundle` CLI command remains unchanged. |
| AI Search | Mosaic AI Vector Search | Older certification material may still use Vector Search. |
| OpenSharing | Delta Sharing | Older API paths, commands, and billing fields can retain the former name. |
| Git folders | Repos | Existing `/Repos` paths and the CLI `repos` command remain for compatibility. |
| Data quality monitoring / data profiling | Lakehouse Monitoring | Review migration and cost behavior before changing production monitors. |

Primary references:

- [What happened to Delta Live Tables?](https://docs.databricks.com/aws/en/ldp/concepts/where-is-dlt)
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [What happened to Databricks Repos?](https://docs.databricks.com/aws/en/repos/what-happened-repos)
- [Data quality monitoring](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring)
- [Databricks product release notes](https://docs.databricks.com/aws/en/release-notes/product/)
