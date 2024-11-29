from os import environ
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    source_path: Path
    extensions: list[str]

    @classmethod
    def from_env(cls) -> "Config":
        source_path = environ.get("STILLFRAME_SOURCE_PATH", ".")
        extensions = environ.get("STILLFRAME_EXTENSIONS", "bmp,jpeg,jpg").split(",")
        return cls(source_path=Path(source_path), extensions=extensions)
