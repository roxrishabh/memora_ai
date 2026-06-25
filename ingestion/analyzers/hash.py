from dataclasses import replace
import hashlib

from ingestion.analyzers.base import Analyzer
from ingestion.models import FileMetadata


class HashAnalyzer(Analyzer):
    """
    Computes the SHA-256 hash of a file.
    """

    CHUNK_SIZE = 1024 * 1024  # 1 MB

    def analyze(self, metadata: FileMetadata) -> FileMetadata:
        hasher = hashlib.sha256()

        with metadata.path.open("rb") as file:
            while chunk := file.read(self.CHUNK_SIZE):
                hasher.update(chunk)

        return replace(
            metadata,
            sha256=hasher.hexdigest(),
        )