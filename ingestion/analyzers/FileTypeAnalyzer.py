from dataclasses import replace

from ingestion.analyzers.base import Analyzer
from ingestion.core.models import FileMetadata


class FileTypeAnalyzer(Analyzer):
    """
    Determines the logical file type of a file
    based on its extension.
    """

    FILE_TYPE_MAP = {
        ".py": "source_code",
        ".java": "source_code",
        ".cpp": "source_code",
        ".cc": "source_code",
        ".cxx": "source_code",
        ".c": "source_code",
        ".h": "source_code",
        ".hpp": "source_code",
        ".js": "source_code",
        ".jsx": "source_code",
        ".ts": "source_code",
        ".tsx": "source_code",

        ".pdf": "pdf",
        ".docx": "docx",
        ".pptx": "pptx",

        ".md": "markdown",
        ".txt": "text",
        ".json": "json",
        ".csv": "csv",
        ".xml": "xml",
        ".yaml": "yaml",
        ".yml": "yaml",

        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
    }

    def analyze(self, metadata: FileMetadata) -> FileMetadata:

        file_type = self.FILE_TYPE_MAP.get(metadata.extension)

        return replace(
            metadata,
            file_type=file_type,
        )