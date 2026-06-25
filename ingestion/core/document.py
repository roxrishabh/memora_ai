from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentMetadata:
    """
    Structured metadata extracted from a document.
    """

    title: str | None = None

    author: str | None = None

    page_count: int = 0

    word_count: int = 0

    character_count: int = 0

    reading_time_minutes: int = 0

    text: str = ""

    headings: list[str] = field(default_factory=list)

    links: list[str] = field(default_factory=list)

    images: list[str] = field(default_factory=list)

    code_blocks: list[str] = field(default_factory=list)

    tables: list[list[str]] = field(default_factory=list)