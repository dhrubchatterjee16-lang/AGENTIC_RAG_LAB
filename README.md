# Agentic RAG Lab: Multi-Agent Literature & Patent Discovery for Chemical Sciences

Agentic RAG Lab is a specialized retrieval-augmented generation framework designed to ingest, cross-verify, and synthesize scientific research papers, reactive chemicals safety sheets (MSDS), and patent claims.

## Core Capabilities
- **Hierarchical Document Chunking:** Formatted specifically for chemical patents to keep IUPAC names, reaction conditions, yields, and claim dependencies contiguous.
- **Hybrid Retrieval:** Dense vector retrieval (BGE-Large / text-embedding-3) fused with lexical BM25 using Reciprocal Rank Fusion (RRF).
- **Multi-Agent Verification Pipeline:**
  1. *Query Decomposer Agent:* Splits complex synthetic queries into sub-questions (catalyst, solvent, temperature, safety).
  2. *Retrieval & Cross-Referencer Agent:* Fetches literature passages from ArXiv / ChemRxiv / Patents.
  3. *Hallucination Scrutinizer Agent:* Re-checks model-generated claims against source citation bounding boxes.

## Quickstart
```bash
git clone https://github.com/dhrubchatterjee16-lang/AGENTIC_RAG_LAB.git
cd AGENTIC_RAG_LAB
pip install -r requirements.txt
python demo_agent.py --query "Optimal solvent selection for Suzuki coupling with base-sensitive halides"
```
