import re
import uuid
from config.settings import Document, Chunk, ChunkStrategy, DocumentMetadata

# --- Configuration ---
FIXED_CHUNK_SIZE    = 300   # words per chunk
FIXED_CHUNK_OVERLAP = 50    # words of overlap between chunks
MIN_CHUNK_LENGTH    = 50    # ignore chunks shorter than this (in characters)


def chunk_by_headings(doc: Document) -> list[Chunk]:
    """
    Splits document content at ## headings.
    Each heading + its body becomes one chunk.
    Best for: FAQs, structured guides with clear sections.
    """
    chunks = []
    # Split on lines that start with ## (level-2 headings)
    # re.split with a capture group keeps the delimiter in the results
    sections = re.split(r'(\n##[^\n]+)', doc.content)

    # re.split gives us: [before_first_heading, heading, body, heading, body, ...]
    # We pair up headings with their bodies
    current_heading = ""
    current_body    = sections[0]  # text before first heading

    for part in sections[1:]:
        if part.startswith("\n##"):
            # Save the previous section if it has content
            combined = (current_heading + "\n" + current_body).strip()
            if len(combined) >= MIN_CHUNK_LENGTH:
                chunks.append(_make_chunk(
                    content=combined,
                    doc=doc,
                    strategy=ChunkStrategy.HEADING,
                    index=len(chunks)
                ))
            current_heading = part.strip()
            current_body    = ""
        else:
            current_body += part

    # Don't forget the last section
    combined = (current_heading + "\n" + current_body).strip()
    if len(combined) >= MIN_CHUNK_LENGTH:
        chunks.append(_make_chunk(
            content=combined,
            doc=doc,
            strategy=ChunkStrategy.HEADING,
            index=len(chunks)
        ))

    return chunks


def chunk_by_fixed_size(doc: Document) -> list[Chunk]:
    """
    Splits document into fixed-size word windows with overlap.
    Best for: Long documents without clear heading structure.
    """
    chunks  = []
    words   = doc.content.split()
    start   = 0

    while start < len(words):
        end        = start + FIXED_CHUNK_SIZE
        chunk_words = words[start:end]
        content    = " ".join(chunk_words)

        if len(content) >= MIN_CHUNK_LENGTH:
            chunks.append(_make_chunk(
                content=content,
                doc=doc,
                strategy=ChunkStrategy.FIXED,
                index=len(chunks)
            ))

        # Move forward by (chunk_size - overlap)
        # This is what creates the overlap
        start += FIXED_CHUNK_SIZE - FIXED_CHUNK_OVERLAP

    return chunks


def _make_chunk(content: str, doc: Document, strategy: ChunkStrategy, index: int) -> Chunk:
    """
    Helper that builds a Chunk object.
    Generates a stable chunk_id from source + index.
    """
    chunk_id = f"{doc.metadata.source_name}-chunk-{index}"
    return Chunk(
        chunk_id    = chunk_id,
        content     = content,
        metadata    = doc.metadata,
        file_path   = doc.file_path,
        strategy    = strategy,
        chunk_index = index
    )