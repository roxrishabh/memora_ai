import mimetypes

from ingestion.analyzers.base import Analyzer
from ingestion.models import FileMetadata


class BasicAnalyzer(Analyzer):

    def analyze(self, metadata: FileMetadata) -> FileMetadata:

        mime_type, _ = mimetypes.guess_type(metadata.path)
        if mime_type is None:
            extension_map = {
                ".md": "text/markdown",
                ".py": "text/x-python",
                ".json": "application/json",
                ".yaml": "application/yaml",
                ".yml": "application/yaml",
            }

            mime_type = extension_map.get(metadata.extension)
        metadata.mime_type = mime_type

        return metadata