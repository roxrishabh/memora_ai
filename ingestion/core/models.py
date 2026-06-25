from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class FileMetadata:

    # Basic
    path: Path
    filename: str
    extension: str
    size: int
    created_at: datetime
    modified_at: datetime

    # General Analysis
    mime_type: str | None = None
    file_type: str | None = None
    programming_language: str | None = None
    sha256: str | None = None

    # Code Analysis
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    async_functions: list[str] = field(default_factory=list)

    # Generic
    tags: list[str] = field(default_factory=list)