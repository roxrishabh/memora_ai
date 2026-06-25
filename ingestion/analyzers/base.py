from abc import ABC, abstractmethod

from ingestion.models import FileMetadata


class Analyzer(ABC):
    """
    Base class for all analyzers.
    """

    @abstractmethod
    def analyze(self, metadata: FileMetadata) -> FileMetadata:
        """
        Analyze a file and enrich its metadata.
        """
        raise NotImplementedError