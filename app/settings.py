from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """
    Central configuration for the application.
    """

    project_root: Path = Path(__file__).resolve().parent.parent

    data_dir: Path = field(init=False)
    cache_dir: Path = field(init=False)
    index_dir: Path = field(init=False)
    logs_dir: Path = field(init=False)

    database_path: Path = field(init=False)

    supported_extensions: set[str] = field(
        default_factory=lambda: {
            ".pdf",
            ".docx",
            ".pptx",
            ".txt",
            ".md",
            ".py",
            ".java",
            ".cpp",
            ".c",
            ".js",
            ".ts",
            ".json",
            ".csv",
            ".xlsx",
            ".png",
            ".jpg",
            ".jpeg",
        }
    )

    ignored_directories: set[str] = field(
        default_factory=lambda: {
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "myvenv",
            ".idea",
            ".vscode",
            "node_modules",
        }
    )

    def __post_init__(self):
        object.__setattr__(self, "data_dir", self.project_root / "data")
        object.__setattr__(self, "cache_dir", self.data_dir / "cache")
        object.__setattr__(self, "index_dir", self.data_dir / "index")
        object.__setattr__(self, "logs_dir", self.data_dir / "logs")

        object.__setattr__(
            self,
            "database_path",
            self.index_dir / "metadata.db",
        )
        for directory in (
            self.data_dir,
            self.cache_dir,
            self.index_dir,
            self.logs_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()