import os
from groq import Groq
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()
MODEL   = "llama-3.1-8b-instant"


def get_client():
    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)


class QueryRewriter:

    def _call(self, prompt: str, max_tokens: int = 200) -> str:
        client   = get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def rewrite_single(self, question: str) -> str:
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

        rewritten = self._call(prompt).strip('"\'')
        console.print(f"[dim]Query rewrite: '{question}' → '{rewritten}'[/dim]")
        return rewritten

    def rewrite_multi(self, question: str) -> list[str]:
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

        raw     = self._call(prompt, max_tokens=300)
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

        rewritten = self._call(prompt).strip('"\'')
        console.print(f"[dim]Memory rewrite: '{question}' → '{rewritten}'[/dim]")
        return rewritten