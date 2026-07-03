from rank_bm25 import BM25Okapi
from rich.console import Console

console = Console()

class BM25Retriever:
    def __init__(self):
        self.chunks = []
        self.bm25 = None

    def index_chunks(self, chunks: list) -> None:
        self.chunks = chunks
        tokenized = [chunk.content.lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized)
        console.print(f"[green]BM25 index built over {len(chunks)} chunks[/green]")

    def search(self, query: str, top_k: int = 5) -> list:
        if not self.bm25:
            console.print("[red]BM25 index not built.[/red]")
            return []

        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)
        scored = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        hits = []
        for idx, score in scored[:top_k]:
            chunk = self.chunks[idx]
            hits.append({
                "chunk_id": chunk.chunk_id,
                "content":  chunk.content,
                "metadata": {
                    "source_name":  chunk.metadata.source_name,
                    "doc_type":     chunk.metadata.doc_type.value,
                    "last_updated": str(chunk.metadata.last_updated),
                },
                "score": float(score)
            })
        return hits