# Session 001 — RAG, embeddings, vector search, chunking

Status: Draft learning record. Last reviewed: 2026-09-21.

Provenance: section 9 of the learner-supplied bootstrap document. No original transcript or scored answers provided. Estimates below are provisional and require re-testing. This import is not a new learning session.

Date: 2026-09-21

Main topics:
- RAG
- embeddings
- vectors
- vector search
- chunking

## RAG

Correct mental model:

> RAG = an LLM plus external knowledge retrieved dynamically at query time.

RAG stands for:
- Retrieval
- Augmented
- Generation

Important correction:
RAG is **not** the same as training or fine-tuning an LLM on private/company data.

Instead:
1. user asks a question,
2. relevant external knowledge is retrieved,
3. retrieved content is inserted into the model context,
4. the LLM generates a response grounded in that context.

Why it is useful:
- knowledge can remain fresh,
- changing data does not require retraining,
- lower cost than repeated retraining/fine-tuning for knowledge refresh,
- better control over which enterprise information is supplied,
- useful for private/internal knowledge.

Current mastery estimate:
- RAG conceptual purpose: `EXPLAIN`
- full RAG architecture: `UNDERSTAND`

## Embeddings

Correct mental model:

> An embedding is a vector of numbers representing semantic information.

Important corrections:
- it is not normally a single numeric ID,
- it is not simply binary,
- in code it is commonly represented similarly to an array/list of floating-point numbers,
- semantically similar items tend to be located closer together in embedding space.

Example intuition:
- embeddings for concepts like "Coca-Cola" and "Fanta" should generally be semantically closer than "Coca-Cola" and "car", depending on model/context.

Current mastery estimate:
- basic intuition: `EXPLAIN`
- embedding-model trade-offs: `UNKNOWN`

## Mathematical vector

Working mental model:

> A mathematical vector can be treated here as an ordered collection of numbers on which mathematical operations can be performed.

In programming, an embedding vector is typically manipulated similarly to a numeric array.

Current mastery estimate:
- basic vector intuition: `EXPLAIN`

## Vector Search

Basic pipeline:
1. split source text into chunks,
2. produce embeddings for chunks,
3. embed the user query,
4. compare query embedding to stored embeddings,
5. retrieve the most relevant chunks,
6. inject those chunks into the LLM context.

Important correction:
A vector database/search engine does not make mathematical similarity disappear. It stores/indexes vectors and performs/optimizes similarity retrieval.

Similarity concepts to learn better:
- cosine similarity
- Euclidean distance
- approximate nearest neighbor search
- hybrid search
- metadata filters
- re-ranking

Current mastery estimate:
- purpose of vector search: `UNDERSTAND`
- similarity math: `UNDERSTAND`
- Databricks Mosaic AI Vector Search implementation: `UNKNOWN`

## Chunking

A chunk is a block of source content used for retrieval.

Trade-off:
- chunks too small → may lose necessary context
- chunks too large → poorer retrieval precision, more irrelevant context, greater token/cost pressure, and possible model/index constraints

Need to study:
- chunk size
- overlap
- document-aware splitting
- semantic chunking
- advanced chunking
- relationship between chunking and retrieval evaluation
- effect of chunking on embedding count/index scale

Current mastery estimate:
- basic chunking trade-off: `EXPLAIN`
- chunking strategy selection: `UNDERSTAND`
- advanced chunking: `UNKNOWN`
