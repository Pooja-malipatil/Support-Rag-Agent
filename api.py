import os
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rich.console import Console

from ingestion.pipeline import run_ingestion
from retrieval.smart_retriever import SmartRetriever
from generation.generator import AnswerGenerator
from config.settings import ChunkStrategy

console = Console()

# --- Global pipeline state ---
# We load everything once at startup and reuse it
retriever  = None
generator  = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once at startup — loads the full pipeline.
    This replaces the old @app.on_event("startup") pattern.
    """
    global retriever, generator

    console.print("\n[bold cyan]Starting RAG pipeline...[/bold cyan]")

    docs_dir = Path("docs")
    chunks   = run_ingestion(docs_dir, strategy=ChunkStrategy.HEADING)

    retriever = SmartRetriever(use_reranker=False)
    retriever.index_chunks(chunks)

    generator = AnswerGenerator()

    console.print("[bold green]Pipeline ready.[/bold green]\n")
    yield

    # Cleanup on shutdown
    if retriever:
        retriever.hybrid.vector_store.client.close()


app = FastAPI(
    title="Support Knowledge Copilot",
    lifespan=lifespan
)

# Allow browser to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response models ---
class AskRequest(BaseModel):
    question: str
    mode:     str = "standard"   # standard | rewrite | multi_query
    rerank:   bool = False


class CitationVerdict(BaseModel):
    chunk_id: str
    verdict:  str


class AskResponse(BaseModel):
    question:    str
    answer:      str
    no_answer:   bool
    cited_ids:   list[str]
    verdicts:    list[CitationVerdict]
    confidence:  float
    chunks_used: int
    retrieved:   list[dict]


# --- Endpoints ---
@app.get("/")
async def serve_ui():
    """Serves the chat UI."""
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    """Simple health check."""
    return {"status": "ok", "pipeline_ready": retriever is not None}


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """
    Main endpoint — takes a question, runs the full RAG pipeline,
    returns a grounded answer with citations.
    """
    if not retriever or not generator:
        return AskResponse(
            question=request.question,
            answer="Pipeline not ready. Please wait.",
            no_answer=True,
            cited_ids=[],
            verdicts=[],
            confidence=0.0,
            chunks_used=0,
            retrieved=[]
        )

    # Retrieve
    hits = retriever.search(
        request.question,
        top_k=5,
        mode=request.mode,
        rerank=request.rerank
    )

    # Generate
    result = generator.generate(request.question, hits)

    # Format verdicts for response
    verdicts = [
        CitationVerdict(chunk_id=cid, verdict=v)
        for cid, v in result.get("verdicts", {}).items()
    ]

    # Format retrieved chunks for display
    retrieved = [
        {
            "chunk_id":  h["chunk_id"],
            "preview":   h["content"][:150] + "...",
            "score":     h.get("rrf_score", h.get("rerank_score", 0)),
            "doc_type":  h.get("metadata", {}).get("doc_type", ""),
        }
        for h in hits[:3]
    ]

    return AskResponse(
        question=request.question,
        answer=result["answer"],
        no_answer=result["no_answer"],
        cited_ids=result.get("cited_ids", []),
        verdicts=verdicts,
        confidence=result["confidence"]["score"],
        chunks_used=result["chunks_used"],
        retrieved=retrieved
    )