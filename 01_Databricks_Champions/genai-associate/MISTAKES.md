# Misconceptions and re-tests

Status: Draft learning record. Last reviewed: 2026-09-23.

Sources: [Sessions 001–003](../sessions/). Reported corrections, not verbatim statements. All re-tests remain pending unless a later record states otherwise.

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

## M7 — Bronze must contain the full extracted document

Correction: a valid design can keep the raw file in governed storage and store path, version, status, and source metadata in an ingestion-control table. Other persistence choices are also valid.
Why it matters: medallion labels do not prescribe one physical RAG layout.
Re-test: choose what to persist when parsing must be replayed after a library upgrade.

## M8 — Parsing means removing punctuation and stop words

Correction: parsing extracts content and structure; cleaning removes demonstrated retrieval noise. Natural language normally retains useful context for modern embeddings.
Why it matters: destructive preprocessing can reduce retrieval quality.
Re-test: classify heading extraction, repeated-footer removal, and deletion of all stop words.

## M9 — A 500-token chunk is a standard

Correction: it is one possible experiment baseline. Choose chunking from structure, model limits, question patterns, and measured retrieval quality.
Why it matters: copied defaults can make a good model appear ineffective.
Re-test: propose alternatives for a policy manual with section-level exceptions.

## M10 — Tokens, embeddings, vectors, and indexes are interchangeable stages

Correction: tokenization creates model input units; an embedding model outputs a vector; a vector index organizes vectors for similarity retrieval. Parameters are learned values inside the model.
Why it matters: each concept has a different owner and lifecycle.
Re-test: trace one chunk from text through tokenization to an indexed vector and distinguish parameters.
