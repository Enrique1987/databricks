# Original scenario questions

Status: Draft learning record. Last reviewed: 2026-09-23.

All questions are unattempted. These are original learning scenarios, not official exam questions.

| ID | Scenario | Expected reasoning |
| --- | --- | --- |
| Q1 | Internal policies change weekly. How do answers stay current without retraining each week? | Refresh source data and retrieval index, retrieve authorized evidence, evaluate grounding |
| Q2 | Retrieved paragraphs omit an important exception clause. What do you investigate? | Document boundaries, chunk size/overlap, retrieval results; compare representative queries before choosing changes |
| Q3 | A user asks about a restricted document. Where should restrictions apply? | Enforce authorization before retrieval results enter model context; prompts alone are insufficient |
| Q4 | A few short documents fit in context. When is direct context simpler than RAG? | Compare corpus size, freshness, quality, latency, cost, and access controls |
| Q5 | You replace the embedding model. Can new query vectors safely use old document vectors? | Validate compatible spaces; usually re-embed and re-index, even when dimensions match |
| Q6 | A search for "bank account" returns a river-bank article. Explain two likely causes and how you would test a fix. | Consider ambiguous input, chunk context, embedding behavior, filters, and a labelled retrieval set; avoid assuming the index understands language |
| Q7 | A support query says "ticket money back" while the policy uses "refund". Why might semantic search help, and when could exact-term search still matter? | Explain vector similarity, failure modes, and a possible hybrid approach with evaluation |
| Q8 | A source PDF changes, but the assistant still cites an old policy. Trace where freshness can fail from ingestion to answer. | Check parsing, chunk updates, index synchronization, retrieval, citations, and monitoring |
| Q9 | A parser upgrade fixes table extraction. Which stored artifacts allow safe replay without fetching every source again? | Raw retention, version/checksum, control status, idempotent reprocessing, lineage, and downstream replacement |
| Q10 | A team proposes 500-token chunks for every document. Design a small experiment to test that choice. | Compare fixed and structure-aware strategies on representative queries; measure retrieval before generation |
| Q11 | Decide whether customer ID lookup and policy-question retrieval need a key index, vector index, or both. | Match exact lookup to keys and semantic retrieval to embeddings; explain combined application flow |

Record answers and IDs in a session before changing mastery. Evaluate reasoning, not keywords.
