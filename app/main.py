from pathlib import Path

from app.logging_config import setup_logging

from database.migrations import initialize_database
from database.repository import FileRepository

from ingestion.analyzers.basic import BasicAnalyzer
from ingestion.analyzers.document import DocumentAnalyzer
from ingestion.analyzers.hash import HashAnalyzer
from ingestion.analyzers.FileTypeAnalyzer import FileTypeAnalyzer
from ingestion.analyzers.language import LanguageAnalyzer
from ingestion.analyzers.pipeline import AnalysisPipeline
from ingestion.analyzers.python import PythonAnalyzer

from ingestion.indexer import Indexer


def main():

    setup_logging()

    initialize_database()

    pipeline = AnalysisPipeline(
    [
        BasicAnalyzer(),
        FileTypeAnalyzer(),
        LanguageAnalyzer(),
        PythonAnalyzer(),
        DocumentAnalyzer(),
    ]
    )

    repository = FileRepository()

    indexer = Indexer(
        pipeline=pipeline,
        repository=repository,
    )

    indexer.index(Path.cwd())


if __name__ == "__main__":
    main()