import atexit
from pathlib import Path
from ingestion.pipeline import run_ingestion
from retrieval.smart_retriever import SmartRetriever
from generation.generator import AnswerGenerator
from evaluation.evaluator import Evaluator
from config.settings import ChunkStrategy
from rich.console import Console

console = Console()

if __name__ == "__main__":
    docs_dir = Path("docs")
    chunks   = run_ingestion(docs_dir, strategy=ChunkStrategy.HEADING)

    retriever = SmartRetriever()
    retriever.index_chunks(chunks)
    atexit.register(lambda: retriever.hybrid.vector_store.client.close())

    generator = AnswerGenerator()
    evaluator = Evaluator(retriever, generator)

    
    evaluator.run_reranking_comparison()