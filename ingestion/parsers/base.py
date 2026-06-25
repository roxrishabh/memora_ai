from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ingestion.core.document import DocumentMetadata


class DocumentParser(ABC):
    """
    Base class for all document parsers.
    """

    @abstractmethod
    def parse(
        self,
        path: Path,
    ) -> DocumentMetadata:
        """
        Parse a document into structured metadata.
        """
        raise NotImplementedError