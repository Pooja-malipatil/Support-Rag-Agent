import ollama
from rich.console import Console

console = Console()
MODEL = "llama3.2"


class QueryRewriter:
    """
    Rewrites user questions into better search queries
    before they hit the retrieval system.
    """

    def rewrite_single(self, question: str) -> str:
        """Rewrites the question into one precise search query."""
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
        rewritten = response["message"]["content"].strip().strip('"\'')
        console.print(f"[dim]Query rewrite: '{question}' → '{rewritten}'[/dim]")
        return rewritten

    def rewrite_multi(self, question: str) -> list[str]:
        """Generates 3 different rewrites of the same question."""
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

        raw     = response["message"]["content"].strip()
        queries = [
            line.strip().strip('"\'')
            for line in raw.split('\n')
            if line.strip()
        ][:3]

        if len(queries) < 3:
            queries.append(question)

        console.print(f"[dim]Multi-query rewrites for: '{question}'[/dim]")
        for i, q in enumerate(queries):
            console.print(f"[dim]  {i+1}. {q}[/dim]")

        return queries

    def rewrite_with_history(self, question: str, history: str) -> str:
        """
        Rewrites a follow-up question into a standalone question
        using conversation history.

        Example:
        History:  "Q: What are Free tier rate limits? A: 100 req/min"
        Question: "What about Pro?"
        Rewritten: "What are the Pro tier rate limits?"
        """
        if not history:
            return question

        prompt = f"""Given a conversation history and a follow-up question,
rewrite the follow-up as a complete standalone question that contains
all necessary context from the history.

Rules:
- The rewritten question must make sense WITHOUT the history
- Keep it concise — one sentence maximum
- If the question is already standalone, return it unchanged
- Return ONLY the rewritten question, nothing else

Conversation history:
{history}

Follow-up question: {question}

Standalone question:"""

        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        rewritten = response["message"]["content"].strip().strip('"\'')
        console.print(f"[dim]Memory rewrite: '{question}' → '{rewritten}'[/dim]")
        return rewritten