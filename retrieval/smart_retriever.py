from rich.console import Console
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.query_rewriter import QueryRewriter
from config.settings import Chunk

console = Console()


class SmartRetriever:
    """
    Extends HybridRetriever with query rewriting.
    Supports three search modes:
    - standard:     no rewriting (baseline)
    - rewrite:      single query rewrite before retrieval
    - multi_query:  multiple rewrites, results merged
    """

    def __init__(self):
        self.hybrid    = HybridRetriever()
        self.rewriter  = QueryRewriter()

    def index_chunks(self, chunks: list[Chunk]) -> None:
        self.hybrid.index_chunks(chunks)

    def search(
        self,
        question: str,
        top_k:    int = 5,
        mode:     str = "rewrite"
    ) -> list[dict]:
        """
        mode options:
        - 'standard'    — no rewriting, baseline behavior
        - 'rewrite'     — single rewrite before search
        - 'multi_query' — 3 rewrites, deduplicated merge
        """
        if mode == "standard":
            return self.hybrid.search(question, top_k=top_k)

        elif mode == "rewrite":
            rewritten = self.rewriter.rewrite_single(question)
            return self.hybrid.search(rewritten, top_k=top_k)

        elif mode == "multi_query":
            return self._multi_query_search(question, top_k=top_k)

        else:
            raise ValueError(f"Unknown mode: {mode}. Use standard/rewrite/multi_query")

    def _multi_query_search(self, question: str, top_k: int) -> list[dict]:
        """
        Runs 3 rewrites through hybrid retrieval,
        merges results, deduplicates, returns top_k.
        """
        queries  = self.rewriter.rewrite_multi(question)
        seen_ids = set()
        all_hits = []

        for query in queries:
            hits = self.hybrid.search(query, top_k=top_k)
            for hit in hits:
                if hit["chunk_id"] not in seen_ids:
                    seen_ids.add(hit["chunk_id"])
                    all_hits.append(hit)

        # Sort by RRF score if available, otherwise keep insertion order
        all_hits.sort(
            key=lambda x: x.get("rrf_score", 0),
            reverse=True
        )

        return all_hits[:top_k]