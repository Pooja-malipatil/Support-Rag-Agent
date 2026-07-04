import re
import ollama
from rich.console import Console
from generation.prompt_builder import build_answer_prompt, build_verification_prompt

console = Console()

MODEL = "llama3.2"

class AnswerGenerator:
    def __init__(self):
        # Test that Ollama is running and model is available
        try:
            ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": "hi"}]
            )
            console.print(f"[green]✓ Ollama connected — using {MODEL}[/green]")
        except Exception as e:
            raise RuntimeError(
                f"Could not connect to Ollama. "
                f"Make sure Ollama is running and '{MODEL}' is pulled.\n"
                f"Run: ollama pull {MODEL}\nError: {e}"
            )

    def generate(self, question: str, chunks: list[dict]) -> dict:
        """
        Full pipeline:
        1. Build prompt with chunks
        2. Generate answer
        3. Parse citations
        4. Verify each citation
        5. Return structured result
        """
        if not chunks:
            return self._no_answer_response(question, reason="no chunks retrieved")

        prompt    = build_answer_prompt(question, chunks)
        raw_answer = self._call_llm(prompt)

        if "could not find this information" in raw_answer.lower():
            return self._no_answer_response(question, reason="not in documentation")

        cited_ids  = self._parse_citations(raw_answer)
        chunk_map  = {c["chunk_id"]: c["content"] for c in chunks}
        verdicts   = self._verify_citations(raw_answer, cited_ids, chunk_map)
        confidence = self._calculate_confidence(cited_ids, verdicts, chunks)

        return {
            "question":    question,
            "answer":      raw_answer,
            "cited_ids":   cited_ids,
            "verdicts":    verdicts,
            "confidence":  confidence,
            "chunks_used": len(chunks),
            "no_answer":   False,
        }

    def _call_llm(self, prompt: str) -> str:
        """Makes a single Ollama call and returns the text response."""
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()

    def _parse_citations(self, answer: str) -> list[str]:
        """
        Extracts all [chunk-id] references from the answer text.
        Returns a deduplicated list of chunk IDs.
        """
        pattern = r'\[([^\]]+)\]'
        matches = re.findall(pattern, answer)

        seen   = set()
        unique = []
        for m in matches:
            if m not in seen:
                seen.add(m)
                unique.append(m)
        return unique

    def _verify_citations(
        self,
        answer:    str,
        cited_ids: list[str],
        chunk_map: dict[str, str]
    ) -> dict[str, str]:
        """
        For each cited chunk ID, verifies whether it supports
        the claim made near it in the answer.
        """
        verdicts = {}

        for chunk_id in cited_ids:
            if chunk_id not in chunk_map:
                verdicts[chunk_id] = "NOT_FOUND"
                continue

            claim         = self._extract_claim_for_citation(answer, chunk_id)
            chunk_content = chunk_map[chunk_id]

            verification_prompt = build_verification_prompt(claim, chunk_content)
            verdict             = self._call_llm(verification_prompt)

            verdict = verdict.strip().upper()
            if "SUPPORTED" in verdict and "PARTIAL" not in verdict:
                verdicts[chunk_id] = "SUPPORTED"
            elif "PARTIAL" in verdict:
                verdicts[chunk_id] = "PARTIAL"
            else:
                verdicts[chunk_id] = "UNSUPPORTED"

        return verdicts

    def _extract_claim_for_citation(self, answer: str, chunk_id: str) -> str:
        """
        Finds the sentence containing [chunk_id] and returns
        it as the claim to verify.
        """
        sentences = re.split(r'(?<=[.!?])\s+', answer)

        for sentence in sentences:
            if chunk_id in sentence:
                claim = re.sub(r'\[[^\]]+\]', '', sentence).strip()
                return claim

        return answer[:200]

    def _calculate_confidence(
        self,
        cited_ids: list[str],
        verdicts:  dict[str, str],
        chunks:    list[dict]
    ) -> dict:
        """Combines signals into a confidence score with breakdown."""
        rrf_scores    = [c.get("rrf_score", 0) for c in chunks[:3]]
        avg_retrieval = sum(rrf_scores) / len(rrf_scores) if rrf_scores else 0

        if verdicts:
            supported     = sum(
                1 for v in verdicts.values()
                if v in ("SUPPORTED", "PARTIAL")
            )
            citation_rate = supported / len(verdicts)
        else:
            citation_rate = 0.0

        has_citations = 1.0 if cited_ids else 0.0

        combined = (
            avg_retrieval * 40 +
            citation_rate  * 40 +
            has_citations  * 20
        )

        return {
            "score":            round(combined, 2),
            "retrieval_signal": round(avg_retrieval * 40, 2),
            "citation_signal":  round(citation_rate * 40, 2),
            "has_citations":    bool(cited_ids),
        }

    def _no_answer_response(self, question: str, reason: str) -> dict:
        """Returns a structured response when we can't answer."""
        return {
            "question":    question,
            "answer":      "I could not find this information in the documentation.",
            "cited_ids":   [],
            "verdicts":    {},
            "confidence":  {"score": 0.0},
            "chunks_used": 0,
            "no_answer":   True,
            "reason":      reason,
        }