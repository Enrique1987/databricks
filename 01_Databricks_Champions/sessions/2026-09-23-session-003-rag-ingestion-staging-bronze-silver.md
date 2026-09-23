# Session 003 — RAG ingestion and offline indexing

Status: Draft learning record. Last reviewed: 2026-09-23.

Source: learner-supplied summary of a conversational session on 2026-09-23. This document synthesizes the learning evidence rather than reproducing the conversation. The source reports conceptual explanations and corrections but no scored cold recall or scenario results, so mastery remains provisional.

## Architecture developed in the session

The working example follows a large enterprise document from raw arrival until it becomes searchable:

```text
raw file
→ staging or governed object storage
→ ingestion/control record
→ parsing and optional cleaning
→ retrieval chunks with metadata
→ embedding generation
→ vector index
```

Staging preserves the source file. A Bronze record can provide lineage, status, source metadata, retry control, and replayability while referring to the raw file by path. Persisting extracted text or binary content in Bronze is also possible. The physical representation and the Bronze/Silver boundary are architecture choices rather than universal rules.

Parsing extracts usable text and structure from a document. Cleaning removes content that degrades retrieval, such as repeated headers, OCR artifacts, or duplicated boilerplate. General removal of punctuation or stop words can destroy useful context and should not be assumed for modern embedding pipelines.

Chunking is the point where one document commonly becomes many retrieval records. Chunk size and boundaries are system-design choices constrained by document structure, expected questions, tokenizer/model limits, and evaluation. A value such as 500 tokens can be an experiment baseline, not a standard.

Tokens are tokenizer-defined text units. Parameters are learned numbers inside a model. Tokenization normally happens within model processing and may also be used explicitly to enforce chunk limits; a separate persisted token table is usually unnecessary.

An embedding is the vector representation produced for a chunk. A vector index is an additional search structure optimized for similarity retrieval; it is not a new embedding or a hash index. Hash lookup targets exact values, while vector retrieval targets nearby representations.

## Evidence and mastery

The supplied summary supports provisional EXPLAIN estimates for staging, chunking, token-versus-parameter, embedding-model output, and embedding-versus-vector. It supports UNDERSTAND for Bronze control, parsing versus cleaning, empirical chunk evaluation, tokenizer ownership, vector indexes, exact versus similarity lookup, model versus algorithm, and the offline path. The offline path is still awaiting cold recall, and no SOLVE or TEACH evidence exists.

## Corrections to retain

- Bronze need not contain the complete extracted document.
- Parsing and cleaning serve different purposes; neither means blindly removing natural-language structure.
- A fixed token count is a starting hypothesis, not a universally correct chunk size.
- Tokens and model parameters are different concepts.
- The embedding is represented as a vector; a vector index accelerates retrieval over those vectors.
- Hash and vector indexes optimize different kinds of search.

## Next action

Begin the next session with an unsupported explanation of the complete offline path. Then learn the online path from query embedding through top-k retrieval, metadata authorization, context construction, and generation. Introduce top-k, similarity scores, and metadata filtering before deeper ANN implementation details.
