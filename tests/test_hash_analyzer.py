from pathlib import Path

from ingestion.ingestion.analyzers.hash import HashAnalyzer
from ingestion.core.models import FileMetadata

from datetime import datetime


def create_metadata(path: Path) -> FileMetadata:
    stat = path.stat()

    return FileMetadata(
        path=path,
        filename=path.name,
        extension=path.suffix,
        size=stat.st_size,
        created_at=datetime.fromtimestamp(stat.st_ctime),
        modified_at=datetime.fromtimestamp(stat.st_mtime),
    )


def test_same_file_has_same_hash():

    path = Path(__file__)

    analyzer = HashAnalyzer()

    metadata1 = analyzer.analyze(create_metadata(path))
    metadata2 = analyzer.analyze(create_metadata(path))

    assert metadata1.sha256 == metadata2.sha256