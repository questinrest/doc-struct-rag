# DocStructRAG

DocStructRAG is a structure-aware documentation RAG pipeline built to preserve semantic hierarchy, code examples, and contextual relationships during ingestion.

Unlike generic document loaders, this system performs custom crawling, HTML structure-aware parsing, and hierarchical chunking (h1/h2/h3) to produce high-coherence, citation-grounded answers over technical documentation.


## Key Features

- Custom web crawling and document preparation over 104 documentation pages (FastAPI). 
- Structure-aware parsing of headings, code blocks, lists, and explanations.
- Hierarchical chunking to preserve semantic context.
- Citation-grounded answers with explicit source URLs.
- Evaluation using RAGAS (faithfulness and context precision).
- Dockerized, minimal chatbot-style interface for interactive Q&A.

## Scope & Limitations

- Optimized for HTML-based technical documentation (e.g., FastAPI docs).
- Uses LangChain for embeddings, retrieval, and generation.
- No incremental crawling or change detection.
- Evaluation performed on a limited question set using RAGAS.


