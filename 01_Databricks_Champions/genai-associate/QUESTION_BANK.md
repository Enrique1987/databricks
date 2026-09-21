# Original scenario questions

Status: Draft learning record. Last reviewed: 2026-09-21.

All questions are unattempted. These are original learning scenarios, not official exam questions.

| ID | Scenario | Expected reasoning |
| --- | --- | --- |
| Q1 | Internal policies change weekly. How do answers stay current without retraining each week? | Refresh source data and retrieval index, retrieve authorized evidence, evaluate grounding |
| Q2 | Retrieved paragraphs omit an important exception clause. What do you investigate? | Document boundaries, chunk size/overlap, retrieval results; compare representative queries before choosing changes |
| Q3 | A user asks about a restricted document. Where should restrictions apply? | Enforce authorization before retrieval results enter model context; prompts alone are insufficient |
| Q4 | A few short documents fit in context. When is direct context simpler than RAG? | Compare corpus size, freshness, quality, latency, cost, and access controls |
| Q5 | You replace the embedding model. Can new query vectors safely use old document vectors? | Validate compatible spaces; usually re-embed and re-index, even when dimensions match |

Record answers and IDs in a session before changing mastery. Evaluate reasoning, not keywords.
