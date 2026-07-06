from rich.console import Console
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.query_rewriter import QueryRewriter
from retrieval.compressor import ContextualCompressor
from config.settings import Chunk

console = Console()


class SmartRetriever:
    """
    Extends HybridRetriever with:
    - Query rewriting (single or multi)
    - Contextual compression
    """

    def __init__(self):
        self.hybrid     = HybridRetriever()
        self.rewriter   = QueryRewriter()
        self.compressor = ContextualCompressor()

    def index_chunks(self, chunks: list[Chunk]) -> None:
        self.hybrid.index_chunks(chunks)

    def search(
        self,
        question:   str,
        top_k:      int  = 5,
        mode:       str  = "rewrite",
        compress:   bool = False
    ) -> list[dict]:
        """
        mode options:
        - 'standard'    — no rewriting
        - 'rewrite'     — single rewrite before search
        - 'multi_query' — 3 rewrites, merged results

        compress=True adds contextual compression after retrieval.
        """
        # Step 1: Retrieve
        if mode == "standard":
            hits = self.hybrid.search(question, top_k=top_k)

        elif mode == "rewrite":
            rewritten = self.rewriter.rewrite_single(question)
            hits      = self.hybrid.search(rewritten, top_k=top_k)

        elif mode == "multi_query":
            hits = self._multi_query_search(question, top_k=top_k)

        else:
            raise ValueError(f"Unknown mode: {mode}")

        # Step 2: Compress (optional)
        if compress:
            hits = self.compressor.compress(question, hits)

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