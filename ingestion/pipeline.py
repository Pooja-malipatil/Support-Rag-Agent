from pathlib import Path
from rich.console import Console
from rich.table import Table
from ingestion.loaders import load_all_documents
from ingestion.chunker import chunk_by_headings, chunk_by_fixed_size
from config.settings import ChunkStrategy, Chunk

console = Console()

def run_ingestion(docs_dir: Path, strategy: ChunkStrategy = ChunkStrategy.HEADING) -> list[Chunk]:
    """
    Full ingestion pipeline:
    1. Load all documents from docs_dir
    2. Chunk each document with the chosen strategy
    3. Return all chunks with a summary table
    """
    # Step 1: Load
    documents = load_all_documents(docs_dir)
    if not documents:
        console.print("[red]No documents loaded. Check your docs/ folder.[/red]")
        return []

    # Step 2: Chunk
    all_chunks = []
    for doc in documents:
        if strategy == ChunkStrategy.HEADING:
            chunks = chunk_by_headings(doc)
        else:
            chunks = chunk_by_fixed_size(doc)
        all_chunks.extend(chunks)

    # Step 3: Show summary table
    table = Table(title=f"Ingestion Complete — Strategy: {strategy}")
    table.add_column("Chunk ID",   style="cyan")
    table.add_column("Doc Type",   style="magenta")
    table.add_column("Words",      justify="right")
    table.add_column("Preview",    style="dim")

    for chunk in all_chunks:
        word_count = str(len(chunk.content.split()))
        preview    = chunk.content[:60].replace("\n", " ") + "..."
        table.add_row(chunk.chunk_id, chunk.metadata.doc_type, word_count, preview)

    console.print(table)
    console.print(f"\n[bold green]Total chunks produced: {len(all_chunks)}[/bold green]")
    return all_chunks