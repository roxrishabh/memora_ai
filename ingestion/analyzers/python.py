"""
Python source code analyzer.

This analyzer extracts structural information from Python files using the
built-in AST (Abstract Syntax Tree) module.
"""

from __future__ import annotations

import ast
import logging
from dataclasses import replace

from ingestion.analyzers.base import Analyzer
from ingestion.core.models import FileMetadata

logger = logging.getLogger(__name__)


class PythonAnalyzer(Analyzer):
    """
    Analyze Python source files.

    Extracts:
    - Imported modules
    - Classes
    - Functions
    - Async functions
    """

    def analyze(self, metadata: FileMetadata) -> FileMetadata:
        """
        Analyze a Python file and enrich its metadata.

        Parameters
        ----------
        metadata : FileMetadata
            Metadata of the file being analyzed.

        Returns
        -------
        FileMetadata
            Updated metadata containing extracted Python information.
        """

        # Ignore non-python files
        if metadata.programming_language != "python":
            return metadata

        try:
            source = metadata.path.read_text(
                encoding="utf-8",
                errors="ignore",
            )


            tree = ast.parse(source)

        except (OSError, SyntaxError) as exc:
            logger.warning(
                "Failed to analyze %s: %s",
                metadata.path,
                exc,
            )
            return metadata

        imports: set[str] = set()
        classes: set[str] = set()
        functions: set[str] = set()
        async_functions: set[str] = set()

        for node in ast.walk(tree):

            # import pandas
            # import numpy
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)

            # from langgraph.graph import StateGraph
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

            # class Agent:
            elif isinstance(node, ast.ClassDef):
                classes.add(node.name)

            # def build_graph():
            elif isinstance(node, ast.FunctionDef):
                functions.add(node.name)

            # async def run():
            elif isinstance(node, ast.AsyncFunctionDef):
                async_functions.add(node.name)

        logger.info("Analyzed Python file: %s", metadata.filename)

        return replace(
            metadata,
            programming_language="python",
            imports=sorted(imports),
            classes=sorted(classes),
            functions=sorted(functions),
            async_functions=sorted(async_functions),
        )