# Consolidated knowledge

Status: Draft learning record. Last reviewed: 2026-09-21.

Evidence: [imported Session 001](sessions/2026-09-21-session-001-rag-embeddings-chunking.md) and [Session 002 synthesis](sessions/2026-09-22-session-002-rag-embeddings-vector-search-chunking.md). General learning notes; no Databricks implementation has been tested.

## RAG

Retrieval-augmented generation retrieves external information for a query and includes selected evidence in the model context. It does not itself change model weights. Updating source data can avoid retraining for factual refresh, but retrieval data/indexes must also stay current. Grounding does not guarantee factual answers or correct access control.

Ingestion extracts and cleans documents, splits them, produces embeddings, and persists content and indexes. Serving retrieves relevant material, constructs context, and generates an answer. Filtering, re-ranking, and evaluation need further practice.

Fine-tuning changes model weights. Prompt engineering changes instructions or context. Long-context prompting directly supplies more material rather than necessarily retrieving a subset. These approaches can be combined; selecting among them remains an active gap.

## Embeddings and vectors

An embedding is an ordered numeric vector representing learned features, commonly stored as floating-point values. It is not a document ID or normally binary. Semantic proximity depends on the model, task, and metric; brand-pair examples are intuition, not guaranteed rankings.

Query and document embeddings need compatible embedding spaces. A vector index stores vectors and computes or approximates similarity; it does not remove the mathematics. Cosine similarity, Euclidean distance, and approximate nearest-neighbor retrieval remain open study topics.

Embeddings existed before modern LLMs. Classical word-embedding methods such as Word2Vec learn from statistical patterns of word use and usually give a word one relatively fixed vector. This makes ambiguous words difficult: "bank" can refer to finance or a river. Contextual models can produce different representations depending on surrounding text. In RAG, the usual retrieval unit is a chunk or another text fragment, not an isolated word. The exact vector depends on the model and input handling; equal dimensions across models do not establish compatible embedding spaces.

An embedding differs from a hash: a hash is designed for identification or integrity checks, whereas a learned embedding is useful because geometric relationships can reflect properties of inputs. Vector Search operates on numbers, not language directly. A semantic match between differently worded queries and documents depends on the embedding model and is not guaranteed. Literal keyword or hybrid retrieval may help where exact terms matter.

## Chunking

A chunk is a retrieval unit from source content. Small chunks can lose necessary context; large chunks can dilute relevance and consume more tokens. Overlap can preserve boundary context but increases duplication, embedding count, storage, and retrieval cost.

Select strategies using document structure, model constraints, and measured retrieval quality. No universal size or overlap percentage is established here.

For an enterprise system, source quality, permissions, freshness, lineage, and monitoring matter alongside similarity. The learner's current rough pipeline captures chunking, embedding, indexing, query embedding, retrieval, and generation; parsing, metadata, authorization, re-ranking, citations, evaluation, and monitoring have yet to be reasoned through.

## Terminology

The exam syllabus uses Mosaic AI Vector Search. Preserve syllabus names when mapping objectives; verify current product terminology and cloud-specific behavior in official documentation before labs.
