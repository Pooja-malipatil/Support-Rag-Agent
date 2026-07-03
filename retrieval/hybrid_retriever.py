from rich.console import Console
from retrieval.vector_store import VectorStore
from retrieval.bm25_retriever import BM25Retriever

console = Console()
RRF_K = 60

class HybridRetriever:
    def __init__(self):
        self.vector_store   = VectorStore()
        self.bm25_retriever = BM25Retriever()

    def index_chunks(self, chunks: list) -> None:
        self.vector_store.index_chunks(chunks)
        self.bm25_retriever.index_chunks(chunks)

    def search(self, query: str, top_k: int = 5) -> list:
        dense_hits  = self.vector_store.search(query, top_k=20)
        sparse_hits = self.bm25_retriever.search(query, top_k=20)
        fused = self._reciprocal_rank_fusion(dense_hits, sparse_hits)
        return fused[:top_k]

    def _reciprocal_rank_fusion(self, dense_hits: list, sparse_hits: list) -> list:
        rrf_scores = {}
        chunk_data = {}

        for rank, hit in enumerate(dense_hits):
            cid = hit["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0) + 1 / (RRF_K + rank + 1)
            chunk_data[cid] = hit

        for rank, hit in enumerate(sparse_hits):
            cid = hit["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0) + 1 / (RRF_K + rank + 1)
            if cid not in chunk_data:
                chunk_data[cid] = hit

        sorted_ids = sorted(rrf_scores, key=lambda x: rrf_scores[x], reverse=True)

        results = []
        for cid in sorted_ids:
            result = chunk_data[cid].copy()
            result["rrf_score"] = round(rrf_scores[cid], 6)
            results.append(result)

        return results