from __future__ import annotations

from dataclasses import replace

from ingestion.analyzers.base import Analyzer
from ingestion.parsers.markdown import MarkdownParser
from ingestion.core.models import FileMetadata


class DocumentAnalyzer(Analyzer):
    """
    Extract document information from supported files.
    """

    def __init__(self) -> None:

        self.parsers = {
            ".md": MarkdownParser(),
        }

    def analyze(self, metadata: FileMetadata):

        parser = self.parsers.get(metadata.extension)

        if parser is None:
            return metadata

        document = parser.parse(metadata.path)

        return replace(
            metadata,
            document=document,
        )