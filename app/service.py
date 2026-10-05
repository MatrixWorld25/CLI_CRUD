"""Business logic for the record manager."""

from __future__ import annotations

from app.models import Record
from app.repository import RecordRepository
from app.validators import (
    validate_email,
    validate_name,
    validate_phone,
    validate_record_id,
    validate_role,
)


class DuplicateRecordError(ValueError):
    """Raised when trying to create a record with an existing ID."""


class RecordNotFoundError(ValueError):
    """Raised when a requested record does not exist."""


class RecordService:
    """Validates input and enforces business rules for records."""

    def __init__(self, repository: RecordRepository) -> None:
        self.repository = repository

    def list_records(self) -> list[Record]:
        """Return all records."""
        return self.repository.all()

    def get_record(self, record_id: int | str) -> Record:
        """Return one record or raise a clear not-found error."""
        normalized_id = validate_record_id(record_id)
        record = self.repository.get(normalized_id)
        if record is None:
            raise RecordNotFoundError(f"No record found with ID {normalized_id}.")
        return record

    def create_record(self, record_id: int | str, name: str, email: str, phone: str, role: str) -> Record:
        """Create a validated record."""
        normalized_id = validate_record_id(record_id)
        if self.repository.get(normalized_id) is not None:
            raise DuplicateRecordError(f"Record ID {normalized_id} already exists.")

        record = Record(
            record_id=normalized_id,
            name=validate_name(name),
            email=validate_email(email),
            phone=validate_phone(phone),
            role=validate_role(role),
        )
        return self.repository.create(record)

    def update_record(
        self,
        record_id: int | str,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        role: str | None = None,
    ) -> Record:
        """Update an existing record, preserving fields passed as None."""
        existing = self.get_record(record_id)
        updated = Record(
            record_id=existing.record_id,
            name=validate_name(name) if name is not None else existing.name,
            email=validate_email(email) if email is not None else existing.email,
            phone=validate_phone(phone) if phone is not None else existing.phone,
            role=validate_role(role) if role is not None else existing.role,
        )
        return self.repository.update(updated)

    def delete_record(self, record_id: int | str) -> None:
        """Delete an existing record."""
        normalized_id = validate_record_id(record_id)
        if not self.repository.delete(normalized_id):
            raise RecordNotFoundError(f"No record found with ID {normalized_id}.")

    def search_records(self, query: str) -> list[Record]:
        """Search records by name, email, phone, or role."""
        return self.repository.search(query)
