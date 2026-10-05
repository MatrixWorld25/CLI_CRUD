"""Unit tests for RecordService."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.repository import RecordRepository
from app.service import DuplicateRecordError, RecordNotFoundError, RecordService
from app.storage import JSONStorage


class RecordServiceTest(unittest.TestCase):
    """Tests service behavior with isolated temporary JSON storage."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "records.json"
        storage = JSONStorage(self.storage_path)
        repository = RecordRepository(storage)
        self.service = RecordService(repository)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_create_and_read(self) -> None:
        self.service.create_record(1, "Ayan", "ayan@example.com", "+91 9876543210", "Developer")

        record = self.service.get_record(1)

        self.assertEqual(record.record_id, 1)
        self.assertEqual(record.name, "Ayan")
        self.assertEqual(record.email, "ayan@example.com")

    def test_update(self) -> None:
        self.service.create_record(1, "Ayan", "ayan@example.com", "+91 9876543210", "Developer")

        updated = self.service.update_record(1, name="Ayan Khan", role="Lead Developer")

        self.assertEqual(updated.name, "Ayan Khan")
        self.assertEqual(updated.email, "ayan@example.com")
        self.assertEqual(updated.role, "Lead Developer")

    def test_delete(self) -> None:
        self.service.create_record(1, "Ayan", "ayan@example.com", "+91 9876543210", "Developer")

        self.service.delete_record(1)

        self.assertEqual(self.service.list_records(), [])

    def test_search(self) -> None:
        self.service.create_record(1, "Ayan", "ayan@example.com", "+91 9876543210", "Developer")
        self.service.create_record(2, "Mira", "mira@example.com", "9876500000", "Designer")

        results = self.service.search_records("design")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].record_id, 2)

    def test_duplicate_id_rejection(self) -> None:
        self.service.create_record(1, "Ayan", "ayan@example.com", "+91 9876543210", "Developer")

        with self.assertRaises(DuplicateRecordError):
            self.service.create_record(1, "Mira", "mira@example.com", "9876500000", "Designer")

    def test_invalid_email_rejection(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_record(1, "Ayan", "not-an-email", "+91 9876543210", "Developer")

    def test_invalid_phone_rejection(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_record(1, "Ayan", "ayan@example.com", "123", "Developer")

    def test_missing_record_handling(self) -> None:
        with self.assertRaises(RecordNotFoundError):
            self.service.get_record(99)


if __name__ == "__main__":
    unittest.main()
