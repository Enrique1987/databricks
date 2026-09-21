# Misconceptions and re-tests

Status: Draft learning record. Last reviewed: 2026-09-21.

Source: [Session 001](../sessions/2026-09-21-session-001-rag-embeddings-chunking.md). Reported corrections, not verbatim statements. All re-tests pending.

## M1 — RAG means training on company data

Correction: RAG retrieves external context; it does not itself change weights.
Why it matters: factual-refresh architecture and costs differ from fine-tuning.
Re-test: explain how yesterday's policy update affects today's answer.

## M2 — An embedding is a numeric ID or binary flag

Correction: the embedding discussed here is a numeric vector encoding learned features.
Why it matters: model compatibility and similarity depend on representation.
Re-test: distinguish a document ID, its text, and its embedding.

## M3 — Vector search removes similarity calculations

Correction: the engine indexes vectors and performs or approximates similarity retrieval.
Why it matters: metrics and approximate search affect quality and latency.
Re-test: explain what the engine does after receiving a query vector.
