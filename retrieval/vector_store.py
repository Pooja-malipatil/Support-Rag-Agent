import os

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams,
    PointStruct, Filter,
    FieldCondition, MatchValue
)
from rich.console import Console
from config.settings import Chunk
from retrieval.embedder import Embedder

console = Console()

COLLECTION_NAME = "support_docs"
VECTOR_SIZE     = 384

class VectorStore:
    def __init__(self, persist_dir: str = "./qdrant_db"):
        import os
        from dotenv import load_dotenv
        load_dotenv()

    # Try Streamlit secrets first (when deployed)
        try:
            import streamlit as st
            qdrant_url     = st.secrets.get("QDRANT_URL")
            qdrant_api_key = st.secrets.get("QDRANT_API_KEY")
        except Exception:
            qdrant_url     = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")

        qdrant_host = os.getenv("QDRANT_HOST")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

        if qdrant_url and qdrant_api_key:
            console.print(f"[dim]Connecting to Qdrant Cloud...[/dim]")
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key
            )
        elif qdrant_host:
            console.print(f"[dim]Connecting to Qdrant at {qdrant_host}:{qdrant_port}[/dim]")
            self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        else:
            self.client = QdrantClient(path=persist_dir)

        self.embedder = Embedder()
        self._ensure_collection()

    def _ensure_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if COLLECTION_NAME not in existing:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
            console.print(f"[green]✓ Created Qdrant collection: {COLLECTION_NAME}[/green]")
        else:
            count = self.client.count(COLLECTION_NAME).count
            console.print(f"[green]✓ Qdrant ready — {count} chunks indexed[/green]")

    def index_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            console.print("[yellow]No chunks to index.[/yellow]")
            return

        console.print(f"\n[bold]Indexing {len(chunks)} chunks into Qdrant...[/bold]")

        texts      = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_batch(texts)

        points = []
        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            points.append(PointStruct(
                id      = i,
                vector  = vector,
                payload = {
                    "chunk_id":    chunk.chunk_id,
                    "content":     chunk.content,
                    "source_name": chunk.metadata.source_name,
                    "section":     chunk.metadata.section,
                    "doc_type":    chunk.metadata.doc_type.value,
                    "access_level":chunk.metadata.access_level.value,
                    "last_updated":str(chunk.metadata.last_updated),
                    "strategy":    chunk.strategy.value,
                    "chunk_index": chunk.chunk_index,
                    "file_path":   chunk.file_path,
                }
            ))

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        console.print(f"[green]✓ Indexed {len(chunks)} chunks[/green]")

    def search(self, query: str, top_k: int = 5, doc_type: str = None) -> list[dict]:
        query_vector = self.embedder.embed_text(query)

        query_filter = None
        if doc_type:
            query_filter = Filter(
                must=[FieldCondition(
                    key="doc_type",
                    match=MatchValue(value=doc_type)
                )]
            )

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True
        ).points

        hits = []
        for r in results:
            hits.append({
                "chunk_id": r.payload["chunk_id"],
                "content":  r.payload["content"],
                "metadata": {
                    "source_name":  r.payload["source_name"],
                    "doc_type":     r.payload["doc_type"],
                    "last_updated": r.payload["last_updated"],
                },
                "score": round(r.score, 4)
            })

        return hits