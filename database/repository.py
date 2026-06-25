from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from database.connection import get_connection
from ingestion.core.models import FileMetadata


class FileRepository:
    """
    Handles persistence of FileMetadata.
    """

    def save(self, metadata: FileMetadata) -> None:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO files(

                    path,
                    filename,
                    extension,
                    file_type,
                    programming_language,
                    mime_type,
                    size,
                    created_at,
                    modified_at,
                    sha256,
                    indexed_at

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                """,
                (
                    str(metadata.path),
                    metadata.filename,
                    metadata.extension,
                    metadata.file_type,
                    metadata.programming_language,
                    metadata.mime_type,
                    metadata.size,
                    metadata.created_at.isoformat(),
                    metadata.modified_at.isoformat(),
                    metadata.sha256,
                    datetime.utcnow().isoformat(),
                ),
            )

            file_id = cursor.lastrowid

            if file_id is None:
                cursor.execute(
                    "SELECT id FROM files WHERE path=?",
                    (str(metadata.path),),
                )

                file_id = cursor.fetchone()[0]

            cursor.executemany(
                """
                INSERT INTO python_imports(file_id,module)
                VALUES (?,?)
                """,
                [(file_id, module) for module in metadata.imports],
            )

            cursor.executemany(
                """
                INSERT INTO python_functions(file_id,function_name)
                VALUES (?,?)
                """,
                [(file_id, func) for func in metadata.functions],
            )

            cursor.executemany(
                """
                INSERT INTO python_classes(file_id,class_name)
                VALUES (?,?)
                """,
                [(file_id, cls) for cls in metadata.classes],
            )

            conn.commit()

    def get_file_metadata(self, path: Path) -> dict[str, Any] | None:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    size,
                    modified_at,
                    sha256
                FROM files
                WHERE path = ?
                """,
                (str(path),),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return dict(row)
        
    def file_exists(self, path: Path) -> bool:
        """
        Check whether a file has already been indexed.
        """

        return self.get_file_hash(path) is not None
    
    def delete(self, path: Path) -> None:
        """
        Remove a file from the index.
        """

        with get_connection() as conn:

            conn.execute(
                """
                DELETE FROM files
                WHERE path = ?
                """,
                (str(path),),
            )

            conn.commit()