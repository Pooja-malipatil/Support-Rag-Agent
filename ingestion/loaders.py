import yaml
from pathlib import Path
from typing import Optional
from rich.console import Console
from config.settings import Document, DocumentMetadata

console = Console()

def parse_markdown_file(file_path: Path) -> Optional[Document]:
    """
    Reads a markdown file, separates frontmatter from content,
    validates metadata, and returns a Document object.
    Returns None if the file is invalid.
    """
    raw_text = file_path.read_text(encoding="utf-8")

    # --- Split frontmatter from content ---
    # Every valid doc starts with ---
    if not raw_text.startswith("---"):
        console.print(f"[yellow]Skipping {file_path.name} — no frontmatter found[/yellow]")
        return None

    # Find the closing ---
    # splitlines() turns the file into a list of lines
    lines = raw_text.splitlines()

    # Find where the second --- is
    closing_index = None
    for i, line in enumerate(lines[1:], start=1):  # skip line 0 which is ---
        if line.strip() == "---":
            closing_index = i
            break

    if closing_index is None:
        console.print(f"[red]Skipping {file_path.name} — frontmatter never closed[/red]")
        return None

    # Extract frontmatter lines and content lines
    frontmatter_lines = lines[1:closing_index]          # between the two ---
    content_lines     = lines[closing_index + 1:]       # everything after

    frontmatter_text = "\n".join(frontmatter_lines)
    content_text     = "\n".join(content_lines).strip()

    # --- Parse the YAML frontmatter ---
    try:
        raw_metadata = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        console.print(f"[red]YAML error in {file_path.name}: {e}[/red]")
        return None

    # --- Validate with Pydantic ---
    try:
        metadata = DocumentMetadata(**raw_metadata)
    except Exception as e:
        console.print(f"[red]Metadata validation failed in {file_path.name}: {e}[/red]")
        return None

    return Document(
        metadata=metadata,
        content=content_text,
        file_path=str(file_path)
    )


def load_all_documents(docs_dir: Path) -> list[Document]:
    """
    Walks the docs/ folder, loads every .md file,
    and returns a list of valid Document objects.
    """
    documents = []
    md_files = list(docs_dir.rglob("*.md"))  # rglob = recursive search

    console.print(f"\n[bold]Found {len(md_files)} markdown files[/bold]")

    for file_path in md_files:
        doc = parse_markdown_file(file_path)
        if doc:
            documents.append(doc)
            console.print(f"[green]✓[/green] Loaded: {doc.metadata.source_name} ({doc.metadata.doc_type})")

    console.print(f"\n[bold green]Successfully loaded {len(documents)}/{len(md_files)} documents[/bold green]\n")
    return documents