from pathlib import Path
from ingestion.pipeline import run_ingestion
from retrieval.smart_retriever import SmartRetriever
from config.settings import ChunkStrategy
from rich.console import Console

console = Console()

if __name__ == "__main__":
    console.print("\n[bold cyan]Running full ingestion pipeline...[/bold cyan]")

    docs_dir = Path("docs")
    chunks   = run_ingestion(docs_dir, strategy=ChunkStrategy.HEADING)

    console.print(f"\n[bold]Indexing {len(chunks)} chunks into Qdrant...[/bold]")
    retriever = SmartRetriever(use_reranker=False)
    retriever.index_chunks(chunks)
    retriever.hybrid.vector_store.client.close()

    console.print(f"\n[bold green]Done! {len(chunks)} chunks indexed and ready.[/bold green]")
    console.print("[dim]Now run: streamlit run app.py[/dim]")