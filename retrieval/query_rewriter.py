import ollama
from rich.console import Console

console = Console()
MODEL = "llama3.2"


class QueryRewriter:
    """
    Rewrites user questions into better search queries
    before they hit the retrieval system.

    Two modes:
    - single: one optimized rewrite
    - multi:  three different rewrites (more coverage)
    """

    def rewrite_single(self, question: str) -> str:
        """
        Rewrites the question into one precise search query.
        Returns the rewritten query as a string.
        """
        prompt = f"""You are a search query optimizer for a technical support knowledge base.

Rewrite the following user question into a precise search query that will find relevant documentation.

Rules:
- Use technical terminology that documentation would contain
- Expand abbreviations and casual language into precise terms
- Include relevant synonyms separated by spaces
- Keep it under 15 words
- Return ONLY the rewritten query, nothing else

User question: {question}

Rewritten query:"""

        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        rewritten = response["message"]["content"].strip()

        # Clean up — remove quotes if LLM added them
        rewritten = rewritten.strip('"\'')
        console.print(f"[dim]Query rewrite: '{question}' → '{rewritten}'[/dim]")
        return rewritten

    def rewrite_multi(self, question: str) -> list[str]:
        """
        Generates 3 different rewrites of the same question.
        Each rewrite approaches the question from a different angle.
        Returns a list of 3 query strings.
        """
        prompt = f"""You are a search query optimizer for a technical support knowledge base.

Generate 3 different search queries for the following user question.
Each query should approach the topic from a different angle to maximize retrieval coverage.

Rules:
- Use technical terminology that documentation would contain
- Each query should be different — don't just rephrase the same words
- Query 1: focus on the action/task
- Query 2: focus on the technical terms/error codes
- Query 3: focus on the outcome/solution

Return ONLY the 3 queries, one per line, no numbering, no explanation.

User question: {question}

Queries:"""

        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response["message"]["content"].strip()
        queries = [
            line.strip().strip('"\'')
            for line in raw.split('\n')
            if line.strip()
        ][:3]  # Take max 3

        # Always include original as fallback
        if len(queries) < 3:
            queries.append(question)

        console.print(f"[dim]Multi-query rewrites for: '{question}'[/dim]")
        for i, q in enumerate(queries):
            console.print(f"[dim]  {i+1}. {q}[/dim]")

        return queries