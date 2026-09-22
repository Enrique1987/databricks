# Next oral session — RAG end-to-end

Status: Draft learning record. Last reviewed: 2026-09-22.

Duration: approximately 20 minutes. Goal: independent EXPLAIN, then evidence toward SOLVE.

Opening prompt:

> Help me practice a complete enterprise RAG architecture. I have Data Engineering experience. I can provisionally explain embeddings and basic chunking, but need to distinguish ingestion from serving. Ask one question at a time, require my reasoning, correct mistakes, and finish with a structured summary. Do not infer mastery from recognition.

1. Minutes 0–3: re-test RAG versus training, embedding versus hash/ID, fixed versus contextual embeddings, and what Vector Search compares. Ask without revealing answers first.
2. Minutes 3–9: explain ingestion, cleaning, chunking, embedding, storage, and indexing.
3. Minutes 9–13: explain query embedding, authorized retrieval/filtering, optional re-ranking, context construction, source citations, generation, evaluation, and monitoring. Enforce access restrictions before unauthorized text reaches the model. Map the flow to Databricks concepts only where verified.
4. Minutes 13–18: answer Q1–Q4, Q6–Q8 selectively from [the question bank](../genai-associate/QUESTION_BANK.md); prioritize full-path and failure scenarios over terminology recall.
5. Minutes 18–20: recap answers, corrections, assistance needed, gaps, and next steps using [the template](TEMPLATE.md).

Supply the resulting summary here for ingestion; voice conversations do not synchronize automatically.
