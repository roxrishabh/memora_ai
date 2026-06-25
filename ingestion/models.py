from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class FileMetadata:
    """
    Represents metadata and analysis information
    about a discovered file.
    """

    # ------------------------
    # Basic
    # ------------------------

    path: Path
    filename: str
    extension: str

    size: int

    created_at: datetime
    modified_at: datetime

    # ------------------------
    # Analysis
    # ------------------------

    mime_type: str | None = None

    language: str |None = None

    sha256: str | None = None

    imports: list[str] = field(default_factory=list)

    symbols: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)