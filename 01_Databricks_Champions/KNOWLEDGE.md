# Consolidated knowledge

Status: Draft learning record. Last reviewed: 2026-09-21.

Evidence: [imported Session 001](sessions/2026-09-21-session-001-rag-embeddings-chunking.md). General learning notes; no Databricks implementation has been tested.

## RAG

Retrieval-augmented generation retrieves external information for a query and includes selected evidence in the model context. It does not itself change model weights. Updating source data can avoid retraining for factual refresh, but retrieval data/indexes must also stay current. Grounding does not guarantee factual answers or correct access control.

Ingestion extracts and cleans documents, splits them, produces embeddings, and persists content and indexes. Serving retrieves relevant material, constructs context, and generates an answer. Filtering, re-ranking, and evaluation need further practice.

Fine-tuning changes model weights. Prompt engineering changes instructions or context. Long-context prompting directly supplies more material rather than necessarily retrieving a subset. These approaches can be combined; selecting among them remains an active gap.

## Embeddings and vectors

An embedding is an ordered numeric vector representing learned features, commonly stored as floating-point values. It is not a document ID or normally binary. Semantic proximity depends on the model, task, and metric; brand-pair examples are intuition, not guaranteed rankings.

Query and document embeddings need compatible embedding spaces. A vector index stores vectors and computes or approximates similarity; it does not remove the mathematics. Cosine similarity, Euclidean distance, and approximate nearest-neighbor retrieval remain open study topics.

## Chunking

A chunk is a retrieval unit from source content. Small chunks can lose necessary context; large chunks can dilute relevance and consume more tokens. Overlap can preserve boundary context but increases duplication, embedding count, storage, and retrieval cost.

Select strategies using document structure, model constraints, and measured retrieval quality. No universal size or overlap percentage is established here.

## Terminology

The exam syllabus uses Mosaic AI Vector Search. Preserve syllabus names when mapping objectives; verify current product terminology and cloud-specific behavior in official documentation before labs.
