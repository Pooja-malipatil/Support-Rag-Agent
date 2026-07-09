from rich.console import Console
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.query_rewriter import QueryRewriter
from retrieval.compressor import ContextualCompressor
from retrieval.reranker import CrossEncoderReranker
from config.settings import Chunk

console = Console()


class SmartRetriever:
    """
    Full smart retrieval pipeline with:
    - Query rewriting (single or multi)
    - Contextual compression
    - Cross-encoder re-ranking
    """

    def __init__(self, use_reranker: bool = True):
        self.hybrid     = HybridRetriever()
        self.rewriter   = QueryRewriter()
        self.compressor = ContextualCompressor()
        self.reranker   = CrossEncoderReranker() if use_reranker else None

    def index_chunks(self, chunks: list[Chunk]) -> None:
        self.hybrid.index_chunks(chunks)

    def search(
        self,
        question: str,
        top_k:    int  = 5,
        mode:     str  = "rewrite",
        compress: bool = False,
        rerank:   bool = False
    ) -> list[dict]:
        """
        Full retrieval pipeline with optional upgrades.

        mode:     'standard' | 'rewrite' | 'multi_query'
        compress: True to apply contextual compression
        rerank:   True to apply cross-encoder re-ranking
        """
        # Stage 1: Retrieve more candidates if reranking
        # We need more candidates so reranker has room to reorder
        fetch_k = top_k * 4 if rerank else top_k

        # Retrieve
        if mode == "standard":
            hits = self.hybrid.search(question, top_k=fetch_k)
        elif mode == "rewrite":
            rewritten = self.rewriter.rewrite_single(question)
            hits      = self.hybrid.search(rewritten, top_k=fetch_k)
        elif mode == "multi_query":
            hits = self._multi_query_search(question, top_k=fetch_k)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        # Optional: compress
        if compress:
            hits = self.compressor.compress(question, hits)

        # Optional: rerank
        if rerank and self.reranker:
            hits = self.reranker.rerank(question, hits, top_k=top_k)
        else:
            hits = hits[:top_k]

        return hits

    def _multi_query_search(self, question: str, top_k: int) -> list[dict]:
        queries  = self.rewriter.rewrite_multi(question)
        seen_ids = set()
        all_hits = []

        for query in queries:
            hits = self.hybrid.search(query, top_k=top_k)
            for hit in hits:
                if hit["chunk_id"] not in seen_ids:
                    seen_ids.add(hit["chunk_id"])
                    all_hits.append(hit)

        all_hits.sort(
            key=lambda x: x.get("rrf_score", 0),
            reverse=True
        )
        return all_hits[:top_k]