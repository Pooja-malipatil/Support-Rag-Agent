from sentence_transformers import SentenceTransformer
from rich.console import Console

console = Console()
MODEL_NAME = "all-MiniLM-L6-v2"

class Embedder:
    def __init__(self):
        console.print(f"[dim]Loading embedding model: {MODEL_NAME}...[/dim]")
        self.model = SentenceTransformer(MODEL_NAME)
        console.print(f"[green]Embedding model loaded[/green]")

    def embed_text(self, text: str) -> list:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list) -> list:
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        return vectors.tolist()