from __future__ import annotations

import math
import re
from pathlib import Path

from ingestion.core.document import DocumentMetadata
from ingestion.parsers.base import DocumentParser


class MarkdownParser(DocumentParser):
    """
    Parser for Markdown documents.
    Extracts structured information from Markdown files.
    """

    # -----------------------------
    # Regex Patterns
    # -----------------------------

    # # Heading
    HEADING_PATTERN = re.compile(
        r"^(#{1,6})\s+(.*)$",
        re.MULTILINE,
    )

    # ```python ... ```
    CODE_BLOCK_PATTERN = re.compile(
        r"```(?:\w+)?\n(.*?)```",
        re.DOTALL,
    )

    # [Google](https://google.com)
    # Negative lookbehind prevents matching images
    MARKDOWN_LINK_PATTERN = re.compile(
        r"(?<!!)\[(.*?)\]\((.*?)\)"
    )

    # https://google.com
    URL_PATTERN = re.compile(
        r"https?://[^\s)]+"
    )

    # ![Architecture](architecture.png)
    IMAGE_PATTERN = re.compile(
        r"!\[(.*?)\]\((.*?)\)"
    )

    def parse(self, path: Path) -> DocumentMetadata:

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        # --------------------------------
        # Headings
        # --------------------------------

        headings = [
            match.group(2).strip()
            for match in self.HEADING_PATTERN.finditer(text)
        ]

        title = headings[0] if headings else None

        # --------------------------------
        # Code Blocks
        # --------------------------------

        code_blocks = [
            match.group(1).strip()
            for match in self.CODE_BLOCK_PATTERN.finditer(text)
        ]

        # --------------------------------
        # Markdown Links
        # --------------------------------

        markdown_links = [
            match.group(2)
            for match in self.MARKDOWN_LINK_PATTERN.finditer(text)
        ]

        # --------------------------------
        # Plain URLs
        # --------------------------------

        plain_links = self.URL_PATTERN.findall(text)

        links = sorted(
            set(markdown_links + plain_links)
        )

        # --------------------------------
        # Images
        # --------------------------------

        images = [
            match.group(2)
            for match in self.IMAGE_PATTERN.finditer(text)
        ]

        # --------------------------------
        # Clean Text
        # --------------------------------

        cleaned = self.CODE_BLOCK_PATTERN.sub("", text)

        # Remove image syntax
        cleaned = self.IMAGE_PATTERN.sub("", cleaned)

        # Replace markdown links with visible text
        cleaned = self.MARKDOWN_LINK_PATTERN.sub(
            lambda m: m.group(1),
            cleaned,
        )

        # Remove heading markers
        cleaned = self.HEADING_PATTERN.sub(
            lambda m: m.group(2),
            cleaned,
        )

        # Remove repeated blank lines
        cleaned = re.sub(
            r"\n{3,}",
            "\n\n",
            cleaned,
        )

        cleaned = cleaned.strip()

        # --------------------------------
        # Statistics
        # --------------------------------

        words = cleaned.split()

        word_count = len(words)

        character_count = len(cleaned)

        reading_time = max(
            1,
            math.ceil(word_count / 200),
        )

        # --------------------------------
        # Return Metadata
        # --------------------------------

        return DocumentMetadata(
            title=title,
            headings=headings,
            text=cleaned,
            links=links,
            images=images,
            code_blocks=code_blocks,
            tables=[],
            page_count=1,
            word_count=word_count,
            character_count=character_count,
            reading_time_minutes=reading_time,
        )