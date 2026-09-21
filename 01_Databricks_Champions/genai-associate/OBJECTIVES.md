# Associate objectives

Status: Draft learning record. Last reviewed: 2026-09-21.

Adapted from the supplied syllabus. March 18, 2026 baseline; see [source checks](../SOURCES.md). Re-map when the official guide changes.

### Section 1 — Design Applications

Topics include:
- prompt design for structured output
- selecting model tasks for business requirements
- selecting chain components
- translating business goals into AI pipeline inputs/outputs
- ordering tools for multi-stage reasoning
- deciding when/how to use Agent Bricks
  - Knowledge Assistant
  - Multiagent Supervisor
  - Information Extraction

### Section 2 — Data Preparation

Topics include:
- chunking strategies
- filtering irrelevant / harmful source content
- Python tools for extracting document content
- writing chunked text into Delta Lake / Unity Catalog
- selecting source documents
- retrieval evaluation
- advanced chunking
- re-ranking

### Section 3 — Application Development

Topics include:
- LangChain and similar tooling
- identifying quality/safety issues in outputs
- choosing chunking from evaluation results
- augmenting prompts with user context
- prompt engineering
- guardrails
- LLM selection
- embedding model/context-length selection
- model cards / model hubs / marketplace
- experiment metrics
- MLflow + Agent Framework
- evaluation vs monitoring
- multi-agent systems
- Genie Spaces / conversational APIs

### Section 4 — Assembling and Deploying Applications

Topics include:
- simple chains
- pyfunc model chains with pre/post-processing
- endpoint access control
- RAG components
- MLflow registration in Unity Catalog
- Vector Search index creation/querying
- Foundation Model APIs
- Mosaic AI Vector Search
- batch inference and `ai_query()`
- Vector Search architecture trade-offs
- persistent state / memory stores
- CI/CD for agents, prompts and Vector Search
- MCP servers
  - managed
  - external
  - custom
- prompt lifecycle/version control
- user interfaces:
  - Databricks Apps
  - Slack
  - Teams
  - etc.

### Section 5 — Governance

Topics include:
- masking
- guardrails against malicious input
- legal/licensing constraints on source data
- mitigation of problematic source text

### Section 6 — Evaluation and Monitoring

Topics include:
- model selection using quantitative metrics
- deployment monitoring metrics
- MLflow scoring and tracing
- inference logging
- cost controls
- inference tables
- Agent Monitoring
- judges requiring ground truth
- AI Gateway
- Usage Tables
- rate limiting
- custom Scorers
- SME feedback and evaluation calibration
