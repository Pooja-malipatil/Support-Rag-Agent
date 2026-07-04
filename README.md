# Support Knowledge Copilot with Verified Citations

A production-grade RAG system that answers support questions using 
internal documentation, with hybrid retrieval and automatic citation 
verification.

## What it does

- Answers questions grounded strictly in provided documentation
- Cites every claim with the exact source chunk
- Automatically verifies whether each citation supports its claim
- Correctly refuses to answer when the information is not in the docs
- Uses hybrid retrieval (dense + BM25 + RRF) for better accuracy

## Results

Evaluated on a 13-question golden dataset covering direct lookups, 
multi-document questions, tricky inference questions, and unanswerable 
questions:

| Metric | Hybrid | Dense-Only | Improvement |
|---|---|---|---|
| Retrieval Accuracy | [YOUR]% | [YOUR]% | +[DIFF]% |
| Content Accuracy | [YOUR]% | [YOUR]% | +[DIFF]% |
| Refusal Accuracy | [YOUR]% | [YOUR]% | +[DIFF]% |
| Citation Quality | [YOUR]% | [YOUR]% | +[DIFF]% |

## Architecture

User Question
↓
Hybrid Retrieval (dense embeddings + BM25, fused with RRF)
↓
LLM reads top 5 chunks, generates grounded answer with citations
↓
Citation Verifier checks each claim against its cited source
↓
Structured response: answer + verdicts + confidence score

## Key design decisions

**Heading-based chunking over fixed-size:** Each chunk maps to one 
complete idea (a Q&A pair, a step, a policy section). Fixed-size 
chunking split ideas across boundaries and reduced retrieval precision.

**Hybrid retrieval over dense-only:** BM25 catches exact technical 
terms (error codes, product names) that semantic search misses. Dense 
retrieval catches paraphrased questions that BM25 misses. RRF combines 
both without requiring score normalization.

**Citation verification as a separate pass:** The answer generation 
and citation verification use separate LLM calls. This keeps each call 
focused on one task and makes failures easier to diagnose.

## Tech stack

- Embeddings: sentence-transformers (all-MiniLM-L6-v2, local)
- Vector store: Qdrant (local persistence)
- Sparse retrieval: BM25 via rank-bm25
- LLM: Ollama (llama3.2, fully local)
- Validation: Pydantic
- Evaluation: custom golden dataset with 4 question types

## Setup

```bash
# Install Ollama from https://ollama.com
ollama pull llama3.2

# Install dependencies
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Run evaluation
python main.py
```

## Project structure
support-rag/
├── docs/               # Knowledge base documents
├── ingestion/          # Document loading and chunking
├── retrieval/          # Hybrid retriever (dense + BM25 + RRF)
├── generation/         # Answer generation and citation verification
├── evaluation/         # Golden dataset and evaluator
└── main.py

