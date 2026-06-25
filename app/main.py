from pathlib import Path

from app.logging_config import setup_logging

from database.migrations import initialize_database
from database.repository import FileRepository

from ingestion.ingestion.analyzers.basic import BasicAnalyzer
from ingestion.ingestion.analyzers.hash import HashAnalyzer
from ingestion.ingestion.analyzers.FileTypeAnalyzer import FileTypeAnalyzer
from ingestion.ingestion.analyzers.language import LanguageAnalyzer
from ingestion.ingestion.analyzers.pipeline import AnalysisPipeline
from ingestion.ingestion.analyzers.python import PythonAnalyzer

from ingestion.ingestion.indexer import Indexer


def main():

    setup_logging()

    initialize_database()

    pipeline = AnalysisPipeline(
    [
        BasicAnalyzer(),
        FileTypeAnalyzer(),
        LanguageAnalyzer(),
        PythonAnalyzer(),
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