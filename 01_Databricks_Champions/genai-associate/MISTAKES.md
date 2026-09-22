# Misconceptions and re-tests

Status: Draft learning record. Last reviewed: 2026-09-22.

Sources: [Session 001](../sessions/2026-09-21-session-001-rag-embeddings-chunking.md) and [Session 002](../sessions/2026-09-22-session-002-rag-embeddings-vector-search-chunking.md). Reported corrections, not verbatim statements. All re-tests pending.

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

## M4 — An embedding is a hash

Correction: hashes primarily support identification or integrity; embeddings are learned vectors whose geometry can support similarity search.
Why it matters: a hash index cannot substitute for semantic retrieval.
Re-test: choose between hashing and embeddings for matching differently worded support requests.

## M5 — Embeddings began with modern LLMs

Correction: word-embedding methods such as Word2Vec predate modern LLMs; newer contextual representations address some limitations of fixed word vectors.
Why it matters: distinguish fixed word representations from context-sensitive sentence or chunk representations.
Re-test: explain how the two meanings of "bank" challenge a single fixed word vector.

## M6 — Vector Search directly understands text or stores explicit meaning labels

Correction: an embedding model maps input to numbers; Vector Search compares those numbers. Semantic relationships are learned, not usually stored as explicit category labels in each vector.
Why it matters: retrieval quality depends on the model, corpus, query, and search configuration.
Re-test: explain how differently worded requests can match and why a semantic match can still fail.
