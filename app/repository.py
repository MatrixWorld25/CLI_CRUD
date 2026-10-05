"""Repository layer for record persistence operations."""

from __future__ import annotations

from app.models import Record
from app.storage import JSONStorage


class RecordRepository:
    """Coordinates storage reads and writes for Record objects."""

    def __init__(self, storage: JSONStorage) -> None:
        self.storage = storage

    def all(self) -> list[Record]:
        """Return every stored record sorted by ID."""
        records = [Record.from_dict(item) for item in self.storage.load()]
        return sorted(records, key=lambda record: record.record_id)

    def get(self, record_id: int) -> Record | None:
        """Return one record by ID, or None when it does not exist."""
        return next((record for record in self.all() if record.record_id == record_id), None)

    def create(self, record: Record) -> Record:
        """Persist a new record."""
        records = self.all()
        records.append(record)
        self._save_records(records)
        return record

    def update(self, record: Record) -> Record:
        """Replace an existing record by ID."""
        records = self.all()
        updated = False
        for index, existing in enumerate(records):
            if existing.record_id == record.record_id:
                records[index] = record
                updated = True
                break

        if updated:
            self._save_records(records)
        return record

    def delete(self, record_id: int) -> bool:
        """Delete a record by ID. Returns True when a record was removed."""
        records = self.all()
        remaining = [record for record in records if record.record_id != record_id]
        if len(remaining) == len(records):
            return False
        self._save_records(remaining)
        return True

    def search(self, query: str) -> list[Record]:
        """Search records across name, email, phone, and role."""
        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        return [
            record
            for record in self.all()
            if normalized_query in record.name.lower()
            or normalized_query in record.email.lower()
            or normalized_query in record.phone.lower()
            or normalized_query in record.role.lower()
        ]

    def _save_records(self, records: list[Record]) -> None:
        self.storage.save([record.to_dict() for record in sorted(records, key=lambda item: item.record_id)])
