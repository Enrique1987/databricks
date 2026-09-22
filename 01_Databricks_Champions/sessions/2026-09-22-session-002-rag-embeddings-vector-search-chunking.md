# Session 002 — RAG, embeddings, search, and chunking

Status: Draft learning record. Last reviewed: 2026-09-22.

Source: learner-supplied summary of a conversational review on 2026-09-22. This is a synthesis of the summary, not a transcript. The summary reports explanations and corrections but no scored scenario answers or independently observed re-tests. Proposed mastery changes remain provisional.

## What became clearer

- RAG supplies retrieved knowledge to a model at request time; it does not train the model on that knowledge. The learner's preferred description is an LLM receiving relevant context in real time.
- An embedding is a numeric vector representing learned features of its input. It is distinct from an ID, binary flag, or hash. Embeddings predate modern LLMs.
- Classical word embeddings such as Word2Vec learn from patterns of word use and typically assign one relatively fixed vector per word. Contextual representations can differ with surrounding text, which helps with ambiguous words. RAG usually embeds chunks or other text units rather than isolated words.
- The same input can receive different vectors from different embedding models. Source and query vectors must be compatible for retrieval.
- Vector Search compares numeric vectors. Its semantic usefulness comes from what the embedding model has encoded, so different wording can still retrieve related content.
- Very small chunks can sever relationships; very large chunks can add irrelevant material and token cost. No chunk-size selection or overlap scenario was solved.
- The learner can describe an approximate document-to-answer path. It still omits extraction quality, metadata, permissions, filtering, re-ranking, citations, evaluation, and monitoring.

## Misconceptions and re-tests

The supplied summary reports renewed corrections on embedding-as-ID/binary and adds embedding-as-hash, embeddings-as-new-to-LLMs, literal-label semantics, and Vector Search as direct language understanding. These are tracked in [mistakes](../genai-associate/MISTAKES.md). The learner has not yet answered the re-test questions recorded there.

## Evidence and mastery

The summary suggests provisional EXPLAIN for RAG versus training, hash versus embedding, basic Vector Search, and semantic versus lexical matching. It suggests UNDERSTAND for classical embedding training and contextual embeddings; one paragraph suggests EXPLAIN for contextual embeddings, but the summary's own mastery table assigns UNDERSTAND, so the conservative state is retained. Existing EXPLAIN estimates for embedding and basic chunking remain. No SOLVE or TEACH evidence exists. See the [matrix](../genai-associate/MASTERY_MATRIX.md).

## Open questions

The previous full RAG architecture gap remains: the summary covers the central path, but not the full ingestion, authorization, evaluation, and monitoring decisions. Similarity metrics, ANN, chunk overlap and advanced chunking, hybrid search, re-ranking, retrieval metrics, model selection, and Databricks implementation remain open.

## Next action

Conduct the [RAG end-to-end oral session](NEXT_SESSION.md): first re-test earlier misconceptions without prompts, then have the learner explain both ingestion and serving paths and reason through original enterprise scenarios.
