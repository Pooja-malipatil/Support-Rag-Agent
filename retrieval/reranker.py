from sentence_transformers import CrossEncoder
from rich.console import Console

console = Console()

# This model is specifically trained for relevance ranking
# It scores query-passage pairs on a 0-1 relevance scale
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker:
    """
    Re-ranks retrieved chunks using a cross-encoder model.

    The cross-encoder reads query and chunk together,
    producing a precise relevance score. Much more accurate
    than cosine similarity but too slow for initial retrieval.

    Typical usage:
    - Retrieve top 20 with hybrid retrieval (fast)
    - Re-rank top 20 with cross-encoder (precise)
    - Return top 5 to generator
    """

    def __init__(self):
        console.print(f"[dim]Loading cross-encoder: {MODEL_NAME}...[/dim]")
        self.model = CrossEncoder(MODEL_NAME)
        console.print("[green]✓ Cross-encoder loaded[/green]")

    def rerank(
        self,
        query:  str,
        chunks: list[dict],
        top_k:  int = 5
    ) -> list[dict]:
        """
        Re-ranks chunks by relevance to the query.
        Returns top_k chunks sorted by cross-encoder score.
        """
        if not chunks:
            return chunks

        # Build query-passage pairs for the cross-encoder
        # Format: [[query, passage1], [query, passage2], ...]
        pairs = [[query, chunk["content"]] for chunk in chunks]

        # Score all pairs in one batch — efficient
        scores = self.model.predict(pairs)

        # Attach scores to chunks
        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = round(float(score), 4)

        # Sort by rerank score descending
        reranked = sorted(
            chunks,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        # Log the reranking changes
        original_order = [c["chunk_id"] for c in chunks]
        new_order      = [c["chunk_id"] for c in reranked[:top_k]]

        console.print(f"[dim]Reranked {len(chunks)} chunks → top {top_k}[/dim]")
        for i, chunk in enumerate(reranked[:top_k]):
            original_rank = original_order.index(chunk["chunk_id"]) + 1
            movement      = original_rank - (i + 1)
            movement_str  = (
                f"↑{movement}"  if movement > 0
                else f"↓{abs(movement)}" if movement < 0
                else "="
            )
            console.print(
                f"[dim]  {i+1}. {chunk['chunk_id']} "
                f"(was {original_rank}) {movement_str} "
                f"score: {chunk['rerank_score']}[/dim]"
            )

        return reranked[:top_k]