# Data Engineer Professional Migration Backlog

Status: Reviewed planning document

Last reviewed: 2026-08-16

## Source inventory

The [legacy notes audit](legacy-notes-audit.md) verified two repository drafts, a 67-file private archive, and one separate course ZIP. The private collection mixes overlapping personal notes with exam-oriented files, screenshots, notebook exports, wheels, third-party code, and course resources. Nothing is promoted in bulk.

The [legacy knowledge summary](legacy-knowledge-summary.md) now replaces the duplicated large notes as the public topic map. It records coverage and gaps without treating unverified legacy claims as technical evidence.

The repository currently preserves two legacy drafts:

| Draft | Useful material | Main review risks | Destination |
| --- | --- | --- | --- |
| [Organized topic notes](../../../drafts/certifications/data-engineer-professional/topic-notes.md) | Compute, Photon, ingestion, streaming, CDC/CDF, optimization, governance, and mental models | Simplified claims, former names, old syntax, and unsupported rules of thumb | Split across domains 1–10 after technical verification |
| [Advanced data engineering notes](../../../drafts/certifications/data-engineer-professional/advanced-data-engineering.md) | Streaming, privacy, Spark UI, performance, and deployment | Course-outline structure, illustrative code, old APIs, and missing validation | Convert into labs and operational guides |

Third-party courseware and commercial practice questions remain private and are excluded from migration.

## Promotion sequence

| Batch | Deliverable | Official domains | Evidence required | Status |
| --- | --- | --- | --- | --- |
| 1 | Python, SQL, dependency, and testing guide | 1, 9 | Modular package, unit tests, bundle target, and CI checks | Reviewed local evidence merged; workspace validation pending |
| 2 | Governed ingestion implementation | 2, 3, 8 | Auto Loader pipeline, schema evolution, quarantine, replay, metrics, and access controls | Foundation merged; DEV execution, quarantine, replay, and operational evidence pending |
| 3 | Streaming and CDC failure lab | 1, 3, 5, 9, 10 | Watermarks, joins, current CDC API or Delta alternative, late data, checkpoint recovery, backfill, and measurements | **Next** |
| 4 | Performance investigation lab | 5, 6 | Spark UI, query profile, skew, shuffle, spill, file layout, measurements, and cost conclusions | Planned |
| 5 | Privacy and compliance pipeline | 7, 8 | Least privilege, masking, pseudonymization, retention, purge, audit, and access tests | Planned |
| 6 | Sharing and federation decision guide | 4, 7, 8 | Consumer requirements, governance, networking, cost, limitations, and a sanitized lab | Planned |
| 7 | Production delivery and recovery | 5, 9 | Multi-environment bundles, promotion, alerts, job repair, rollback, SLOs, and runbook | Planned |
| 8 | Dimensional and Delta modeling lab | 3, 6, 10 | SCD/CDC, dimensional model, liquid clustering, benchmark, and serving trade-offs | Planned |

## Definition of done for each batch

- The change is original and independently understandable.
- Claims and terminology are checked against current primary sources.
- Code is tested locally where possible and clearly labels platform-only validation.
- No private question, paid material, screenshot, binary, credential, or customer detail is included.
- The objectives matrix and learning log are updated.
- The pull request is narrow enough to review as one coherent technical argument.
