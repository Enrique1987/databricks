# Next oral session — RAG end-to-end

Status: Draft learning record. Last reviewed: 2026-09-23.

Duration: approximately 20 minutes. Goal: cold-recall the offline path and connect it to online retrieval.

Opening prompt:

> Help me practice an enterprise RAG architecture. First ask me to explain, without hints, everything that happens from a 1,000-page source document until it becomes searchable. Then teach and test the online query path. Ask one question at a time, require my reasoning, and finish with a structured evidence summary.

1. Minutes 0–5: cold review — raw file, controlled ingestion, parsing, cleaning, chunking, metadata, embeddings, and vector index. Do not provide the sequence until the learner finishes.
2. Minutes 5–11: teach the online path — query, query embedding, top-k candidate retrieval, authorized metadata filtering, context construction, generation, and citations.
3. Minutes 11–15: introduce similarity scores and the precision/context trade-off of top-k. Keep ANN/HNSW internals in the parking lot unless required for a decision.
4. Minutes 15–18: answer Q8–Q11 selectively from [the question bank](../genai-associate/QUESTION_BANK.md), including source updates and persistence choices.
5. Minutes 18–20: record actual answers, corrections, assistance needed, and proposed mastery changes using [the template](TEMPLATE.md).

Supply the resulting summary here for ingestion; voice conversations do not synchronize automatically.
