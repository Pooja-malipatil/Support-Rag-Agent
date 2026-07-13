import os
import re
from groq import Groq
from dotenv import load_dotenv
from rich.console import Console
from generation.prompt_builder import build_answer_prompt, build_verification_prompt

load_dotenv()
console = Console()
MODEL   = "llama-3.1-8b-instant"


class AnswerGenerator:
    def __init__(self):
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found")

        self.client = Groq(api_key=api_key)
        console.print(f"[green]✓ Groq connected — using {MODEL}[/green]")

    def generate(
        self,
        question: str,
        chunks:   list[dict],
        history:  str = ""
    ) -> dict:
        if not chunks:
            return self._no_answer_response(question, reason="no chunks retrieved")

        prompt     = build_answer_prompt(question, chunks, history=history)
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
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _parse_citations(self, answer: str) -> list[str]:
        pattern = r'\[([^\]]+)\]'
        matches = re.findall(pattern, answer)
        seen    = set()
        unique  = []
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
        verdicts = {}
        for chunk_id in cited_ids:
            if chunk_id not in chunk_map:
                verdicts[chunk_id] = "NOT_FOUND"
                continue
            claim               = self._extract_claim_for_citation(answer, chunk_id)
            chunk_content       = chunk_map[chunk_id]
            verification_prompt = build_verification_prompt(claim, chunk_content)
            verdict             = self._call_llm(verification_prompt).strip().upper()
            if "SUPPORTED" in verdict and "PARTIAL" not in verdict:
                verdicts[chunk_id] = "SUPPORTED"
            elif "PARTIAL" in verdict:
                verdicts[chunk_id] = "PARTIAL"
            else:
                verdicts[chunk_id] = "UNSUPPORTED"
        return verdicts

    def _extract_claim_for_citation(self, answer: str, chunk_id: str) -> str:
        sentences = re.split(r'(?<=[.!?])\s+', answer)
        for sentence in sentences:
            if chunk_id in sentence:
                return re.sub(r'\[[^\]]+\]', '', sentence).strip()
        return answer[:200]

    def _calculate_confidence(
        self,
        cited_ids: list[str],
        verdicts:  dict[str, str],
        chunks:    list[dict]
    ) -> dict:
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