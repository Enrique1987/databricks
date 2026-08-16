# Data Engineer Professional Legacy Notes Audit

Status: Reviewed content-governance audit

Last reviewed: 2026-08-16

## Decision

The historical material is useful as a map of topics learned, but it is not suitable for bulk publication. The safe strategy is to preserve the private source, remove restricted material from the public drafts, and rewrite one current, original, evidence-backed domain at a time.

This audit classifies content without reproducing private questions, answer choices, paid course material, screenshots, or third-party code.

## Scope and method

The review covered:

- two Markdown drafts already tracked in this repository;
- one private legacy archive containing 67 files and approximately 4.16 MB;
- one separate ZIP copy of Professional course material in the local reference area; and
- the current public Professional hub and its ten-domain evidence matrix.

The two repository drafts were reviewed directly. For exam-oriented and third-party material, the audit used filenames, directory boundaries, file types, headings, and duplication signals only. It did not promote or summarize question-by-question content.

## Verified inventory

| Location or family | Count | Composition | Decision | Reason |
| --- | ---: | --- | --- | --- |
| Repository Professional drafts | 2 | Markdown | **Rewrite** | Original topic coverage is useful, but terminology, APIs, examples, and evidence are inconsistent |
| Private archive: consolidated top-level notes | 3 | Large Markdown files | **Deduplicate, then rewrite by domain** | The three files substantially overlap; publishing any one wholesale would preserve stale and mixed-origin material |
| Private archive: old summary stubs | 2 | Small Markdown files | **Archive** | Superseded and too small to justify migration |
| Private archive: exam-oriented top-level files | 5 | Markdown questions, solutions, and exam notes | **Restricted — no migration** | Question and answer material is incompatible with the public source policy |
| Private archive: `LH` question material | 3 | Markdown | **Restricted — no migration** | Exam/practice framing and uncertain origin |
| Private archive: Whizlabs | 2 | PNG screenshots | **Restricted — recommend deletion after manual confirmation** | Commercial practice content must not be published |
| Private archive: courseware | 45 | Python, images, Markdown, DBC, notebook, and wheel | **Third-party — no migration** | License and provenance are not established; examples must be recreated from first principles |
| Private archive: standalone images | 7 | PNG diagrams and screenshots | **Manual provenance review** | Some may illustrate useful concepts, but ownership and current accuracy are unclear |
| Separate local course ZIP | 1 | ZIP archive | **Potential duplicate — manual deletion candidate** | It duplicates the same course family and has no role in the public repository |

The 67-file private archive contains 31 Python files, 19 PNG files, 14 Markdown files, one DBC export, one notebook, and one wheel. None of these private files were copied into this repository.

## Duplication finding

The three large top-level study documents are not independent bodies of knowledge:

- one Fundamentals variant differs from another mainly by approximately 147 inserted lines and five deleted lines;
- the Nutshell variant differs from the first Fundamentals file mainly by removing approximately 45 lines; and
- their shared headings cover the same ingestion, transformation, performance, governance, deployment, and monitoring topics.

They should therefore be treated as one historical source family, not three assets to publish. The public [legacy knowledge summary](legacy-knowledge-summary.md) replaces that duplication with a domain-level map.

## Public draft decisions

| Draft | Decision | Content retained as candidate knowledge | Content that must not be promoted |
| --- | --- | --- | --- |
| [Organized topic notes](../../../drafts/certifications/data-engineer-professional/topic-notes.md) | Rewrite by domain | Compute, UDF choices, Auto Loader, streaming state, CDC/CDF, quality, layout optimization, sharing, and governance | Former product names, simplified guarantees, stale syntax, unsupported rules of thumb, and exam-style Q&A |
| [Advanced data engineering notes](../../../drafts/certifications/data-engineer-professional/advanced-data-engineering.md) | Rewrite as labs and operational guides | Streaming, privacy, Spark diagnostics, performance, deployment, and CDC | Course-outline structure, unmeasured examples, generic cloud claims, former APIs, and conversational fragments |

As part of this audit, two exam-style questions with answers and a conversational closing section were removed from `topic-notes.md`. The rest of the file remains explicitly marked as a legacy draft.

## Decision meanings

- **Promote:** move only material already verified, original, current, and independently understandable.
- **Rewrite:** retain the underlying capability, but replace the prose, example, and architecture with current primary-source-backed work.
- **Archive:** preserve privately for traceability, but do not use it as a public technical reference.
- **Restricted:** do not copy, paraphrase question by question, or use distinctive scenarios and answer logic.
- **Delete candidate:** remove only after a human confirms that the file is duplicated, unnecessary, and not required for private records.

## Manual review queue

No private file was deleted during this audit. The following actions require an explicit human decision:

1. confirm whether the Whizlabs screenshots can be deleted permanently;
2. compare the separate ZIP with the extracted courseware and delete the duplicate if no archive obligation exists;
3. identify the provenance of the seven standalone images;
4. decide whether the private third-party courseware must be retained for personal records; and
5. retain only one private consolidated note after the useful topic map has been fully rewritten.

## Promotion gate

A legacy topic can move into reviewed documentation only when:

- its current relevance is confirmed against the official exam guide;
- product names and APIs are checked against current Databricks documentation;
- the explanation is rewritten from first principles;
- code and scenarios are original and use synthetic data;
- limitations, security, observability, failure recovery, performance, and cost are addressed;
- runnable evidence is added or the platform-only gap is explicit; and
- the source and practice-question policy passes.

## Primary references

- [Databricks Certified Data Engineer Professional exam guide current for this review](https://www.databricks.com/sites/default/files/2025-11/databricks-certified-data-engineer-professional-exam-guide-november-30-2025_0.pdf)
- [Developer best practices on Databricks](https://docs.databricks.com/aws/en/developers/best-practices)
- [Spark Declarative Pipelines](https://docs.databricks.com/aws/en/ldp/)
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
