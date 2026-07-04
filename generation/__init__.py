from pathlib import Path
from ingestion.pipeline import run_ingestion
from retrieval.hybrid_retriever import HybridRetriever
from generation.generator import AnswerGenerator
from config.settings import ChunkStrategy
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

if __name__ == "__main__":
    # Ingest and index
    docs_dir = Path("docs")
    chunks   = run_ingestion(docs_dir, strategy=ChunkStrategy.HEADING)

    retriever = HybridRetriever()
    retriever.index_chunks(chunks)

    generator = AnswerGenerator()

    # Test questions
    test_questions = [
        "How do I reset my API key?",
        "What happens if I exceed the rate limit?",
        "How do I store my API key securely?",
        "Can I use the API to mine cryptocurrency?",  # answer exists
        "What is the refund policy?",                 # answer does NOT exist
    ]

    for question in test_questions:
        console.print(f"\n[bold cyan]Question:[/bold cyan] {question}")

        # Retrieve
        hits   = retriever.search(question, top_k=5)

        # Generate
        result = generator.generate(question, hits)

        # Display answer
        console.print(Panel(
            result["answer"],
            title="Answer",
            border_style="green" if not result["no_answer"] else "yellow"
        ))

        # Display citations and verdicts
        if result["cited_ids"]:
            table = Table(title="Citation Verdicts", show_header=True)
            table.add_column("Chunk ID",  style="cyan")
            table.add_column("Verdict",   style="bold")

            for cid in result["cited_ids"]:
                verdict = result["verdicts"].get(cid, "—")
                color   = {
                    "SUPPORTED":   "green",
                    "PARTIAL":     "yellow",
                    "UNSUPPORTED": "red",
                    "NOT_FOUND":   "red"
                }.get(verdict, "white")
                table.add_row(cid, f"[{color}]{verdict}[/{color}]")

            console.print(table)

        # Display confidence
        conf = result["confidence"]
        console.print(
            f"[dim]Confidence: {conf['score']}/100 | "
            f"Retrieval: {conf.get('retrieval_signal', 0)} | "
            f"Citations: {conf.get('citation_signal', 0)}[/dim]"
        )