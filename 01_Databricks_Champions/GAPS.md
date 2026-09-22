# Active learning gaps

Status: Draft learning record. Last reviewed: 2026-09-22.

All items remain open after Session 002. Close only with linked re-test evidence. The basic pipeline was described, but the complete design was not independently demonstrated.



1. Explain the full RAG pipeline precisely from ingestion to generation.
2. Distinguish:
   - RAG
   - fine-tuning
   - prompt engineering
   - long-context prompting
3. Understand tokenization and context windows.
4. Understand cosine similarity vs Euclidean distance.
5. Understand approximate nearest-neighbor retrieval.
6. Understand chunk overlap and its trade-offs.
7. Understand retrieval metrics.
8. Understand re-ranking.
9. Learn Databricks Mosaic AI Vector Search concepts.
10. Learn how embeddings/chunks are stored in Delta/Unity Catalog and indexed.
11. Learn embedding model selection and context-length trade-offs.
12. Explain why a vector-search match can fail despite related meaning, including exact-term and hybrid retrieval cases.
13. Understand dot product, HNSW at a high level, and how approximate search trades recall for latency/cost.
14. Apply metadata and authorization filters before retrieved text enters model context.
15. Distinguish Delta Sync from other Vector Search index approaches using current Databricks documentation.
16. Evaluate retrieval with representative queries, relevance labels, and metrics such as recall@k; separate retrieval from answer quality.
17. Design source citations, freshness checks, and monitoring for an enterprise RAG application.
