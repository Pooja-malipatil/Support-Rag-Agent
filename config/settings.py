from pydantic import BaseModel
from enum import Enum
from datetime import date
from pathlib import Path

class DocType(str, Enum):
    FAQ     = "faq"
    GUIDE   = "guide"
    POLICY  = "policy"

class AccessLevel(str, Enum):
    PUBLIC   = "public"
    INTERNAL = "internal"

class DocumentMetadata(BaseModel):
    source_name:  str
    section:      str
    last_updated: date
    doc_type:     DocType
    access_level: AccessLevel

class Document(BaseModel):
    metadata: DocumentMetadata   # the WHO/WHEN/WHAT of the doc
    content:  str                # the raw text body
    file_path: str         
    
class ChunkStrategy(str, Enum):
    HEADING = "heading"
    FIXED   = "fixed"

class Chunk(BaseModel):
    chunk_id:   str              # unique ID: "api-keys-faq-chunk-0"
    content:    str              # the actual text of this chunk
    metadata:   DocumentMetadata # inherited from parent document
    file_path:  str              # where it came from
    strategy:   ChunkStrategy    # which strategy produced this chunk
    chunk_index: int             # 0, 1, 2... within its document# where it came from on disk