from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from evaluation.golden_dataset import GOLDEN_DATASET

console = Console()

class Evaluator:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator

    def run(self, silent: bool = False) -> dict:
        if not silent:
            console.print("\n[bold cyan]=== EVALUATION SUITE ===[/bold cyan]")
            console.print(f"Running {len(GOLDEN_DATASET)} questions...\n")

        results = []
        for item in GOLDEN_DATASET:
            result = self._evaluate_single(item)
            results.append(result)
            self._print_single_result(result)

        report = self._build_report(results)
        self._print_report(report)
        return report

    def _evaluate_single(self, item: dict) -> dict:
        """Runs one question through the full pipeline and scores it."""
        question = item["question"]

        # Run retrieval
        hits = self.retriever.search(question, top_k=5)
        retrieved_ids = [h["chunk_id"] for h in hits]

        # Run generation
        result = self.generator.generate(question, hits)

        # Score 1: Retrieval — did expected chunks appear?
        expected  = item["expected_chunks"]
        retrieval_hit = all(
            any(exp in rid for rid in retrieved_ids)
            for exp in expected
        ) if expected else True

        # Score 2: Refusal — did system correctly refuse/answer?
        if item["should_refuse"]:
            refusal_correct = result["no_answer"]
        else:
            refusal_correct = not result["no_answer"]

        # Score 3: Answer content — does answer contain expected keywords?
        if item["answer_contains"] and not result["no_answer"]:
            answer_lower = result["answer"].lower()
            content_correct = any(
                kw.lower() in answer_lower
                for kw in item["answer_contains"]
            )
        else:
            content_correct = True  # unanswerable questions skip this check

        # Score 4: Citation quality
        verdicts = result.get("verdicts", {})
        if verdicts:
            supported = sum(
                1 for v in verdicts.values()
                if v in ("SUPPORTED", "PARTIAL")
            )
            citation_quality = supported / len(verdicts)
        else:
            citation_quality = 1.0 if item["should_refuse"] else 0.0

        return {
            "question":        question,
            "question_type":   item["question_type"],
            "retrieval_hit":   retrieval_hit,
            "refusal_correct": refusal_correct,
            "content_correct": content_correct,
            "citation_quality":citation_quality,
            "no_answer":       result["no_answer"],
            "answer":          result["answer"],
            "confidence":      result["confidence"]["score"],
            "retrieved_ids":   retrieved_ids,
            "expected_chunks": expected,
        }

    def _build_report(self, results: list[dict]) -> dict:
        """Aggregates individual results into overall metrics."""
        total = len(results)

        retrieval_hits   = sum(1 for r in results if r["retrieval_hit"])
        refusal_correct  = sum(1 for r in results if r["refusal_correct"])
        content_correct  = sum(1 for r in results if r["content_correct"])
        avg_citation     = sum(r["citation_quality"] for r in results) / total

        # Break down by question type
        types = {}
        for r in results:
            t = r["question_type"]
            if t not in types:
                types[t] = {"total": 0, "correct": 0}
            types[t]["total"] += 1
            # A result is fully correct if all signals pass
            fully_correct = (
                r["retrieval_hit"] and
                r["refusal_correct"] and
                r["content_correct"]
            )
            if fully_correct:
                types[t]["correct"] += 1

        return {
            "total":                  total,
            "retrieval_accuracy":     round(retrieval_hits  / total * 100, 1),
            "refusal_accuracy":       round(refusal_correct / total * 100, 1),
            "content_accuracy":       round(content_correct / total * 100, 1),
            "avg_citation_quality":   round(avg_citation    * 100, 1),
            "by_type":                types,
            "results":                results,
        }

    def _print_single_result(self, result: dict) -> None:
        """Prints a compact one-line result for each question."""
        icons = {
            "retrieval_hit":   "✓" if result["retrieval_hit"]   else "✗",
            "refusal_correct": "✓" if result["refusal_correct"] else "✗",
            "content_correct": "✓" if result["content_correct"] else "✗",
        }
        color = "green" if all(
            v == "✓" for v in icons.values()
        ) else "red"

        console.print(
            f"[{color}]{icons['retrieval_hit']}R "
            f"{icons['refusal_correct']}F "
            f"{icons['content_correct']}C[/{color}] "
            f"[dim]{result['question_type']:15}[/dim] "
            f"{result['question'][:55]}"
        )

    def _print_report(self, report: dict) -> None:
        """Prints the final summary report."""
        console.print("\n")

        # Overall metrics table
        table = Table(title="Evaluation Results", show_header=True)
        table.add_column("Metric",   style="cyan", width=30)
        table.add_column("Score",    justify="right", width=10)
        table.add_column("Meaning",  style="dim")

        table.add_row(
            "Retrieval Accuracy",
            f"{report['retrieval_accuracy']}%",
            "Did the right chunks appear in top 5?"
        )
        table.add_row(
            "Refusal Accuracy",
            f"{report['refusal_accuracy']}%",
            "Did it correctly answer/refuse?"
        )
        table.add_row(
            "Content Accuracy",
            f"{report['content_accuracy']}%",
            "Did answers contain correct information?"
        )
        table.add_row(
            "Avg Citation Quality",
            f"{report['avg_citation_quality']}%",
            "Were citations supported by chunks?"
        )
        console.print(table)

        # By question type
        type_table = Table(title="Results by Question Type", show_header=True)
        type_table.add_column("Type",    style="cyan")
        type_table.add_column("Correct", justify="right")
        type_table.add_column("Total",   justify="right")
        type_table.add_column("Score",   justify="right")

        for qtype, stats in report["by_type"].items():
            score = round(stats["correct"] / stats["total"] * 100, 1)
            color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
            type_table.add_row(
                qtype,
                str(stats["correct"]),
                str(stats["total"]),
                f"[{color}]{score}%[/{color}]"
            )

        console.print(type_table)

        # Summary verdict
        overall = (
            report["retrieval_accuracy"] +
            report["refusal_accuracy"] +
            report["content_accuracy"]
        ) / 3

        color = "green" if overall >= 70 else "yellow" if overall >= 50 else "red"
        console.print(Panel(
            f"[{color}]Overall Score: {round(overall, 1)}%[/{color}]\n"
            f"[dim]Across {report['total']} questions — "
            f"retrieval + refusal + content averaged[/dim]",
            title="Final Verdict"
        ))def run_comparison(self) -> dict:
    """
    Runs the golden dataset twice:
    once with hybrid retrieval, once with dense-only.
    Returns both reports for comparison.
    """
    console.print("\n[bold cyan]=== RETRIEVAL COMPARISON ===[/bold cyan]")
    console.print("Running hybrid vs dense-only on the same questions...\n")

    # --- Hybrid results (already have this) ---
    console.print("[bold]1. Hybrid Retrieval (dense + BM25 + RRF)[/bold]")
    hybrid_report = self.run(silent=True)

    # --- Dense-only results ---
    console.print("\n[bold]2. Dense-Only Retrieval (embeddings only)[/bold]")
    dense_report = self._run_dense_only()

    # --- Print comparison table ---
    self._print_comparison(hybrid_report, dense_report)

    return {"hybrid": hybrid_report, "dense": dense_report}

