"""JSON persistence layer."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class StorageError(RuntimeError):
    """Raised when records cannot be read from or written to disk."""


class JSONStorage:
    """Safely loads and saves record dictionaries in a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict[str, Any]]:
        """Load all records from disk, creating an empty file if missing."""
        if not self.path.exists():
            self.save([])
            return []

        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise StorageError(f"Invalid JSON in {self.path}. Please repair the file or reset it to [].") from exc
        except OSError as exc:
            raise StorageError(f"Could not read {self.path}: {exc}") from exc

        if not isinstance(data, list):
            raise StorageError(f"Invalid data format in {self.path}. Expected a JSON list.")
        if not all(isinstance(item, dict) for item in data):
            raise StorageError(f"Invalid data format in {self.path}. Each record must be an object.")
        return data

    def save(self, records: list[dict[str, Any]]) -> None:
        """Save records using a temporary file followed by atomic replacement."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_name: str | None = None

        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self.path.parent,
                delete=False,
                suffix=".tmp",
            ) as temp_file:
                json.dump(records, temp_file, indent=2)
                temp_file.write("\n")
                temp_name = temp_file.name

            os.replace(temp_name, self.path)
        except OSError as exc:
            raise StorageError(f"Could not write {self.path}: {exc}") from exc
        finally:
            if temp_name and Path(temp_name).exists():
                try:
                    Path(temp_name).unlink()
                except OSError:
                    pass
