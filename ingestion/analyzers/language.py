from dataclasses import replace

from ingestion.analyzers.base import Analyzer
from ingestion.core.models import FileMetadata


class LanguageAnalyzer(Analyzer):
    """
    Determines the programming language for source code files.
    """

    LANGUAGE_MAP = {
        ".py": "python",
        ".java": "java",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",
        ".h": "c",
        ".c": "c",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".go": "go",
        ".rs": "rust",
        ".cs": "csharp",
        ".php": "php",
        ".rb": "ruby",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
    }

    def analyze(self, metadata: FileMetadata) -> FileMetadata:
        """
        Determine the programming language of a source code file.
        """

        # Only source code files have programming languages
        if metadata.file_type != "source_code":
            return metadata

        language = self.LANGUAGE_MAP.get(metadata.extension)

        return replace(
            metadata,
            programming_language=language,
        )