def _run_dense_only(self) -> dict:
    """Runs eval using only the vector store, bypassing BM25."""
    results = []
    for item in GOLDEN_DATASET:
        question = item["question"]

        # Use vector store directly instead of hybrid retriever
        hits = self.retriever.vector_store.search(question, top_k=5)
        retrieved_ids = [h["chunk_id"] for h in hits]

        result = self.generator.generate(question, hits)

        expected      = item["expected_chunks"]
        retrieval_hit = all(
            any(exp in rid for rid in retrieved_ids)
            for exp in expected
        ) if expected else True

        if item["should_refuse"]:
            refusal_correct = result["no_answer"]
        else:
            refusal_correct = not result["no_answer"]

        if item["answer_contains"] and not result["no_answer"]:
            answer_lower    = result["answer"].lower()
            content_correct = any(
                kw.lower() in answer_lower
                for kw in item["answer_contains"]
            )
        else:
            content_correct = True

        verdicts = result.get("verdicts", {})
        if verdicts:
            supported = sum(
                1 for v in verdicts.values()
                if v in ("SUPPORTED", "PARTIAL")
            )
            citation_quality = supported / len(verdicts)
        else:
            citation_quality = 1.0 if item["should_refuse"] else 0.0

        results.append({
            "question":         question,
            "question_type":    item["question_type"],
            "retrieval_hit":    retrieval_hit,
            "refusal_correct":  refusal_correct,
            "content_correct":  content_correct,
            "citation_quality": citation_quality,
            "no_answer":        result["no_answer"],
        })

    total = len(results)
    return {
        "total":                total,
        "retrieval_accuracy":   round(sum(1 for r in results if r["retrieval_hit"])   / total * 100, 1),
        "refusal_accuracy":     round(sum(1 for r in results if r["refusal_correct"]) / total * 100, 1),
        "content_accuracy":     round(sum(1 for r in results if r["content_correct"]) / total * 100, 1),
        "avg_citation_quality": round(sum(r["citation_quality"] for r in results)     / total * 100, 1),
    }
    def _print_comparison(self, hybrid: dict, dense: dict) -> None:
        """Prints a side-by-side comparison table."""
        table = Table(title="Hybrid vs Dense-Only Retrieval", show_header=True)
        table.add_column("Metric",         style="cyan", width=28)
        table.add_column("Hybrid",         justify="right", width=12)
        table.add_column("Dense Only",     justify="right", width=12)
        table.add_column("Difference",     justify="right", width=12)
        metrics = [
            ("Retrieval Accuracy",   "retrieval_accuracy"),
            ("Refusal Accuracy",     "refusal_accuracy"),
            ("Content Accuracy",     "content_accuracy"),
            ("Avg Citation Quality", "avg_citation_quality"),
            ]
        for label, key in metrics:
            h_val = hybrid[key]
            d_val = dense[key]
            diff  = round(h_val - d_val, 1)
            color = "green" if diff > 0 else "red" if diff < 0 else "white"
            table.add_row(
                label,
                f"{h_val}%",
                f"{d_val}%",
                f"[{color}]{'+' if diff > 0 else ''}{diff}%[/{color}]"
                )
            console.print(table)
        
        
        
        
        
        