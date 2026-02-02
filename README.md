# DocStructRAG: Structure-Aware Documentation RAG Pipeline 

A **structure-aware Retrieval-Augmented Generation (RAG) system** built over the official FastAPI documentation, focused on **clean parsing, hierarchy-aware chunking, and metadata-driven retrieval** for accurate, citation-grounded answers.

---

## Overview

This project is built on the principle that **retrieval quality dominates generation quality** in RAG systems.

Instead of relying on generic loaders or naive token-based chunking, the system crawls and parses FastAPI documentation from scratch, reconstructs its hierarchy, and aligns chunks to semantic sections with rich metadata for precise retrieval.

---

## Architecture

FastAPI Docs → Custom Crawler → HTML Parsing
→ Hierarchy Reconstruction → Structure-Aware Chunking
→ Metadata-Enriched Chunks → Vector Retrieval
→ LLM (Under Evaluation) → Grounded Answers + Sources



---

## Built From Scratch

- Documentation crawler and canonical traversal  
- HTML parsing and noise removal  
- Hierarchy reconstruction across pages  
- Structure-aware chunking strategy  
- Metadata schema for retrieval and citations  

Embeddings, vector storage, and evaluation tooling use standard libraries.

---

## Completed (as of now)

- **Custom web crawler** for 104 FastAPI pages with canonical URL handling and loop-safe traversal  
- **Manual HTML parsing** to extract headings, text, lists, and code blocks (indentation preserved)  
- **Hierarchy reconstruction** preserving h1/h2/h3 relationships across pages  
- **Structure-aware chunking**, keeping code and explanations together (~300+ chunks)  
- **Metadata design** (`section_path`, depth, URL, code flags) to enable filtered and citation-aware retrieval  
- **Vector-based retrieval** integrated with an instruction-tuned LLM  

---

## Key Design Decisions

### Why custom crawling instead of document loaders?
Generic loaders flatten structure and lose section boundaries.  
Custom crawling preserves **navigation order, canonical transitions, and hierarchy**, which is critical for documentation QA.

### Why hierarchy-aware chunking instead of token windows?
Documentation is inherently structured. Chunking along **section boundaries** keeps explanations and code together, improving retrieval precision and answer faithfulness.

### Why metadata-driven retrieval?
Metadata enables **scoped retrieval** (e.g. section depth, code-heavy sections) and reliable citation grounding, reducing context noise for smaller models.

### Why delay final LLM selection?
Model performance is highly dependent on retrieval quality.  
LLM size and architecture are being evaluated after retrieval stabilization to make informed tradeoffs between latency, cost, and faithfulness.

---

## Hierarchy

The system preserves documentation hierarchy during parsing and chunk construction, enabling **hierarchy-aware, metadata-driven retrieval**.  
Recursive or tree-walk retrieval is intentionally out of scope at this stage.

---

## In Progress

- **Conversation-based chatbot interface** (multi-turn QA)
- Retriever tuning and metadata-based filtering  
- Evaluation with **RAGAS**  
- LLM benchmarking and model-size tradeoff analysis  
- Dockerized deployment  
- User logs and activity tracking for usage analysis
- Refactoring Code
---


