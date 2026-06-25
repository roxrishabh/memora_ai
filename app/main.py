from pathlib import Path

from ingestion.analyzers.basic import BasicAnalyzer
from ingestion.analyzers.hash import HashAnalyzer
from ingestion.analyzers.pipeline import AnalysisPipeline
from ingestion.scanner import scan_directory


pipeline = AnalysisPipeline(
    analyzers=[
        BasicAnalyzer(),
        HashAnalyzer(),
    ]
)


for metadata in scan_directory(Path.cwd()):

    metadata = pipeline.run(metadata)

    print(
        metadata.filename,
        metadata.mime_type,
        metadata.sha256[:12],
    )