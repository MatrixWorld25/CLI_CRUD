"""Data models for the record manager."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Record:
    """Represents one managed contact-style record."""

    record_id: int
    name: str
    email: str
    phone: str
    role: str

    def to_dict(self) -> dict[str, Any]:
        """Convert the record into a JSON-serializable dictionary."""
        return {
            "record_id": self.record_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Record":
        """Build a Record from dictionary data loaded from storage."""
        return cls(
            record_id=int(data["record_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            phone=str(data["phone"]),
            role=str(data["role"]),
        )
