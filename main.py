from pathlib import Path
from ingestion.pipeline import run_ingestion
from retrieval.hybrid_retriever import HybridRetriever
from config.settings import ChunkStrategy
from rich.console import Console
from rich.table import Table

console = Console()

if __name__ == "__main__":
    # Step 1: Ingest with heading strategy (better for our structured docs)
    docs_dir = Path("docs")
    console.print("\n[bold cyan]=== INGESTION ===[/bold cyan]")
    chunks = run_ingestion(docs_dir, strategy=ChunkStrategy.HEADING)

    # Step 2: Build both indexes
    console.print("\n[bold cyan]=== INDEXING ===[/bold cyan]")
    retriever = HybridRetriever()
    retriever.index_chunks(chunks)

    # Step 3: Run test queries
    console.print("\n[bold cyan]=== RETRIEVAL TESTS ===[/bold cyan]")

    test_queries = [
        "How do I reset my API key?",
        "What happens if I exceed rate limits?",
        "HTTP 429 error",
        "how to rotate credentials securely",
    ]

    for query in test_queries:
        console.print(f"\n[bold yellow]Query:[/bold yellow] {query}")

        results = retriever.search(query, top_k=3)

        table = Table(show_header=True, header_style="bold")
        table.add_column("Rank",      width=6)
        table.add_column("Chunk ID",  style="cyan", width=32)
        table.add_column("RRF Score", justify="right", width=10)
        table.add_column("Preview",   width=45)

        for i, hit in enumerate(results):
            preview = hit["content"][:80].replace("\n", " ") + "..."
            table.add_row(
                str(i + 1),
                hit["chunk_id"],
                str(hit.get("rrf_score", "—")),
                preview
            )

        console.print(table)