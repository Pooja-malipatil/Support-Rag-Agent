import atexit
from pathlib import Path
from ingestion.pipeline import run_ingestion
from retrieval.hybrid_retriever import HybridRetriever
from generation.generator import AnswerGenerator
from evaluation.evaluator import Evaluator
from config.settings import ChunkStrategy
from rich.console import Console

console = Console()

if __name__ == "__main__":
    # Ingest and index
    docs_dir = Path("docs")
    chunks   = run_ingestion(docs_dir, strategy=ChunkStrategy.HEADING)

    retriever = HybridRetriever()
    retriever.index_chunks(chunks)
    atexit.register(lambda: retriever.vector_store.client.close())

    generator = AnswerGenerator()

    # Run evaluation
    evaluator = Evaluator(retriever, generator)
    report    = evaluator.run()