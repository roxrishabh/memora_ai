from ingestion.models import FileMetadata
from ingestion.analyzers.base import Analyzer


class AnalysisPipeline:
    """
    Runs a sequence of analyzers on a file.
    """

    def __init__(self, analyzers: list[Analyzer]) -> None:
        self.analyzers = analyzers

    def run(self, metadata: FileMetadata) -> FileMetadata:

        for analyzer in self.analyzers:
            metadata = analyzer.analyze(metadata)

        return metadata