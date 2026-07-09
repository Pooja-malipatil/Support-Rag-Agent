from dataclasses import dataclass, field
from rich.console import Console

console = Console()

@dataclass
class Turn:
    """One exchange in the conversation."""
    question: str
    answer:   str

@dataclass
class ConversationMemory:
    """
    Stores conversation history and provides
    context for follow-up questions.
    
    Keeps last N turns to avoid context overflow.
    """
    max_turns: int = 5
    turns:     list[Turn] = field(default_factory=list)

    def add_turn(self, question: str, answer: str) -> None:
        """Add a completed exchange to memory."""
        self.turns.append(Turn(question=question, answer=answer))
        # Keep only last N turns
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]

    def get_history_text(self) -> str:
        """
        Formats conversation history as text for LLM context.
        Returns empty string if no history.
        """
        if not self.turns:
            return ""

        lines = []
        for i, turn in enumerate(self.turns):
            lines.append(f"User: {turn.question}")
            # Truncate long answers to save context window space
            answer_preview = turn.answer[:300] + "..." \
                if len(turn.answer) > 300 else turn.answer
            lines.append(f"Assistant: {answer_preview}")

        return "\n".join(lines)

    def is_followup(self, question: str) -> bool:
        """
        Heuristic to detect if a question is a follow-up.
        Checks for pronouns and references that imply prior context.
        """
        if not self.turns:
            return False

        followup_signals = [
            "what about", "how about", "and what",
            "also", "what if", "can i also",
            "what else", "tell me more", "elaborate",
            "why", "how so", "give me an example",
            "what does that mean", "clarify",
        ]

        question_lower = question.lower()
        return any(signal in question_lower for signal in followup_signals)

    def clear(self) -> None:
        """Reset conversation history."""
        self.turns = []
        console.print("[dim]Conversation memory cleared[/dim]")