import ollama
from rich.console import Console

console = Console()
MODEL = "llama3.2"


class ContextualCompressor:
    """
    Compresses retrieved chunks by extracting only the
    sentences relevant to the user's question.

    This reduces noise in the context window and helps
    the LLM focus on what actually answers the question.
    """

    def compress(
        self,
        question: str,
        chunks:   list[dict],
        min_length: int = 30
    ) -> list[dict]:
        """
        Takes retrieved chunks and compresses each one.
        Returns a new list of chunks with compressed content.
        Chunks that are entirely irrelevant are dropped.
        """
        compressed = []

        for chunk in chunks:
            result = self._compress_single(question, chunk)

            if result is None:
                # Chunk was entirely irrelevant — drop it
                console.print(
                    f"[dim]Dropped irrelevant chunk: {chunk['chunk_id']}[/dim]"
                )
                continue

            compressed_text, kept_ratio = result

            # Skip if compression produced something too short
            if len(compressed_text) < min_length:
                console.print(
                    f"[dim]Dropped too-short chunk: {chunk['chunk_id']}[/dim]"
                )
                continue

            # Build compressed chunk — same structure, smaller content
            compressed_chunk = chunk.copy()
            compressed_chunk["content"]          = compressed_text
            compressed_chunk["original_content"] = chunk["content"]
            compressed_chunk["compression_ratio"] = kept_ratio

            console.print(
                f"[dim]Compressed {chunk['chunk_id']}: "
                f"{len(chunk['content'])} → {len(compressed_text)} chars "
                f"({round(kept_ratio * 100)}% kept)[/dim]"
            )
            compressed.append(compressed_chunk)

        # If compression dropped everything, fall back to originals
        if not compressed:
            console.print(
                "[yellow]All chunks compressed away — "
                "falling back to originals[/yellow]"
            )
            return chunks

        return compressed

    def _compress_single(
        self,
        question: str,
        chunk:    dict
    ) -> tuple[str, float] | None:
        """
        Compresses one chunk against the question.
        Returns (compressed_text, ratio) or None if irrelevant.
        """
        prompt = f"""You are a precise text extractor.

Given a question and a document chunk, extract ONLY the sentences 
from the chunk that directly help answer the question.

Rules:
- Copy sentences verbatim from the chunk — do not paraphrase
- Only include sentences that directly answer or support the question
- If NO sentences are relevant, respond with exactly: IRRELEVANT
- Do not add any explanation or commentary

Question: {question}

Chunk:
{chunk['content']}

Relevant sentences:"""

        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response["message"]["content"].strip()

        # Check if LLM said the chunk is irrelevant
        if result.upper() == "IRRELEVANT" or len(result) < 10:
            return None

        # Calculate how much of the original we kept
        original_len  = len(chunk["content"])
        compressed_len = len(result)
        ratio = compressed_len / original_len if original_len > 0 else 1.0

        return result, ratio