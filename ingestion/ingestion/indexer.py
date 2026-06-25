from __future__ import annotations

import logging
from pathlib import Path

from database.repository import FileRepository
from ingestion.ingestion.analyzers.hash import HashAnalyzer
from ingestion.ingestion.analyzers.pipeline import AnalysisPipeline
from ingestion.ingestion.scanner import scan_directory

logger = logging.getLogger(__name__)


class Indexer:
    """
    Coordinates the indexing workflow.

    Workflow:
        Scanner
            ↓
        Compare metadata
            ↓
        Compute hash (only if needed)
            ↓
        Compare hash
            ↓
        Analysis Pipeline
            ↓
        Repository
    """

    def __init__(
        self,
        pipeline: AnalysisPipeline,
        repository: FileRepository,
    ) -> None:

        self.pipeline = pipeline
        self.repository = repository
        self.hash_analyzer = HashAnalyzer()

    def index(self, root: Path) -> None:

        logger.info("Starting indexing: %s", root)

        scanned = 0
        indexed = 0
        skipped = 0

        for metadata in scan_directory(root):

            scanned += 1

            # ----------------------------------
            # Check existing metadata
            # ----------------------------------

            existing = self.repository.get_file_metadata(metadata.path)

            if existing is not None:

                if (
                    existing["size"] == metadata.size
                    and existing["modified_at"] == metadata.modified_at.isoformat()
                ):

                    skipped += 1

                    logger.info(
                        "Skipped (unchanged): %s",
                        metadata.filename,
                    )

                    continue

                # ----------------------------------
                # Metadata changed
                # Compute hash only now
                # ----------------------------------

                metadata = self.hash_analyzer.analyze(metadata)

                if existing["sha256"] == metadata.sha256:

                    skipped += 1

                    logger.info(
                        "Skipped (same hash): %s",
                        metadata.filename,
                    )

                    continue

            else:
                # New file
                metadata = self.hash_analyzer.analyze(metadata)

            # ----------------------------------
            # Run remaining analyzers
            # ----------------------------------

            metadata = self.pipeline.run(metadata)

            # ----------------------------------
            # Save
            # ----------------------------------

            self.repository.save(metadata)

            indexed += 1

            logger.info(
                "Indexed: %s",
                metadata.filename,
            )

        logger.info("=" * 50)
        logger.info("Indexing Complete")
        logger.info("Files Scanned : %d", scanned)
        logger.info("Files Indexed : %d", indexed)
        logger.info("Files Skipped : %d", skipped)
        logger.info("=" * 50)