from collections.abc import Generator
from datetime import datetime
from pathlib import Path

from app.settings import settings
from ingestion.core.models import FileMetadata


def scan_directory(root: Path) -> Generator[FileMetadata, None, None]:
    """
    Recursively scan a directory and yield metadata
    for every supported file.
    """

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if any(part in settings.ignored_directories for part in path.parts):
            continue

        if path.suffix.lower() not in settings.supported_extensions:
            continue

        stat = path.stat()

        yield FileMetadata(
            path=path,
            filename=path.name,
            extension=path.suffix.lower(),
            size=stat.st_size,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
        )